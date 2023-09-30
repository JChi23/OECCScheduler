""" Object built off of QGraphicsRectItem that represents all procedure blocks created in schedule """
import typing

import ProcedureDicts

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor, QFont
from PyQt6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsItem,
)      

class GraphicsRectItem(QGraphicsRectItem):

    desc = ""
    blockStr = ""

    #def __init__(self, x, y, blockWidth, blockHeight, timeWidth, typeWidth, time, name, blockTypes, blockColor, segLength):
    def __init__(self, x, y, blockWidth, blockHeight, timeWidth, typeWidth, time, name, blockTypes, segLength):
        super().__init__(x, y, blockWidth, blockHeight)
        #self.setBrush(blockColor)
        self.setPen(QPen(Qt.GlobalColor.black))

        timeFontSize = 12
        nameFontSize = 14
        typeFontSize = 11

        # Add name
        if blockTypes[0] == "Break":
            rectText = QGraphicsTextItem("Break", self)
        else:
            if len(name) < 1:
                rectText = QGraphicsTextItem("Patient", self)
            else:
                rectText = QGraphicsTextItem(name, self)
        rectText.setData(3, 1)              # identifier for graphics to tell that this is block text

        # Add type name
        r, g, b = 0, 0, 0
        
        for type in blockTypes:
            self.desc += ProcedureDicts.procedureDesc[type] + " "
            self.blockStr += str(ProcedureDicts.procedureIDs[type]) + "-"
            r += ProcedureDicts.blockColors[type].red()
            g += ProcedureDicts.blockColors[type].green()
            b += ProcedureDicts.blockColors[type].blue()
        r /= len(blockTypes)
        g /= len(blockTypes)
        b /= len(blockTypes)
        self.setBrush(QColor(r, g, b))

        self.desc = self.desc[:-1]
        self.blockStr = self.blockStr[:-1]
        
        typeRect = QGraphicsRectItem(blockWidth, 0, typeWidth, blockHeight, self)
        typeRect.setBrush(QColor(255, 255, 255, 255))
        typeRect.setPen(QPen(Qt.GlobalColor.black))
        #typeRect.setBrush(blockColor)
        typeRect.setBrush(QColor(r, g, b))
        typeRect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        typeRectText = QGraphicsTextItem(self.desc, self)
        typeRectText.setX(blockWidth)
        typeRectText.setTextWidth(typeWidth)
        typeRectText.setData(3, 3)              # identifier for graphics to tell that this is block type text

        # Add time
        timeRect = QGraphicsRectItem(blockWidth + typeWidth, 0, timeWidth, blockHeight, self)
        timeRect.setBrush(QColor(255, 255, 255, 255))
        timeRect.setPen(QPen(Qt.GlobalColor.black))
        timeRect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        timeRectText = QGraphicsTextItem(time, self)
        timeRectText.setX(blockWidth + typeWidth)
        timeRectText.setTextWidth(timeWidth)
        timeRectText.setData(3, 2)              # identifier for graphics to tell that this is block time text

        # Adjust font sizes if needed
        if blockTypes[0] == "Custom":
            if segLength == 3:
                #timeFontSize = 8
                timeRectText.setY(-2)
            elif segLength == 2:
                timeFontSize = 8
                #nameFontSize = 10
                #rectText.setY(-2)
                timeRectText.setX(timeRectText.x() - 2)
                timeRectText.setY(-2)
            elif segLength == 1:
                timeFontSize = 7
                nameFontSize = 9
                typeFontSize = 9
                rectText.setY(-3)
                typeRectText.setY(-3)
                timeRectText.setY(-2)
                timeRectText.setX(timeRectText.x() - 2)
        rectText.setFont(QFont("Helvetica", nameFontSize))
        timeRectText.setFont(QFont("Helvetica", timeFontSize))
        typeRectText.setFont(QFont("Helvetica", typeFontSize))


