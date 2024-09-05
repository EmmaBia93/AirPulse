# import re
# import paramiko


# def create_ssh_client(ip, port, username, password):
#         ssh = paramiko.SSHClient()
#         ssh.load_system_host_keys()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#         try:
#             ssh.connect(ip, port=port, username=username, password=password)
#         except paramiko.SSHException as e:
#             print(f"SSH connection error: {e}")
#             raise

#         return ssh
    
# client = create_ssh_client("10.107.1.155","23","ubnt","628819872")
# stdin, stdout, stderr = client.exec_command(command="iwlist ath0 scanning")
# output = stdout.read().decode("utf-8").strip()


# code_status = stdout.channel.recv_exit_status()

# if code_status == 0:
#         print (output)
# else:
#     print("no se puedo conseguir nada")

    

