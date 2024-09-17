from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

Base = declarative_base()

class Panel(Base):
    __tablename__ = 'paneles'
    id = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String(255), nullable=False, unique=True)
    ip = Column(String(255), nullable=False, unique=True)
    localidad = Column(String(255),nullable=False)
    frecuencia = Column(String(255),nullable=True)
    tecnologia = Column(String(255), nullable=False)
   
class Enlace(Base):
    __tablename__ = 'enlaces'
    id = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String(255), nullable=False, unique=True)
    ip = Column(String(255), nullable=False, unique=True)
    localidad = Column(String(255),nullable=False)
    frecuencia = Column(String(255),nullable=True)
    tecnologia = Column(String(255), nullable=False)
   

def init_db():
    load_dotenv()
    DATA_URL = f"mysql+pymysql://root:{os.getenv('PASS_DATA')}@localhost:3306/ciudad_internet"
    engine = create_engine(DATA_URL) 
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)