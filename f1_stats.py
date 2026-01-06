#!/usr/bin/env python3
import os, argparse

from lib.tables import Table
from lib.classes import (
    Streak, 
    F1DB, 
    GP,
    DB,
    Driver, 
    Season,
    Circuit
)

def main(args: argparse.Namespace):
    table = Table(
        args.adjustment,
        args.double_headers,
        args.no_delimiters
    )

    f1db = F1DB(
        root_dir=os.path.dirname(os.path.realpath(__file__))
    ) 

    match args.command:
        case "circuit":
            circuit = Circuit(args.id, args.rows, args.reverse, f1db, table)

            if args.info:
                circuit.info()

            if args.best_lap:
                circuit.record("best-lap")

            if args.best_qualifying:
                circuit.record("best-qualifying")

            if args.most_wins:
                circuit.record("most-wins")

            if args.most_podiums:
                circuit.record("most-podiums")
        
        case "season":
            season = Season(args.year, args.gp_flags, f1db, table)
            season.championship(args.constructor)

        case "driver":
            driver = Driver(args.id, args.year, f1db, table)

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

        case "gp":
            gp = GP(args.id, args.year, f1db, table)

            if args.race:
                gp.race()

            if args.sprint:
                gp.sprint()

            if args.race_qualifying:
                gp.race_qualifying()

            if args.sprint_qualifying:
                gp.sprint_qualifying()

        case "db":
            db = DB(f1db, table)

            if args.sql:
                db.execute_sql(args.sql)

            if args.update:
                db.update()

            if args.search:
                queries = []

                if args.driver:
                    queries.append((args.driver, "driver"))

                if args.constructor:
                    queries.append((args.constructor, "constructor"))

                if args.circuit:
                    queries.append((args.circuit, "circuit"))

                if args.grand_prix:
                    queries.append((args.grand_prix, "grand_prix"))
            
                for query, table in queries:
                    db.search(query, table, args.column, args.pattern)
            
        case _:
            print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Diferrent charts, statistics, records, all time bests of Formula One")

    subps = p.add_subparsers(dest="command", help="Available commands")
    p.add_argument("--double-headers", action="store_true", help="Print table headers twice (at the top and bottom)")
    p.add_argument("--no-delimiters", action="store_true", help="Do not print any separators for tables")
    p.add_argument("--adjustment", default="left", choices=("left", "center", "right"), help="Table text alignment")
    p.add_argument("--gp-flags", action="store_true", help="Add emoji flags to grand prix")

    circuit_p = subps.add_parser("circuit", help="Get different records for a circuit")
    circuit_p.add_argument      ("id",  metavar="ID", type=str,                   help="Circuit id")
    circuit_p.add_argument      ("-i",  "--info",            action="store_true", help="Show circuit info")
    circuit_p.add_argument      ("-bl", "--best-lap",        action="store_true", help="All time best laps during the race")
    circuit_p.add_argument      ("-bq", "--best-qualifying", action="store_true", help="All time best qualifying records")
    circuit_p.add_argument      ("-mw", "--most-wins",       action="store_true", help="List of drivers with most wins")
    circuit_p.add_argument      ("-mp", "--most-podiums",    action="store_true", help="List of drivers with most podiums")
    circuit_p.add_argument      ("-R",  "--reverse",         action="store_true", help="Reverse results")
    circuit_p.add_argument      ("-r",  "--rows", type=int,  default=15,          help="Amount of rows to fetch, -1 means all. Defaults to 15")

    driver_p = subps.add_parser("driver", help="Different driver's statistics, data over the season")
    driver_p.add_argument      ("id",   metavar="ID",   type=str,            help="Driver id")
    driver_p.add_argument      ("year", metavar="YEAR", type=str,            help="Season year")
    driver_p.add_argument      ("-r", "--races",        action="store_true", help="Table of driver season races")
    driver_p.add_argument      ("-s", "--sprints",      action="store_true", help="Table of driver season sprints")
    driver_p.add_argument      ("-q", "--qualifying",   action="store_true", help="Table of driver race qualifyings")
    driver_p.add_argument      ("-p", "--pit-stops",    action="store_true", help="Table of pit stops for each race")
    driver_p.add_argument      ("-o", "--overview",     action="store_true", help="An overview, driver statistics for a season")
    
    race_p = subps.add_parser("gp",   help="Grand prix results tables")
    race_p.add_argument      ("id",   metavar="ID",         type=str,             help="Grand prix id, e.g: monaco")
    race_p.add_argument      ("year", metavar="YEAR",       type=str,             help="Year gp held")
    race_p.add_argument      ("-r", "--race",               action="store_true",  help="Show race results")
    race_p.add_argument      ("-s", "--sprint",             action="store_true",  help="Show sprint results")
    race_p.add_argument      ("-rq", "--race-qualifying",   action="store_true",  help="Show race qualifying result")
    race_p.add_argument      ("-sq", "--sprint-qualifying", action="store_true",  help="Show sprint qualifying result")

    champ_p = subps.add_parser("season", help="Fancy wikipedia like season table for driver/constructor championship")
    champ_p.add_argument      ("year", metavar="YEAR", type=str, help="Season year")
    champ_p.add_argument      ("-c", "--constructor", action="store_true", help="Show constructor standing instead of driver")


    db_p = subps.add_parser("db",  help="Different database related commands")
    db_p.add_argument      ("-s",  "--sql",          type=str,              help="Run arbitrary sql on the f1db")
    db_p.add_argument      ("-u",  "--update",       action="store_true",   help="Update/init f1db")
    db_p.add_argument      ("-S",  "--search",       action="store_true",   help="Search by given part")
    db_p.add_argument      ("-d",  "--driver",       type=str,              help="If searching, search for driver")
    db_p.add_argument      ("-t",  "--constructor",  type=str,              help="If searching, search for a constructor (team)")
    db_p.add_argument      ("-c",  "--circuit",      type=str,              help="If searching, search for circuit")
    db_p.add_argument      ("-g",  "--grand-prix",   type=str,              help="If searching, search for grand prix")
    db_p.add_argument      ("--pattern",             type=str,              help="If searching, treat part as entire pattern for sql LIKE when searching")
    db_p.add_argument      ("--column",  type=str,   default="name",        help="If searching, use given colum to match part, defaults to \"name\"")

    args = p.parse_args()

    if any(vars(args).values()):
        main(args)
    else:
        p.print_help()