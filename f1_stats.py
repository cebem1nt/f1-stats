#!/usr/bin/env python3
import os, argparse

from argparse import ArgumentParser
from typing import Any, Optional
from lib.tables import print_table, Table
from lib.classes import (
    Streak, 
    F1DB, 
    GP, 
    Driver, 
    Season
)

db = F1DB(
    root_dir=os.path.dirname(os.path.realpath(__file__))
)

def execute_sql(file: Optional[str]):
    try:
        fetched, headers = db.run_file(file)
        
        print_table(
            fetched, 
            headers,        
            double_headers=is_double_headers,
            adjustment=adjustment,
            hide_delimiters=is_no_delims
        )

    except FileNotFoundError:
        return print(f'File "{file}" does not exist')
   
def circuit(circuit_id: str, sql: str, rows=15, is_reversed=False):
    fetched = db.run_script(sql, [circuit_id])
    headers = [c[0] for c in db.cur.description]

    if rows != -1:
        fetched = fetched[:rows]

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
    sql = """
        SELECT 
            circuit.*, 
            GROUP_CONCAT(race.year ,',') as years 
        FROM circuit 
        JOIN race on race.circuit_id = :id 
        WHERE circuit.id = :id
    """
    fetched = db.execute(sql, {"id": circuit_id})[0]

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

    fetched = db.execute(
        f"SELECT * FROM {table} WHERE {table}.{column} LIKE ?"
    , [pattern])

    headers = []
    name_index = 0

    for i, c in enumerate(db.cur.description):
        headers.append(c[0])
        if c[0] == "name": 
            name_index = i

    for found in fetched:
        print(f"\n---- Found: {found[name_index]} ----\n")

        for i in range(len(headers)):
            print(f"{headers[i]}: {found[i]}")

def main(args: Any):
    table = Table(
        args.adjustment,
        args.double_headers,
        args.no_delimiters
    ) 

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
            season = Season(args.year, args.gp_flags, db, table)
            season.standing(args.constructor)

        case "driver":
            driver = Driver(args.id, args.year, db, table)

            if args.races:
                driver.races()
            
            if args.pit_stops:
                driver.pits(s)

            if args.overview:
                driver.overview()

            if args.qualifying:
                driver.qualifying()

            if args.sprints:
                driver.sprints()

        case "db":
            if args.sql:
                execute_sql(args.sql)

            if args.update:
                db.update()

        case "gp":
            gp = GP(args.id, args.year, db, table)

            if args.race:
                gp.race()

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
    
    race_p = subps.add_parser("gp", help="Grand prix results tables")
    race_p.add_argument      ("id", metavar="ID", type=str, help="Grand prix id, e.g: monaco")
    race_p.add_argument      ("year", metavar="YEAR", type=str, help="Year gp held")
    race_p.add_argument      ("-r", "--race", action="store_true", help="Show race results")
    race_p.add_argument      ("-s", "--sprint", action="store_true", help="Show sprint results")
    race_p.add_argument      ("-q", "--qualifying", action="store_true", help="Show qualifying result")

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
    db_p.add_argument      ("-s", "--sql", type=str, help="Run arbitrary sql on the f1db")
    db_p.add_argument      ("-u", "--update", action="store_true", help="Update/init f1db")

    args = p.parse_args()

    if any(vars(args).values()):
        main(args)
    else:
        p.print_help()