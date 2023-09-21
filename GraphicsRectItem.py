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

    def __init__(self, x, y, width, blockSize, height, time, name, blockType):
        blockHeight = blockSize * height
        super().__init__(x, y, width, blockHeight)

        timeFontSize = 10
        nameFontSize = 13
        if blockType == "Break":
            rectText = QGraphicsTextItem("Break", self)
        else:
            rectText = QGraphicsTextItem(name, self)
        rectText.setData(3, 1)              # identifier for graphics to tell that this is block text

        timeRect = QGraphicsRectItem(100, 0, 40, blockHeight, self)
        timeRect.setBrush(QColor(255, 255, 255, 255))
        timeRect.setPen(QPen(Qt.GlobalColor.black))

        timeRectText = QGraphicsTextItem(time, self)
        timeRectText.setX(100)
        timeRectText.setTextWidth(50)
        timeRectText.setData(3, 2)              # identifier for graphics to tell that this is block time text

        if blockType == "Custom":
            if blockHeight == 3:
                timeFontSize = 8
                timeRectText.setY(-2)
            elif blockType == 2:
                timeFontSize = 6
                nameFontSize = 10
                rectText.setY(-2)
                timeRectText.setX(98)
            elif blockType == 1:
                timeFontSize = 4
                nameFontSize = 5
                rectText.setY(-3)
                timeRectText.setY(-2)
        rectText.setFont(QFont("Helvetica", nameFontSize))
        timeRectText.setFont(QFont("Helvetica", timeFontSize))


