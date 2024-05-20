from sqlalchemy import Column, Integer, String, Sequence, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(16), nullable=False)
    password = Column(String(50), nullable=False)


engine = create_engine('postgresql://postgres:postgres@users-db:5432/users-db')
Session = sessionmaker(bind=engine)
session = Session()
