from __future__ import annotations
import os
import sqlite3
import inspect
from typing import Dict, List, NamedTuple, Union
from operators import OPERATORS


class GenerateTableName:
    def __get__(self, instance, owner) -> str:
        return owner.__name__.lower()


class GenerateDBName:
    def __get__(self, instance, owner) -> str:
        file_address = inspect.getfile(owner)
        db_name = os.path.basename(file_address)[:-3]
        return f"{db_name}.db"


class GetColumns:
    def get_columns(self, owner) -> Dict[str, str]:
        class_variables: Dict[str, str] = owner.__dict__
        return (
            (key, value)
            for key, value in class_variables.items()
            # remove python magic method from class variables
            if not key.startswith('__')
        )

    def __get__(self, instance, owner) -> Dict[str, str]:
        return {
            name.lower(): f"{name.lower()} {value}"
            for name, value in self.get_columns(owner)
        }


class Rows:
    def __init__(self, rows: List[DB]):
        self.rows = rows

    def count(self) -> int:
        return len(self.rows)

    def first(self) -> Union[DB, None]:
        if self.rows:
            return self.rows[0]
        return None

    def last(self) -> Union[DB, None]:
        if self.rows:
            return self.rows[-1]
        return None

    def __repr__(self) -> str:
        return repr(self.rows)

    def __iter__(self) -> List[DB]:
        return iter(self.rows)


class ResultConfig(NamedTuple):
    limit: Union[int, None] = None
    order_by: Union[str, None] = None
    reverse: bool = False


class DB:
    db_name = GenerateDBName()
    table_name = GenerateTableName()
    columns = GetColumns()
    _query = ''

    def __init__(self, **data):
        self.data = data
        for key, value in data.items():
            self.__setattr__(key, value)
        self.insert(**data)

    def __init_subclass__(cls, **kwargs):
        cls._create_table()

    def insert(self, **data: dict):
        fields = ', '.join(data.keys())
        values = ', '.join(
            map(repr, data.values())
        )
        query = (f'INSERT OR IGNORE INTO {self.table_name} '
                 f'({fields}) VALUES ({values});')
        self._execute(query)

    @classmethod
    def all(cls, config: Union[ResultConfig, None] = None) -> List[DB]:
        filters = cls._set_config(config)
        query = f'SELECT * FROM {cls.table_name} {filters};'
        return cls._fetchall(query)

    @classmethod
    def get(cls, *fields: dict,
            config: Union[ResultConfig, None] = None) -> List[DB]:
        fields = [
            field
            for field in fields
            if field in cls.columns
        ]
        fields_string = ', '.join(fields) or '*'
        filters = cls._set_config(config)
        query = f'SELECT {fields_string} FROM {cls.table_name} {filters};'
        return cls._fetchall(query)

    @classmethod
    def filter(cls, *args, config: Union[ResultConfig, None] = None,
               **kwargs) -> List[DB]:
        conditions = []
        for key, value in kwargs.items():
            if key not in cls.columns:
                condition = None
            elif '__' in key:
                condition = cls._set_operator_filter(key, value)
            else:
                condition = f'{key} = {repr(value)}'
            if condition is not None:
                conditions.append(condition)
                condition = None
        conditions.extend(list(map(repr, args)))
        statements = ' AND '.join(conditions) or 'true'
        filters = cls._set_config(config)
        query = (
            f'SELECT * FROM {cls.table_name} WHERE {statements} {filters};'
        )
        return cls._fetchall(query)

    @classmethod
    def max(cls, column_name: str):
        query = f'SELECT MAX({column_name}) FROM {cls.table_name}'
        result = cls._fetch_result(query)
        if result:
            return {column_name: result[0]}

    @classmethod
    def min(cls, column_name: str):
        query = f'SELECT MIN({column_name}) FROM {cls.table_name}'
        result = cls._fetch_result(query)
        if result:
            return {column_name: result[0]}

    @classmethod
    def avg(cls, column_name: str):
        query = f'SELECT AVG({column_name}) FROM {cls.table_name}'
        result = cls._fetch_result(query)
        if result:
            return {column_name: result[0]}

    @classmethod
    def sum(cls, column_name: str):
        query = f'SELECT SUM({column_name}) FROM {cls.table_name}'
        result = cls._fetch_result(query)
        if result:
            return {column_name: result[0]}

    @classmethod
    def count(cls):
        query = f'SELECT COUNT(1) FROM {cls.table_name}'
        result = cls._fetch_result(query)
        if result:
            return {'count': result[0]}

    def remove(self):
        where = ' AND '.join([
            f'{key} = {repr(value)}'
            for key, value in self.data.items()
        ])
        query = f'DELETE FROM {self.table_name} WHERE {where}'
        self._execute(query)

    def update(self, **kwargs):
        where = ' AND '.join([
            f'{key} = {repr(value)}'
            for key, value in self.data.items()
        ])
        new_data = ', '.join([
            f'{key} = {repr(value)}'
            for key, value in kwargs.items()
        ])
        if new_data.strip():
            query = (
                f'UPDATE {self.table_name} SET {new_data} WHERE {where}'
            )
            self._execute(query)

    @classmethod
    def remove_table(cls):
        query = f'DROP TABLE {cls.table_name}'
        cls._execute(query)

    @classmethod
    def queries(cls):
        return cls._query.strip()

    @classmethod
    def _create_table(cls) -> str:
        string_columns = ', '.join(cls.columns.values())
        query = ('CREATE TABLE IF NOT EXISTS '
                 f'{cls.table_name}({string_columns});')
        cls._execute(query)

    @staticmethod
    def _set_config(config: Union[ResultConfig, None]) -> str:
        if config is None:
            return ''
        limit, order_by, reverse = config
        if limit is None:
            limit = ''
        else:
            limit = f'LIMIT {limit}'
        if order_by is None:
            order_by = ''
            sorting = ''
        else:
            order_by = F' ORDER BY {order_by}'
            if reverse is False:
                sorting = ' ASC'
            else:
                sorting = ' DESC'
        return f'{limit}{order_by}{sorting}'

    @staticmethod
    def _set_operator_filter(key: str, value: str):
        filter = key.split('__')
        if len(filter) != 2:
            return None
        key, operator = filter
        key, operator = key.lower(), operator.lower()
        if operator in OPERATORS:
            return (
                f'{key} {OPERATORS[operator]} {repr(value)}'
            )
        elif operator == 'between':
            start, *_, end = value
            return (
                f'{key} BETWEEN {repr(start)} AND {repr(end)}'
            )

    @classmethod
    def _execute(cls, query: str):
        cls._query += f"{query}\n\n"
        conn = sqlite3.connect(cls.db_name)
        conn.execute(query)
        conn.commit()
        conn.close()

    @classmethod
    def _fetchall(cls, query: str) -> list:
        cls._query += f"{query}\n\n"
        conn = sqlite3.connect(cls.db_name)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        result = []
        for row in rows:
            row = dict(zip(
                cls.columns.keys(),
                row
            ))
            result.append(
                cls(**row)
            )
        conn.close()
        return Rows(result)

    @classmethod
    def _fetch_result(cls, query: str):
        cls._query += f"{query}\n\n"
        conn = sqlite3.connect(cls.db_name)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        conn.close()
        return result

    def __repr__(self) -> str:
        result = ' | '.join([
            f'{repr(attr)}:{repr(value)}'
            for attr, value in self.data.items()
        ])
        return f"<{result}>"
