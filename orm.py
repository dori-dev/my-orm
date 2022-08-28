import os
import sqlite3
import inspect
from typing import Dict, List


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


class Operator:
    def __init__(self, *args, **kwargs):
        self.fields = kwargs
        self.args = args
        self.operator = self.__class__.__name__

    def generate_statements(self):
        operator = f' {self.operator} '
        statements = [
            f'{key}={repr(value)}'
            for key, value in self.fields.items()
        ]
        args_statements = operator.join(
            map(
                lambda arg: arg.generate_statements()
                if isinstance(arg, Operator)
                else str(arg),
                self.args
            )
        )
        if args_statements:
            statements.append(args_statements)
        return f"({operator.join(statements)})"

    def __repr__(self) -> str:
        return self.generate_statements()


class AND(Operator):
    pass


class OR(Operator):
    pass


class NOT(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operator = 'AND'

    def __repr__(self) -> str:
        return f"NOT {super().__repr__()}"


class DB:
    db_name = GenerateDBName()
    table_name = GenerateTableName()
    columns = GetColumns()
    _query = ''

    def __init__(self, **data):
        for key, value in data.items():
            self.__setattr__(key, value)
        self.insert(**data)

    def __init_subclass__(cls, **kwargs):
        cls._create_table()

    @classmethod
    def get_columns(cls):
        return cls.columns.values()

    @classmethod
    def _create_table(cls) -> str:
        string_columns = ', '.join(cls.get_columns())
        query = ('CREATE TABLE IF NOT EXISTS '
                 f'{cls.table_name}({string_columns});')
        cls._execute(query)
        return query

    def insert(self, **data: dict):
        fields = ', '.join(data.keys())
        values = ', '.join(
            map(repr, data.values())
        )
        query = (f'INSERT OR IGNORE INTO {self.table_name} '
                 f'({fields}) VALUES ({values});')
        self._execute(query)

    @classmethod
    def all(cls) -> List[Row]:
        query = f'SELECT * FROM {cls.table_name}'
        return cls._fetchall(query)

    @classmethod
    def get(cls, *fields: dict) -> List[Row]:
        fields = [field for field in fields if field in cls.columns]
        fields_string = ', '.join(fields) or '*'
        query = f'SELECT {fields_string} FROM {cls.table_name}'
        return cls._fetchall(query)

    @classmethod
    def filter(cls, *args, **kwargs):
        operator_statement = ' AND '.join(map(
            lambda arg: f'{arg}',
            args
        )).strip()
        statements = [
            f'{field}={repr(value)}'
            for field, value in kwargs.items()
            if field in cls.columns
        ]
        if operator_statement:
            statements.append(operator_statement)
        statements = ' AND '.join(statements) or 'true'
        query = f'SELECT * FROM {cls.table_name} WHERE {statements}'
        return cls._fetchall(query)

    @classmethod
    def queries(cls):
        return cls._query.strip()

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
            result.append(Row(**row))
        conn.close()
        return result


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
