import os
import sys
import sqlite3


class DB:
    def __init__(self):
        self.db_name = os.path.basename(sys.argv[0])[:-3]
        self.table_name = self.__class__.__name__.lower()

    def create_table(self,  columns: list):
        string_columns = ', '.join(columns)
        query = ('CREATE TABLE IF NOT EXISTS '
                 f'{self.table_name}({string_columns});')
        self.execute(query)

    def insert_column(self, **data: dict):
        fields = ', '.join(data.keys())
        values = ', '.join(
            map(repr, data.values())
        )
        query = (f'INSERT INTO {self.table_name} '
                 f'({fields}) VALUES ({values});')
        self.execute(query)

    def execute(self, query: str):
        conn = sqlite3.connect(self.db_name)
        conn.execute(query)
        conn.commit()
        conn.close()


def column(name: str, type: str,
           primary_key: bool = False, unique: bool = False,
           nullable: bool = True, default: str = None):
    if primary_key:
        return f'{name} {type} PRIMARY KEY NOT NULL'
    constraints = ''
    if nullable:
        if default is not None:
            constraints += f'DEFAULT {default}'
    else:
        constraints += 'NOT NULL'
    if unique:
        constraints += 'UNIQUE'
    return f'{name} {type} {constraints}'.strip()
