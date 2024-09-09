from PySide6.QtWidgets import QApplication,QWidget,QHBoxLayout,QFrame,QLineEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QDialog, QPushButton, QHeaderView, QLabel, QProgressBar
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QColor, QIcon, QBrush,QCursor
from app.gui.dialog_success import DialogSuccess
from app.gui.dialog_error import DialogError
import os
from app.ssh.ssh_client import ComunicationSSH
import threading
import webbrowser
from app.gui.dialog_auth import AuthDialog
from tkinter.filedialog import askdirectory
from PySide6.QtCore import Qt, QThread, Signal, Slot
import time
import pyperclip
import re
from app.gui.user_windows_edit import SecondaryWindow
from dotenv import load_dotenv
import requests


class CustomTooltip(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurar ventana del tooltip
        self.setWindowFlags(Qt.ToolTip)
        self.setStyleSheet("""
            background-color: #2980b9;
            color: #e5e7e9;
            border: 1px solid #186a3b;
            padding: 5px;
            font-size: 12px;
            border-radius: 10px; /* Redondear los bordes del contenedor */
        """)

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)  # Asegura que el contenido no esté pegado a los bordes

        # Etiqueta de texto donde se mostrará la información
        self.label = QLabel(self)
        self.label.setStyleSheet("border-radius: 10px;")  # Asegura que el contenido también respete el borde redondeado
        self.layout.addWidget(self.label)

        # Botón de cierre
        self.close_button = QPushButton("Cerrar", self)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: black;
                border: 4px solid #c0392b;
                font-size: 17px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
                color: white;
            }
        """)
        self.close_button.clicked.connect(self.hide)
        self.layout.addWidget(self.close_button)

    def set_message(self, message):
        """Actualizar el mensaje del tooltip."""
        self.label.setText(message)
        self.adjustSize()





class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        self.setWindowTitle("Reiniciando Usuarios")
        self.setFixedSize(500, 200)
        layout = QVBoxLayout(self)

        self.label_static = QLabel("Reiniciando usuario:", self)
        self.label_static.setAlignment(Qt.AlignCenter)
        self.label_static.setStyleSheet("""
            QLabel {
                border: 5px solid #1c2d3d; /* Color del borde */
                border-radius: 10px;      /* Esquinas redondeadas */
                
                background-color: #2f4b67; /* Color de fondo */
                color: #dedede;           /* Color del texto */
                font-size: 25px;          /* Tamaño del texto */
                font-weight: bold;        /* Estilo de la fuente */
            }
        """)
        layout.addWidget(self.label_static)

        self.label_user = QLabel("", self)
        self.label_user.setAlignment(Qt.AlignCenter)
        self.label_user.setStyleSheet("font-weight: bold; color: #e74c3c;")  # Ajusta el color y estilo
        layout.addWidget(self.label_user)

        self.ok_button = QPushButton("Aceptar", self)
        self.ok_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: '#27ae60';
                                        color: black;
                                        border: 4px solid #229954;
                                        font-size:17px;
                                        border-radius: 10px;
                                    }
                                    QPushButton:hover {
                                        background-color: '#229954';
                                        color: white;
                                    }
                                """)
        
        self.ok_button.setVisible(False)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button, alignment=Qt.AlignCenter)
        

    @Slot(str)
    def update_user(self, user_name):
        self.label_user.setText(user_name)
        
    @Slot()
    def finish(self):
        self.label_static.setStyleSheet("""
            QLabel {
                border: 5px solid #145a32; 
                border-radius: 10px;     
                background-color: #27ae60; 
                color: #dedede;          
                font-size: 25px;         
                font-weight: bold;       
            }
        """)
        self.label_static.setText("Reinicio completado")
        self.label_user.setVisible(False)
        self.ok_button.setVisible(True)
        
       
    


class UserTable(QDialog):
    def __init__(self, name, ip, tecnologia,current_panels ,parent=None):
        super(UserTable, self).__init__(parent)
        self.name = name
        self.tecnologia = tecnologia
        self.setWindowTitle(name)
        self.setGeometry(100, 100, 1920, 1080)
        self.showMaximized()
        self.current_panels = current_panels

        main_layout = QVBoxLayout(self)

        # Frame para la barra de búsqueda y los botones
        top_frame = QWidget()
        
        top_frame.setStyleSheet("""
            QWidget {
                border: 2px solid #2e86c1;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        top_layout = QHBoxLayout(top_frame)
        # Barra de búsqueda
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar por nombre...")
        self.search_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_bar.setFixedWidth(500)
        
        
        self.search_bar.textChanged.connect(self.filter_table)
        top_layout.addWidget(self.search_bar)
        
        
        # Botones
        backup_button = QPushButton("Respaldar Información")
        backup_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: '#27ae60';
                                        color: black;
                                        border: 4px solid #229954;
                                        font-size:17px;
                                        border-radius: 10px;
                                    }
                                    QPushButton:hover {
                                        background-color: '#229954';
                                        color: white;
                                    }
                                """)
        
        backup_button.clicked.connect(self.backup_user_data)  
        top_layout.addWidget(backup_button)

        restart_all_button = QPushButton("Reiniciar a todos")
        restart_all_button.setStyleSheet("""
                                QPushButton {
                                    background-color: '#e74c3c';
                                    color: black;
                                    border: 4px solid #c0392b;
                                    font-size:17px;
                                    border-radius: 10px;
                                }
                                QPushButton:hover {
                                    background-color: '#c0392b';
                                    color: white;
                                }
                            """)
        restart_all_button.clicked.connect(self.restart_all_users)
        top_layout.addWidget(restart_all_button)

        restart_button = QPushButton("Reiniciar")
        restart_button.setStyleSheet("""
                            QPushButton {
                                background-color: '#f39c12';
                                color: black;
                                border: 4px solid #d68910;
                                font-size:17px;
                                border-radius: 10px;
                            }
                            QPushButton:hover {
                                background-color: '#d68910';
                                color: white;
                            }
                        """)
        restart_button.clicked.connect(self.restart_selected_user)
        top_layout.addWidget(restart_button)

        backup_button = QPushButton("Backup")
        backup_button.setStyleSheet("""
                            QPushButton {
                                background-color: '#9b59b6';
                                color: black;
                                border: 4px solid #512e5f;
                                font-size:17px;
                                border-radius: 10px;
                            }
                            QPushButton:hover {
                                background-color: '#76448a';
                                color: white;
                            }
                        """)
        backup_button.clicked.connect(self.backup_user)  
        top_layout.addWidget(backup_button)

        main_layout.addWidget(top_frame)

        # Configurar la tabla
        self.table = QTableWidget()
        
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["Nombre", "IP", "Frecuencia", "Cable", "Señal", "CCQ", 'Distancia','Activo','Modelo'])
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)
        self.table.setColumnWidth(0, 320)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 120)
        self.table.setColumnWidth(7, 200)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.event_double)
        self.table.horizontalHeader().sectionClicked.connect(self.sortColumn)
        
        
        
        self.table.setMouseTracking(True)
        self.table.cellEntered.connect(self.on_cell_hover)
        self.tooltip = CustomTooltip(self)
        self.tooltip.hide()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_tooltip)

        self.hovered_row = None  # Fila que está siendo hovered
        self.hovered_col = None  # Columna que está siendo hovered
        
        
        
        main_layout.addWidget(self.table)

        # Agregar barra de progreso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedHeight(30)  # Altura fija para la barra de progreso
        self.progress_bar.setStyleSheet("""
                                QProgressBar {
                                    border: 3px solid #2c3e50;     /* Borde */
                                    border-radius: 0px;          /* Esquinas redondeadas */
                                    background-color: #181920;     /* Color de fondo de la barra */
                                    text-align: center;            /* Texto centrado */
                                    font: bold 14px;               /* Estilo del texto */
                                    color: #2c3e50;                /* Color del texto */
                                }

                                QProgressBar::chunk {
                                    border-radius: 10px;           /* Esquinas redondeadas de la parte de progreso */
                                    background-color: qlineargradient(
                                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #1abc9c, stop:1 #16a085);   /* Degradado */
                                }
                            """)
        self.progress_bar.setRange(0, 0)  # Rango normal
        main_layout.addWidget(self.progress_bar)

        close_button = QPushButton("Cerrar")
        close_button.setStyleSheet("""
                                QPushButton {
                                    background-color: '#2980b9';
                                    color: black;
                                    border: 4px solid #154360;
                                    font-size:17px;
                                    border-radius: 10px;
                                }
                                QPushButton:hover {
                                    background-color: '#1f618d';
                                    color: white;
                                }
                            """)
        close_button.clicked.connect(self.accept)  
        main_layout.addWidget(close_button, alignment=Qt.AlignBottom)
        
        self.table.setFocusPolicy(Qt.NoFocus)
        self.setFocus()
        
        # Ejecutar la carga de datos en un hilo separado
        threading.Thread(target=self.load_datatable, args=(ip, tecnologia)).start()

    def filter_table(self, text):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            self.table.setRowHidden(row, text.lower() not in item.text().lower())


    

    def load_datatable(self, ip, tecnologia):
        ssh = ComunicationSSH()
        
        self.response = ssh.request_client(ip,tecnologia)
        self.table.setRowCount(len(self.response))
        
        
        # Rellenar la tabla con datos de SSH
        for row, user in enumerate(self.response):
            self.set_table_item(row, 0, user['name'])
            self.set_table_item(row, 1, user['ip'])
            self.set_table_item(row, 2, user['frequency'])
            self.set_table_item(row, 3, user['speed'] if user['speed'] else 'Desconectado')
            self.set_table_item(row, 4, user['signal'])
            self.set_table_item(row, 5, user['ccq'])
            self.set_table_item(row, 6, user['distance'])
            self.set_table_item(row, 7, user['uptime'])
            self.set_table_item(row, 8, user['platform'])
            


        # Ocultar la barra de progreso cuando se complete la carga
        self.progress_bar.setVisible(False)

    def set_table_item(self, row, column, text):
        text = str(text)
        dic_colors = {
            'enabled': '#d35400', 'Desconocido': '#506fad',
            'disabled': '#2ecc71', 'Desconectado': '#e74c3c',
            '10': '#e74c3c', '100': '#2ecc71'
        }

        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        def set_color(color):
            item.setForeground(QBrush(QColor(color)))

        
        color_mapping = {
            0: lambda: set_color("#dedede"),
            1: lambda: set_color("#e74c3c") if text == 'N/A' else None,
            2: lambda: set_color(dic_colors.get(text, "#000000")),
            3: lambda: set_color(dic_colors.get(text, "#000000")),
            4: lambda: set_color("#2ecc71") if int(text) < 68 else set_color("#f1c40f") if int(text) <= 77 else set_color("#e74c3c"),
            5: lambda: set_color("#2ecc71") if int(text) >= 75 else set_color("#f1c40f") if int(text) >= 60 else set_color("#e74c3c"),
            6: lambda: set_color("#2ecc71") if float(text.replace("km", "").strip()) <= 2.0 else set_color("#f1c40f") if float(text.replace("km", "").strip()) <= 3.0 else set_color("#e74c3c"),
            7: lambda: process_days_column(text),
            8: lambda: set_color("#82a7f5")
        }

        def process_days_column(text):
            match = re.match(r'(\d+)\sdía[s]?\s\d{2}:\d{2}:\d{2}', text)
            if match:
                days = int(match.group(1))
                if days < 15:
                    set_color("#2ecc71")
                elif 15 <= days <= 25:
                    set_color("#f1c40f")
                else:
                    set_color("#e74c3c")
            else:
                set_color("#2ecc71")

        color_mapping.get(column, lambda: None)()

        self.table.setItem(row, column, item)


    def event_double(self, row, column):
        def open_url(data):
            url = f"http://{data}:83"
            webbrowser.open(url)
        
        def show_dialog(dialog_type, message):
            dialog = dialog_type(self, message)
            dialog.exec()
        
        def handle_mac_column():
            pyperclip.copy(self.response[row]['mac'])
        
        def handle_ip_column():
            data = self.table.item(row, 1).text()
            if data != 'N/A':
                open_url(data)
        
        def identificar_tecnologia(nombre_modelo):
            # Definir las expresiones regulares para las diferentes tecnologías
            patrones = {
                "M5": re.compile(r"\bM5\b|\b5AC\b"),
                "AC": re.compile(r"\bAC\b"),
                "M2": re.compile(r"\bM2\b")
            }

            # Verificar contra cada patrón
            for tecnologia, patron in patrones.items():
                if patron.search(nombre_modelo):
                    return tecnologia

            # Si no se encontró ninguna coincidencia
            return "Desconocido"
        
        def filtrar_paneles_compatibles(paneles, tipo_cliente):
            paneles_compatibles = []

            for panel in paneles:
                tipo_panel = panel.tecnologia
                
                if tipo_cliente == "M5":
                    if tipo_panel in ["M5", "AC"]:
                        paneles_compatibles.append(panel.nombre)
                elif tipo_cliente == "AC":
                    if tipo_panel == "AC":
                        paneles_compatibles.append(panel.nombre)
                elif tipo_cliente == "M2":
                    if tipo_panel == "M2":
                        paneles_compatibles.append(panel.nombre)

            return paneles_compatibles
        
        def handle_edit_user():
            current_row = self.table.currentRow()
            tecno = identificar_tecnologia(self.table.item(current_row,8).text())
            
            paneles = filtrar_paneles_compatibles(self.current_panels,tecno)
            
            windows = SecondaryWindow(self.table.item(current_row,0).text(),self.table.item(current_row,1).text(),paneles,self.name,self)
            
            if windows.exec() == QDialog.Accepted:
                response = windows.get_new_info()
                ssh = ComunicationSSH()
                resquest = ssh.change_panel(ip=self.table.item(current_row,1).text(),tecno=tecno,changes=response)
                if resquest:
                    show_dialog(DialogSuccess, f"Se ha cambiado al usuario: {self.table.item(current_row,0).text()} al panel {response['new_panel']}")
                else:
                    show_dialog(DialogError, "No se ha podido cambiar de panel el usuario")
            
        
        def handle_status_column():
            status = self.table.item(row, 2).text()
            ip = self.table.item(row, 1).text()
            ssh = ComunicationSSH()

            if status == 'enabled':
                response = ssh.desmarcar_frecuencia(ip=ip)
                if response:
                    show_dialog(DialogSuccess, "Se ha desmarcado la frecuencia con éxito!!!")
                else:
                    show_dialog(DialogError, "No se ha podido desmarcar la frecuencia")
            elif status == 'disabled':
                show_dialog(DialogError, "Ya está desmarcada la frecuencia")
        
        
        column_actions = {
            0: handle_mac_column,
            1: handle_ip_column,
            2: handle_status_column,
            8: handle_edit_user
        }

        
        action = column_actions.get(column)
        if action:
            action()


        
        
    
    def restart_all_users(self):
        # Crear la ventana emergente
        if self.table.rowCount()>0:
            sesion = AuthDialog(self)
            if sesion.exec_() == QDialog.Accepted:
                self.progress_dialog = ProgressDialog(self)
                self.progress_dialog.show()
                threading.Thread(target=self.restart_users_in_thread).start()

    def restart_users_in_thread(self):
        ssh = ComunicationSSH()
        for row in range(self.table.rowCount()):
            user_name = self.table.item(row, 0).text()
            user_ip = self.table.item(row, 1).text()
            self.progress_dialog.update_user(user_name)
            if self.table.item(row,1).text() != 'N/A':
                tecno = 'AIRMAX' if not 'AC' in self.table.item(row,7).text() else 'AC'
                request = ssh.reboot(user_ip, tecno)
            else:
                pass
               
            

        
        self.progress_dialog.finish()

    


    def backup_user_data(self):

        if self.table.rowCount()>0:
            ruta = askdirectory()
                
            if not ruta:
                print("No se seleccionó ninguna ruta.")
            else:
                local_path = os.path.join(ruta, self.name.replace(" ", "") + ".txt")
                with open(local_path, 'w') as archivo:
                    row = self.table.rowCount()
                    for fila in range(row):
                        datos_fila = []
                        for columna in [0,1]:
                            item = self.table.item(fila, columna)
                            if item is not None:
                                datos_fila.append(item.text().strip())
                            else:
                                datos_fila.append('')  # Si el item está vacío
                        linea = ','.join(datos_fila)  # Separar datos por comas (puedes cambiar el separador)
                        archivo.write(linea + '\n')  # Escribir la línea en el archivo
                    linea = f"Cantidad de usuarios {row}"
                    archivo.write(linea + '\n')
            
            DialogSuccess(self,"Se ha Creado el Archivo con exito!!!").exec()
    
    def restart_selected_user(self):
        row = self.table.currentRow()
        if row > 0 and self.table.item(row,1).text() != 'N/A':
            nombre = self.table.item(row,0).text()
            tecno = 'AIRMAX' if not 'AC' in self.table.item(row,7).text() else 'AC'
            ssh = ComunicationSSH()
            request = ssh.reboot(self.table.item(row,1).text(),tecno)
        if request:
            
            DialogSuccess(self,f"Se ha reiniciado al Usuario: {nombre.title()}, con exito!!!").exec()
        else:
            DialogError(self,f"No se ha podido reiniciar al Usuario: {nombre.title()}").exec()
    
    def backup_user(self):
        row = self.table.currentRow()
        
        if row >0 and self.table.item(row,1).text() != 'N/A':
            
            nombre = self.table.item(row,0).text()
            ssh = ComunicationSSH()
            tecno = 'AIRMAX' if not 'AC' in self.table.item(row,7).text() else 'AC'
            request = ssh.backup(nombre,self.table.item(row,1).text(),tecno)
            if request:
                nombre = self.table.item(row,0).text()
                DialogSuccess(self,f"Backup de: {nombre.title()}, con exito!!!").exec()
            else:
                DialogError(self,f"No se ha podido realizar el Backup al Usuario: {nombre.title()}").exec()
    
    def sortColumn(self, column):
        # Lista de columnas que pueden ser ordenadas
        sortable_columns = [4,5,6]  # Por ejemplo, solo columna 0 y 1 son ordenables

        if column in sortable_columns:
            order = self.table.horizontalHeader().sortIndicatorOrder()
            self.table.sortItems(column, order)
        else:
            # Ignora la ordenación en esta columna
            pass
        
        
    def on_cell_hover(self, row, column):
        # Guardar la celda actual sobre la que el cursor está
        
        self.hovered_row = row
        self.hovered_col = column

        # Reiniciar el temporizador para ejecutar la función después de unos segundos
        self.timer.start(1000)  # 1000 ms = 1 segundo

    def show_tooltip(self):
        cursor_pos = QCursor.pos()
        load_dotenv()

        if self.hovered_row is not None and self.hovered_col == 3:
            mac=self.response[self.hovered_row]['mac']
            url = os.getenv('URL')
            api = os.getenv("API")
            headers = {
            'Authorization':api 
            } 
            params = {
            'mac_cpe':mac
            }

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                response = response.json()
                filtered_data = {}
                for user in response.get('results', []):
                    filtered_data={
                        "nombre": user["nombre"],
                        "ip":user["ip"],
                        "direccion": user["direccion"],
                        "telefono": user["telefono"],
                        "estado": user["estado"],
                        "plan_internet":user["plan_internet"]["nombre"]
                    }

                

                tooltip_message = (
                        f"Nombre: {filtered_data['nombre']}\n"
                        f"IP: {filtered_data['ip']}\n"
                        f"Dirección: {str(filtered_data['direccion']).split('-')[0]}\n"
                        f"Teléfono: {filtered_data['telefono']}\n"
                        f"Estado: {filtered_data['estado']}"
                    )

                self.tooltip.set_message(tooltip_message)
                self.tooltip.move(cursor_pos)
                self.tooltip.show()