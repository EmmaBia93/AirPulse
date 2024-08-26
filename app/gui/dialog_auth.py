import os
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from dotenv import load_dotenv

class AuthDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Autenticación de Admin")

        load_dotenv()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 20)  # Establecer márgenes
        layout.setSpacing(20)

        
        # Usuario
        user_layout = QHBoxLayout()
        user_label = QLabel("Usuario:")
        user_label.setAlignment(Qt.AlignRight)
        
        self.user_input = QLineEdit()
        self.user_input.setFixedWidth(300)
        self.user_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
      
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_input)
        layout.addLayout(user_layout)

        # Contraseña
        pass_layout = QHBoxLayout()
        pass_label = QLabel("Contraseña:")
        pass_label.setAlignment(Qt.AlignRight)
        


        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedWidth(300)
        self.pass_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pass_layout.addWidget(pass_label)
        pass_layout.addWidget(self.pass_input)
        layout.addLayout(pass_layout)

        # Botones
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Aceptar")
        self.cancel_button = QPushButton("Cancelar")
        self.ok_button.setMaximumHeight(40)
        self.cancel_button.setMaximumHeight(40)
        self.ok_button.setStyleSheet("""
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
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.ok_button.clicked.connect(self.authenticate)
        self.cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)

    def authenticate(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        # Aquí debes reemplazar con tu lógica de autenticación
        if username == os.getenv("CIUSER") and password == os.getenv("CIPASS"):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")