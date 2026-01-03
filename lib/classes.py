import sqlite3, os, subprocess
from typing import Callable, Iterable, Optional, Tuple, Any
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

class F1DB:
    def __init__(self, root_dir: str):
        self.sql_scripts_dir = join(root_dir, "sql")
        self.db_file = join(root_dir, "data", "f1db.db")
        self.con = sqlite3.connect(self.db_file)
        self.cur = self.con.cursor()
        self.root_dir = root_dir

    def run_script(
        self, name: str, 
        params: Optional[Iterable]
    ) -> list[Any]:
        script = join(self.sql_scripts_dir, name + ".sql")
        
        with open(script) as s:
            sql = s.read()

        if params:
            self.cur.execute(sql, params)
        else:
            self.cur.execute(sql)

        return self.cur.fetchall()

    def run_file(self, file: str) -> tuple[list[Any], list[str]]:
        with open(file) as f:
            content = f.read()
        
        self.cur.execute(content)
        return (
            self.cur.fetchall(), 
            [c[0] for c in self.cur.description]
        )

    def update(self):
        os.chdir(self.root_dir)
        subprocess.run(
            [join(self.root_dir, "install")], check=True
        )

    def execute(
        self, sql: str, 
        params: Optional[Iterable]
    ) -> list[Any]:
        self.cur.execute(sql, params)
        return self.cur.fetchall()