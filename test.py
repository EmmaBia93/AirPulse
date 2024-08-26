import paramiko
from dotenv import load_dotenv
import json
import re
from scp import SCPClient,SCPException
import os
from tkinter.filedialog import askopenfilename
from time import sleep

def __create_ssh_client(ip, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
            ssh.connect(ip, port=port, username=username, password=password)
    except paramiko.SSHException as e:
        print(f"SSH connection error: {e}")
        raise

    return ssh


load_dotenv()
path = askopenfilename()
dir_name, file_name = os.path.split(path)
base_name, ext = os.path.splitext(file_name)
new_name="fwupdate"
new_file_path = os.path.join(dir_name, new_name + ext)

try:
    os.rename(path, new_file_path)
except Exception as e:
    print("No se pudo")

try:

    #client = __create_ssh_client("10.110.0.65",os.getenv('PORT'),os.getenv('UBNT'),os.getenv('PASS_AIRMAX'))
    # with SCPClient(client.get_transport()) as scp:
    #     scp.put(new_file_path, '/tmp/fwupdate.bin')
    #     sleep(3)
    #     client.exec_command("/sbin/fwupdate -m")
except SCPException as e:
    print(f"Error al transferir el archivo: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    # Cerrar la conexión SSH
    client.close()


 