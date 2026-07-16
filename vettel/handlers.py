from typing import Iterable, Optional
from statistics import mean, stdev, median, median_low, median_high, mode

from collections import defaultdict
from itertools import islice

from vettel.helpers import (
    strsign, annotate_pf,
    ifnone, separator, 
    print_comments,
    Date, Streak,
    format_date, Today
)

from vettel import fetchers
from vettel.database import DB

from vettel.tables import Table
from vettel.emoji import gp_flags, get_ioc_flag

Opt = Optional

class Database:
    def __init__(self, out_table: Table):
        self.table = out_table

    def update(self):
        DB.update()

    def execute_sql(self, file: str):
        try:
            self.table.headers, self.table.rows = DB.run_file(file)
            self.table.flush()

        except FileNotFoundError:
            return print(f'File "{file}" does not exist')

        except Exception as e:
            print(str(e))

class Search:
    def search(
        self, 
        part: str, 
        table: str, 
        column: str,
        overwrite_pattern=False
    ):
        pattern = part if overwrite_pattern else f"%{part}%"
        fetched = fetchers.raw_sql(
            f"SELECT * FROM {table} WHERE {table}.{column} LIKE ?", [pattern], as_dict=True)

        for found in fetched:
            print(f"\n---- Found: {found["name"]} ----\n")

            for key, value in found.items():
                print(f"{key}: {value}")                

class Race:
    def __init__(
        self,
        id: str, 
        year: int,
        table: Table,
        is_full: bool = False,
    ):
        self.table = table
        self.is_full = is_full
        self.id = id
        self.year = year

        if not self.is_full:
            self.table.hide_delimiters = True

        if id.lower() == "last":
            self.id = fetchers.get_last_race_circuit_id() 

    def race(self):
        headers, rows = fetchers.race(self.id, self.year)

        if not rows:
            return print(f"No race found: {self.id} - {self.year}")

        comments = []
        dnf_comments = []

        for is_fastest, _, reason_retired, pts_pos_gained, fastest_lap_gap, pos_gained, penalty, *row in rows:
            driver = row[1]

            if is_fastest:
                comments.append(f"Fastest lap: {driver} - {row[-3]} (lap {row[-4]})\n")

            if reason_retired:
                dnf_comments.append(f"{driver} - Reason retired: {reason_retired}")

            if pos_gained:
                row[0] += f" ({strsign(pos_gained)})"

            if penalty:
                row[0] += '*'
                comments.append(f"* - {driver} got {penalty}s penalty")

            if pts_pos_gained:  row[-2] += f" ({strsign(pts_pos_gained)})"
            if fastest_lap_gap: row[-3] += f" ({fastest_lap_gap})"

            if self.is_full:
                self.table.add_row(row)
            else:
                self.table.add_row([row[0], driver, row[-1]])

        if self.is_full:
            self.table.headers = headers[7:] # Strip these, we used first 7 columns for some anotations 
        else:
            self.table.headers = ["Finish", "Driver", "Points"]

        self.table.flush()
        print_comments(comments)

        if dnf_comments:
            print(separator())
            print_comments(dnf_comments)

    def qualifying(self):
        headers, rows = fetchers.qualifying(self.id, self.year, as_dict=not self.is_full)

        if not rows:
            return print(f"No race qualifying found: {self.id} - {self.year}")

        self.table.headers = headers
        self.table.rows = rows

        if not self.is_full:
            self.table.headers = ["Driver", "Time", "Grid"]
            self.table.rows = []
            
            for inf in rows:
                q = inf.get("Time") or inf.get("Q3") or inf.get("Q2") or inf.get("Q1")
                self.table.add_row([inf["Driver"], q, inf["Grid"]])

        self.table.flush()

class Results:
    def __init__(
        self, 
        year: int, 
        table: Table, 
        is_full: bool = False
    ):
        self.table = table
        self.year = year
        self.is_full = is_full

        if not is_full:
            self.table.hide_delimiters = True

    def results(self, is_quali: bool):
        self.table.headers, rows = fetchers.race_results(self.year, is_quali)
        
        if not rows:
            return print(f"No races found for: {self.year}")

        if not self.is_full:
            self.table.headers = self.table.headers[:5]

        for gp_date, *row in rows:
            if not self.is_full:
                row = row[:4]

            date_formatted = format_date(gp_date)
            self.table.rows.append([date_formatted] + row)
        
        self.table.flush()

class Sprint:
    def __init__(
        self,
        id: str, 
        year: int,
        table: Table,
        is_full: bool = False
    ):
        self.table = table
        self.id = id
        self.year = year
        self.is_full = is_full

        if not self.is_full:
            self.table.hide_delimiters = True

    def sprint(self):
        headers, rows = fetchers.sprint(self.id, self.year) 
        if not rows:
            return print(f"No sprint found: {self.id} - {self.year}")

        if self.is_full:
            self.table.headers = headers[3:]
        else:
            self.table.headers = ["Finish", "Driver", "Points"]

        comments = []
        dnf_comments = []

        for pos_gained, reason_retired, penalty, *row in rows:
            driver = row[1]

            if reason_retired:
                dnf_comments.append(f"{driver} - Reason retired: {reason_retired}")

            if pos_gained: row[0] += f" ({strsign(pos_gained)})"

            if penalty:
                row[0] += '*'
                comments.append(f"* - {driver} got {penalty}s penalty")

            if self.is_full:
                self.table.add_row(row)
            else:
                self.table.add_row([driver, row[3], row[-1]])

        self.table.flush()
        if comments: 
            print_comments(comments)

        if dnf_comments:
            print(separator())
            print_comments(dnf_comments)

    def qualifying(self):
        headers, rows = fetchers.sprint_qualifying(self.id, self.year, as_dict=not self.is_full)

        if not rows:
            return print(f"No sprint qualifying found: {self.id} - {self.year}")

        self.table.headers = headers
        self.table.rows = rows

        if not self.is_full:
            self.table.headers = ["Driver", "Time", "Grid"]
            self.table.rows = []
            
            for inf in rows:
                q = inf.get("Q3") or inf.get("Q2") or inf.get("Q1")
                self.table.add_row([inf["Driver"], q, inf["Grid"]])

        self.table.flush()

class Driver:
    def __init__(
        self,
        id: str, 
        year: int,
        table: Table,
        is_all_time: bool = False
    ):
        self.id = id
        self.year = year
        self.table = table
        self.is_all_time = is_all_time

    def races(self):
        headers, rows = fetchers.driver_races(self.id, self.year, self.is_all_time)

        comments = []
        dnf_comments = []
        teams_played = defaultdict(int)

        self.table.headers = headers[7:]

        for is_fastest, is_pole, reason_retired, pts_pos_gained, fastest_gap, pos_gained, penalty, *row in rows:
            row[3] = annotate_pf(row[3], is_pole, is_fastest)
            team = row[1]

            if penalty:
                comments.append(f"{row[0]} - got {penalty}s penalty")
                row[3] += '*'

            if reason_retired:
                dnf_comments.append(f"{row[0]} - Retired because of {reason_retired}")
                row[3] += '*'

            if fastest_gap:     row[-4] += f" ({fastest_gap})"
            if pts_pos_gained:  row[-2] += f" ({strsign(pts_pos_gained)})"
            
            self.table.add_row(row)
            teams_played[team] += 1

        self.table.flush()

        for team, total in teams_played.items():
            if len(teams_played) == 1:
                print(f"All {total} races completed in: {team}")
            else:
                print(f"{total} races completed in {team}")

        if comments:
            print(separator())
            print_comments(comments)

        if dnf_comments:
            print(separator())
            print_comments(dnf_comments)

    def pits(self):
        _, rows = fetchers.driver_pits(self.id, self.year, as_dict=True)
        races_pits = defaultdict(list)
        most_pits = -1

        for pit in rows:
            gp = pit["GP"]
            races_pits[gp].append(pit)
            total_pits = len(races_pits[gp])

            if total_pits > most_pits:
                most_pits = total_pits

        self.table.headers = ['Grand prix'] + [f"pit {i+1}" for i in range(most_pits)] + ['']

        for race, pits in races_pits.items():
            row = [race]
            total_pits = 0   
            
            for i in range(most_pits):
                if i >= len(pits):
                    row.append(None)
                    continue

                pit = pits[i]
                row.append(f"lap {pit["Lap"]} - {pit["Time"]}")
                total_pits += 1

            row.append(total_pits)
            self.table.add_row(row)

        self.table.flush()

    def qualifying(self):
        self.table.headers, self.table.rows = fetchers.driver_qualifying(self.id, self.year, self.is_all_time)
        self.table.flush()

    def sprints(self):
        self.table.headers, self.table.rows = fetchers.driver_sprints(self.id, self.year, self.is_all_time)
        self.table.flush()

    def overview(self):
        _, rows = fetchers.driver_overview(self.id, self.year, self.is_all_time)
    
        if not rows:
            return print(f"No data found for {self.id} - {self.year}")

        per_race_pts_made = []
        per_race_team_pts_made = []
        grid_postitions = []
        finish_positions = []
        gained_positions = []
        race_pit_stops = []
        season_pts_pos = None
        team_prev_pts = 0

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

        for year, gp, is_fastest, is_pole, q3, pits, start, finish, finish_text, reason_retired, gained,\
            gap, laps, penalty, pts_made, pts_pos_after, sprint_points, team_pts_after_race in rows:

            longest_win_streak.update(finish, (year, gp))
            longest_pod_streak.update(finish, (year, gp))
            longest_pts_streak.update(finish, (year, gp))

            pts_made = ifnone(pts_made, 0)
            sprint_points = ifnone(sprint_points, 0)
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

            if team_prev_pts > team_pts_after_race:
                team_pts_made = team_pts_after_race
            else:
                team_pts_made = team_pts_after_race - team_prev_pts

            total["races"] += 1
            total["poles"] += ifnone(is_pole, 0)
            total["fastest_laps"] += ifnone(is_fastest, 0)
            total["pts"] += pts_made + sprint_points
            total["team_pts"] += team_pts_made
            season_pts_pos = pts_pos_after
            per_race_pts_made.append(pts_made)
            per_race_team_pts_made.append(team_pts_made)
            
            team_prev_pts = team_pts_after_race

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

        _, rows = fetchers.driver_pits(self.id, self.year)
        
        pit_times = []
        problematic_pits = 0
        avg_pit_time = 0

        for ms, *_ in rows:
            if not ms: continue
            pit_times.append(ms / 1000)

        if pit_times:
            pit_times.sort()
        
            n = len(pit_times)
            q1 = median_low(pit_times[:n//2])
            q3 = median_high(pit_times[(n+1)//2:])
            iqr = q3 - q1

            slow_thresh = median(pit_times) + 1.5 * iqr
            problematic_thresh = median(pit_times) + 3.0 * iqr

            problematic_pits = sum(1 for t in pit_times if t > problematic_thresh)
            avg_pit_time = mean([t for t in pit_times if t < problematic_thresh])

        print(f"\nSeason overview — {self.id} ({"All time" if self.is_all_time else self.year})")
        print("-" * 50)
        print(f"Races: {total["races"]}  Finished: {total["finished"]}  Not finished/started: {not_finished} ",
              f"(rate: {not_finished_rate:.1%})" if not_finished > 0 else '', end="\n\n")

        print("Points")
        print(f"- Total pts: {total["pts"]} pts { '' if self.is_all_time else f"({season_pts_pos} place)"}")
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
        print(f"- Races net gain: {pct_gain:.1%}")
        print(f"- Races net loss: {pct_loss:.1%}")
        print(f"- Races no change: {pct_no_change:.1%}")

        pod_streak = len(longest_pod_streak.get())
        win_streak = len(longest_win_streak.get())
        pts_streak = len(longest_pts_streak.get())

        print(f"- Longest podium streak: {pod_streak}" + 
              (f"\n  * {longest_pod_streak}" if pod_streak else ''))
        print(f"- Longest win streak: {win_streak}" +
              (f"\n  * {longest_win_streak}" if win_streak else ''))
        print(f"- Longest points streak: {pts_streak}" +
              (f"\n  * {longest_pts_streak}" if pts_streak else ''))

class Season:
    def __init__(
        self, 
        year: int,
        add_gp_flags: bool,
        table: Table
    ):
        self.table = table
        self.year = year
        self.add_gp_flags = add_gp_flags

    def championship(self, is_constructor: bool = False):
        _, rows = fetchers.gps(self.year)

        grandprix_cols = []
        grandprix_template = {}

        if self.add_gp_flags:
            flags = []

        for gp, abbr in rows:
            if self.add_gp_flags:
                flags.append(gp_flags[gp])

            grandprix_cols.append(abbr)
            grandprix_template[abbr] = None

        _, rows = fetchers.season_gps(self.year)

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
        table: Table
    ):
        self.table = table
        self.id = id
        self.rows = rows
        self.is_reversed = is_reversed

    def record(self, script: str):
        self.table.headers, fetched = fetchers.raw_script(f"circuit/{script}", [self.id])

        if self.rows != -1:
            fetched = fetched[:self.rows]

        if self.is_reversed:
            fetched.reverse()

        self.table.rows = fetched
        self.table.flush()

    def info(self, years_per_row=8):
        _, rows = fetchers.circuit_info(self.id)

        if not rows:
            return print(f"Circuit: \"{self.id}\" was not found")

        _, name, full_name, prev_names, circuit_type, direction, \
        place, country_id, lat, lon, length, turns, total_races, races_years = rows[0]

        print()
        print(f"* {name} ({full_name})")
        print(f"At: {country_id} - {place}")
        print(f"Lenght: {length}km, turns: {turns}")
        print(f"Total races: {total_races}")
        years = races_years.split(',')

        for i in range(0, len(years), years_per_row):
            print('\t' + ', '.join(years[i:i+years_per_row]))

        if prev_names:
            print(f"Previous names: \n\t{prev_names}")

        print()
        print(f"Direction: {direction.lower()}")        
        print(f"Type: {circuit_type.lower()}\n")
        print("Coordinates: ")
        print(f"{lat},{lon}\n")

class Calendar:
    def __init__(self, year: int, is_utc: bool):
        self.year = year
        self.as_local = not is_utc

    def calendar(self, show_full: bool, show_circuit: bool, free_practice: bool, rounds_ahead: int = 0):
        _, rows = fetchers.calendar(self.year)
        
        today = Today()
        is_current_found = False
        time_fmt = "%H:%M"
        separator_width = 36
        as_local = self.as_local 

        if not self.as_local:
            time_fmt += " %Z"
            separator_width += 4

        for rnd, gp, circuit, \
                fp1, fp1_time, fp2, fp2_time, \
                fp3, fp3_time, fp4, fp4_time, \
                race_date, race_time, \
                sprint_date, sprint_time, \
                quali_date, quali_time, \
                sprint_quali_date, sprint_quali_time in rows:

            is_current_stage = False

            race = Date(race_date, race_time)
            quali = Date(quali_date, quali_time)

            if (today < race) and (not is_current_found):
                is_current_stage = True
                is_current_found = True

            round_string = f"R{rnd} - {gp}"
            if is_current_stage:
                round_string = "-*- " + round_string + " -*-"
            
            print(round_string.center(separator_width + 2))
            
            if show_circuit: 
                print(f"Circuit: {circuit}".center(separator_width + 2))
            
            print("  " + separator(separator_width))

            if free_practice:
                practice = [(fp1, fp1_time), (fp2, fp2_time), (fp3, fp3_time), (fp4, fp4_time)]
                i = 1

                for fp_date, fp_time in practice:
                    if not fp_date or not fp_time:
                        continue

                    fp = Date(fp_date, fp_time)
                    print(f"  - Free Practice {i}:   {fp.date(as_local)} at {fp.time(as_local, time_fmt)}")
                    i += 1

            if sprint_date:
                sprint = Date(sprint_date, sprint_time)
                sprint_quali = Date(sprint_quali_date, sprint_quali_time)

                print(f"  - Sprint qualifying: {sprint_quali.date(as_local)} at {sprint_quali.time(as_local, time_fmt)}")
                print(f"  - Sprint:            {sprint.date(as_local)} at {sprint.time(as_local, time_fmt)}")

            print(f"  - Qualifying:        {quali.date(as_local)} at {quali.time(as_local, time_fmt)}")
            print(f"  - Race:              {race.date(as_local)} at {race.time(as_local, time_fmt)}")
            print()

            if not show_full and is_current_found:
                if rounds_ahead > 0:
                    rounds_ahead -= 1
                    continue

                print("....".center(separator_width))
                print()
                break

class Standings:
    def __init__(
        self,
        year: int,
        table: Table,
        is_full: bool = False
    ):
        self.table = table
        self.year = year
        self.is_full = is_full

        self.table.hide_delimiters = True

    def standings(self, is_constructor: bool = False, show_flags: bool = False):
        headers, rows = fetchers.standings(self.year, is_constructor)

        if not rows:
            return print(f"No standings found for: {self.year}")

        self.table.headers = headers[1:]

        for is_winner, *row in rows:
            if not is_constructor and show_flags:
                row[2] = f"{get_ioc_flag(row[2])} {row[2]}"

            if is_winner:
                row[1] = f"♔ {row[1]}" # "👑" messes alignment

            self.table.rows.append(row)

        self.table.flush()
