import threading as th
import paramiko
import os
from scp import SCPClient
import concurrent.futures
from dotenv import load_dotenv
from tkinter.filedialog import askdirectory
from app.ssh.tools_aux import cantidad_horas_activo
import time
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
class ComunicationSSH:
    
        
    def __create_ssh_client(self,ip, port, username, password):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(ip, port=port, username=username, password=password)
        except paramiko.SSHException as e:
            print(f"SSH connection error: {e}")
            raise

        return ssh
    
    
    def backup(self,name:str,ip:str,tecno:str):
        ruta = askdirectory()
        load_dotenv()
        
        if not ruta:
            print("No se seleccionó ninguna ruta.")
            return False

        try:
            if tecno != 'AC':
                client = self.__create_ssh_client(ip, os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AIRMAX'))
            else:
                client = self.__create_ssh_client(ip, os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AC'))
           
            local_path = os.path.join(ruta, name.replace(" ", "") + ".cfg")
                       
            with SCPClient(client.get_transport()) as scp:
                scp.get('/var/tmp/system.cfg', local_path)
        
            return True

        except paramiko.AuthenticationException as e:
            print(f"Error de autenticación: {e}")
            return False
        except paramiko.SSHException as e:
            print(f"Error SSH: {e}")
            return False
        except OSError as e:
            print(f"No se pudo realizar la transferencia \nError: {e}")
            return False
        except Exception as e:
            print(f"Error inesperado: {e}")
            return False
        finally:
            client.close()

    
    def reboot(self, ip: str,tecno:str) -> bool:
        
        load_dotenv()
        try:
            if tecno != 'AC':
                client = self.__create_ssh_client(ip, os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AIRMAX'))
            else:
                client = self.__create_ssh_client(ip, os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AC'))
            
            if client:
                stdin, stdout, stderr = client.exec_command('reboot')
                client.close()
                return True
            else:
                print("Failed to create SSH client.")
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
        
    def __info_device(self,ip: str, port: int, username: str, get_pass: str, name_device: str,tecno:str):
        
        if tecno !='AIRFIBER':
            command = "(((wstalist -p | grep -c \"mac\" ; mca-status | grep uptime | cut -c8- ;mca-status | grep lanSpeed | awk -F'[=M]' '{print $2}')| xargs echo -n)| tr \" \" \", \" )"

        else:
           command = "(((wstalist -p | grep -c \"mac\" ; mca-status | grep uptime | cut -c8- ; mca-status | ifconfig ath0 | grep txqueuelen | sed 's/.*txqueuelen:\\([0-9]*\\).*/\\1/') | xargs echo -n) | tr \" \" \",\")"

        client = None
        try:
            
            client =self.__create_ssh_client(ip=ip, port=port, username=username, password=get_pass)
           
            if client:
                stdin, stdout, stderr = client.exec_command(command=command, timeout=3)
                
                output = stdout.read().decode("utf-8").strip()
                error = stderr.read().decode("utf-8").strip()
               
                # Verificar estado de ejecución del comando
                code_status = stdout.channel.recv_exit_status()
                
                if code_status == 0:
                    
                    results = output.split(",")
                    
                    if len(results) == 3:
                        
                        return(f"{output},{ip},{name_device}")
                    else:
                        return (f"{output},0,{ip},{name_device}")
                else:
                    return (f"0,0,0,{ip},{name_device}")
                    
        except TimeoutError as e:
            print(f"SSH connection timeout error: {e}")
        except paramiko.SSHException as e:
            print(f"SSH connection error: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if client:
                client.close()


    def inicializacion_ssh(self,ips: list) -> dict:
        """
        La funcion recibe como parametro una lista de lista, la cual esta compuesta por:
        Nombre: El nombre del dispositivo.
        IP: Direccion del dispositivo.
        Tecnologia: Ya sea AC, M2 o M5.
        Se debe respetar ese orden al momento de armar la lista.

        Retorna: Un diccionario con la siguiente estructura:

        Nombre:{ "clientes": client_count,"ip": ip,"tiempo": cantidad_horas_activo,"velocidad": speed }
        
        """
        load_dotenv()
        def connection_wrapper(name,ip,tecno):
            
            if tecno == 'M5' or tecno =='M2':
                
                return self.__info_device(ip,os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AIRMAX'), name,tecno)
            
            else:
                
                return self.__info_device(ip,os.getenv('PORT'), os.getenv('UBNT'), os.getenv('PASS_AC'), name,tecno)
            
        
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(ips)) as executor:
            future_to_ip = {executor.submit(connection_wrapper,name,ip,tecno): (name,ip,tecno) for name,ip,tecno in ips}
            
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    data = future.result()
                    split_text = data.split(",")
                   
                    client_count, uptime, speed, ip, name = split_text[0], int(split_text[1]), split_text[2], split_text[3], split_text[4]
                    
                    results[name] = {
                        "clientes": client_count,
                        "ip": ip,
                        "tiempo": cantidad_horas_activo(uptime),
                        "velocidad": speed
                    }
                except Exception as exc:
                    print(f'Error processing {ip}: {exc}')
        
        return results
                

    def desmarcar_frecuencia(self,ip):
        load_dotenv()
        ssh = self.__create_ssh_client(ip=ip,port=os.getenv('PORT'),username=os.getenv('UBNT'),password=os.getenv('PASS_AIRMAX'))
        if ssh:
            
            command = "sed -i 's/^wireless.1.scan_list.status=enabled$/wireless.1.scan_list.status=disabled/' /tmp/system.cfg && cfgmtd -wp /etc"
            command1 = "reboot"
            try:
                ssh.exec_command(command=command)
                time.sleep(2)
                ssh.exec_command(command=command1)
                
                return True
            except TimeoutError as e:
                print(f"SSH connection timeout error: {e}")
                return False
            except paramiko.SSHException as e:
                print(f"SSH connection error: {e}")
                return False
            
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return False
            finally:
                ssh.close()


    def request_client(self,ip,tecno):
        load_dotenv()
        port = os.getenv('PORT')
        user = os.getenv('UBNT')
        results = []
        command = "wstalist"

        if tecno != "AC":
            password = os.getenv('PASS_AIRMAX')
        else:
            password = os.getenv('PASS_AC')
        
        client = self.__create_ssh_client(ip=ip,port=port,username=user,password=password)
        stdin, stdout, stderr = client.exec_command(command=command)
        output = stdout.read().decode("utf-8").strip()
        output = json.loads(output)

        def fetch_additional_info(client_ip,password_client,tecno_client):
            
            client = self.__create_ssh_client(client_ip, os.getenv('PORT'), os.getenv('UBNT'), password_client)
            if client:
                if tecno_client != 'AC':
                    command_f = "cat /tmp/system.cfg | grep -o 'wireless.1.scan_list.status=[^,]*' |awk -F '=' '{print $2}'"
                else:
                    command_f ="cat /tmp/system.cfg | grep -o 'radio.1.scan_list.status=[^,]*' | awk -F '=' '{print $2}'"
                stdin, stdout, stderr = client.exec_command(command=command_f, timeout=3)
                return stdout.read().decode("utf-8").strip()
            return "Desconocido"
        
        futures = {}

        with ThreadPoolExecutor() as executor:
            
            
            for current in output:
                ip_address = current.get('lastip', '')

                name = re.sub(r'\b(M2|M5|AC)\b|\B(M2|M5)', '', current.get('remote', {}).get('hostname', '')).strip() or '-'
                
                distance = f"{int(current.get('remote', {}).get('distance', 0)) / 1000:.1f} km"
                
                signal = str(current.get('remote', {}).get('signal', '0')).replace('-', '')
                
                lan = current.get('remote', {}).get('ethlist', [{'speed': '10'}])[0].get('speed', '10')
                
                mac = current.get('mac', '')
                
                platform = current.get('remote', {}).get('platform', 'Demasiado Vieja')
                
                ccq = current.get('ccq', '100')
                
                uptime = current.get('remote', {}).get('uptime', '0')
                
                if ip_address != "0.0.0.0":
                    password_client = os.getenv('PASS_AIRMAX') if not '5AC' in platform else os.getenv('PASS_AC')
                    tecno_client = 'AIRMAX' if not '5AC' in platform else 'AC'
                    future = executor.submit(fetch_additional_info, ip_address,password_client,tecno_client)
                    futures[future] = current
                
                results.append({
                    'name': name,
                    'ip': ip_address if ip_address != "0.0.0.0" else "N/A",
                    'frequency': 'Desconocido',  # Inicialmente desconocido
                    'speed': lan,
                    'signal': signal,
                    'ccq': ccq,
                    'distance': distance,
                    'mac': mac,
                    'platform': platform,
                    'uptime':cantidad_horas_activo(int(uptime))
                })
        
        for future in as_completed(futures):
            current = futures[future]
            try:
                frequency = future.result()
                # Encuentra el diccionario correspondiente y actualiza la frecuencia
                for result in results:
                    if result['mac'] == current['mac']:
                        result['frequency'] = frequency if frequency else "Desconocido"
            except Exception as exc:
                print(f'Error al obtener frecuencia para {current["mac"]}: {exc}')
    
        return results
    
    def scanning(self,ip,tecno):
        load_dotenv()
        
        username = os.getenv('UBNT')
        port = os.getenv('PORT')
        
        if tecno != 'AC':
            password = os.getenv('PASS_AIRMAX')
        else:
            password = os.getenv('PASS_AC')
            
        client = self.__create_ssh_client(ip,port,username,password)
        
        if client:
            stdin, stdout, stderr = client.exec_command(command="iwlist ath0 scanning")
            output = stdout.read().decode("utf-8").strip()
            code_status = stdout.channel.recv_exit_status()
            if code_status == 0:
                
                pattern = r'Address:\s*([\w:]+).*?ESSID:"(.*?)".*?Frequency:(\d+\.\d+) GHz.*?Signal level=(-\d+ dBm)'

                result = []
                matches = re.findall(pattern, output, re.DOTALL)
                for address, essid, frequency, signal_level in matches:
                   
                    frequency_mhz = float(frequency) * 1000
                    result.append({'Address': {address}, 'ESSID': {essid}, 'Signal Level': {signal_level}, 'Frequency':{frequency}})
                client.close()
                return result
            else:
                print("no se puedo conseguir nada")
                client.close()
                return result
        
    def change_panel(self,ip:str,tecno:str,changes:dict):
        username = os.getenv('UBNT')
        port = os.getenv('PORT')
        try:
            new_panel = changes.get('new_panel')
            user_panel = f"{changes.get('user_panel','-')} {tecno}"
            command= f"""
            sed -i 's/^wpasupplicant.profile.1.network.1.ssid=.*$/wpasupplicant.profile.1.network.1.ssid={new_panel}/' /tmp/system.cfg
            sed -i 's/^wireless.1.ssid=.*$/wireless.1.ssid={new_panel}/' /tmp/system.cfg
            sed -i 's/^resolv.host.1.name=.*$/resolv.host.1.name={user_panel}/' /tmp/system.cfg
            cfgmtd -wp /etc
            """
            if tecno != 'AC':
                password = os.getenv('PASS_AIRMAX')
            else:
                password = os.getenv('PASS_AC')
            
            client = self.__create_ssh_client(ip=ip,port=port,username=username,password=password)
            if client:
                client.exec_command(command=command)
                time.sleep(3)
                client.exec_command(command="reboot")
                return True
        except:
            return False
        finally:
            client.close()
    
    
    def stats_enlace(self,ip:str,tecno:str):
        load_dotenv()
        password = os.getenv("PASS_AC")
        user = os.getenv("UBNT")
        port = os.getenv("PORT")
        client = self.__create_ssh_client(ip=ip,port=port,username=user,password=password)
        
        if tecno == 'AIRFIBER':
            
            if client:
                stdin, stdout, stderr = client.exec_command("af get rxcapacity; af get txcapacity; af get rxpps; af get txpps;mca-status | grep 'distance' | awk -F '=' '{print $2}'")
                output = stdout.read().decode('utf-8')
                lines = output.splitlines()

                if len(lines) == 5:
                    rxcapacity = int(lines[0])/1000
                    txcapacity = int(lines[1])/1000
                    rxpps = int(lines[2])
                    txpps = int(lines[3])
                    distance = int(lines[4])/1000
                    if rxpps>txpps:
                        txpps=txpps/1000
                        rxpps=rxpps/100
                    else:
                        txpps=txpps/100
                        rxpps=rxpps/1000


                    return {"rxcapacidad":f"{rxcapacity:.1f}","txcapacidad":f"{txcapacity:.1f}","rxvivo":f"{rxpps:.1f}","txvivo":f"{txpps:.1f}","distancia":f"{distance:.1f}"}
                else:
                    return {"rxcapacidad":0,"txcapacidad":0,"rxvivo":0,"txvivo":0}
            else:
                return {"rxcapacidad":0,"txcapacidad":0,"rxvivo":0,"txvivo":0}
        else:
            if client:
                stdin, stdout, stderr = client.exec_command("mca-status | grep 'wlanDownlinkCapacity' | awk -F '=' '{print $2}';mca-status | grep 'wlanUplinkCapacity' | awk -F '=' '{print $2}'; mca-status | grep 'distance' | awk -F '=' '{print $2}'")
                output = stdout.read().decode('utf-8')
                lines = output.splitlines()
                
                if len(lines) == 3:
                    rxcapacity = int(lines[0])/1000
                    txcapacity = int(lines[1])/1000
                    distance = int(lines[2])/1000
                    return{"rxcapacidad":rxcapacity,"txcapacidad":txcapacity,"distancia":distance}
