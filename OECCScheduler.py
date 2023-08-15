""" Represents the entire Scheduler window including the button functionality and graphics scene """

import os
import numpy as np

from BlockSegment import BlockSegment
from GraphicsScene import GraphicsScene
from ScheduleColors import BlockColors

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPen, QColor, QIcon, QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QGraphicsItemGroup,
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

class Window(QWidget):

    schedule = []
    blockSize = 24
    blockType = "Regular"
    blockName = "Patient"
    blockTimes = {
        "Regular" : 1,
        "Laser" : 1.25,
        "Premium" : 1.5,
    }
    blockColors = {
        "Regular" : BlockColors.REGULAR.value,
        "Laser" : BlockColors.LASER.value,
        "Premium" : BlockColors.PREMIUM.value,
    }
    blockEndMinutes = {
        0 : { 0 : "03", 1 : "07", 2 : "11", 3 : "14",},
        15 : { 0 : "18", 1 : "22", 2 : "26", 3 : "39",},
        30 : { 0 : "33", 1 : "37", 2 : "41", 3 : "44",},
        45 : { 0 : "48", 1 : "52", 2 : "56", 3 : "59",},
    }
    blockBeginMinutes = {
        0 : { 0 : "00", 1 : "04", 2 : "08", 3 : "12",},
        15 : { 0 : "15", 1 : "19", 2 : "23", 3 : "27",},
        30 : { 0 : "30", 1 : "34", 2 : "38", 3 : "42",},
        45 : { 0 : "45", 1 : "49", 2 : "53", 3 : "57",},
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
        self.scene = GraphicsScene(0, 0, 260, self.blockSize * numBlocks, self)
        


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
                blockSegBox.setBrush(QColor(0, 0, 0, 0))
                blockSegBox.setPen(QPen(Qt.GlobalColor.gray))
                blockSegBox.setData(0, i * 4 + j)   # Set 0 to be the id of block segment
                blockSegBox.setData(1, 0)           # Set 1 to represent full-ness (0 empty, 1 occupied)
                # blockSegBox.setData(20, textHour)   # Set 20 to represent the hour of the block
                # blockSegBox.setData(21, self.blockMinutes[startMinute][j])  # Set 21 to represent the minutes of the block
                self.scene.addItem(blockSegBox)
                self.scene.schedule.append(BlockSegment(i * 4 + j, (self.blockSize * i) + ((self.blockSize / 4) * j),
                                                        textHour + ":" + self.blockBeginMinutes[startMinute][j],
                                                        textHour + ":" + self.blockEndMinutes[startMinute][j]))
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
        breakBlock.setBrush(QBrush(BlockColors.BREAK.value))
        breakBlock.setPen(QPen(Qt.GlobalColor.black))
        breakBlock.setPos(80, self.blockSize * 19)
        breakBlock.setData(0, breakStart)                                     # id of first block segment that break occupies
        breakBlock.setData(1, 4 * breakBlockLength)     # number of segments that break occupies
        breakText = QGraphicsTextItem("Break", breakBlock)
        breakText.setFont(QFont("Helvetica", 16))
        timeRect = QGraphicsRectItem(100, 0, 40, self.blockSize * breakBlockLength, breakBlock)
        timeRect.setBrush(QColor(255, 255, 255, 255))
        timeRect.setPen(QPen(Qt.GlobalColor.black))

        timeText = "Time"
        try:
            lastBlockIndex = breakStart + int(4 * breakBlockLength) - 1
            timeText = self.scene.schedule[breakStart].beginString + " - " + self.scene.schedule[lastBlockIndex].endString
        except:
            print("There was an issue populating break time")

        timeRectText = QGraphicsTextItem(timeText, breakBlock)
        timeRectText.setX(100)
        timeRectText.setFont(QFont("Helvetica", 10))
        timeRectText.setTextWidth(50)
        timeRectText.setData(3, 2)              # identifier for graphics to tell that this is block time text
        
        self.scene.addItem(breakBlock)
        breakBlock.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        breakBlock.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        
        try:
            for i in range(4 * breakBlockLength):
                self.scene.schedule[breakStart + i].isFull = True
                self.scene.schedule[breakStart + i].isBreak = True
        except:
            print("There was an issue")

        skipCount = 0

        try:
            for savedBlock in saved:
                firstChar = savedBlock[0]
                otherChars = savedBlock[1:]
                if len(otherChars) < 1:
                    otherChars = "Patient"
                if int(firstChar) == 0:
                    skipCount += 1
                else:
                    self.insertSaved(int(firstChar), skipCount, otherChars)
                    if int(firstChar) == 1:
                        skipCount += 4
                    elif int(firstChar) == 2:
                        skipCount += 5
                    elif int(firstChar) == 3:
                        skipCount += 6
                

        except:
            print("Could not insert saved procedures")




        # Define our layout & add functionality buttons
        vbox = QVBoxLayout()

        self.patientName = QLineEdit("Patient Name")
        self.patientName.textChanged.connect(self.name_changed)
        vbox.addWidget(self.patientName)

        self.changeName = QPushButton("Change Name")
        self.changeName.setEnabled(False)
        self.changeName.clicked.connect(self.changePatientName)
        vbox.addWidget(self.changeName)

        insert = QPushButton("Insert Procedure")
        insert.clicked.connect(self.insert)
        vbox.addWidget(insert)

        setBlock = QComboBox()
        setBlock.addItems(["Regular", "Laser", "Premium"])
        setBlock.currentTextChanged.connect(self.text_changed)
        vbox.addWidget(setBlock)

        delete = QPushButton("Delete")
        delete.setIcon(QIcon(os.path.join(self.baseDir, "icons", "lightning.png")))
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
            if item.data(2) is not None:
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
            with open(os.path.join(self.baseDir, "resources", "SavedSchedule.txt"), "w") as scheduleFile:
                schedule = np.zeros((len(self.scene.schedule), 2))
                scheduleNames = [""] * len(self.scene.schedule)
                scheduleStr = ''
                for item in self.scene.items():
                    if item.data(2) is not None:
                        schedule[item.data(0), 0] = item.data(2)
                        for i in range(item.data(1)):
                            schedule[item.data(0) + i, 1] = 1

                        subItems = item.childItems()
                        for subItem in subItems:
                            if subItem.data(3) is not None and subItem.data(3) == 1:
                                scheduleNames[item.data(0)] = subItem.toPlainText()

                for i in range(len(schedule)):
                    if schedule[i][0] == 0 and schedule[i][1] != 1:
                        scheduleStr += "0\n"
                    elif schedule[i][0] != 0:
                        scheduleStr += (str(int(schedule[i][0])) + scheduleNames[i] + "\n")

                scheduleFile.write(scheduleStr)
                print("Saved schedule")
        except:
            print("Could not save schedule")
    
    def insertSaved(self, inputType = -1, skip = 0, name="Patient"):
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
                try: #this can be optimized to not recheck block segments that are filled probably
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
            
            rectText = QGraphicsTextItem(name, rect)
            rectText.setData(3, 1)              # identifier for graphics to tell that this is block text

            timeRect = QGraphicsRectItem(100, 0, 40, self.blockSize * self.blockTimes[blockType], rect)
            timeRect.setBrush(QColor(255, 255, 255, 255))
            timeRect.setPen(QPen(Qt.GlobalColor.black))

            timeText = "Time"
            try:
                lastBlockIndex = firstEmpty + int(self.blockTimes[blockType] * 4) - 1
                timeText = self.scene.schedule[firstEmpty].beginString + " - " + self.scene.schedule[lastBlockIndex].endString
            except:
                print("There was an issue populating times")

            timeRectText = QGraphicsTextItem(timeText, rect)
            timeRectText.setX(100)
            timeRectText.setFont(QFont("Helvetica", 10))
            timeRectText.setTextWidth(50)
            timeRectText.setData(3, 2)              # identifier for graphics to tell that this is block time text
            

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

            rectText = QGraphicsTextItem(self.blockName, rect)
            rectText.setData(3, 1)              # identifier for graphics to tell that this is block text
            # curFontSize = rectText.font().pointSize()
            # print(curFontSize)
            # rectText.setFont(QFont("Helvetica", 10))

            timeRect = QGraphicsRectItem(100, 0, 40, self.blockSize * self.blockTimes[blockType], rect)
            timeRect.setBrush(QColor(255, 255, 255, 255))
            timeRect.setPen(QPen(Qt.GlobalColor.black))

            timeText = "Time"
            try:
                lastBlockIndex = firstEmpty + int(self.blockTimes[blockType] * 4) - 1
                timeText = self.scene.schedule[firstEmpty].beginString + " - " + self.scene.schedule[lastBlockIndex].endString
            except:
                print("There was an issue populating times")

            timeRectText = QGraphicsTextItem(timeText, rect)
            timeRectText.setX(100)
            timeRectText.setFont(QFont("Helvetica", 10))
            timeRectText.setTextWidth(50)
            timeRectText.setData(3, 2)              # identifier for graphics to tell that this is block time text

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
        """ Change the stored procedure type when combobox is updated """
        self.blockType = s

    def name_changed(self, s):
        """ Change the stored patient name when the text box is updated """
        self.blockName = s
    
    def changePatientName(self):
        """ Change the name of the selected block """
        self.scene.changeName(self.blockName)

    def changeInputPatientName(self, name="Patient"):
        """ Change the name of the text input widget """
        self.patientName.setText(name)

    def changeNameChange(self, enable=False):
        """ Change the change name button on widget """
        self.changeName.setEnabled(enable)
