# My ORM

It's a simple ORM built with Python and sqlite.<br>This is not a real ORM to use in your project.

#

# Use My ORM

You can see sample codes in [examples.py](examples.py).<br>
I will be glad if you cooperate in the development of this project 😊

#

## Install My ORM

```
pip install dori-orm
```

#

## Imports

Import DB, ResultConfig, operators and columns from the _dori-orm_ library.
<br>
**DB**: For create classes and database table.<br>
**ResultConfig**: Change the result, e.g. ordering and limit.<br>
**operators**: SQL operators like AND, OR, NOT<br>
**columns**: To create table columns with specific _data type_ and _constraints_. For example `age = columns.Integer(nullable=False)` means `age INTEGER NOT NULL`

```python
from dori_orm import DB, ResultConfig
from dori_orm.operators import AND, OR, NOT
from dori_orm import columns
```

#

## Create Table

Create class and inheritance from `DB`, tables created automatically in database(set db name with file name) when you inheritance from DB, you can define class variable and use `columns` to create table column.

```python
class Person(DB):
    name = columns.Text(nullable=False)
    family = columns.Text(nullable=False)
    age = columns.Integer()
    phone = columns.Integer()
    salary = columns.Real(default=100_000)


class School(DB):
    name = columns.VarChar(nullable=False, unique=True)
    created_at = columns.Date()
    address = columns.Text()
    students_count = columns.SmallInt(default=300)


class Student(DB):
    person = columns.ForeignKey(Person)
    school = columns.ForeignKey(School)
    class_name = columns.VarChar()
```

#

## Insert Data

Insert data to table with create instance from class. this code create two row in database with this arguments.

```python
person1 = Person(
    name='Mohammad',
    family='Dori',
    age=20,
    phone=1234567890,
    salary=110_000,
)
print(person1.age)  # 20

person2 = Person(
    name='John',
    family='Gits',
    age=30,
    phone=1234567890,
)
```

#

## Select Data

Select rows from table.<br>
`all` method select all rows from table.<br>
`get` method, select all rows with defined columns.
`filter` method select all rows that match the given conditions.

```python
print(Person.all())
```

```python
# Result:
[
    <'id':1, 'name':'Mohammad', 'family':'Dori', 'age':20, 'phone':1234567890, 'salary':110000.0>,
    <'id':2, 'name':'John', 'family':'Gits', 'age':30, 'phone':1234567890, 'salary':100000.0>
]
```

```python
print(Person.get('id', 'name', 'family'))
```

```python
# Result:
[
    <'id':1, 'name':'Mohammad', 'family':'Dori'>,
    <'id':2, 'name':'John', 'family':'Gits'>
]
```

```python
print(Person.filter(id=1, name='Mohammad'))
```

```python
# Result:
[
    <'id':1, 'name':'Mohammad', 'family':'Dori', 'age':20, 'phone':1234567890, 'salary':110000.0>
]
```

#

## Advance Filtering

You can use operators in filter method. like AND, OR, NOT, BETWEEN, LIKE, IN, =, !=, <, <=, >, >=.

**AND**: e.g. `AND(x='', y=123)` that means `x='' AND y=123`

```python
rows = Person.filter(
    AND(id=2, name='Ali')
)
```

**OR**: e.g. `OR(x='', y=123)` that means `x='' OR y=123`

```python
rows = Person.filter(
    OR(id=2, name='Ali')
)
```

**NOT**: e.g. `NOT(OR(x='', y=123))` that means `NOT (x='' OR y=123)`

```python
rows = Person.filter(
    NOT(AND(id=2, name='Ali'))
)
```

You can use another operator in operator.

```python
rows = Person.filter(
    OR(OR(name='Ali', id=2), OR(salary=10, age=20))
)
```

**BETWEEN**: Return row, if it value between x and y.

```python
print(Person.filter(id__between=(2, 8)))
```

**LIKE**: Use pattern with % and \_ to filter rows.

```python
print(Person.filter(
    name__like='Mo%',
    config=ResultConfig(
        limit=2,
        order_by='age',
    )
))
```

**lt**: less than, means `<`

```python
print(Person.filter(id__lt=5))
```

**lte**: less than or equal, means `<=`

```python
print(Person.filter(id__lte=5))
```

**gt**: greater than, means `>`

```python
print(Person.filter(id__gt=5))
```

**gte**: greater than or equal, means `>=`

```python
print(Person.filter(id__gte=5))
```

**not**: not equal, means `!=`

```python
print(Person.filter(id__n=5))
```

You can use any filter together.

```python
print(Person.filter(
    OR(
        id__n=5,
        name__in=('Mohammad', 'Salar'),
        age__gte=8
    )
))
```

#

## Result Methods

`result.count()` return count of results.<br>
`result.first()` return first row in result.<br>
`result.last()` return last row in result.

```python
not_mohammad = Person.filter(name__n='Mohammad')
print(not_mohammad.count())
print(not_mohammad.first())
print(not_mohammad.last())
```

Iterate on result.

```python
for row in not_mohammad:
    print(row.name)
    row.remove()
    # row.update(...)
```

#

## Update Row

```python
person1 = Person(
    name='Mohammad',
    family='Dori',
    age=20,
    phone=1234567890,
    salary=110_000,
)

print(person1)
person1.update(name='Salar')
print(person1)
```

#

## Table Class Method

**max**: Return maximum value of column.

```python
print(Person.max('salary'))
```

**min**: Return minimum value of column.

```python
print(Person.min('salary'))
```

**sum**: Return sum of column values.

```python
print(Person.sum('salary'))
```

**avg**: Return average of column values.

```python
print(Person.avg('salary'))
```

**count**: Return count of rows in table.

```python
print(Person.count())
```

**first**: Return first row of table.

```python
print(Person.first())
```

**last**: Return last row of table.

```python
print(Person.last())
```

#

## Result configuration

`limit` Limit the number of result rows.<br>
`order_by` Order result by columns.<br>
`reverse` Use with order_by, False means sort ASC and True means sort DESC.

```python
print(Person.all(
    config=ResultConfig(
        order_by='id',
        reverse=True
    )
))
print(Person.get(
    config=ResultConfig(
        limit=5
    )
))
```

#

## Foreign Key

```python
person1 = Person(
    name='Mohammad',
    family='Dori',
    age=20,
    phone=1234567890,
    salary=110_000,
)
school1 = School(
    name='The Sample School',
    created_at='2002-01-04',
    address='1600 Amphitheatre Parkway in Mountain View, California',
)

print(school1)

student = Student(
    person=person1,
    school=school1,
    class_name='A3',
)

print(school1.id)
print(person1.id)

print(student)
```

#

## Change Easy

Remove `class_name` column and add gpa column. now add a row to table.

```python
class Student(DB):
    person = columns.ForeignKey(Person)
    school = columns.ForeignKey(School)
    gpa = columns.TinyInt(default=20)

person1 = Person(
    name='Mohammad',
    family='Dori',
    age=20,
    phone=1234567890,
    salary=110_000,
)
school1 = School(
    name='The Sample School',
    created_at='2002-01-04',
    address='1600 Amphitheatre Parkway in Mountain View, California',
)

print(school1)

student = Student(
    person=person1,
    school=school1,
    gpa=10,
)

print(school1.id)
print(person1.id)

print(student)
```

#

## See All Query Usage

```python
print(Person.queries())
```

#

# Links

Download Source Code: [Click Here](https://github.com/dori-dev/my-orm/archive/refs/heads/main.zip)

My Github Account: [Click Here](https://github.com/dori-dev/)
