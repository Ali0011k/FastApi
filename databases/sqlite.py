from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from decouple import config

SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL", cast=str)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """user model in database"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    # create a relationship from Items model to User model with verbose_name = owner
    items = relationship("Item", back_populates="owner")


class Item(Base):
    """item model in database"""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer, default=1000)

    # foreignkey to User model
    owner_id = Column(Integer, ForeignKey("users.id"))

    # create a relationship from User model to Item model with verbose_name = items
    owner = relationship("User", back_populates="items")
