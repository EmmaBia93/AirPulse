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

    
# pattern = r'ESSID:"(.*?)".*?Signal level=(-\d+ dBm)'
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QProgressBar,
    QPushButton, QHBoxLayout, QHeaderView
)
from PySide6.QtCore import Qt, QTimer

class SecondaryWindow(QMainWindow):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Escaneo de Paneles")
        
        # Layout principal
        main_layout = QVBoxLayout()

        # Etiqueta para el nombre del usuario
        user_label = QLabel(f"Usuario: {username}")
        user_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(user_label)
        
        # Tabla para mostrar los paneles
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Nombre del Panel", "MAC", "Señal", "Frecuencia"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)
        
        # Barra de progreso infinita
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # 0, 0 para hacerlo infinito
        main_layout.addWidget(self.progress_bar)
        
        # Botones de "Cambiar" y "Cancelar"
        button_layout = QHBoxLayout()
        self.change_button = QPushButton("Cambiar")
        self.cancel_button = QPushButton("Cancelar")
        button_layout.addWidget(self.change_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)
        
        # Configurar el layout principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        # Timer para simular la actualización de la tabla
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_panel_entry)
        self.timer.start(2000)  # Simula la adición de un panel cada 2 segundos
        
        # Conectar el botón de cancelar
        self.cancel_button.clicked.connect(self.stop_scan)

    def add_panel_entry(self):
        # Ejemplo de panel añadido
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem("Panel A"))
        self.table.setItem(row_position, 1, QTableWidgetItem("00:11:22:33:44:55"))
        self.table.setItem(row_position, 2, QTableWidgetItem("-70 dBm"))
        self.table.setItem(row_position, 3, QTableWidgetItem("5500 MHz"))

    def stop_scan(self):
        self.timer.stop()
        self.progress_bar.setRange(0, 1)  # Detiene la barra de progreso infinita

# Ejemplo de cómo iniciar la ventana secundaria
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    username = "UsuarioEjemplo"
    window = SecondaryWindow(username)
    window.show()

    sys.exit(app.exec())
