from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///Academy.db")


class Base(DeclarativeBase):
    pass

class Teacher(Base):
    __tablename__ = "Teacher"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column()
    surname:Mapped[str] =  mapped_column()
    salary:Mapped[float] = mapped_column()
    dataofemployment:Mapped[str] = mapped_column()
    position:Mapped[str] = mapped_column()
    isassistent:Mapped[int] = mapped_column(default=0)
    isproffessor:Mapped[int] = mapped_column(default=0)
    premium:Mapped[float] = mapped_column(default=0)
    groups: Mapped[list["Group"]] = relationship(secondary="Group_Teacher", back_populates="teachers")
    def __repr__(self) -> str:
        return f"Teacher#(id={self.id!r}, name={self.name!r}, surname={self.surname!r}, salary={self.salary!r}, dataofemployment={self.dataofemployment!r}, position={self.position!r}, premium={self.premium!r})"



class Group(Base):
    __tablename__="Group"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True)
    year: Mapped[int] = mapped_column()
    raiting:Mapped[int] = mapped_column()
    teachers: Mapped[list["Teacher"]] = relationship(secondary="Group_Teacher", back_populates="groups")
    def __repr__(self) -> str:
        return f"Group#(id={self.id!r}, name={self.name!r}, raiting={self.raiting!r}, rating={self.year!r})"

class Department(Base):
    __tablename__ = "Department"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    id_faculties: Mapped[int] = mapped_column(ForeignKey("Faculties.id"))
    name:Mapped[str] = mapped_column(unique=True)
    financing:Mapped[float] = mapped_column(default=0)
    facultaies: Mapped["Facultaies"] = relationship(back_populates="departments")

    def __repr__(self) -> str:
        return f"Department(id={self.id!r}, name={self.name!r}, financing={self.financing!r})"


class Facultaies(Base):
    __tablename__ = "Faculties"
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(unique=True)
    dekan:Mapped[str] = mapped_column()
    departments: Mapped[list["Department"]] = relationship(back_populates="facultaies", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Faculties(id={self.id!r}, name={self.name!r}, dekan={self.dekan!r})"


class Group_Teacher(Base):
    __tablename__ = "Group_Teacher"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id_group: Mapped[int] = mapped_column(ForeignKey("Group.id"))
    id_teacher: Mapped[int] = mapped_column(ForeignKey("Teacher.id"))



Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with Session(engine) as session:
    groups1 = []
    groups1.append(Group(name="OBD1", year=3, raiting=4))
    groups1.append(Group(name="OBD2", year=5, raiting=3))
    groups1.append(Group(name="OBD3", year=3, raiting=4))
    groups1.append(Group(name="OBD4", year=2, raiting=3))
    groups1.append(Group(name="OBD5", year=1, raiting=5))
    teach1 = Teacher(name="Иван", surname="Середа", salary=1200, dataofemployment="12.08.1998", position="Професор",isassistent=0, isproffessor=1, premium=0,groups=groups1)
    teach2 = Teacher(name="Антон", surname="Ганжа", salary=1050, dataofemployment="10.03.2001", position="Ассистент",isassistent=1, isproffessor=0, premium=0)
    teach3 = Teacher(name="Степан", surname="След", salary=1100, dataofemployment="15.02.1997", position="Професор",isassistent=0, isproffessor=1, premium=0)
    teach4 = Teacher(name="Алексей",surname="Вторник",salary=800,dataofemployment="06.04.2003",position="Ассистент",isassistent=1, isproffessor=0, premium=0,groups=groups1)
    teach5 = Teacher(name="Юрий", surname="Вишня", salary=1300, dataofemployment="02.02.2002", position="Ассистент",isassistent=1, isproffessor=0, premium=0)

session.add_all(groups1)
session.add_all((teach1, teach2,teach3,teach4,teach5))
session.commit()

with Session(engine) as session:
    faculty1 = Facultaies(name="Computer Science", dekan="Arnold", departments=[])
    faculty2 = Facultaies(name="Mathematic", dekan="Alfred", departments=[])
    faculty3 = Facultaies(name="Finance", dekan="Benjamin", departments=[])

    session.add_all([faculty1, faculty2, faculty3])
    session.commit()

    faculty1.departments.append(Department(name="Computer Science", financing=13500.0))
    faculty2.departments.append(Department(name="Nature Science", financing=20000.0))
    faculty3.departments.append(Department(name="Phisic Science", financing=13500.0))

    session.commit()


# 1. Вывести таблицу кафедр, но расположить ее поля в
# обратном порядке.

question1 = session.query(Department).filter(
    Department.id).order_by(Department.id.desc()).limit(10).all()

# print(question1)

# Задание 2
#  Вывести названия групп и их рейтинги с уточнением имен полей именем таблицы.

question2 = session.query(Group.name, Group.raiting).order_by(
    Group.raiting.desc()).limit(10).all()

# print(question2)
# Задание 5
# Вывести фамилии преподавателей, которые являются профессорами и ставка которых превышает 1050.

question5 = session.query(Teacher).filter((
    Teacher.salary>1050) & (Teacher.isproffessor == 1)).all()

print(question5)

# Задание 6. Вывести названия кафедр, фонд финансирования от 11600 до 25000.

question6 = session.query(Department).filter((
    Department.financing >= 11000) & (Department.financing <=25000)).all()

# print(question6)

# Задание 7. Вывести названия факультетов кроме факультета “Информационных технологий”

question7 = session.query(Facultaies).filter(
    Facultaies.name != "Computer Science").all()

# print(question7)

# Задание 8. Вывести фамилии и должности преподавателей, которые не являются профессорами

question8 = session.query(Teacher.surname, Teacher.position).filter(
    Teacher.isproffessor == 0).all()

print(question8)

# Задание 9. Вывести фамилии, должности, ставки и надбавки ассистентов, у которых надбавка в диапазоне от 550 до 1500.

question9 = session.query(Teacher.surname, Teacher.position, Teacher.salary, Teacher.premium).filter(
    (Teacher.isassistent == 1) &
    (Teacher.premium.between(550, 1550))).all()

print(question9)