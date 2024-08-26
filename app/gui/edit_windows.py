import sys
from PySide6 import QtCore
from PySide6.QtGui import QFont, QRegularExpressionValidator
from PySide6.QtWidgets import QDialog,QLineEdit,QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import QRegularExpression

class EditWindow(QDialog):
    def __init__(self, parent=None):
        super(EditWindow, self).__init__(parent)
        self.setWindowTitle("Editar Dispositivo")
        self.setFixedSize(400, 600)
        self.data=[]
        layout = QVBoxLayout(self)
        
        layout.setSpacing(20) 
        
        # Campos de edición
        height=40
        self.name_edit = QLineEdit()
        self.name_edit.setFixedHeight(height)
        self.name_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ip_edit = QLineEdit()
        self.ip_edit.setFixedHeight(height)
        self.ip_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.freq_edit = QLineEdit()
        self.freq_edit.setFixedHeight(height)
        self.freq_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tecno_edit = QLineEdit()
        self.tecno_edit.setFixedHeight(height)
        self.tecno_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        ip_regex = QRegularExpression(r"^10\.(10[3-9]|110)\.\d{1,3}\.\d{1,3}$")
        ip_validator = QRegularExpressionValidator(ip_regex, self.ip_edit)
        self.ip_edit.setValidator(ip_validator)

        frec_regex = QRegularExpression(r'^(?:[2-5]\d{3}|6000)$')
        frec_validator = QRegularExpressionValidator(frec_regex,self.freq_edit)
        self.freq_edit.setValidator(frec_validator)

        layout.addWidget(QLabel("Nombre:",alignment=QtCore.Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("IP:",alignment=QtCore.Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.ip_edit)
        layout.addWidget(QLabel("Frecuencia:",alignment=QtCore.Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.freq_edit)

        layout.addWidget(QLabel("Tecnologia:",alignment=QtCore.Qt.AlignmentFlag.AlignCenter))
        layout.addWidget(self.tecno_edit)
        

        # Botones
        self.save_button = QPushButton("Aceptar")
        self.save_button.setStyleSheet("""
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
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def set_data(self, data):
        self.data=data
        self.name_edit.setText(data[0])
        self.ip_edit.setText(data[1])
        self.freq_edit.setText(data[5])
        self.tecno_edit.setText(data[6])
      

    def get_data(self):
        return [
            self.name_edit.text(),
            self.ip_edit.text(),
            self.data[2],
            self.data[3],
            self.data[4],
            self.freq_edit.text(),
            self.tecno_edit.text(),
       
        ]
