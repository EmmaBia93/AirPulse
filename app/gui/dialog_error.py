import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMainWindow
from PySide6.QtGui import QIcon, QPixmap


class DialogError(QDialog):
    def __init__(self,parent=None,message=None):
        super().__init__(parent)
        self.setWindowTitle("Operación Fallida")
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 10, 30, 20)  # Establecer márgenes
        main_layout.setSpacing(20)
        # Layout horizontal para icono y mensaje
        icon_message_layout = QHBoxLayout()

        # Icono
        icon_label = QLabel()
        pixmap = QPixmap("app\gui\img\error.png")  # Reemplaza con la ruta de tu icono
        icon_label.setPixmap(pixmap.scaled(70, 70))  # Ajusta el tamaño del icono a 32x32 píxeles
        icon_message_layout.addWidget(icon_label)

        # Mensaje
        message_label = QLabel(message)
        icon_message_layout.addWidget(message_label)

        # Añadir el layout de icono y mensaje al layout principal
        main_layout.addLayout(icon_message_layout)

        # Botón Aceptar
        accept_button = QPushButton("Aceptar")
        accept_button.setStyleSheet("""
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
        accept_button.setFixedWidth(150)
        accept_button.clicked.connect(self.on_accept)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(accept_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def on_accept(self):
    
        self.accept()