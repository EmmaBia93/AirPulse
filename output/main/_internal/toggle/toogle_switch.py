from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Toggle(QCheckBox):

    def __init__(self,
                 width=60,
                 bg_color="#28B463",
                 circle_color="#1a1a1a",
                 active_color="#f42f1b",
                 active_circle_color="#DDD",  # Nuevo color para el círculo cuando está activo
                 animation_curve=QEasingCurve.OutBounce
                 ):
        QCheckBox.__init__(self)

        self.setFixedSize(width, 28)
        self.setCursor(Qt.PointingHandCursor)

        self._bg_color = QColor(bg_color)
        self._circle_color = QColor(circle_color)
        self._active_color = QColor(active_color)
        self._active_circle_color = QColor(active_circle_color)
        self._current_color = self._bg_color
        self._current_circle_color = self._circle_color

        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)

        self.color_animation = QPropertyAnimation(self, b"color", self)
        self.color_animation.setEasingCurve(QEasingCurve.Linear)
        self.color_animation.setDuration(500)

        self.circle_color_animation = QPropertyAnimation(self, b"circle_color", self)
        self.circle_color_animation.setEasingCurve(QEasingCurve.Linear)
        self.circle_color_animation.setDuration(500)

        self.stateChanged.connect(self.start_transition)

    @Property(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    @Property(QColor)
    def color(self):
        return self._current_color

    @color.setter
    def color(self, c):
        self._current_color = c
        self.update()

    @Property(QColor)
    def circle_color(self):
        return self._current_circle_color

    @circle_color.setter
    def circle_color(self, c):
        self._current_circle_color = c
        self.update()

    def start_transition(self, value):
        self.animation.stop()
        self.color_animation.stop()
        self.circle_color_animation.stop()

        if value:
            self.animation.setEndValue(self.width() - 26)
            self.color_animation.setStartValue(self._bg_color)
            self.color_animation.setEndValue(self._active_color)
            self.circle_color_animation.setStartValue(self._circle_color)
            self.circle_color_animation.setEndValue(self._active_circle_color)
        else:
            self.animation.setEndValue(3)
            self.color_animation.setStartValue(self._active_color)
            self.color_animation.setEndValue(self._bg_color)
            self.circle_color_animation.setStartValue(self._active_circle_color)
            self.circle_color_animation.setEndValue(self._circle_color)

        self.animation.start()
        self.color_animation.start()
        self.circle_color_animation.start()

    def StateButton(self):
        return self.isChecked()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())

        # Dibujar el fondo del toggle con el color interpolado
        p.setBrush(self._current_color)
        p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

        # Dibujar el círculo del toggle con el color interpolado
        p.setBrush(self._current_circle_color)
        p.drawEllipse(self._circle_position, 3, 22, 22)

        p.end()
