#!/usr/bin/env python3
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

def circuit(circuit_id: str, sql: str, rows=15, is_reversed=False):
    run_sql(sql, [circuit_id])
    fetched = cur.fetchall() if rows == -1 else cur.fetchmany(rows)
    headers = [c[0] for c in cur.description]

    if is_reversed:
        print_table(fetched[::-1], headers, double_headers=True)
    else:
        print_table(fetched, headers, double_headers=True)

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
    print(f"Type: {circuit_type.lower()}")
    print()
    print("Coordinates: ")
    print(f"{lat},{lon}")
    print()


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
        
        case "champ":
            championship(args.year, args.constructor)
        
        case "driver":
            if args.season:
                driver_season(args.id, args.year)

        case "search":
            if args.driver:
                table = "driver"
            elif args.team:
                table = "constructor"
            elif args.circuit:
                table = "circuit"
            elif args.grand_prix:
                table = "grand_prix"
            else:
                return print("I dont know what to search for...")
            
            search(args.part, table, args.column, args.overwrite_pattern)
        case _:
            print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    p = ArgumentParser(description="Diferrent charts, statistics, records, all time bests of Formula One")

    subps = p.add_subparsers(dest="command", help="Available commands")

    circuit_p = subps.add_parser("circuit", help="Get different records for a circuit")
    circuit_p.add_argument      ("id", metavar="ID", type=str, help="Circuit id")
    circuit_p.add_argument      ("-bl", "--best-lap", action="store_true", help="All time best laps during the race")
    circuit_p.add_argument      ("-bq", "--best-qualifying", action="store_true", help="All time best qualifying records")
    circuit_p.add_argument      ("-mw", "--most-wins", action="store_true", help="List of drivers with most wins")
    circuit_p.add_argument      ("-mp", "--most-podiums", action="store_true", help="List of drivers with most podiums")
    circuit_p.add_argument      ("-r", "--rows", type=int, default=15, help="Amount of rows to fetch, -1 means all. Defaults to 15")
    circuit_p.add_argument      ("-R", "--reverse", action="store_true", help="Reverse results")

    driver_p = subps.add_parser("driver", help="Different driver's statistics, data over the season")
    driver_p.add_argument      ("id", metavar="ID", type=str, help="Driver id")
    driver_p.add_argument      ("year", metavar="YEAR", type=str, help="Season year")
    driver_p.add_argument      ("-s", "--season", action="store_true", help="Get overall driver's statistics over season")
    
    champ_p = subps.add_parser("champ", help="Fancy wikipedia like season table for driver/constructor champ")
    champ_p.add_argument      ("year", metavar="YEAR", type=str, help="Season year")
    champ_p.add_argument      ("-c", "--constructor", action="store_true", help="Show constructor standing instead of driver")

    search_p = subps.add_parser("search", help="Search for different things by name")
    search_p.add_argument      ("part", metavar="PART", type=str, help="Part to search for")
    search_p.add_argument      ("-d", "--driver", action="store_true", help="Search for driver")
    search_p.add_argument      ("-t", "--team", action="store_true", help="Search for a team (constructor)")
    search_p.add_argument      ("-c", "--circuit", action="store_true", help="Search for circuit")
    search_p.add_argument      ("-gp", "--grand-prix", action="store_true", help="Search for grand prix")
    search_p.add_argument      ("-C", "--column", type=str, default="name", help="Colum to match part, defaults to \"name\"")
    search_p.add_argument      ("-op", "--overwrite-pattern", action="store_true", help="Treat part as entire pattern for sql LIKE when searching")

    args = p.parse_args()

    if any(vars(args).values()):
        main(args)
    else:
        p.print_help()