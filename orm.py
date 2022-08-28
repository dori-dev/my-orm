import os
import sqlite3
import inspect
from typing import Dict


class GenerateTableName:
    def __get__(self, instance, owner):
        return owner.__name__.lower()


class GenerateDBName:
    def __get__(self, instance, owner):
        file_address = inspect.getfile(owner)
        db_name = os.path.basename(file_address)[:-3]
        return f"{db_name}.db"


class GetColumns:
    def __get__(self, instance, owner):
        columns: Dict[str] = owner.__dict__
        result = {}
        for name in columns:
            if not name.startswith('__'):
                name = name.lower()
                result[name] = f"{name} {columns[name]}"
        return result


class Row:
    def __init__(self, **data):
        for key, value in data.items():
            self.__setattr__(key, value)

    def __repr__(self) -> str:
        data = self.__dict__
        result = ' | '.join([
            f'{repr(attr)}:{repr(data[attr])}' for attr in data
        ])
        return f"<{result}>"


class DB:
    db_name = GenerateDBName()
    table_name = GenerateTableName()
    columns = GetColumns()

    def __init__(self, **data):
        for key, value in data.items():
            self.__setattr__(key, value)
        self.insert_column(**data)

    @classmethod
    def get_columns(cls):
        return cls.columns.values()

    @classmethod
    def create_table(cls) -> str:
        string_columns = ', '.join(cls.get_columns())
        query = ('CREATE TABLE IF NOT EXISTS '
                 f'{cls.table_name}({string_columns});')
        cls._execute(query)
        return query

    def insert_column(self, **data: dict):
        fields = ', '.join(data.keys())
        values = ', '.join(
            map(repr, data.values())
        )
        query = (f'INSERT OR IGNORE INTO {self.table_name} '
                 f'({fields}) VALUES ({values});')
        self._execute(query)

    @classmethod
    def all(cls):
        query = f'SELECT * FROM {cls.table_name}'
        result = []
        rows = cls._fetchall(query)
        for row in rows:
            row = dict(zip(cls.columns.keys(), row))
            result.append(Row(**row))
        return result

    @classmethod
    def _execute(cls, query: str):
        conn = sqlite3.connect(cls.db_name)
        conn.execute(query)
        conn.commit()
        conn.close()

    @classmethod
    def _fetchall(cls, query: str) -> list:
        conn = sqlite3.connect(cls.db_name)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows


def column(type: str, primary_key: bool = False, unique: bool = False,
           nullable: bool = True, default: str = None):
    if primary_key:
        return f'{type} PRIMARY KEY NOT NULL'
    constraints = ''
    if nullable:
        if default is not None:
            constraints += f'DEFAULT {default}'
    else:
        constraints += 'NOT NULL'
    if unique:
        constraints += 'UNIQUE'
    return f'{type} {constraints}'.strip()
