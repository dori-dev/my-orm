import os
import sqlite3
import inspect


class GenerateTableName:
    def __get__(self, instance, owner):
        return owner.__name__.lower()


class GenerateDBName:
    def __get__(self, instance, owner):
        file_address = inspect.getfile(owner)
        db_name = os.path.basename(file_address)[:-3]
        return f"{db_name}.db"


class DB:
    db_name = GenerateDBName()
    table_name = GenerateTableName()

    def __init__(self) -> None:
        cls = self.__class__
        columns = cls.__dict__
        for column in columns:
            if not column.startswith('__'):
                self.__setattr__(
                    column,
                    columns[column].__get__(self, cls)
                )

    def get_columns(self):
        return self.__dict__.values()

    def create_table(self) -> str:
        string_columns = ', '.join(self.get_columns())
        query = ('CREATE TABLE IF NOT EXISTS '
                 f'{self.table_name}({string_columns});')
        self.execute(query)
        return query

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


class Column:
    def __set_name__(self, owner, name: str):
        self.query = f"{name.lower()} " + self.query

    def __init__(self, type: str,
                 primary_key: bool = False, unique: bool = False,
                 nullable: bool = True, default: str = None):
        if primary_key:
            self.query = f'{type} PRIMARY KEY NOT NULL'
            return
        constraints = ''
        if nullable:
            if default is not None:
                constraints += f'DEFAULT {default}'
        else:
            constraints += 'NOT NULL'
        if unique:
            constraints += 'UNIQUE'
        self.query = f'{type} {constraints}'.strip()

    def __get__(self, instance, owner):
        return self.query
