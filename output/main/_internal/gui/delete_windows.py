import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6 import QtCore
from PySide6.QtGui import QFont

class DeletePanelDialog(QDialog):
    def __init__(self, parent=None):
        super(DeletePanelDialog, self).__init__(parent)
        self.setFixedSize(500, 400)
        


    def set_data(self,panel):
        self.panel=panel
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Confirmar Eliminación")

        layout = QVBoxLayout()
        
        layout.setContentsMargins(10, 10, 10, 10)  # Establecer márgenes
        layout.setSpacing(20) 
        # Mostrar la información del panel
        info_label = QLabel(f"Está a punto de eliminar el panel:\n\nNombre: {self.panel[0]}\nIP: {self.panel[1]}\n\nEscriba 'sudo_delete' para continuar.",alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(info_label)

        # Campo de entrada para la frase de confirmación
        self.confirm_input = QLineEdit(self)
        layout.addWidget(self.confirm_input)

        # Botones de aceptar y cancelar
        self.accept_button = QPushButton("Eliminar", self)
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
        self.accept_button.clicked.connect(self.accept)
        layout.addWidget(self.accept_button)

        self.cancel_button = QPushButton("Cancelar", self)
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
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def accept(self):
        if self.confirm_input.text() == "sudo_delete":
            super().accept()
        else:
            QMessageBox.warning(self, "Error", "La frase de confirmación es incorrecta.")

    def exec(self):
        result = super().exec()
        return result == QDialog.Accepted