# PanelesPyside6
Un script para el manejo de Dispositivos Ubiquiti, para el monitoreo y gestion de los mismos.

Solucion mensaje de TripleDES Paramiko:
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
en archivos pkey.py y transport.py
"cipher": algorithms.TripleDES, ---> "cipher": TripleDES,
