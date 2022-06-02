from .Book import Book_get
from .Library import Library_get
from .Autor import Autor_get
from .Publisher import Publisher_get
from .Faculty import Faculty_get
from typing import List

class BookSchema(Book_get):
    librarys:List[Library_get]
    autors:List[Autor_get]

class LibrarySchema(Library_get):
    books:List[Book_get]    

class AutorSchema(Autor_get):
    books:List[Book_get]

class PublisherSchema(Publisher_get):
    books:List[Book_get] 

class FacultySchema(Faculty_get):
    books:List[Book_get]     