import sqlite3, os
from lib.tables import print_table
from statistics import mean
from argparse import ArgumentParser
from collections import defaultdict

from itertools import islice

SUP_F = "\u1DA0"
SUP_P = "\u1D56"

conn = sqlite3.connect("data/f1db.db")
cur = conn.cursor()

def ifnone(data: any, then: any):
    return data if data is not None else then

def run_sql(name: str, params: list | dict):
    with open(os.path.join("sql", name + ".sql")) as f:
        sql = f.read()

    cur.execute(sql, params)

def driver_season(driver_id: str, year: int):
    run_sql("driver-season", { "id": driver_id, "year": year })

    rows = cur.fetchall()
    headers = [c[0] for c in cur.description[2:]]
    out_rows = [] 

    for is_fastest, is_pole, *row in rows:
        if is_pole:
           row[2] += SUP_P

        if is_fastest:
            row[2] += SUP_F
        
        out_rows.append(row)

    print_table(out_rows, headers, hide_nones=True, double_headers=True)

def best_lap(circuit_id: str, rows=15, is_reversed=False):
    run_sql("best-lap", [circuit_id])
    fetched = cur.fetchall() if rows == -1 else cur.fetchmany(rows)
    headers = [c[0] for c in cur.description]

    if is_reversed:
        print_table(fetched[::-1], headers)
    else:
        print_table(fetched, headers)

def best_qual(circuit_id: str, rows=15, is_reversed=False):
    run_sql("best-qualifying", [circuit_id])

    fetched = cur.fetchall() if rows == -1 else cur.fetchmany(rows)
    headers = [c[0] for c in cur.description]

    if is_reversed:
        print_table(fetched[::-1], headers, double_headers=True, hide_nones=True)
    else:
        print_table(fetched, headers, double_headers=True, hide_nones=True)

def championship(year: int, is_constructor=False):
    cur.execute(
        "SELECT grand_prix.abbreviation FROM grand_prix JOIN race on race.year = ? WHERE race.grand_prix_id = grand_prix.id"
    , [year])

    grandprix_cols = []
    grandprix_template = {}
    out_rows = []

    for col in cur.fetchall():
        abbr = col[0]
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
        teams_points[team] = team_points

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

    print_table(
        out_rows,
        ["pos", "name"] + grandprix_cols + ["pts"],
        hide_nones=True,
        double_headers=True
    )

def main(args: any):
    match args.command:
        case "circuit":
            if args.best_lap:
                best_lap(args.id, args.rows, args.reverse)

            if args.qualifying_record:
                best_qual(args.id, args.rows, args.reverse)
        
        case "champ":
            championship(args.year, args.constructor)
        
        case "driver":
            if args.season:
                driver_season(args.id, args.year)

        case _:
            print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    p = ArgumentParser(description="Diferrent charts, statistics, records, all time bests of Formula One")

    subps = p.add_subparsers(dest="command", help="Available commands")

    circuit_p = subps.add_parser("circuit", help="Get different records for a circuit")
    circuit_p.add_argument      ("id", metavar="ID", type=str, help="Circuit id")
    circuit_p.add_argument      ("-bl", "--best-lap", action="store_true", help="All time best laps during the race")
    circuit_p.add_argument      ("-qr", "--qualifying-record", action="store_true", help="All time best qualifying records")
    circuit_p.add_argument      ("-r", "--rows", type=int, default=15, help="Amount of rows to fetch")
    circuit_p.add_argument      ("-R", "--reverse", action="store_true", help="Reverse results")

    driver_p = subps.add_parser("driver", help="Different driver's statistics, data over the season")
    driver_p.add_argument      ("id", metavar="ID", type=str, help="Driver id")
    driver_p.add_argument      ("year", metavar="YEAR", type=str, help="Season year")
    driver_p.add_argument      ("-s", "--season", action="store_true", help="Get overall driver's statistics over season")
    
    champ_p = subps.add_parser("champ", help="Fancy wikipedia like season table for driver/constructor champ")
    champ_p.add_argument      ("year", metavar="YEAR", type=str, help="Season year")
    champ_p.add_argument      ("-c", "--constructor", action="store_true", help="Show constructor standing instead of driver")

    args = p.parse_args()

    if any(vars(args).values()):
        main(args)
    else:
        p.print_help()