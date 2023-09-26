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
# THINK ABOUT INCLUDING CREATION OF TIME TEX HERE OR CREATE A SEPARATE METHOD FOR IT

class GraphicsRectItem(QGraphicsRectItem):

    def __init__(self, x, y, blockWidth, blockHeight, timeWidth, typeWidth, time, name, blockType, blockColor, segLength):
        super().__init__(x, y, blockWidth, blockHeight)
        self.setBrush(blockColor)
        self.setPen(QPen(Qt.GlobalColor.black))

        timeFontSize = 10
        nameFontSize = 13
        typeFontSize = 13

        # Add name
        if blockType == "Break":
            rectText = QGraphicsTextItem("Break", self)
        else:
            rectText = QGraphicsTextItem(name, self)
        rectText.setData(3, 1)              # identifier for graphics to tell that this is block text

        # Add type name
        typeRect = QGraphicsRectItem(blockWidth, 0, typeWidth, blockHeight, self)
        typeRect.setBrush(QColor(255, 255, 255, 255))
        typeRect.setPen(QPen(Qt.GlobalColor.black))
        typeRect.setBrush(blockColor)

        typeRectText = QGraphicsTextItem(blockType, self)
        typeRectText.setX(blockWidth)
        typeRectText.setTextWidth(typeWidth)
        typeRectText.setData(3, 3)              # identifier for graphics to tell that this is block type text

        # Add time
        timeRect = QGraphicsRectItem(blockWidth + typeWidth, 0, timeWidth, blockHeight, self)
        timeRect.setBrush(QColor(255, 255, 255, 255))
        timeRect.setPen(QPen(Qt.GlobalColor.black))

        timeRectText = QGraphicsTextItem(time, self)
        timeRectText.setX(blockWidth + typeWidth)
        timeRectText.setTextWidth(timeWidth)
        timeRectText.setData(3, 2)              # identifier for graphics to tell that this is block time text

        # Adjust font sizes if needed
        if blockType == "Custom":
            if segLength == 3:
                timeFontSize = 8
                timeRectText.setY(-2)
            elif segLength == 2:
                timeFontSize = 8
                #nameFontSize = 10
                #rectText.setY(-2)
                timeRectText.setX(timeRectText.x() - 2)
                timeRectText.setY(-2)
            elif segLength == 1:
                timeFontSize = 6
                nameFontSize = 9
                typeFontSize = 9
                rectText.setY(-3)
                typeRectText.setY(-3)
                timeRectText.setY(-2)
        rectText.setFont(QFont("Helvetica", nameFontSize))
        timeRectText.setFont(QFont("Helvetica", timeFontSize))
        typeRectText.setFont(QFont("Helvetica", typeFontSize))


