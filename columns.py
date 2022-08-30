class Column:
    def __init__(self, primary_key: bool = False, unique: bool = False,
                 nullable: bool = True, default: str = None) -> None:
        self.type = None
        self.primary_key = primary_key
        self.unique = unique
        self.nullable = nullable
        self.default = default

    def __repr__(self):
        if self.primary_key:
            return f'{self.type} PRIMARY KEY NOT NULL'
        constraints = ''
        if self.nullable:
            if self.default is not None:
                constraints += f'DEFAULT {self.default}'
        else:
            constraints += 'NOT NULL'
        if self.unique:
            constraints += 'UNIQUE'
        return f'{self.type} {constraints}'.strip()


class Int(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'INT'


class Integer(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'INTEGER'


class TinyInt(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'TINYINT'


class SmallInt(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'SMALLINT'


class MediumInt(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'MEDIUMINT'


class Text(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'TEXT'


class VarChar(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'VARCHAR(255)'


class Blob(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'BLOB'


class Real(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'REAL'


class Double(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'DOUBLE'


class Float(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'FLOAT'


class Numeric(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'NUMERIC'


class Decimal(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'DECIMAL(10,5)'


class Boolean(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'BOOLEAN'


class Date(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'DATE'


class DateTime(Column):
    def __init__(self, primary_key: bool = False, unique: bool = False, nullable: bool = True, default: str = None) -> None:
        super().__init__(primary_key, unique, nullable, default)
        self.type = 'DATETIME'
