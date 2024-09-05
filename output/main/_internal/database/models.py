from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Panel(Base):
    __tablename__ = 'paneles'
    id = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String, nullable=False, unique=True)
    ip = Column(String, nullable=False, unique=True)
    localidad = Column(String,nullable=False)
    frecuencia = Column(String,nullable=True)
    tecnologia = Column(String, nullable=False)
   
class Enlace(Base):
    __tablename__ = 'enlaces'
    id = Column(Integer, primary_key=True,autoincrement=True)
    nombre = Column(String, nullable=False, unique=True)
    ip = Column(String, nullable=False, unique=True)
    localidad = Column(String,nullable=False)
    frecuencia = Column(String,nullable=True)
    tecnologia = Column(String, nullable=False)
   

def init_db():
    #engine = create_engine('sqlite:///app/database/database.db') #Emma
    engine = create_engine('sqlite:///C:\\Users\\PC\\repositorio\\PanelesPY\\server\\app\\database\\database.db') #Elias
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)