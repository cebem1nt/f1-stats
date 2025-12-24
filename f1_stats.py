import sqlite3, os
from lib.tables import print_table
from statistics import mean
from argparse import ArgumentParser

conn = sqlite3.connect("data/f1db.db")
cur = conn.cursor()

def ifnone(data: any, then: any):
    return data if data is not None else then

def run_sql(name: str, params: list):
    with open(os.path.join("sql", name)) as f:
        sql = f.read()

    cur.execute(sql, params)

def driver_season(driver_id: str, year: int):
    run_sql("driver_season.sql", [driver_id, driver_id, year])

    rows = cur.fetchall()
    headers = [c[0] for c in cur.description]
    
    print_table(rows, headers, hide_nones=True)

def best_lap(circuit_id: str, rows=5, is_reversed=False):
    headers = [
        "year", "pos", "num", "driver id", "constructor", "engine manufactor", "tyre manufactor", "lap", "time", "ms"
    ]

    run_sql("best_lap.sql", [circuit_id])
    fetched = cur.fetchall() if rows == -1 else cur.fetchmany(rows)

    if is_reversed:
        print_table(fetched[::-1], headers)
    else:
        print_table(fetched, headers)

def main(args: any):
    match args.command:
        case "best-lap":
            best_lap(args.id, args.rows, args.reverse)
        
        case "driver-season":
            driver_season(args.id, args.year)
        
        case _:
            print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    p = ArgumentParser(description="Diferrent charts, statistics about Formula One")

    subparsers = p.add_subparsers(dest="command", help="Available commands")

    best_lap_p = subparsers.add_parser("best-lap", help="Get best lap info for a circuit")
    best_lap_p.add_argument("id", metavar="ID", type=str, help="Circuit id")
    best_lap_p.add_argument("-r", "--rows", default=5, type=int, help="Amount of rows to fetch")
    best_lap_p.add_argument("-R", "--reverse", action="store_true", help="Reverse results")

    driver_season_p = subparsers.add_parser("driver-season", help="Driver season stats")
    driver_season_p.add_argument("id", metavar="ID", type=str, help="Driver id")
    driver_season_p.add_argument("year", metavar="YEAR", type=str, help="Season year")

    args = p.parse_args()

    main(args)