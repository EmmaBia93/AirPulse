from PySide6.QtWidgets import QApplication,QDialog,QLabel,QStatusBar,QMainWindow,QButtonGroup, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame
from PySide6.QtCore import QFile, QTextStream, Qt,QSize
from PySide6.QtGui import QColor,QIcon,QPixmap,QPainter
import threading
from time import sleep
import datetime
from app.database.manage import get_paneles,update_device,create_device,delete_device,get_enlaces
from app.icmp.icmp_client import is_device_online
from  app.ssh.ssh_client import ComunicationSSH
from app.toggle.toogle_switch import Toggle
from app.gui.edit_windows import EditWindow
from app.gui.delete_windows import DeletePanelDialog
from app.gui.new_device_windows import NewPanelWindows
from app.gui.dialog_success import DialogSuccess
from app.gui.dialog_error  import DialogError
from app.gui.dialog_auth import AuthDialog
from app.gui.circle_status import StatusCircle
from app.gui.users_windows import UserTable
import webbrowser


class MainWindow(QMainWindow):
    def __init__(self, useCustomTheme=False, themeFile=""):
        super().__init__()

        self.setWindowTitle("Gestión de Paneles")
        self.setGeometry(100, 100, 1920, 1080)
        self.showMaximized()  # Iniciar en pantalla completa
        self.current_device=""
        self.count_client=0
        self.hora_inicio = datetime.time(9, 0)
        self.hora_fin = datetime.time(21, 0) 
        # Widget central
        #self.setWindowFlags(Qt.FramelessWindowHint)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon("C:\\Users\\PC\\Documents\\repositorio\\PanelesPyside6\\app\\gui\\img\\iconsatelite.ico"))
        self.setIconSize(QSize(30,30))
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
      
        # Menú de localidades
        menu_frame = QFrame()
        menu_frame.setFrameShape(QFrame.StyledPanel)
        menu_frame.setStyleSheet("""
                QFrame {
                    border: 2px solid #2e86c1; /* Cambia el ancho y el color del borde */
                    border-radius: 5px;   /* Si quieres esquinas redondeadas */
                }
            """)
        menu_layout = QVBoxLayout(menu_frame)
        
        self.ssh_switch = Toggle()
        self.ssh_switch.toggled.connect(self.toggle_banner)
        
        menu_layout.addWidget(self.ssh_switch,Qt.AlignCenter,Qt.AlignHCenter)
        
        localidades = ["Media Agua", "Los Berros", "Colonia", "Cochagual", "Carpinteria","Cañada", "Tres Esquinas","Enlaces"]
        self.botones = []
        # Crear un QButtonGroup para gestionar la exclusividad
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)  # Asegura que solo un botón esté presionado a la vez
        for localidad in localidades:
            btn = QPushButton(localidad)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                                QPushButton {
                                    background-color: '#4b4985';
                                    color: black;
                                    border: 4px solid #1b1a2e;
                                    border-radius: 10px;
                                }
                                QPushButton:hover {
                                    background-color: '#35345c';
                                    color: white;
                                }
                              QPushButton:checked {
                                    background-color: #d35400;
                                    color: black;
                                    border: 4px solid #6e2c00;
                                    
                                }
                               QPushButton::checked:hover{
                                    background-color: #a04000;
                                    color: white;
                              } 
                            """)
            btn.setFixedHeight(60)  
            btn.setFixedWidth(200)
            
            
            btn.setIconSize(QSize(10,10))
            
            btn.clicked.connect(lambda checked, loc=localidad: self.load_data(loc))
            self.button_group.addButton(btn)
            self.botones.append(btn)
            menu_layout.addWidget(btn)
            
            
            
        ping_thread = threading.Thread(target=self.update_buttons)
        ping_thread.daemon = True
        ping_thread.start()
        
        # Expandir botones verticalmente
        menu_layout.addStretch(1)
        
        main_layout.addWidget(menu_frame)
        
        # Panel derecho
        right_panel = QWidget()
        right_panel.setContentsMargins(0,0,0,0)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0,0,0,0)
        # Botones superiores
        buttons_frame = QFrame()
        buttons_frame.setContentsMargins(0,0,0,0)
        buttons_frame.setStyleSheet("""
                QFrame {
                    border: 2px solid #2e86c1; 
                    border-radius: 5px; 
                }
            """)
        buttons_frame.setFrameShape(QFrame.StyledPanel)
        buttons_layout = QHBoxLayout(buttons_frame)
        btn_funcion = {"Editar":self.edit_selected_row,
                       "Eliminar":self.borrar_device,
                       "Nuevo Enlace":self.new_enlace,
                       "Nuevo Panel":self.new_panel,
                       "Backup":self.create_backup,
                       "Reiniciar":self.reboot
                       }
        

        button_labels = ["Editar", "Eliminar", "Nuevo Enlace", "Nuevo Panel", "Backup", "Reiniciar"]
        for label in button_labels:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                                QPushButton {
                                    background-color: '#147a93';
                                    color: black;
                                    border: 3px solid #072a32;
                                    font-size:17px;
                                    border-radius: 10px;
                                }
                                QPushButton:hover {
                                    background-color: '#0e5364';
                                    color: white;
                                }
                              
                                
                            """)
            buttons_layout.addWidget(btn)
            btn.clicked.connect(btn_funcion[label])
        
        right_layout.addWidget(buttons_frame)
        main_layout.addWidget(right_panel)
        
        # Tabla de paneles
        self.table = QTableWidget()
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setColumnCount(8)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(["Nombre", "IP", "Tiempo", "Clientes", "LAN", "Hz","Tec","Estado"])
        self.table.horizontalHeader().setSectionResizeMode(7,QHeaderView.Stretch)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 70)
        self.table.setColumnWidth(6, 100)

      
        
       

        # Hacer las filas seleccionables pero no editables
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.event_double)
        
       


        right_layout.addWidget(self.table)
        
        
        
        self.footer_label = QLabel("Cantidad de clientes: ")
        self.footer_label.setAlignment(Qt.AlignCenter)
        self.footer_label.setFixedHeight(30)
        self.footer_label.setStyleSheet("""
            QLabel {
                border:1px solid #2e86c1;
                background-color: #3498db;
                color: #dedede;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px;
            }
        """)
        self.footer_label.setVisible(False)
        right_layout.addWidget(self.footer_label)
        
        

        # Aplicar el tema personalizado si está habilitado
        if useCustomTheme:
            self.apply_theme(themeFile)
            
    def toggle_banner(self, enabled):
        """Mostrar u ocultar el banner según el estado de ssh_switch."""
        
        self.footer_label.setText("Cantidad de clientes: ")
        self.footer_label.setVisible(enabled)
        
    def apply_theme(self, qss_file):
        file = QFile(qss_file)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def create_colored_dot_icon(self,color):
        pixmap = QPixmap(30, 30)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 30, 30)
        painter.end()
        return QIcon(pixmap)

    def load_data(self, localidad):
        if localidad!="Enlaces":
            self.current_device="Panel"
            if self.ssh_switch.StateButton():
                self.toggle_banner(True)
            devices = get_paneles(localidad)
            self.current_paneles = devices
        else:
            self.current_device="Enlace"
            self.toggle_banner(False)
            devices = get_enlaces()
            
        devices_ssh = [[panel.nombre, panel.ip,panel.tecnologia] for panel in devices]
            
        threading.Thread(target=self.update_table_data, args=(devices,devices_ssh)).start()

    

    def update_table_data(self, devices,devices_ssh):

       
        ssh_enabled = self.ssh_switch.StateButton()
        self.count_client=0
        if ssh_enabled:
            conn = ComunicationSSH()
            ssh_data = conn.inicializacion_ssh(devices_ssh)
        else:
            ssh_data = {device.nombre: {"clientes": "-", "tiempo": "-", "velocidad": "-"} for device in devices}
        
        ips = [device.ip for device in devices]
        online_status = is_device_online(ips)

        # Actualizar la tabla en el hilo principal
        self.table.setRowCount(len(devices))
        
        for row, device in enumerate(devices):
            name = device.nombre
            ip = device.ip
            frec = device.frecuencia
            tec = device.tecnologia
            data = ssh_data.get(name, {})
            online = online_status.get(ip, False)
            if data.get("clientes") != '-':
                self.count_client+=int(data.get("clientes",0))
            self.set_table_item(row, 0, name)
            self.set_table_item(row, 1, ip)
            self.set_table_item(row, 2, str(data.get("tiempo", "-")))
            self.set_table_item(row, 3, str(data.get("clientes", "-")))
            self.set_table_item(row, 4, data.get("velocidad", "-"))
            self.set_table_item(row, 5, frec)
            self.set_table_item(row, 6, tec)
            self.set_table_item(row, 7, "Online" if online else "Offline")
            
        self.footer_label.setText(f"Cantidad de clientes: {self.count_client}")



           

    def set_table_item(self, row, column, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        
        if column == 4:
            self.speed = text
        if column == 6:
            self.tecno = text
        self.tecnos={"AC":"1000","AIRFIBER":"1000","M2":"100","M5":"100"}
        icon=QIcon()
        if column==7:
            if text == "Online":
                if self.ssh_switch.StateButton():
                    
                    if self.tecnos[self.tecno] == self.speed:
                        icon = self.create_colored_dot_icon(QColor("#2ecc71"))
                    else:
                        icon = self.create_colored_dot_icon(QColor("#e67e22"))
                else:
                    icon = self.create_colored_dot_icon(QColor("#2ecc71"))
            else:
                icon = self.create_colored_dot_icon(QColor("#e74c3c"))

        if icon:
            item.setIcon(icon)
            
        self.table.setItem(row, column, item)
        


    def event_double(self,row,column):
        selected_row = self.table.currentRow()
    
        
        if column==0 and self.current_device=="Panel" and self.table.item(row,7).text()=="Online":
            
            user_table = UserTable(self.table.item(row,0).text(),self.table.item(row, 1).text(),self.table.item(row, 6).text(),self.current_paneles,self)
            user_table.exec()
            
            
           
        elif column == 1:
            data = self.table.item(row, column).text()
            url = f"http://{data}:83"
            webbrowser.open(url)
        

    def edit_selected_row(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return
        else:
            auth=AuthDialog(self)
        
            if auth.exec_() == QDialog.Accepted:
            

                data = [
                    self.table.item(selected_row, col).text() if self.table.item(selected_row, col) is not None else "" 
                    for col in range(self.table.columnCount())
                ]

                edit_dialog = EditWindow(self)
                edit_dialog.set_data(data)
                
                if edit_dialog.exec_() == QDialog.Accepted:
                    new_data = edit_dialog.get_data()
                    request=update_device(new_data[1],new_data[0],new_data[5],new_data[6],self.current_device)
                    if request:
                        DialogSuccess(self,"Se Actualizó Correctamente!!!").exec()
                        
                        for col in range(len(new_data)):
                            self.set_table_item(selected_row, col, new_data[col])

                    else:
                        DialogError(self,"No Se Pudo Actualizar!!!").exec()

        
    
    def borrar_device(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return
        else:
            auth=AuthDialog(self)
            
            if auth.exec_() == QDialog.Accepted:
                
                data = [
                    self.table.item(selected_row, col).text() if self.table.item(selected_row, col) is not None else "" 
                    for col in range(self.table.columnCount())
                 ]

                dialog = DeletePanelDialog(self)
                dialog.set_data(data)
                
                if dialog.exec():
                    
                    request=delete_device(data[0],self.current_device)
                    

                    if request:
                        self.table.removeRow(selected_row)
                        DialogSuccess(self,"Se Eliminó Correctamente el Dispositivo").exec()
                    else:
                        DialogError(self,"No Se Pudo Eliminar el Dispositivo").exec()
                else:
                    DialogError(self,"Se Canceló la Operación!!!").exec()
                


    def new_enlace(self):
        window = NewPanelWindows(self)
    
        if window.exec() == QDialog.Accepted:
            data = window.get_data()
            
            if data:
                
                request=create_device(data[0],data[1],data[2],data[3],data[4],"Enlace")

                if request:

                    DialogSuccess(self,"Se Ha Creado el Dispositivo Con Éxito!!!").exec()
                else:
                     DialogError(self, "Surgió un Problema al Tratar de Crear el Dispositivo").exec()
    
    
    def new_panel(self):
        window = NewPanelWindows(self)
    
        if window.exec() == QDialog.Accepted:
            data = window.get_data()
            
            if data:
                
                request=create_device(data[0],data[1],data[2],data[3],data[4],"Panel")

                if request:

                    DialogSuccess(self,"Se Ha Creado el Dispositivo Con Éxito!!!").exec()
                else:
                   DialogError(self, "Surgió un Problema al Tratar de Crear el Dispositivo").exec()
                
                    






    def create_backup(self):
        selected_row = self.table.currentRow()
        conn=ComunicationSSH()
        if selected_row < 0:
                return

        data = [
                self.table.item(selected_row, col).text() if self.table.item(selected_row, col) is not None else "" 
                for col in range(self.table.columnCount())
            ]
        request = conn.backup(data[0],data[1],data[6])
       
        if request:

            DialogSuccess(self,"Se Realizó el Backup con exito.").exec()
        else:
            DialogError(self,"No Se pudo realizar el Backup.").exec()


    def reboot(self):
        selected_row = self.table.currentRow()
        conn=ComunicationSSH()
        if selected_row < 0:
                return
        if self.current_device == "Panel":
            data = [
                    self.table.item(selected_row, col).text() if self.table.item(selected_row, col) is not None else "" 
                    for col in range(self.table.columnCount())
                ]
            request = conn.reboot(data[1],data[6])
        else:
            if selected_row%2==0:
                request = conn.reboot(self.table.item(selected_row,1),self.table.item(selected_row,6))
                request = conn.reboot(self.table.item(selected_row+1,1),self.table.item(selected_row+1,6))
            else:
                request = conn.reboot(self.table.item(selected_row-1,1),self.table.item(selected_row-1,6))
                request = conn.reboot(self.table.item(selected_row,1),self.table.item(selected_row,6))
       
        if request and self.current_device=="Panel":

            DialogSuccess(self, "Se Realizó el Reinicio con Éxito.").exec()
        elif request and self.current_device=="Enalce":
            DialogSuccess(self, "Se Realizó el Reinicio del Enlace Completo con Éxito.").exec()
        else:
            DialogError(self, "No Se pudo realizar el Reinicio.").exec()
            
    
    def reset_buttons(self):
        
        def obtener_icono(estado):
                """ Devuelve un icono basado en el estado. """
                return self.create_colored_dot_icon(QColor(estado))
            
        for boton in self.botones:
                    
            boton.setIcon(obtener_icono("transparent"))
            continue
            
    
    
    def update_buttons(self):
         
        def obtener_icono(estado):
                """ Devuelve un icono basado en el estado. """
                return self.create_colored_dot_icon(QColor(estado))      
        while True:
            
            if self.hora_inicio >= datetime.datetime.now().time() or datetime.datetime.now().time() >= self.hora_fin:
                
                if datetime.datetime.now().time() < self.hora_inicio:
                    tiempo_restante = datetime.datetime.combine(datetime.date.today(), self.hora_inicio) - datetime.datetime.combine(datetime.date.today(), datetime.datetime.now().time())
                    self.reset_buttons()
                    sleep(tiempo_restante.total_seconds())
                else:
                    
                    tiempo_restante = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), self.hora_inicio) - datetime.datetime.combine(datetime.date.today(), datetime.datetime.now().time())
                    self.reset_buttons()
                    sleep(tiempo_restante.total_seconds())
                    
            
            for boton in self.botones:
                    
                if boton.text()!="Enlaces":
                        devices = get_paneles(boton.text())
                else:
                        devices = get_enlaces()
                    
                ips = [device.ip for device in devices]
                
                online_status = is_device_online(ips)
                    
                test_false= not all(online_status.values())
               
                if test_false:
                    boton.setIcon(obtener_icono("#e74c3c"))
                    
                    
                else:
                    boton.setIcon(obtener_icono("#2ecc71"))
                    
            sleep(900)
        
        
        
        