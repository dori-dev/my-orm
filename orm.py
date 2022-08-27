import sqlite3

DB_NAME = 'test.db'


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


def execute(query: str):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(query)
    conn.commit()
    conn.close()


def create_table(table_name: str, columns: list):
    string_columns = ', '.join(columns)
    query = f'CREATE TABLE IF NOT EXISTS {table_name}({string_columns});'
    execute(query)


def insert_column(table_name: str, **kwargs: dict):
    fields, values = zip(*kwargs.items())
    values = map(lambda value: f"'{value}'", values)
    fields_string, values_string = ', '.join(fields), ', '.join(values)
    query = (f'INSERT INTO {table_name} '
             f'({fields_string}) VALUES ({values_string});')
    execute(query)
