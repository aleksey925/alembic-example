from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI
from models import Group, Student

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()

po_42 = Group(group='ПО-42')
rpis_34 = Group(group='РПИС-34')

student = Student(
    name='Иван', surname='Иванов', patronymic='Иванович', group=rpis_34
)
student_1 = Student(
    name='Алексей', surname='Сидоров', patronymic='Валерьевич', group=po_42
)
student_2 = Student(
    name='Сергей', surname='Козлов', patronymic='Викторович', group=po_42
)

session.add(student)
session.add(student_1)
session.add(student_2)

session.add(po_42)
session.add(rpis_34)

session.commit()
session.close()
