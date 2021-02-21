from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

from werkzeug.security import generate_password_hash


engine = create_engine("postgresql://postgres:postgresqlpass@localhost/rating", echo = True)
Session = sessionmaker(bind=engine)


Base = declarative_base()

teacher_group = Table('teacher_group', Base.metadata,
    Column('teacher_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

user_subject = Table('user_subject', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('subjec_id', Integer, ForeignKey('subjects.id'))
)

class groups(Base):
    __tablename__ = "groups"

    id = Column('id', Integer, primary_key=True)
    name = Column('name',String, nullable=False)


    students = relationship('users', backref = 'group')

class users(Base):
    __tablename__ = 'users'

    id = Column('id',Integer,primary_key=True)
    name = Column('name',String,nullable=False)
    email = Column('email',String, unique = True, nullable=False)
    password = Column('password',String, nullable=False)
    type_of_user = Column('type_of_user',String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))


    teacher_group = relationship('groups', secondary = teacher_group, backref = backref('groups', lazy = 'dynamic'))
    user_subject = relationship('subjects', secondary = user_subject, backref = backref('subjects', lazy = 'dynamic'))
    rating_points = relationship('rating', backref = 'student')
    mark = relationship('marks', backref = 'student')

class rating(Base):
    __tablename__ = "rating"

    id = Column('id',Integer,primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    student_name = Column('student_name',String, nullable=False)
    group_name = Column('group_name',String, nullable=False)
    mark = Column('mark',Float , nullable=False)

class subjects(Base):
    __tablename__ = "subjects"
    
    id = Column('id',Integer,primary_key=True)
    name = Column('name',String,nullable=False)

    marks = relationship('marks', backref = 'subject')

class marks(Base):
    __tablename__ = 'marks'

    id = Column('id',Integer,primary_key=True)
    date = Column('name',Date,nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    student_id = Column(Integer, ForeignKey('users.id'))
