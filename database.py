from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import models

# Укажите параметры подключения к вашей базе данных
DATABASE_URL = "postgresql://postgres:5335@localhost/postgres"

# Создаем движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Сессия, которая будет использоваться для всех операций с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс моделей
Base = models.Base  # Это должно быть импортировано из models.py, если Base определен там

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для создания всех таблиц в базе данных
def create_tables():
    Base.metadata.create_all(bind=engine)

# # Функция для удаления всех таблиц
# def drop_tables():
#     Base.metadata.drop_all(bind=engine)
