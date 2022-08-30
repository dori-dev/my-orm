from db import DB, ResultConfig
from operators import AND, OR, NOT
import columns


class Person(DB):
    # id = columns.Integer(primary_key=True)
    name = columns.Text(nullable=False)
    age = columns.Integer(nullable=False)
    address = columns.VarChar()
    salary = columns.Real()


class School(DB):
    # id = columns.Integer(primary_key=True)
    name = columns.VarChar(nullable=False)
    created_at = columns.Date()
    address = columns.Text()
    students_count = columns.SmallInt()


class School2(DB):
    # id = columns.Integer(primary_key=True)
    name = columns.VarChar(nullable=False)
    created_at = columns.Date()
    address = columns.Text()
    students_count = columns.SmallInt()


p1 = Person(
    # id=9,
    name='salar',
    age=20,
    address='hello there',
    salary='wow'
)
p2 = Person(
    # id=10,
    name='salar',
    age=20,
    address='hello there',
    salary='wow'
)

print(p1.age)

print(Person.all())

print(Person.get('id', 'name'))


print(Person.filter(a=45, b=4, id=1))

print(Person.filter(name='mohammadd', id=5))

print(Person.filter())
print(Person.queries())

# conditions = {
#     'p': 1,
#     'p__lt': 5,
#     'p__lte': 5,
#     'p__gt': 5,
#     'p__gte': 5,
#     'p__in': (10, 4, 'df'),
#     'p__n': 5,
#     'p__like': 'd%',
#     'p__between': (5, 10),
#     'p__between': (5, 6, 10),
# }

print('----------------')
a = Person.filter(OR(OR(name='4', id=4), id=4, name='salar'),
                  config=ResultConfig(order_by='id', reverse=True))
print('----------------')
for i in a:

    # i.remove()
    print(i.id)
    print(i.remove())
    # i.remove()
    # print(i.age)

print('-'*100)
print(a)
print('-'*100)
print(a.count())
print('*'*10)
print('*'*10)
print(a.first().id)
print(a.last())

print(Person.filter(id=45).last())


print(Person.sum('id'))


# Person.remove()
# p1.remove()

print(p1)

print(Person.all(config=ResultConfig(limit=3)).count())
print(Person.get(config=ResultConfig(limit=1)).count())


# p1.update(id=19)

# add Foreign key
# add last, first to Person class method
# TODO test
# TODO check with get them Table.queries()
# TODO create document and video
# package it

# p1.remove()
print(p1)
print(p1)


print(Person.count())
print(Person.last())

print(p1.id)


p1.remove()
