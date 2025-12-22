import sqlite3, sys, os
from lib.tables import print_table

conn = sqlite3.connect("data/f1db.db")
cur = conn.cursor()

def run_sql(name: str, params: list):
    with open(os.path.join("sql", name)) as f:
        sql = f.read()

    cur.execute(sql, params)

def best_lap(circuit_id: str, rows=50):
    headers = ["year", "pos", "num", "driver id", "constructor", "engine manufactor", "tyre manufactor", "lap", "time", "ms"]
    run_sql("best_lap.sql", [circuit_id])

    print_table(cur.fetchmany(rows), headers)

if __name__ == "__main__":
    best_lap(sys.argv[1])