# AirPulse

**Panel de escritorio para la gestión y supervisión de dispositivos Ubiquiti.**

AirPulse es una aplicación desarrollada en Python que reúne en una interfaz gráfica las tareas de administración y monitoreo de equipos Ubiquiti. Está pensada para facilitar el trabajo cotidiano sobre infraestructura de red, ofreciendo una base centralizada para consultar dispositivos y comunicarse con ellos.

## ¿Qué ofrece?

- **Interfaz gráfica:** aplicación de escritorio construida con PySide6.
- **Comunicación remota:** conexión con los dispositivos mediante SSH.
- **Verificación de conectividad:** comprobaciones ICMP para conocer si un equipo responde.
- **Persistencia de información:** utiliza SQLAlchemy para gestionar los datos almacenados.
- **Transferencia de archivos:** incluye soporte SCP para operaciones de transferencia.

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| PySide6 | Interfaz gráfica |
| Paramiko | Comunicación SSH |
| icmplib | Verificación ICMP |
| SQLAlchemy | Acceso y gestión de datos |
| SCP | Transferencia de archivos |

## Ejecución

Cloná el repositorio e instalá las dependencias:

```bash
git clone https://github.com/EmmaBia93/AirPulse.git
cd AirPulse
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

En Windows, activá el entorno con `.venv\\Scripts\\activate`.

> **Nota:** la aplicación requiere acceso de red a los dispositivos que se quieran administrar. Las operaciones disponibles dependen de la implementación y configuración de cada equipo.

## Objetivo

AirPulse nace de la experiencia en administración de redes y busca convertir tareas habituales de operación en un flujo de trabajo más cómodo, visual y organizado.

---
Desarrollado por [EmmaBia93](https://github.com/EmmaBia93).
