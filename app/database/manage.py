from sqlalchemy.orm import sessionmaker
from app.database.models import Panel,Enlace, init_db

Session = init_db()
session = Session()

def get_paneles(localidad):
    """Obtiene todos los dispositivos de una localidad específica.
    Si se especifica el tipo, filtra por tipo ('panel' o 'enlace').
    """
    try:
        query = session.query(Panel).filter_by(localidad=localidad)
        return query.all()
    except:
        return []
    finally:
         session.close()

def get_enlaces():
    
    try:
        query = session.query(Enlace).all()
        return query
    except:
        return []
    finally:
         session.close()

def create_device(nombre, ip, localidad, frecuencia, tecnologia,currente_device):
    """Crea un nuevo dispositivo."""
    try:
        if currente_device == "Panel":
            new_device = Panel(nombre=nombre, ip=ip, localidad=localidad, frecuencia=frecuencia, tecnologia=tecnologia)
        else:
            new_device = Enlace(nombre=nombre, ip=ip, localidad=localidad, frecuencia=frecuencia, tecnologia=tecnologia)
        
        session.add(new_device)
        session.commit()
        return True
    
    except:
        return False
    finally:
         session.close()

def create_enlace(nombre, ip, localidad, frecuencia, tecnologia):
    """Crea un nuevo dispositivo."""
    new_device = Enlace(nombre=nombre, ip=ip, localidad=localidad, frecuencia=frecuencia, tecnologia=tecnologia)
    session.add(new_device)
    session.commit()
    return new_device

def delete_device(nombre,current_device):
    """Elimina un dispositivo por su nombre."""

    try:

        if current_device == "Panel":
            device = session.query(Panel).filter_by(nombre=nombre).first()
        else:
            device = session.query(Enlace).filter_by(nombre=nombre).first()
        if device:
            session.delete(device)
            session.commit()
            return True
        return False
    except:
        return False
    finally:
         session.close()

def update_device(ip,nuevo_nombre=None, nueva_frecuencia=None, nueva_tecnologia=None,current_device=None):
    try:
        # Buscar el registro por IP
        if current_device=="Panel":
            device = session.query(Panel).filter_by(ip=ip).first()
        else:
            device = session.query(Enlace).filter_by(ip=ip).first()
            
         # Si el registro no existe, retornar un mensaje
        if not device:
            return False
        
        #Actualizar los campos si se proporcionaron nuevos valores
        if nuevo_nombre:
            device.nombre = nuevo_nombre
        if nueva_frecuencia:
            device.frecuencia = nueva_frecuencia
        if nueva_tecnologia:
            device.tecnologia = nueva_tecnologia
        
        # # Guardar los cambios en la base de datos
        session.commit()
        return True
    except Exception as e:
        # En caso de error, deshacer los cambios
        session.rollback()
        return False
    finally:
        session.close()