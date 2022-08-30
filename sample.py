from db import DB, ResultConfig
from operators import AND, OR, NOT
import columns


class Person(DB):
    name = columns.Text(nullable=False)
    family = columns.Text(nullable=False)
    age = columns.Integer()
    phone = columns.Integer()
    salary = columns.Real(default=100_000)


class School(DB):
    name = columns.VarChar(nullable=False)
    created_at = columns.Date()
    address = columns.Text()
    students_count = columns.SmallInt(default=300)


p1 = Person(
    name='Mohammad',
    family='Dori',
    age=20,
    phone=1234567890,
    salary=110_000,
)

p2 = Person(
    name='John',
    family='Gits',
    age=30,
    phone=1234567890,
)

print(p1.age)

print(Person.all())

print(Person.get('id', 'name', 'family'))

print(Person.filter(id=1, name='Mohammad'))

not_mohammad = Person.filter(name__n='Mohammad')
print(not_mohammad)
print(not_mohammad.count())
print(not_mohammad.first())
print(not_mohammad.last())
for row in not_mohammad:
    print(row.name)
    # row.remove()

print(p1)
p1.update(name='Salar')
print(p1)

print(Person.count())

print(Person.first())

print(Person.last())

print(Person.max('salary'))
print(Person.min('salary'))
print(Person.sum('salary'))
print(Person.avg('salary'))

print(Person.all(config=ResultConfig(order_by='id', reverse=True)))
print(Person.get(
    config=ResultConfig(
        limit=5
    )
))

# id__lt, id__lte, id__gt, id__gte, id__n
print(Person.filter(id__lte=5))
print(Person.filter(id__between=(2, 8)))
print(Person.filter(
    name__like='Mo%',
    config=ResultConfig(
        limit=2,
        order_by='age',
    )
))


rows = Person.filter(
    OR(id=2, name='Ali')
)
print()
print(rows)

rows = Person.filter(
    NOT(AND(id=2, name='Ali'))
)
print()
print(rows.count())

rows = Person.filter(
    OR(OR(name='Ali', id=2), OR(salary=10, age=20))
)
print()
print(rows.count())


print(Person.queries())
