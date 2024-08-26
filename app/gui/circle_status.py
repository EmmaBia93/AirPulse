from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QSize

class StatusCircle(QWidget):
  
    def __init__(self, color=None, parent=None):
            super().__init__(parent)
            self.color = color if color else "transparent"  # Inicialmente sin color
            self.setFixedSize(QSize(30, 30))

    def paintEvent(self, event):
            painter = QPainter(self)
            painter.setBrush(QColor(self.color))
            painter.setPen(QColor(self.color))
            painter.drawEllipse(0, 0, 30, 30)