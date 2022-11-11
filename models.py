import datetime
import re

from sqlalchemy import Column, Integer, ForeignKey, Unicode, Date
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship


@as_declarative()
class Base(object):
    def __init__(self, *args, **kwargs):
        pass

    @declared_attr
    def __tablename__(cls):
        return re.sub('(?!^)([A-Z][a-z]+)', r'_\1', cls.__name__).lower()


class Group(Base):
    id = Column(Integer, primary_key=True)
    group = Column(Unicode(length=5))
    student = relationship('Student', back_populates="group")

    def __str__(self):
        return f'<Group: {self.group}>'

    def __repr__(self):
        return f'<Group: {self.group}>'


class Student(Base):
    id = Column(Integer, primary_key=True)
    id_group = Column(Integer, ForeignKey('group.id'))
    name = Column(Unicode(length=20))
    surname = Column(Unicode(length=30))
    patronymic = Column(Unicode(length=30))
    create_date = Column(Date, default=lambda: datetime.datetime.now())

    group = relationship('Group', back_populates="student")

    def __str__(self):
        return f'<Student: {self.name} {self.surname} {self.patronymic}>'

    def __repr__(self):
        return f'<Student: {self.name} {self.surname} {self.patronymic}>'
