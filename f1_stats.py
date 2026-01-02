#!/usr/bin/env python3
from statistics import mean, stdev, median, median_low, median_high, mode

import sqlite3, os, subprocess
from lib.tables import print_table
from lib.emoji import gp_flags
from argparse import ArgumentParser
from collections import defaultdict
from typing import Callable

from itertools import islice
from os.path import join

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

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE_DIR = join(ROOT_DIR, "data", "f1db.db")
SQL_SCRIPTS_DIR = join(ROOT_DIR, "sql")

SUP_F = "\u1DA0"
SUP_P = "\u1D56"

is_double_headers = False
is_no_delims = False
add_gp_flags = False
adjustment = "left"

conn = sqlite3.connect(DATABASE_DIR)
cur = conn.cursor()

def ifnone(data: any, then: any):
    return data if data is not None else then

def run_sql(name: str, params=None):
    with open(join(SQL_SCRIPTS_DIR, name + ".sql")) as f:
        sql = f.read()

    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)

def execute_sql(file: str | None):
    is_tmp = False

    if file is None:
        file = "tmp.sql"
        os.system(f"{os.getenv("EDITOR", "nano")} {file}")
        
        if not os.path.exists(file):
            return

        is_tmp = True

    try:
        content = None
        with open(file) as f:
            content = f.read()
        
        cur.execute(content)
        fetched = cur.fetchall()
        headers = [c[0] for c in cur.description]
        
        print_table(
            fetched, 
            headers,        
            double_headers=is_double_headers,
            adjustment=adjustment,
            hide_delimiters=is_no_delims
        )

    except FileNotFoundError:
        return print(f"File \"{file}\" does not exist")

    finally:
        if is_tmp: os.remove(file)


def driver_races_table(driver_id: str, year: int):
    run_sql("driver-races-table", { "id": driver_id, "year": year })

    rows = cur.fetchall()
    headers = [c[0] for c in cur.description[6:]]
    out_rows = []
    comments = []

    teams_played = defaultdict(int)
    FINISHED = 2
    PTS_POS = -2
    BEST_LAP_TIME = -5

    for is_fastest, is_pole, reason_retired, team, \
        pts_pos_gained, gap_from_fastest_lap, *row in rows:

        if reason_retired is not None:
            comments.append(f"* Retired because of - {reason_retired}")
            row[FINISHED] += '*'

        if is_pole:
            row[FINISHED] += SUP_P

        if is_fastest:
            row[FINISHED] += SUP_F

        if pts_pos_gained:
            sign = '+' if pts_pos_gained > 0 else ''
            row[PTS_POS] += f" ({sign}{pts_pos_gained})"

        if gap_from_fastest_lap:
            row[BEST_LAP_TIME] += f" ({gap_from_fastest_lap})"
        
        out_rows.append(row)
        teams_played[team] += 1

    comments.append('-' * 40)
    for team, total in teams_played.items():
        if len(teams_played) == 1:
            comments.append(f"All {total} games played in: {team}")
        else:
            comments.append(f"{total} games played in {team}")

    print_table(
        out_rows, 
        headers, 
        double_headers=is_double_headers,
        adjustment=adjustment,
        hide_delimiters=is_no_delims
    )
    
    print('\n'.join(comments), end="\n\n")

def driver_pit_stops(driver_id: str, year: int):
    run_sql("driver-pits", {"id": driver_id, "year": year})
    fetched = cur.fetchall()

    races_pits = defaultdict(list)
    most_pits = -1

    for race, lap, time in fetched:
        pit = {
            "lap": lap,
            "time": time
        }

        races_pits[race].append(pit)
        total_pits = len(races_pits[race])

        if  total_pits > most_pits:
            most_pits = total_pits

    out_rows = []
    headers = [f"pit {i+1}" for i in range(most_pits)]

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
        out_rows.append(row)

    print_table(
        out_rows, 
        [''] + headers + [''], 
        double_headers=is_double_headers,
        adjustment=adjustment,
        hide_delimiters=is_no_delims
    )

def driver_qualifying(driver_id: str, year: int):
    run_sql("driver-qualifying", {"id": driver_id, "year": year})
    fetched = cur.fetchall()
    headers = [c[0] for c in cur.description]

    print_table(
        fetched, 
        headers, 
        double_headers=is_double_headers,
        adjustment=adjustment,
        hide_delimiters=is_no_delims
    )

def driver_sprints(driver_id: str, year: int):
    run_sql("driver-sprints", {"id": driver_id, "year": year})
    fetched = cur.fetchall()
    headers = [c[0] for c in cur.description]

    print_table(
        fetched, 
        headers, 
        double_headers=is_double_headers,
        adjustment=adjustment,
        hide_delimiters=is_no_delims
    )

def driver_overview(driver_id: str, year: int):
    run_sql("driver-season-overview", {"id": driver_id, "year": year})
    fetched = cur.fetchall()
    
    if not fetched:
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
        gap, laps, penalty, pts_after_race, pts_made, pts_pos_after, team_pts_after_race in fetched:

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
    cur.execute(
        "SELECT pit.pit_stop_time_millis FROM race_data pit JOIN race on race.id = pit.race_id WHERE pit.type = 'PIT_STOP' and pit.driver_id = :id and race.year = :year",
        {"id": driver_id, "year": year}
    )

    pit_times = []
    problematic_pits = 0
    avg_pit_time = 0

    for row in cur.fetchall():
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

    print(f"\nSeason overview — {driver_id}, {year}")
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

def circuit(circuit_id: str, sql: str, rows=15, is_reversed=False):
    run_sql(sql, [circuit_id])
    fetched = cur.fetchall() if rows == -1 else cur.fetchmany(rows)
    headers = [c[0] for c in cur.description]

    if is_reversed:
        fetched.reverse()

    print_table(
        fetched, 
        headers, 
        double_headers=is_double_headers,
        adjustment=adjustment,
        hide_delimiters=is_no_delims
    )

def circuit_info(circuit_id: str, years_per_row=8):
    cur.execute(
        "SELECT circuit.*, GROUP_CONCAT(race.year ,',') as years FROM circuit JOIN race on race.circuit_id = :id WHERE circuit.id = :id"
    , {"id": circuit_id})

    fetched = cur.fetchone()

    if not fetched or fetched[0] is None:
        return print(f"Circuit: \"{circuit_id}\" was not found")

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


def search(part: str, table: str, column: str, overwrite_pattern=False):
    pattern = part if overwrite_pattern else f"%{part}%"

    cur.execute(
        f"SELECT * FROM {table} WHERE {table}.{column} LIKE ?"
    , [pattern])

    fetched = cur.fetchall()
    headers = []
    name_index = 0

    for i, c in enumerate(cur.description):
        headers.append(c[0])
        if c[0] == "name": 
            name_index = i

    for found in fetched:
        print(f"\n---- Found: {found[name_index]} ----\n")

        for i in range(len(headers)):
            print(f"{headers[i]}: {found[i]}")

def season(year: int, is_constructor=False):
    cur.execute(
        "SELECT grand_prix.id, grand_prix.abbreviation FROM grand_prix JOIN race on race.year = ? WHERE race.grand_prix_id = grand_prix.id"
    , [year])

    grandprix_cols = []
    grandprix_template = {}
    out_rows = []

    if add_gp_flags:
        flags = []

    for gp, abbr in cur.fetchall():
        if add_gp_flags:
            flags.append(gp_flags[gp])

        grandprix_cols.append(abbr)
        grandprix_template[abbr] = None

    run_sql("championship", {"year": year})
    rows = cur.fetchall()

    drivers_results = defaultdict(lambda: dict(grandprix_template))
    teams_drivers = defaultdict(dict)
    drivers_points = {}
    teams_points = {}

    for abbrev, name, finish_pos, points, is_pole, is_fastest, team, team_points in rows:
        drivers_results[name][abbrev] = finish_pos
        drivers_points[name] = points
        teams_points[team] = ifnone(team_points, 0)

        if is_pole:
            drivers_results[name][abbrev] += SUP_P

        if is_fastest:
            drivers_results[name][abbrev] += SUP_F
        
        teams_drivers[team][name] = drivers_results[name]

    pos = 1

    if is_constructor:
        sorted_teams_points = sorted(teams_points.items(), reverse=True, key=lambda kv: kv[1])
        
        for team, points in sorted_teams_points:
            team_drivers = teams_drivers[team]

            for name, results in islice(team_drivers.items(), 2):
                per_races = [results[abbr] for abbr in grandprix_cols]
                out_rows.append([pos, team] + per_races + [points])
            
            pos += 1
    else:
        for name, points in drivers_points.items():
            per_races = [drivers_results[name].get(abbr) for abbr in grandprix_cols]
            out_rows.append([pos, name] + per_races + [points])
            pos += 1

    if add_gp_flags:
        for i in range(len(grandprix_cols)):
            abbr = grandprix_cols[i]
            grandprix_cols[i] = f"{flags[i]} {abbr}"

    print_table(
        rows=out_rows,
        headers=["pos", "name"] + grandprix_cols + ["pts"],
        double_headers=is_double_headers,
        adjustment=adjustment,
        hide_delimiters=is_no_delims
    )

def main(args: any):
    global is_double_headers
    global is_no_delims
    global adjustment
    global add_gp_flags

    add_gp_flags = args.gp_flags
    is_double_headers = args.double_headers
    is_no_delims = args.no_delimiters
    adjustment = args.adjustment

    match args.command:
        case "circuit":
            if not args.best_lap and not args.best_qualifying and \
                not args.most_wins and not args.most_podiums:
                circuit_info(args.id)

            if args.best_lap:
                circuit(args.id, "best-lap", args.rows, args.reverse)

            if args.best_qualifying:
                circuit(args.id, "best-qualifying", args.rows, args.reverse)

            if args.most_wins:
                circuit(args.id, "most-wins", args.rows, args.reverse)

            if args.most_podiums:
                circuit(args.id, "most-podiums", args.rows, args.reverse)
        
        case "season":
            season(args.year, args.constructor)
        
        case "driver":
            if args.races:
                driver_races_table(args.id, args.year)
            
            if args.pit_stops:
                driver_pit_stops(args.id, args.year)

            if args.overview:
                driver_overview(args.id, args.year)

            if args.qualifying:
                driver_qualifying(args.id, args.year)

            if args.sprints:
                driver_sprints(args.id, args.year)

        case "db":
            if args.sql:
                execute_sql(args.sql)

            if args.update:
                os.chdir(ROOT_DIR)
                subprocess.run(
                    [join(ROOT_DIR, "install")], 
                    check=True
                )

        case "search":
            if args.driver:
                table = "driver"
            elif args.constructor:
                table = "constructor"
            elif args.circuit:
                table = "circuit"
            elif args.grand_prix:
                table = "grand_prix"
            else:
                return print("I don't know what to search for...")
            
            search(args.part, table, args.column, args.overwrite_pattern)
        case _:
            print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    p = ArgumentParser(description="Diferrent charts, statistics, records, all time bests of Formula One")

    subps = p.add_subparsers(dest="command", help="Available commands")
    p.add_argument("--double-headers", action="store_true", help="Print table headers twice (at the top and bottom)")
    p.add_argument("--no-delimiters", action="store_true", help="Do not print any separators for tables")
    p.add_argument("--adjustment", default="left", choices=("left", "center", "right"), help="Table text alignment")
    p.add_argument("--gp-flags", action="store_true", help="Add emoji flags to grand prix")

    circuit_p = subps.add_parser("circuit", help="Get different records for a circuit")
    circuit_p.add_argument      ("id",  metavar="ID", type=str,                   help="Circuit id")
    circuit_p.add_argument      ("-bl", "--best-lap",        action="store_true", help="All time best laps during the race")
    circuit_p.add_argument      ("-bq", "--best-qualifying", action="store_true", help="All time best qualifying records")
    circuit_p.add_argument      ("-mw", "--most-wins",       action="store_true", help="List of drivers with most wins")
    circuit_p.add_argument      ("-mp", "--most-podiums",    action="store_true", help="List of drivers with most podiums")
    circuit_p.add_argument      ("-R",  "--reverse",         action="store_true", help="Reverse results")
    circuit_p.add_argument      ("-r",  "--rows", type=int,  default=15,          help="Amount of rows to fetch, -1 means all. Defaults to 15")

    driver_p = subps.add_parser("driver", help="Different driver's statistics, data over the season")
    driver_p.add_argument      ("id",   metavar="ID",   type=str,            help="Driver id")
    driver_p.add_argument      ("year", metavar="YEAR", type=str,            help="Season year")
    driver_p.add_argument      ("-r", "--races",        action="store_true", help="Get a table of driver season races")
    driver_p.add_argument      ("-s", "--sprints",      action="store_true", help="Get a table of driver season sprints")
    driver_p.add_argument      ("-q", "--qualifying",   action="store_true", help="Get a table of driver qualifyings")
    driver_p.add_argument      ("-p", "--pit-stops",    action="store_true", help="Get a table of pit stops for each race")
    driver_p.add_argument      ("-o", "--overview",     action="store_true", help="An overview, driver statistics for a season")
    
    champ_p = subps.add_parser("season", help="Fancy wikipedia like season table for driver/constructor championship")
    champ_p.add_argument      ("year", metavar="YEAR", type=str, help="Season year")
    champ_p.add_argument      ("-c", "--constructor", action="store_true", help="Show constructor standing instead of driver")

    search_p = subps.add_parser("search", help="Search for different rows in tables by name")
    search_p.add_argument      ("part", metavar="PART",       type=str,            help="Part to search for")
    search_p.add_argument      ("-d",  "--driver",            action="store_true", help="Search for driver")
    search_p.add_argument      ("-c",  "--constructor",       action="store_true", help="Search for a constructor (team)")
    search_p.add_argument      ("-C",  "--circuit",           action="store_true", help="Search for circuit")
    search_p.add_argument      ("-gp", "--grand-prix",        action="store_true", help="Search for grand prix")
    search_p.add_argument      ("-op", "--overwrite-pattern", action="store_true", help="Treat part as entire pattern for sql LIKE when searching")
    search_p.add_argument      ("-col","--column", type=str,  default="name",      help="Colum to match part, defaults to \"name\"")

    db_p = subps.add_parser("db", help="Different database related commands")
    db_p.add_argument      ("-s", "--sql", type=str, nargs='?', help="Run arbitrary sql on the f1db")
    db_p.add_argument      ("-u", "--update", action="store_true", help="Update/init f1db")

    args = p.parse_args()

    if any(vars(args).values()):
        main(args)
    else:
        p.print_help()