from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QComboBox, QPushButton, QSpacerItem, QSizePolicy,QStyledItemDelegate
)
from PySide6.QtCore import Qt

class CenteredComboBoxDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(CenteredComboBoxDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter





class SecondaryWindow(QDialog):
    def __init__(self, username, ip_address, panel_names, connected_panel, parent=None):
        super(SecondaryWindow, self).__init__(parent)

        # Configuración de la ventana
        self.setWindowTitle("Configuración del Cliente")
        self.setFixedSize(400, 600)
        self.setContentsMargins(0,20,0,20)
        # Layout principal
        layout = QVBoxLayout()

        # Campo de nombre de usuario (etiqueta y QLineEdit en un layout horizontal)
        username_layout = QVBoxLayout()
        self.username_label = QLabel("Nombre de Usuario:")
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username_edit = QLineEdit(username)
        self.username_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_edit)
        layout.addLayout(username_layout)

        # Añadir un espaciador entre conjuntos
        layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Campo de IP (etiqueta y QLineEdit en un layout horizontal)
        ip_layout = QVBoxLayout()
        self.ip_label = QLabel("IP Address:")
        self.ip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ip_edit = QLineEdit(ip_address)
        self.ip_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ip_edit.setReadOnly(True)
        ip_layout.addWidget(self.ip_label)
        ip_layout.addWidget(self.ip_edit)
        layout.addLayout(ip_layout)

        # Añadir un espaciador entre conjuntos
        layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # ComboBox para la lista de nombres de paneles
        panel_layout = QVBoxLayout()
        self.panel_label = QLabel("Seleccionar Panel:")
        self.panel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.panel_combo = QComboBox()
        
        self.panel_combo.setFixedHeight(50)
        delegate = CenteredComboBoxDelegate(self.panel_combo)
        self.panel_combo.setItemDelegate(delegate)
        self.panel_combo.addItems(panel_names)

        # Establecer el panel conectado como el seleccionado por defecto
        if connected_panel in panel_names:
            self.panel_combo.setCurrentText(connected_panel)

        panel_layout.addWidget(self.panel_label)
        panel_layout.addWidget(self.panel_combo)
        layout.addLayout(panel_layout)

        # Añadir un espaciador grande antes de los botones
        layout.addSpacerItem(QSpacerItem(0, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botones Aceptar y Cancelar
        button_layout = QHBoxLayout()
        self.accept_button = QPushButton("Cambiar")
        self.accept_button.setStyleSheet("""
                                QPushButton {
                                    background-color: '#28b463';
                                    color: black;
                                    border: 2px solid #196f3d;
                                }
                                QPushButton:hover {
                                    background-color: '#1d8348';
                                    color: white;
                                }
                            """)
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setStyleSheet("""
                                QPushButton {
                                    background-color: '#e74c3c';
                                    color: black;
                                    border: 2px solid #943126;
                                }
                                QPushButton:hover {
                                    background-color: '#cb4335';
                                    color: white;
                                }
                            """)
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # Conectar botones a funciones
        self.accept_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)




    def get_new_info(self):
        return {'user_panel':self.username_edit.text(),'new_panel':self.panel_combo.currentText()}

    