import sqlite3, os, subprocess

from typing import Callable, Iterable, Optional, Tuple, Any
from statistics import mean, stdev, median, median_low, median_high, mode

from collections import defaultdict
from itertools import islice

from lib.tables import Table
from lib.helpers import strsign, annotate_pf, ifnone
from lib.emoji import gp_flags

class Streak:
    def __init__(self, condition: Callable[[int], bool]):
        self.longest = 0
        self.current = 0
        self._is_continued = condition

    def update(self, value: int):
        if self._is_continued(value):
            self.current += 1
            return

        if self.current > self.longest:
            self.longest = self.current
        
        self.current = 0
    
    def get(self) -> int:
        return max(self.longest, self.current)

class F1DB:
    def __init__(self, root_dir: str):
        self.sql_scripts_dir = os.path.join(root_dir, "sql")
        self.db_file = os.path.join(root_dir, "data", "f1db.db")
        self.con = sqlite3.connect(self.db_file)
        self.cur = self.con.cursor()
        self.root_dir = root_dir

    def run_script(
        self, name: str, 
        params: Optional[Iterable]
    ) -> list[Any]:
        script = os.path.join(self.sql_scripts_dir, name + ".sql")
        
        with open(script) as s:
            sql = s.read()

        if params:
            self.cur.execute(sql, params)
        else:
            self.cur.execute(sql)

        return self.cur.fetchall()

    def run_file(self, file: str) -> tuple[list[Any], list[str]]:
        with open(file) as f:
            content = f.read()
        
        self.cur.execute(content)
        return (
            self.cur.fetchall(), 
            [c[0] for c in self.cur.description]
        )

    def update(self):
        os.chdir(self.root_dir)
        subprocess.run(
            [os.path.join(self.root_dir, "install")], check=True
        )

    def execute(self, sql: str, params: Optional[Iterable] ) -> list[Any]:
        self.cur.execute(sql, params)
        return self.cur.fetchall()

    def get_columns(self, start=0) -> list[Any]:
        return [c[0] for c in self.cur.description[start:]] 


class GP:
    race_sql = "gp-race"
    
    def __init__(
        self,
        id: str, 
        year: int,
        db_handler: F1DB,
        out_table: Table
    ):
        self.id = id
        self.year = year
        self.db = db_handler
        self.table = out_table

    def race(self):
        rows = self.db.run_script(
            self.race_sql, 
            {"id": self.id, "year": self.year}
        )

        self.table.headers = self.db.get_columns(6)
        comments = []

        for is_fastest, is_pole, reason_retired, pts_pos_gained, \
            fastest_lap_gap, pos_gained, *row in rows:
            
            driver = row[0]

            if is_fastest:
                comments.append(
                    f"Fastest lap: {driver} - {row[-5]} (lap {row[-4]})"
                )

            if is_pole:
                comments.append(f"Pole position: {driver}")

            if pos_gained:
                row[3] += f" ({strsign(pos_gained)})"

            if pts_pos_gained:
                row[-2] += f" ({strsign(pts_pos_gained)})"

            if fastest_lap_gap:
                row[-5] += f" ({fastest_lap_gap})"

            if reason_retired is not None:
                comments.append(f"{driver} - Reason retired: {reason_retired}")

            self.table.add_row(row)
    
        self.table.flush()
        print('\n'.join(comments), end="\n\n")

class Driver:
    races_sql = "driver-races" 
    pits_sql = "driver-pits"
    qualifying_sql = "driver-qualifying"
    sprints_sql = "driver-sprints"
    overview_sql = "driver-season-overview"

    def __init__(
        self,
        id: str, 
        year: int,
        db_handler: F1DB,
        out_table: Table
    ):
        self.id = id
        self.year = year
        self.db = db_handler
        self.table = out_table

    def races(self):
        rows = self.db.run_script(
            self.races_sql,
            { "id": self.id, "year": self.year }
        )

        self.table.headers = self.db.get_columns(6)
        comments = []

        teams_played = defaultdict(int)
        finished = 2

        for is_fastest, is_pole, reason_retired, team, \
            pts_pos_gained, gap_from_fastest_lap, *row in rows:

            if reason_retired is not None:
                comments.append(f"* Retired because of - {reason_retired}")
                row[finished] += '*'

            row[finished] = annotate_pf(row[finished], is_pole, is_fastest)

            if pts_pos_gained:
                row[-2] += f" ({strsign(pts_pos_gained)})"

            if gap_from_fastest_lap:
                row[-5] += f" ({gap_from_fastest_lap})"
            
            self.table.add_row(row)
            teams_played[team] += 1

        comments.append('-' * 40)

        for team, total in teams_played.items():
            if len(teams_played) == 1:
                comments.append(f"All {total} games played in: {team}")
            else:
                comments.append(f"{total} games played in {team}")

        self.table.flush()
        print('\n'.join(comments), end="\n\n")

    def pits(self):
        rows = self.db.run_script(
            self.pits_sql, 
            {"id": self.id, "year": self.year}
        )

        races_pits = defaultdict(list)
        most_pits = -1

        for race, lap, time in rows:
            pit = {
                "lap": lap,
                "time": time
            }

            races_pits[race].append(pit)
            total_pits = len(races_pits[race])

            if  total_pits > most_pits:
                most_pits = total_pits

        self.table.headers = [f"pit {i+1}" for i in range(most_pits)]

        for race, pits in races_pits.items():
            row = [race]
            total_pits = 0
            
            for i in range(most_pits):
                if i >= len(pits):
                    row.append(None)
                    continue

                pit = pits[i]
                row.append(f"lap {pit["lap"]} - {pit["time"]}")
                total_pits += 1

            row.append(total_pits)
            self.table.add_row(row)
        
        self.table.flush()

    def __flush_script(self, script: str):
        self.table.rows = self.db.run_script(
            script, {"id": self.id, "year": self.year}
        )

        self.table.headers = self.db.get_columns()
        self.table.flush()

    def qualifying(self):
        self.__flush_script(self.qualifying_sql)

    def sprints(self):
        self.__flush_script(self.sprints_sql)

    def overview(self):
        rows = self.db.run_script(
            self.overview_sql,
            {"id": self.id, "year": self.year}
        )
    
        if not rows:
            return print("Couldn't find anything")

        per_race_pts_made = []
        per_race_team_pts_made = []
        grid_postitions = []
        finish_positions = []
        gained_positions = []
        race_pit_stops = []
        season_pts_pos = None

        total = {
            "gains": 0,
            "losses": 0,
            "q1_q2_elim": 0,
            "q3": 0,
            "races": 0,
            "finished": 0,
            "wins": 0,
            "podiums": 0,
            "score_finishes": 0,
            "pts": 0,
            "team_pts": 0,
            "fastest_laps": 0,
            "poles": 0,
            "penalties": 0,
        }

        nfs = {
            "DNF": [0, [], []], # N, gp, reasons
            "DNS": [0, [], []],
            "DSQ": [0, [], []],
            "NC":  [0, [], []]
        }

        longest_win_streak = Streak(lambda x: x and x == 1)
        longest_pod_streak = Streak(lambda x: x and x <= 3)
        longest_pts_streak = Streak(lambda x: x and x <= 10)

        for gp, is_fastest, is_pole, q3, pits, start, finish, finish_text, reason_retired, gained,\
            gap, laps, penalty, pts_after_race, pts_made, pts_pos_after, team_pts_after_race in rows:

            longest_win_streak.update(finish)
            longest_pod_streak.update(finish)
            longest_pts_streak.update(finish)

            pts_made = ifnone(pts_made, 0)
            team_pts_after_race = ifnone(team_pts_after_race, 0)

            if not start and finish: # PL start case
                start = finish + gained

            # Old records don't have q1, q2, q3
            if q3: total["q3"] += 1
            else: total["q1_q2_elim"] += 1

            if start: grid_postitions.append(start)
            if gained: gained_positions.append(gained)            
            if penalty: total["penalties"] += 1
            if pits: race_pit_stops.append(pits)

            if finish:
                finish_positions.append(finish)
                total["finished"] += 1

                if finish < start:
                    total["gains"] += 1
                elif finish > start:
                    total["losses"] += 1

                if finish == 1:
                    total["wins"] += 1

                if finish <= 3:
                    total["podiums"] += 1

                if finish <= 10:
                    total["score_finishes"] += 1
            else:
                nfs[finish_text][0] += 1
                nfs[finish_text][1].append(gp)
                nfs[finish_text][2].append(reason_retired)

            team_pts_made = team_pts_after_race - total["team_pts"]

            total["races"] += 1
            total["poles"] += ifnone(is_pole, 0)
            total["fastest_laps"] += ifnone(is_fastest, 0)
            total["pts"] = pts_after_race
            total["team_pts"] = team_pts_after_race
            season_pts_pos = pts_pos_after
            per_race_pts_made.append(pts_made)
            per_race_team_pts_made.append(team_pts_made)

        pole_conversion = total["poles"] / total["q3"] if total["q3"] else 0
        finish_rate = total["finished"] / total["races"]
        pts_per_race = total["pts"] / total["races"]

        win_rate = total["wins"] / total["races"]
        podium_rate = total["podiums"] / total["races"]
        scoring_rate = total["score_finishes"] / total["races"]
        pole_rate = total["poles"] / total["races"]
        fastest_lap_rate = total["fastest_laps"] / total["races"]

        not_finished = total["races"] - total["finished"]
        not_finished_rate = not_finished / total["races"]
        q1_q2_elim_rate = total["q1_q2_elim"] / total["races"]
        
        avg_finish_position = mean(finish_positions) 
        avg_grid_position = mean(grid_postitions)
        avg_gained_positions = mean(gained_positions)
        avg_race_pit_stops = mean(race_pit_stops) if race_pit_stops else 0

        median_grid_position = median(grid_postitions)
        mode_grid_position = mode(finish_positions)

        median_finish_position = median(finish_positions)
        mode_finish_position = mode(finish_positions)

        avg_points_when_scoring = total["pts"] / total["score_finishes"] if total["score_finishes"] else 0
        no_pos_change = total["finished"] - total["gains"] - total["losses"]
        
        pct_gain = total["gains"]  / total["finished"]
        pct_loss = total["losses"] / total["finished"] 
        pct_no_change = no_pos_change /  total["finished"]

        finish_pos_cv = stdev(finish_positions) / avg_finish_position
        pts_volatility = stdev(per_race_pts_made)

        points_share = total["pts"] / total["team_pts"]

        # pit stops
        sql = """
            SELECT 
                pit.pit_stop_time_millis 
            FROM race_data pit 
            JOIN race on race.id = pit.race_id 
            WHERE 
                pit.type = 'PIT_STOP' 
                and pit.driver_id = :id 
                and race.year = :year
        """

        rows = self.db.execute(sql, {"id": self.id, "year": self.year})

        pit_times = []
        problematic_pits = 0
        avg_pit_time = 0

        for row in rows:
            if not row[0]: continue
            pit_times.append(row[0] / 1000)

        if pit_times:
            pit_times.sort()
        
            n = len(pit_times)
            q1 = median_low(pit_times[:n//2])
            q3 = median_high(pit_times[(n+1)//2:])
            iqr = q3 - q1

            slow_thresh = median(pit_times) + 1.5 * iqr
            problematic_thresh = median(pit_times) + 3.0 * iqr

            problematic_pits = sum(1 for t in pit_times if t > problematic_thresh)
            avg_pit_time = mean(pit_times)

        print(f"\nSeason overview — {self.id}, {self.year}")
        print("-" * 50)
        print(f"Races: {total["races"]}  Finished: {total["finished"]}  Not finished/started: {not_finished}  (rate: {not_finished_rate:.1%})\n")

        print("Points")
        print(f"- Total pts: {total["pts"]} pts ({season_pts_pos} place)")
        print(f"- Team pts share: {points_share:.2%}")
        print(f"- Pts per race: {pts_per_race:.2f} pts")
        print(f"- Avg pts when scoring: {avg_points_when_scoring:.2f} pts")
        print(f"- Points volatility (std): {pts_volatility:.2f} pts\n")

        print("Qualifying & starts")
        print(f"- Poles: {total["poles"]}  (Pole rate: {pole_rate:.1%})")
        print(f"- Q1, Q2 eliminations: {total["q1_q2_elim"]} (rate: {q1_q2_elim_rate:.1%})")
        if total["q3"]:
            print(f"- Q3 appearances: {total["q3"]}")
            print(f"- Pole conversion (poles / Q3s): {pole_conversion:.1%}")
        print(f"- Avg grid position: {avg_grid_position:.2f}")
        print(f"- Median grid position: {median_grid_position:.2f}")
        print(f"- Most common grid position: {mode_grid_position}")
        print(f"- Penalties: {total["penalties"]}\n")

        print("Results & rates")
        print(f"- Wins: {total["wins"]}  (Win rate: {win_rate:.1%})")
        print(f"- Podiums: {total["podiums"]}  (Podium rate: {podium_rate:.1%})")
        print(f"- Scoring finishes: {total["score_finishes"]}  (Scoring rate: {scoring_rate:.1%})")
        print(f"- Fastest laps: {total["fastest_laps"]}  (Fastest-lap rate: {fastest_lap_rate:.1%})")
        print(f"- Finish rate: {finish_rate:.1%}")
        print(f"- Avg finish position: {avg_finish_position:.2f}")
        print(f"- Median finish position: {median_finish_position:.2f}")
        print(f"- Most common finish position: {mode_finish_position}")
        print(f"- Finish position CV (coefficient of variation): {finish_pos_cv:.3f}\n")

        print("Pit stops & strategy")
        print(f"- Avg pit stops per race: {avg_race_pit_stops:.2f}")
        print(f"- Avg pit stops time: {avg_pit_time:.2f}s")
        print(f"- Problematic pit stops: {problematic_pits}\n")

        print("Not started/finished/classified, disqualified: ")
        for nf in sorted(nfs, key=lambda k: nfs[k][0], reverse=True):
            n, gps, reasons = nfs[nf]
            rate = n / total["races"]
            print(f"- {nf}: {n} ({rate:.1%})")

            for i in range(n): print(f"  * {gps[i]} - {reasons[i]}")
        print()

        print("Race progress")
        print(f"- Avg positions gained per race: {avg_gained_positions:.2f}")
        print(f"- % races net gain: {pct_gain:.1%}")
        print(f"- % races net loss: {pct_loss:.1%}")
        print(f"- % races no change: {pct_no_change:.1%}")
        print(f"- Longest podium streak: {longest_pod_streak.get()}")
        print(f"- Longest win streak: {longest_win_streak.get()}")
        print(f"- Longest points streak: {longest_pts_streak.get()}\n")

class Season:
    def __init__(
        self, 
        year: int, 
        add_gp_flags: bool,
        db_handler: F1DB,
        out_table: Table
    ):
        self.year = year
        self.add_gp_flags = add_gp_flags
        self.db = db_handler
        self.table = out_table

    def championship(self, is_constructor=False):
        sql = """
            SELECT 
                grand_prix.id, 
                grand_prix.abbreviation 
            FROM grand_prix 
            JOIN race on race.year = ? 
            WHERE race.grand_prix_id = grand_prix.id
        """

        rows = self.db.execute(sql, [self.year])

        grandprix_cols = []
        grandprix_template = {}

        if self.add_gp_flags:
            flags = []

        for gp, abbr in rows:
            if self.add_gp_flags:
                flags.append(gp_flags[gp])

            grandprix_cols.append(abbr)
            grandprix_template[abbr] = None

        rows = self.db.run_script("championship", {"year": self.year})

        drivers_results = defaultdict(lambda: dict(grandprix_template))
        teams_drivers = defaultdict(dict)
        drivers_points = {}
        teams_points = {}

        for abbrev, name, finish_pos, points, is_pole, is_fastest, team, team_points in rows:
            drivers_results[name][abbrev] = annotate_pf(finish_pos, is_pole, is_fastest)
            drivers_points[name] = points
            teams_points[team] = ifnone(team_points, 0)
            
            teams_drivers[team][name] = drivers_results[name]

        pos = 1

        if is_constructor:
            sorted_teams_points = sorted(teams_points.items(), reverse=True, key=lambda kv: kv[1])
            
            for team, points in sorted_teams_points:
                team_drivers = teams_drivers[team]

                for name, results in islice(team_drivers.items(), 2):
                    per_races = [results[abbr] for abbr in grandprix_cols]
                    self.table.add_row([pos, team] + per_races + [points])
                
                pos += 1
        else:
            for name, points in drivers_points.items():
                per_races = [drivers_results[name].get(abbr) for abbr in grandprix_cols]
                self.table.add_row([pos, name] + per_races + [points])
                pos += 1

        if self.add_gp_flags:
            for i in range(len(grandprix_cols)):
                abbr = grandprix_cols[i]
                grandprix_cols[i] = f"{flags[i]} {abbr}"

        self.table.headers = ["pos", "name"] + grandprix_cols + ["pts"]
        self.table.flush()

class Circuit:
    def __init__(
        self, 
        id: str,
        rows: int,
        is_reversed: bool,
        db_handler: F1DB,
        out_table: Table
    ):
        self.id = id
        self.db = db_handler
        self.table = out_table
        self.rows = rows
        self.is_reversed = is_reversed

    def record(
        self, 
        script: str
    ):
        fetched = self.db.run_script(script, [self.id])
        if self.rows != -1:
            fetched = fetched[:self.rows]

        if self.is_reversed:
            fetched.reverse()

        self.table.headers = self.db.get_columns()
        self.table.rows = fetched
        self.table.flush()

    def info(self, years_per_row=8):
        sql = """
            SELECT 
                circuit.*, 
                GROUP_CONCAT(race.year ,',') as years 
            FROM circuit 
            JOIN race on race.circuit_id = :id 
            WHERE circuit.id = :id
        """
        fetched = self.db.execute(sql, {"id": self.id})[0]

        if not fetched or fetched[0] is None:
            return print(f"Circuit: \"{self.id}\" was not found")

        _, name, full_name, prev_names, circuit_type, direction, \
        place, country_id, lat, lon, length, turns, total_races, races_years = fetched

        print()
        print(f"* {name} ({full_name})")
        print(f"At: {country_id} - {place}")
        print(f"Lenght: {length}km, turns: {turns}")
        print(f"Total races held: {total_races}")
        years = races_years.split(',')

        for i in range(0, len(years), years_per_row):
            print('\t' + ','.join(years[i:i+years_per_row]))

        if prev_names:
            print(f"Previous names: \n\t{prev_names}")

        print()
        print(f"Direction: {direction.lower()}")        
        print(f"Type: {circuit_type.lower()}\n")
        print("Coordinates: ")
        print(f"{lat},{lon}\n")

class DB:
    def __init__(
        self, 
        db_handler: F1DB,
        out_table: Table
    ):
        self.db = db_handler
        self.table = out_table

    def update(self):
        self.db.update()

    def execute_sql(self, file: str):
        try:
            self.table.rows, self.table.headers = self.db.run_file(file)
            self.table.flush()

        except FileNotFoundError:
            return print(f'File "{file}" does not exist')
    
    def search(
        self, 
        part: str, 
        table: str, 
        column: str,
        overwrite_pattern=False
    ):
        pattern = part if overwrite_pattern else f"%{part}%"

        fetched = self.db.execute(
            f"SELECT * FROM {table} WHERE {table}.{column} LIKE ?"
        , [pattern])

        headers = []
        name_index = 0

        for i, c in enumerate(self.db.cur.description):
            headers.append(c[0])
            if c[0] == "name": 
                name_index = i

        for found in fetched:
            print(f"\n---- Found: {found[name_index]} ----\n")

            for i in range(len(headers)):
                print(f"{headers[i]}: {found[i]}")
