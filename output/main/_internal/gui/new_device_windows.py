from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout)
from PySide6.QtCore import Qt,QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

class NewPanelWindows(QDialog):
    def __init__(self, parent=None):
        super(NewPanelWindows, self).__init__(parent)
        self.setWindowTitle("Crear Nuevo Dispositivo")
        self.setFixedSize(500, 600)

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 30, 20, 20)  # Establecer márgenes
        self.layout.setSpacing(20)  # Espaciado entre elementos

        # Formulario
        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(10, 10, 10, 10)  # Establecer márgenes
        self.form_layout.setSpacing(20)  # Espaciado entre elementos

        self.name_edit = QLineEdit()
        self.name_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_edit.setFixedHeight(50)

        self.ip_edit = QLineEdit()
        self.ip_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ip_edit.setFixedHeight(50)

        self.localidad_combo = QComboBox()
        self.localidad_combo.setFixedHeight(50)

        self.frecuencia = QLineEdit()
        self.frecuencia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.frecuencia.setFixedHeight(50)

        self.tecnologia_combo = QComboBox()
        self.tecnologia_combo.setFixedHeight(50)
        
        
       
        # Agregar items a los combobox
        localidades = ["Media Agua", "Los Berros", "Colonia", "Cochagual", "Cañada", "Tres Esquinas", "Carpinteria"]
        tecnologias = ["AIRFIBER","AC", "M5", "M2"]
        self.localidad_combo.addItems(localidades)
        self.tecnologia_combo.addItems(tecnologias)


        ip_regex = QRegularExpression(r"^10\.(10[3-9]|110)\.\d{1,3}\.\d{1,3}$")
        ip_validator = QRegularExpressionValidator(ip_regex, self.ip_edit)
        self.ip_edit.setValidator(ip_validator)

        
        frec_regex = QRegularExpression(r'^(?:[2-5]\d{3}|6000)$')
        frec_validator = QRegularExpressionValidator(frec_regex,self.frecuencia)
        self.frecuencia.setValidator(frec_validator)
        # Agregar widgets al formulario
        self.form_layout.addRow("Nombre:", self.name_edit)
        self.form_layout.addRow("IP:", self.ip_edit)
        self.form_layout.addRow("Localidad:", self.localidad_combo)
        self.form_layout.addRow("Frecuencia:",self.frecuencia)
        self.form_layout.addRow("Tecnologia:", self.tecnologia_combo)

        self.layout.addLayout(self.form_layout)

        # Botones
        self.button_layout = QHBoxLayout()
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
        self.load_button = QPushButton("Cargar")
        self.load_button.setStyleSheet("""
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
        # Conectar botones a funciones
        self.cancel_button.clicked.connect(self.cancel)
        self.load_button.clicked.connect(self.load)

        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.load_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def cancel(self):
        self.reject()

    def load(self):
        data = [
            self.name_edit.text(),
            self.ip_edit.text(),
            self.localidad_combo.currentText(),
            self.frecuencia.text(),
            self.tecnologia_combo.currentText()
        ]
        self.accept()
        self.data = data

    def get_data(self):
        return self.data if hasattr(self, 'data') else None
        
        