#!/usr/bin/env python3
import os, argparse, sys

from vettel.tables import Table
from vettel.helpers import Today
from vettel.handlers import (
    Database,
    Search,
    Race,
    Sprint,
    Driver, 
    Season,
    Circuit,
    Calendar,
    Standings,
    Results
)

VERSION = "1.3.0"
CURRENT_YEAR = Today().year()

def match_args(args: argparse.Namespace):
    table = Table(
        args.adjustment,
        args.double_headers,
        args.no_delimiters
    )

    argc = len(sys.argv)

    match args.command:
        case "circuit":
            circuit = Circuit(args.id, args.rows, args.reverse, table)

            if args.info or argc == 3:
                circuit.info()

            if args.best_lap:           circuit.record("best-lap")
            if args.best_qualifying:    circuit.record("best-qualifying")
            if args.most_wins:          circuit.record("most-wins")
            if args.most_podiums:       circuit.record("most-podiums")
        
        case "standings":
            standings = Standings(args.year, table)
            standings.standings(args.constructor, args.flags)

        case "season":
            season = Season(args.year, args.flags, table)
            season.championship(args.constructor)

        case "driver":
            driver = Driver(args.id, args.year, table, args.all_time)

            if args.overview:   driver.overview()
            if args.races:      driver.races()
            if args.pit_stops:  driver.pits()
            if args.qualifying: driver.qualifying()
            if args.sprints:    driver.sprints()

        case "calendar":
            calendar = Calendar(args.year, args.utc)
            calendar.calendar(args.full, args.circuit, args.free_practice, args.rounds_ahead)

        case "results":
            results = Results(args.year, table, args.full)
            results.results(args.qualifying)

        case "race":
            race = Race(args.id, args.year, table, args.full)

            if args.qualifying:
                race.qualifying()
            else:
                race.race()

        case "sprint":
            sprint = Sprint(args.id, args.year, table, args.full)

            if args.qualifying:
                sprint.qualifying()
            else:
                sprint.sprint()

        case "db":
            db = Database(table)

            if args.sql:
                db.execute_sql(args.sql)

            if args.update:
                db.update()

        case "search":
            search = Search()
            queries = []

            if args.driver:         queries.append((args.driver, "driver"))
            if args.constructor:    queries.append((args.constructor, "constructor"))
            if args.circuit:        queries.append((args.circuit, "circuit"))
            if args.grand_prix:     queries.append((args.grand_prix, "grand_prix"))
        
            for query, table in queries:
                search.search(query, table, args.column, args.as_pattern)
            
        case _:
            print(f"Unknown command: {args.command}")

def main():
    p = argparse.ArgumentParser(description="Different info, statistics, records, all time bests of Formula One")

    p.add_argument("-v", "--version",  action="store_true",                                 help="Show vettel version and exit")
    p.add_argument("--double-headers", action="store_true",                                 help="Print table headers twice (at the top and bottom)")
    p.add_argument("--no-delimiters",  action="store_true",                                 help="Do not print any separators for tables")
    p.add_argument("--adjustment",     default="left", choices=("left", "center", "right"), help="Table text alignment")

    subps = p.add_subparsers(dest="command", help="Available commands")

    circuit_p = subps.add_parser("circuit", help="Get different records for a circuit")
    circuit_p.add_argument      ("id",  metavar="ID",        type=str,            help="Circuit id")
    circuit_p.add_argument      ("-i",  "--info",            action="store_true", help="Show circuit info")
    circuit_p.add_argument      ("-bl", "--best-lap",        action="store_true", help="All time best laps during the race")
    circuit_p.add_argument      ("-bq", "--best-qualifying", action="store_true", help="All time best qualifying records")
    circuit_p.add_argument      ("-mw", "--most-wins",       action="store_true", help="List of drivers with most wins")
    circuit_p.add_argument      ("-mp", "--most-podiums",    action="store_true", help="List of drivers with most podiums")
    circuit_p.add_argument      ("-R",  "--reverse",         action="store_true", help="Reverse results")
    circuit_p.add_argument      ("-r",  "--rows", type=int,  default=15,          help="Amount of rows to fetch, -1 means all. Defaults to 15")

    driver_p = subps.add_parser("driver", help="Different driver's statistics, data over the season or all time")
    driver_p.add_argument      ("id",  metavar="ID",        type=str,            help="Driver id")
    driver_p.add_argument      ("year",metavar="YEAR",      type=int, nargs="?", default=CURRENT_YEAR, help="Optional season year. Current year if omitted")
    driver_p.add_argument      ("-o",  "--overview",        action="store_true", help="An overview, driver statistics for a season")
    driver_p.add_argument      ("-r",  "--races",           action="store_true", help="Driver race results for given season")
    driver_p.add_argument      ("-s",  "--sprints",         action="store_true", help="Driver season sprints results")
    driver_p.add_argument      ("-q",  "--qualifying",      action="store_true", help="Driver qualifying results for the season")
    driver_p.add_argument      ("-p",  "--pit-stops",       action="store_true", help="Table of pit stops for each race")
    driver_p.add_argument      ("-a",  "--all-time",        action="store_true", help="Show all time results instead")
    
    race_p = subps.add_parser("race", help="Show race results for given year and race id. Use \"last\" to show the result of the last race")
    race_p.add_argument      ("id",   metavar="ID",      type=str,            help="Grand prix or circuit id, e.g: monaco/china, shanghai")
    race_p.add_argument      ("year", metavar="YEAR",    type=int, nargs="?", default=CURRENT_YEAR, help="Year of the race. Current year if omitted")
    race_p.add_argument      ("-f", "--full",            action="store_true", help="Show full information table")
    race_p.add_argument      ("-q", "--qualifying",      action="store_true", help="Show the qualifying result instead")

    results_p = subps.add_parser("results", help="Show results for all races/quali for given year")
    results_p.add_argument      ("year",metavar="YEAR", type=int, nargs="?", default=CURRENT_YEAR, help="Season year. Current year if omitted")
    results_p.add_argument      ("-f",  "--full",       action="store_true", help="Show full information table")
    results_p.add_argument      ("-q",  "--qualifying", action="store_true", help="Show qualifying results instead")

    sprint_p = subps.add_parser("sprint", help="Sprint results")
    sprint_p.add_argument      ("id",   metavar="ID",   type=str,            help="Grand prix or circuit id, e.g: monaco/china, shanghai")
    sprint_p.add_argument      ("year", metavar="YEAR", type=int, nargs="?", default=CURRENT_YEAR, help="Year of the sprint. Current year if omitted")
    sprint_p.add_argument      ("-f", "--full",         action="store_true", help="Show full information table")
    sprint_p.add_argument      ("-q", "--qualifying",   action="store_true", help="Show the qualifying result instead")

    standings_p = subps.add_parser("standings", help="Season driver standings")
    standings_p.add_argument      ("year", metavar="YEAR", type=int, nargs="?",  default=CURRENT_YEAR,  help="Season year. Current year if omitted")
    standings_p.add_argument      ("-c", "--constructor",  action="store_true",  help="Show constructor standings instead")
    standings_p.add_argument      ("--flags",              action="store_true",  help="Add emoji flags to driver's nationality")

    season_p = subps.add_parser("season", help="Fancy wikipedia like season table for driver/constructor championship")
    season_p.add_argument      ("year", metavar="YEAR", type=int, nargs="?", default=CURRENT_YEAR, help="Season year. Current year if omitted")
    season_p.add_argument      ("-c", "--constructor",  action="store_true", help="Show constructor table instead")
    season_p.add_argument      ("--flags",              action="store_true", help="Add emoji flags to grand prix columns")

    calendar_p = subps.add_parser("calendar", help="Calendar for a given season")
    calendar_p.add_argument      ("year",metavar="YEAR",    type=int, nargs="?", default=CURRENT_YEAR, help="Season year. Current year if omitted")
    calendar_p.add_argument      ("-f",  "--full",          action="store_true", help="Show full calendar, do not stop at current stage")
    calendar_p.add_argument      ("-fp", "--free-practice", action="store_true", help="Show free practice")
    calendar_p.add_argument      ("-c",  "--circuit",       action="store_true", help="Show circuit name for each round")
    calendar_p.add_argument      ("-r",  "--rounds-ahead",  type=int, default=0, help="How much more rounds to show after the current one")
    calendar_p.add_argument      ("--utc",                  action="store_true", help="Show time in utc timezone instead")

    search_p = subps.add_parser("search", help="Search the database")
    search_p.add_argument      ("-d", "--driver",      metavar="PART", type=str,  help="search driver with given part in the name")
    search_p.add_argument      ("-t", "--constructor", metavar="PART", type=str,  help="search for a constructor (team)")
    search_p.add_argument      ("-c", "--circuit",     metavar="PART", type=str,  help="search circuit")
    search_p.add_argument      ("-gp", "--grand-prix", metavar="PART", type=str,  help="search grand prix")
    search_p.add_argument      ("--as-pattern",              action="store_true", help="treat part as entire pattern for sql LIKE")
    search_p.add_argument      ("--column",  type=str,       default="name",      help="use given colum to match part, defaults to \"name\"")

    db_p = subps.add_parser("db", help="Different database related commands")
    db_p.add_argument      ("-s", "--sql",              type=str,             help="Run arbitrary sql script on the f1db")
    db_p.add_argument      ("-u", "--update",           action="store_true",  help="Update/init f1db")

    args = p.parse_args()

    if args.version:
        print('v'+VERSION)
    elif any(vars(args).values()) and args.command:
        match_args(args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()