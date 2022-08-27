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


def execute_query(query: str):
    conn = sqlite3.connect(DB_NAME)
    conn.execute(query)
