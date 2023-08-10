""" Represents the entire Scheduler window including the button functionality and graphics scene """

import os
import numpy as np

from BlockSegment import BlockSegment
from GraphicsScene import GraphicsScene

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPen, QColor
from PyQt6.QtWidgets import (
    QComboBox,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,

)       

class Window(QWidget):

    schedule = []
    blockSize = 24
    blockType = "Regular"
    blockTimes = {
        "Regular" : 1,
        "Laser" : 1.25,
        "Premium" : 1.5,
    }
    blockColors = {
        "Regular" : Qt.GlobalColor.red,
        "Laser" : Qt.GlobalColor.cyan,
        "Premium" : Qt.GlobalColor.green,
    }
    firstEmptyBlock = 0

    def __init__(self, saved=None, baseDir=""):
        super().__init__()

        # Defining scene and adding basic layout elements to scene
        self.baseDir = baseDir
        numHours = 8
        startHour = 7
        startMinute = 30
        AMPMTag = "AM"
        numBlocks = 4 * numHours + 1

            # Defining a scene rect of 400x200, with it's origin at 0,0.
        self.setWindowTitle("Scheduler")
        self.scene = GraphicsScene(0, 0, 260, self.blockSize * numBlocks)
        


            # Add time slots & corresponding boxes to graphics scene
        for i in range(0,numBlocks):
            if startHour < 10:
                textHour = "0" + str(startHour)
            else:
                textHour = str(startHour)
            
            if startMinute == 0:
                textMinute = "00"
            else:
                textMinute = str(startMinute)
            
            textItem = self.scene.addText( textHour + ":" + textMinute + " " + AMPMTag)
            textItem.setPos(0, self.blockSize * i)

            timeBox = QGraphicsRectItem(0, 0, 80, self.blockSize)
            timeBox.setBrush(QColor(255, 0, 0, 0))
            timeBox.setPen(QPen(Qt.GlobalColor.black))
            timeBox.setPos(0, self.blockSize * i)
            self.scene.addItem(timeBox)
            for j in range(4):
                blockSegBox = QGraphicsRectItem(0, 0, 180, (self.blockSize / 4))
                blockSegBox.setPos(80, (self.blockSize * i) + ((self.blockSize / 4) * j))
                blockSegBox.setBrush(QColor(255, 0, 0, 0))
                blockSegBox.setPen(QPen(Qt.GlobalColor.gray))
                blockSegBox.setData(0, i * 4 + j)   # Set 0 to be the id of block segment
                blockSegBox.setData(1, 0)           # Set 1 to represent full-ness (0 empty, 1 occupied)
                self.scene.addItem(blockSegBox)
                self.scene.schedule.append(BlockSegment(i * 4 + j, (self.blockSize * i) + ((self.blockSize / 4) * j)))
            blockBox = QGraphicsRectItem(80, self.blockSize * i, 180, self.blockSize)
            blockBox.setBrush(QColor(255, 0, 0, 0))
            blockBox.setPen(QPen(Qt.GlobalColor.black))
            self.scene.addItem(blockBox)
            

            startMinute += 15
            if startMinute >= 60:
                startMinute = 0
                startHour += 1
                if startHour >= 13:
                    startHour = 1
                elif startHour == 12:
                    if AMPMTag == "AM":
                        AMPMTag = "PM"
                    else:
                        AMPMTag = "AM"


        # Add breaktime
        breakBlockLength = 2
        breakStart = 4 * 19
        breakBlock = QGraphicsRectItem(0, 0, 100, self.blockSize * breakBlockLength)
        breakBlock.setBrush(QBrush(Qt.GlobalColor.yellow))
        breakBlock.setPen(QPen(Qt.GlobalColor.black))
        breakBlock.setPos(80, self.blockSize * 19)
        breakBlock.setData(0, breakStart)                                     # id of first block segment that break occupies
        breakBlock.setData(1, self.blockSize * breakBlockLength)     # number of segments that break occupies
        self.scene.addItem(breakBlock)
        try:
            for i in range(4 * breakBlockLength):
                self.scene.schedule[breakStart + i].isFull = True
                self.scene.schedule[breakStart + i].isBreak = True
        except:
            print("There was an issue")

        skipCount = 0
        for savedBlock in saved:
            if int(savedBlock) == 0:
                skipCount += 1
            else:
                self.insertSaved(int(savedBlock), skipCount)
                if int(savedBlock) == 1:
                    skipCount += 4
                elif int(savedBlock) == 2:
                    skipCount += 5
                elif int(savedBlock) == 3:
                    skipCount += 6



        # Define our layout & add functionality buttons
        vbox = QVBoxLayout()

        insert = QPushButton("Insert")
        insert.clicked.connect(self.insert)
        vbox.addWidget(insert)

        setBlock = QComboBox()
        setBlock.addItems(["Regular", "Laser", "Premium"])
        setBlock.currentTextChanged.connect( self.text_changed )
        vbox.addWidget(setBlock)

        delete = QPushButton("Delete")
        delete.clicked.connect(self.delete)
        vbox.addWidget(delete)

        clear = QPushButton("Clear")
        clear.clicked.connect(self.clear)
        vbox.addWidget(clear)

        save = QPushButton("Save")
        save.clicked.connect(self.save)
        vbox.addWidget(save)

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        hbox = QHBoxLayout(self)
        hbox.addLayout(vbox)
        hbox.addWidget(self.view)

        self.setLayout(hbox)
    
            
    def delete(self):
        """ Delete currently selected blocks """

        for item in self.scene.selectedItems():
            if item.data(0) is not None and item.data(1) is not None:
                for cItem in item.collidingItems():
                    if (cItem.data(0) is not None and
                        item.data(0) == cItem.data(0)):
                        for i in range(item.data(1)):
                            self.scene.schedule[item.data(0) + i].isFull = False
            self.scene.removeItem(item)

    def clear(self):
        """ Clear all blocks in schedule """

        for item in self.scene.items():
            if item.data(2) is not None:
                self.scene.removeItem(item)
        
        for block in self.scene.schedule:
            try:
                if block.isBreak != True:
                    block.isFull = False
            except:
                break

    def save(self):
        """ Save current schedule to SavedSchedule.txt (does not include break) """

        try:
            with open(os.path.join(self.baseDir, "SavedSchedule.txt"), "w") as scheduleFile:
                schedule = np.zeros((len(self.scene.schedule), 2))
                scheduleStr = ''
                for item in self.scene.items():
                    if item.data(2) is not None:
                        schedule[item.data(0), 0] = item.data(2)
                        for i in range(item.data(1)):
                            schedule[item.data(0) + i, 1] = 1

                for segment in schedule:
                    if segment[0] == 0 and segment[1] != 1:
                        scheduleStr += "0\n"
                    elif segment[0] != 0:
                        scheduleStr += (str(int(segment[0])) + "\n")

                scheduleFile.write(scheduleStr)
                print("Saved schedule")
        except:
            print("Could not save schedule")
    
    def insertSaved(self, inputType = -1, skip = 0):
        """" Insert a new schedule block for saved schedule"""
        
        if inputType == 0:
            return
        elif inputType == 1:
            blockType = "Regular"
        elif inputType == 2:
            blockType = "Laser"
        elif inputType == 3:
            blockType = "Premium"
        else:
            blockType = self.blockType
        # Find first empty block in scene that can accommodate new insertion
        firstEmpty = -1
        firstY = -1
        numSkips = skip
        for block in self.scene.schedule:
            if numSkips > 0:
                numSkips -= 1
            else:
                try: #this can be optimized to not recheck block segments
                    if block.isFull == False:
                        isColliding = False
                        for i in range(1, int(self.blockTimes[blockType] * 4)):
                            if self.scene.schedule[block.order + i].isFull == True:
                                isColliding = True
                                break
                        
                        if not isColliding:
                            firstEmpty = block.order
                            firstY = block.y
                            break
                except:
                    break

        if firstEmpty != -1:

            # Draw a rectangle item, setting the dimensions and location corresponding to empty block.
            rect = QGraphicsRectItem(0, 0, 100, self.blockSize * self.blockTimes[blockType])
            rect.setBrush(QBrush(self.blockColors[blockType]))
            rect.setPos(80, firstY)
            rect.setData(0, firstEmpty)                                     # id of first block segment that rect occupies
            rect.setData(1, int(self.blockTimes[blockType] * 4))     # number of segments that rect occupies
            rect.setData(2, int(self.blockTimes[blockType] * 4) - 3)   # identifier for graphics to tell that this is a rect

            # Define the pen (line)
            pen = QPen(Qt.GlobalColor.black)
            rect.setPen(pen)
            self.scene.addItem(rect)
            try:
                for i in range(int(self.blockTimes[blockType] * 4)):
                    self.scene.schedule[firstEmpty + i].isFull = True
                
            except:
                print("There was an issue")
            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
    

    def insert(self):
        """" Insert a new schedule block """
        
        blockType = self.blockType
        # Find first empty block in scene that can accommodate new insertion
        firstEmpty = -1
        firstY = -1

        for block in self.scene.schedule:
            
            try: #this can be optimized to not recheck block segments
                if block.isFull == False:
                    isColliding = False
                    for i in range(1, int(self.blockTimes[blockType] * 4)):
                        if self.scene.schedule[block.order + i].isFull == True:
                            isColliding = True
                            break
                    
                    if not isColliding:
                        firstEmpty = block.order
                        firstY = block.y
                        break
            except:
                break

        if firstEmpty != -1:

            # Draw a rectangle item, setting the dimensions and location corresponding to empty block.
            rect = QGraphicsRectItem(0, 0, 100, self.blockSize * self.blockTimes[blockType])
            rect.setBrush(QBrush(self.blockColors[blockType]))
            rect.setPos(80, firstY)
            rect.setData(0, firstEmpty)                                     # id of first block segment that rect occupies
            rect.setData(1, int(self.blockTimes[blockType] * 4))     # number of segments that rect occupies
            rect.setData(2, int(self.blockTimes[blockType] * 4) - 3)   # identifier for graphics to tell that this is a rect

            # Define the pen (line)
            pen = QPen(Qt.GlobalColor.black)
            rect.setPen(pen)
            self.scene.addItem(rect)
            try:
                for i in range(int(self.blockTimes[blockType] * 4)):
                    self.scene.schedule[firstEmpty + i].isFull = True
                
            except:
                print("There was an issue")
            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        

    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        self.blockType = s
        print(self.blockType)
