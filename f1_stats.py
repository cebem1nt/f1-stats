import sqlite3, os
from lib.tables import print_table
from statistics import mean
from argparse import ArgumentParser
from collections import defaultdict

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
    run_sql("best_lap.sql", [circuit_id])
    fetched = cur.fetchall() if rows == -1 else cur.fetchmany(rows)
    headers = [c[0] for c in cur.description]

    if is_reversed:
        print_table(fetched[::-1], headers)
    else:
        print_table(fetched, headers)

def season_table(year: int):
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

    run_sql("season_table.sql", [year, year])
    rows = cur.fetchall()

    drivers_results = defaultdict(lambda: dict(grandprix_template))
    drivers_points = {}

    for abbrev, name, finish_pos, points, is_pole, is_fastest in rows:
        drivers_results[name][abbrev] = finish_pos
        drivers_points[name] = points

        if is_pole:
            drivers_results[name][abbrev] += "\u1D56" # sup P

        if is_fastest:
            drivers_results[name][abbrev] += "\u1DA0" # sup F

    pos = 1
    for name, points in drivers_points.items():
        per_races = [drivers_results[name].get(abbr) for abbr in grandprix_cols]
        out_rows.append([pos, name] + per_races + [points])
        pos += 1

    print_table(
        out_rows,
        ["pos", "driver"] + grandprix_cols + ["pts"],
        hide_nones=True
    )

def main(args: any):
    match args.command:
        case "best-lap":
            best_lap(args.id, args.rows, args.reverse)
        
        case "season-table":
            season_table(args.year)
        
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

    season_table_p = subparsers.add_parser("season-table", help="Fancy wikipedia like season table")
    season_table_p.add_argument("year", metavar="YEAR", type=str, help="Season year")

    args = p.parse_args()

    main(args)