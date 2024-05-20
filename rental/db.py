from enum import Enum

from sqlalchemy import Column, Integer, String, Sequence, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Enum as saEnum

Base = declarative_base()


class RentalStatus(Enum):
    borrowed = "borrowed"
    retrieved = "retrieved"


class RentalRecord(Base):
    __tablename__ = 'rental_records'

    id = Column(Integer, Sequence('rental_records_id_seq'), primary_key=True)
    book_id = Column(String(24), nullable=False)
    user_id = Column(Integer, nullable=False)
    borrowed_date = Column(DateTime(timezone=True))
    retrieved_date = Column(DateTime(timezone=True))
    status = Column(saEnum(RentalStatus), nullable=False)


engine = create_engine('postgresql://postgres:postgres@rental-db:5432/rental-db')
Session = sessionmaker(bind=engine)
session = Session()
