from sqlite3 import Row, Cursor
from typing import List, Optional as Opt, Iterable

from vettel.helpers import Today
from vettel.database import DB

def __dict_row_factory(cursor: Cursor, row: Row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

def __new_dict_cursor():
    cursor = DB.con.cursor()
    cursor.row_factory = __dict_row_factory
    return cursor

def __run_script(
    script: str, 
    params: Iterable = [], 
    as_dict: bool = False
):
    if not as_dict:
        return DB.run_script(script, params)

    return DB.run_script(script, params, cursor=__new_dict_cursor())

def raw_sql(
    sql: str, 
    params: Iterable = [], 
    as_dict: bool = False
):
    if not as_dict:
        return DB.get_columns(), DB.execute(sql, params)
    
    return DB.execute(sql, params, cursor=__new_dict_cursor())

def raw_script(script: str, params: Iterable = []):
    return DB.run_script(script, params)

def race(id: str, year: int, as_dict: bool = False):
    return __run_script("race/race", {"id": id, "year": year}, as_dict)
    
def qualifying(id: str, year: int, as_dict: bool = False):
    script = "race/qualifying-pre-2006" if year < 2006 else \
             "race/qualifying"

    return __run_script(script, {"id": id, "year": year}, as_dict)

def sprint(id: str, year: int, as_dict: bool = False):
    return __run_script("sprint/sprint", {"id": id, "year": year}, as_dict)

def sprint_qualifying(id: str, year: int, as_dict: bool = False):
    return __run_script("sprint/qualifying", {"id": id, "year": year}, as_dict)

def race_results(year: int, is_qualifying: bool, as_dict: bool = False):
    script = "results/qualifying" if is_qualifying else \
             "results/results"

    return __run_script(script, [year], as_dict)

def __all_time_dynamic(id: str, year: int, script: str, is_all_time: bool):
    params = {"id": id}
    extra_sql = ""

    if not is_all_time:
        params["year"] = year
        extra_sql = " and r.year = :year"

    return DB.run_script(script, params, extra_sql)

def driver_races(id: str, year: int, is_all_time: bool):
    return __all_time_dynamic(id, year, "driver/races", is_all_time)
    
def driver_qualifying(id: str, year: int, is_all_time: bool):
    return __all_time_dynamic(id, year, "driver/qualifying", is_all_time)

def driver_sprints(id: str, year: int, is_all_time: bool):
    return __all_time_dynamic(id, year, "driver/sprints", is_all_time)

def driver_overview(id: str, year: int, is_all_time: bool):
    return __all_time_dynamic(id, year, "driver/overview", is_all_time)

def driver_pits(id: str, year: int, as_dict: bool = False):
    return __run_script("driver/pits", {"id": id, "year": year}, as_dict)

def season_gps(year: int, as_dict: bool = False):
    return __run_script("season", {"year": year}, as_dict)

def calendar(year: int, as_dict: bool = False):
    return __run_script("calendar", [year], as_dict)

def gps(year: int, as_dict: bool = False):
    sql = """
        SELECT 
            grand_prix.id, 
            grand_prix.abbreviation 
        FROM grand_prix 
        JOIN race on race.year = ? 
        WHERE race.grand_prix_id = grand_prix.id
    """

    return raw_sql(sql, [year], as_dict)

def circuit_info(id: str, as_dict: bool = False): 
    sql = """
        SELECT 
            circuit.*, 
            GROUP_CONCAT(race.year ,',') as years 
        FROM circuit 
        JOIN race on race.circuit_id = :id 
        WHERE circuit.id = :id
    """

    return raw_sql(sql, {"id": id}, as_dict)

def standings(year: int, is_constructor: bool, as_dict: bool = False):
    script = "standings/constructor" if is_constructor else \
             "standings/standings"

    return __run_script(script, {"year": year}, as_dict)

def get_last_race_circuit_id():
    out = raw_sql("""
    SELECT
        race.circuit_id
    FROM 
        race
    JOIN (
        SELECT 
            race_id
        FROM 
            race_result
        ORDER BY race_id DESC
        LIMIT 1
    ) race_result ON race_result.race_id = race.id;
    """, as_dict=True)[0]

    return out["circuit_id"]
