# вставка начальных данных
from sqlalchemy.orm import Session
from database import engine
import models

with Session(bind=engine) as session:
    book1 = models.Book(nameBook='Волшебник', price = 159, number_of_pages = 99, number_of_copies = 3, 
    yearPublished = 1986, idPublisher = 1, idFaculty = 1)

    book2 = models.Book(nameBook='Женщины', price = 160, number_of_pages = 414, number_of_copies = 5, 
    yearPublished = 1978, idPublisher = 1, idFaculty = 1)

    book3 = models.Book(nameBook='Лолита', price = 450, number_of_pages = 448, number_of_copies = 1, 
    yearPublished = 1955, idPublisher = 2, idFaculty = 3)

    book4 = models.Book(nameBook='Дым', price = 150, number_of_pages = 200, number_of_copies = 2, 
    yearPublished = 1867, idPublisher = 2, idFaculty = 2)

    book5 = models.Book(nameBook='Клара Милич', price = 80, number_of_pages = 88, number_of_copies = 4, 
    yearPublished = 1883, idPublisher = 3, idFaculty = 1)

    book6 = models.Book(nameBook='Отцы и дети', price = 255, number_of_pages = 288, number_of_copies = 4, 
    yearPublished = 1862, idPublisher = 3, idFaculty = 1)

    autors1 = models.Autor(name = 'Владимир', middleName = 'Владимирович', surname = 'Набоков', books = [book1, book3])
    autors2 = models.Autor(name = 'Чарльз', middleName = 'Чарльз', surname = 'Буковски', books = [book2])
    autors3 = models.Autor(name = 'Иван', middleName = 'Сергеевич', surname = 'Тургенев', books = [book4, book5, book6])
    
    library1 = models.Library(nameLibrary = 'Городская №3', address = 'Матросова, 8', books = [book1, book2])
    library2 = models.Library(nameLibrary = 'Районая библиотека имени Белинского', address = 'Речная, 17', books = [book3, book4])
    library3 = models.Library(nameLibrary = 'Филиал городской №3 на Вые', address = 'Фрунзе, 11', books = [book5, book6])

    publisher1 = models.Publisher(namePublisher='АСТ', city = 'Санкт-Петербург')
    publisher2 = models.Publisher(namePublisher='Лань', city = 'Нижний Тагил')
    publisher3 = models.Publisher(namePublisher='Эксмо', city = 'Москва')

    faculty1 = models.Faculty(nameFaculty = 'Филологический')
    faculty2 = models.Faculty(nameFaculty = 'Исторический')
    faculty3 = models.Faculty(nameFaculty = 'Психологический')
    
    session.add_all([book1, book2, book3, book4, book5, book6, autors1, autors2, autors3,
     library1, library2, library3, publisher1, publisher2, publisher3, faculty1, faculty2, faculty3])
    session.commit()

    