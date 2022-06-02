from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, Table
from sqlalchemy.orm import relationship

from database import Base

# Вспомогательная таблица для связи многие ко многим у книг и библиотек
library_books = Table('library_books', Base.metadata,
 Column('book_id', ForeignKey('books.id'), primary_key=True),
 Column('library_id', ForeignKey('librarys.id'), primary_key=True))

 # Вспомогательная таблица для связи многие ко многим у книг и авторов
autor_books = Table('autor_books', Base.metadata,
 Column('book_id', ForeignKey('books.id'), primary_key=True),
 Column('autor_id', ForeignKey('autors.id'), primary_key=True))

# Таблица "Книги"
class Book(Base):
    __tablename__='books'
    id = Column(Integer, primary_key=True)
    nameBook = Column(String, unique=True, index=True)
    price = Column(Numeric, default=0)
    number_of_pages = Column(Integer,index=True)
    number_of_copies = Column(Integer,index=True)
    yearPublished = Column(Integer,index=True)
    idPublisher = Column(Integer,ForeignKey("publishers.id"))
    idFaculty = Column(Integer, ForeignKey('faculties.id'))

    publishers = relationship("Publisher", back_populates="books")
    faculties = relationship("Faculty", back_populates="books")

# Таблица "Библиотеки"
class Library(Base):
    __tablename__ = 'librarys'
    id = Column(Integer, primary_key=True)
    nameLibrary = Column(String, unique=True, index=True)
    address = Column(String, index=True)

    # backref автоматически делает связь в другой таблице
    books = relationship("Book", secondary="library_books", backref="librarys")

# Таблица "Пользователи"
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))

# Таблица "Авторы"
class Autor(Base):
    __tablename__ = 'autors'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    middleName = Column(String, unique=True, index=True)
    surname = Column(String, unique=True, index=True)

    books = relationship("Book", secondary = "autor_books", backref="autors")

# Таблица "Издательства"
class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True)
    namePublisher = Column(String, unique=True, index=True)
    city = Column(String, unique=True, index=True)

    books = relationship("Book", back_populates="publishers")

# Таблица "Факультеты"
class Faculty(Base):
    __tablename__ = 'faculties'
    id = Column(Integer, primary_key=True)
    nameFaculty = Column(String, unique=True, index=True)

    books = relationship("Book", back_populates="faculties")