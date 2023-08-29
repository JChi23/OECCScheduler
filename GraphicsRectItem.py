import typing

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor, QIcon, QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QGraphicsItemGroup,
    QDoubleSpinBox,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QWidget,

)      


class GraphicsRectItem(QGraphicsRectItem):

    def __init__(self, x, y, width, height, time, name):
        super().__init__(x, y, width, height)

        rectText = QGraphicsTextItem(name, self)
        rectText.setData(3, 1)              # identifier for graphics to tell that this is block text

        timeRect = QGraphicsRectItem(100, 0, 40, height, self)
        timeRect.setBrush(QColor(255, 255, 255, 255))
        timeRect.setPen(QPen(Qt.GlobalColor.black))

        timeRectText = QGraphicsTextItem(time, self)
        timeRectText.setX(100)
        timeRectText.setFont(QFont("Helvetica", 10))
        timeRectText.setTextWidth(50)
        timeRectText.setData(3, 2)              # identifier for graphics to tell that this is block time text


