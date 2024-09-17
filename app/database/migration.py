from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

Base = declarative_base()

# Definimos las tablas para Paneles y Enlaces
class Panel(Base):
    __tablename__ = 'paneles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False, unique=True)
    ip = Column(String(255), nullable=False, unique=True)
    localidad = Column(String(255), nullable=False)
    frecuencia = Column(String(255), nullable=True)
    tecnologia = Column(String(255), nullable=False)

class Enlace(Base):
    __tablename__ = 'enlaces'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False, unique=True)
    ip = Column(String(255), nullable=False, unique=True)
    localidad = Column(String(255), nullable=False)
    frecuencia = Column(String(255), nullable=True)
    tecnologia = Column(String(255), nullable=False)

def init_db():
    load_dotenv()
    # Conexión a MySQL
    DATA_URL = f"mysql+pymysql://root:{os.getenv('PASS_DATA')}@localhost:3306/ciudad_internet"
    engine_mysql = create_engine(DATA_URL)
    # Crear tablas en MySQL si no existen
    Base.metadata.create_all(engine_mysql)
    
    # Conexión a SQLite
    engine_sqlite = create_engine('sqlite:///C:\\Users\\PC\\Documents\\repositorio\\PanelesPyside6\\app\\database\\database.db')
    
    return sessionmaker(bind=engine_mysql), sessionmaker(bind=engine_sqlite)
def migrate_data():
    # Inicializar las sesiones para MySQL y SQLite
    MySQLSession, SQLiteSession = init_db()
    
    mysql_session = MySQLSession()
    sqlite_session = SQLiteSession()
    
    try:
        # Leer todos los registros de la tabla 'paneles' en SQLite
        paneles = sqlite_session.query(Panel).all()
        for panel in paneles:
            # Insertar cada panel en la tabla correspondiente en MySQL
            mysql_session.add(Panel(
                nombre=panel.nombre,
                ip=panel.ip,
                localidad=panel.localidad,
                frecuencia=panel.frecuencia,
                tecnologia=panel.tecnologia
            ))
        
        # Leer todos los registros de la tabla 'enlaces' en SQLite
        enlaces = sqlite_session.query(Enlace).all()
        for enlace in enlaces:
            # Insertar cada enlace en la tabla correspondiente en MySQL
            mysql_session.add(Enlace(
                nombre=enlace.nombre,
                ip=enlace.ip,
                localidad=enlace.localidad,
                frecuencia=enlace.frecuencia,
                tecnologia=enlace.tecnologia
            ))
        
        # Confirmar la transferencia de datos a MySQL
        mysql_session.commit()
        print("Migración completada con éxito.")
    
    except Exception as e:
        # En caso de error, revertir los cambios
        mysql_session.rollback()
        print(f"Error durante la migración: {e}")
    
    finally:
        # Cerrar las sesiones
        mysql_session.close()
        sqlite_session.close()

# Ejecutar la migración
migrate_data()
