""" Represents the entire Scheduler window including the button functionality and graphics scene """
""" Data keys used in graphics objects: 
        0 = (segment) block id placement; (procedure) beginning block, 
        1 = (procedure) length of block, 
        2 = (procedure) block procedure identifier, 
        3 = (2-date text, 1-name text) text object identifier, 
        4 = block segment identifier"""

import os
import numpy as np
import openpyxl as op
from datetime import date

from BlockSegment import BlockSegment
from GraphicsScene import GraphicsScene
from GraphicsRectItem import GraphicsRectItem
from ScheduleColors import BlockColors
import ProcedureDicts

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPen, QColor, QIcon, QFont, QPixmap
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
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

class Window(QWidget):

    canvasWidth = 100
    canvasHeight = 100
    schedule = []
    timeBoxWidth = 80
    blockSize = 40
    blockWidth = 100
    timeWidth = 50
    typeWidth = 70
    numSubBlocks = 4
    currentCaseCount = 0
    blockType = "Regular"
    blockName = "Patient"
    blockTimeCustom = 1
    customBlockLength = 1.00
    blockTimes = ProcedureDicts.blockTimes
    blockColors = ProcedureDicts.blockColors
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
    scaleAddition = 0

    def __init__(self, saved=None, baseDir=""):
        super().__init__()

        # Defining scene and adding basic layout elements to scene
        numHours = 11
        numBlocks = self.numSubBlocks * numHours + 1
        startHour = 7
        startMinute = 30
        AMPMTag = "AM"
        segBoxWidth = self.blockWidth + self.timeWidth + self.typeWidth + 40
        topWhiteSpace = 24

        self.baseDir = baseDir
        self.canvasHeight = self.blockSize * numBlocks + topWhiteSpace
        self.canvasWidth = self.timeBoxWidth + segBoxWidth

            # Defining a scene rect, with it's origin at 0,-24 along with background & date time plus case count.
        self.setWindowTitle("Scheduler")
        self.scene = GraphicsScene(0, -1 * topWhiteSpace, self.canvasWidth, self.canvasHeight, self)

        self.scene.addRect(0, -1 * topWhiteSpace, self.canvasWidth, self.canvasHeight, brush = QBrush(Qt.GlobalColor.white))
        
        dateItem = self.scene.addText("Today's date: " + str(date.today()))
        dateItem.setPos(10, -1 * topWhiteSpace)
        self.caseCountItem = self.scene.addText("Cases: " + str(self.currentCaseCount))
        self.caseCountItem.setPos(180, -1 * topWhiteSpace)


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

            timeBox = QGraphicsRectItem(0, 0, self.timeBoxWidth, self.blockSize)
            timeBox.setBrush(QColor(255, 0, 0, 0))
            timeBox.setPen(QPen(Qt.GlobalColor.black))
            timeBox.setPos(0, self.blockSize * i)
            self.scene.addItem(timeBox)
            for j in range(self.numSubBlocks):
                blockSegBox = QGraphicsRectItem(0, 0, segBoxWidth, (self.blockSize / self.numSubBlocks))
                blockSegBox.setPos(80, (self.blockSize * i) + ((self.blockSize / self.numSubBlocks) * j))
                blockSegBox.setBrush(QColor(0, 0, 0, 0))
                blockSegBox.setPen(QPen(Qt.GlobalColor.gray))
                blockSegBox.setData(0, i * self.numSubBlocks + j)   # Set 0 to be the id of block segment
                # blockSegBox.setData(1, 0)           # Set 1 to represent full-ness (0 empty, 1 occupied)
                blockSegBox.setData(4, 0)           # Set 4 to be identifier for a block segment
                # blockSegBox.setData(20, textHour)   # Set 20 to represent the hour of the block
                # blockSegBox.setData(21, self.blockMinutes[startMinute][j])  # Set 21 to represent the minutes of the block
                
                # blockSegBoxText = QGraphicsTextItem(str(i *4 + j), blockSegBox)   #UTILITY NUMBERING OF BOXES
                # blockSegBoxText.setPos(140, -4)
                # blockSegBoxText.setFont(QFont("Helvetica", 6))
                
                self.scene.addItem(blockSegBox)
                self.scene.schedule.append(BlockSegment(i * self.numSubBlocks + j, (self.blockSize * i) + ((self.blockSize / self.numSubBlocks) * j),
                                                        textHour + ":" + self.blockBeginMinutes[startMinute][j],
                                                        textHour + ":" + self.blockEndMinutes[startMinute][j]))
            blockBox = QGraphicsRectItem(80, self.blockSize * i, segBoxWidth, self.blockSize)
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



            # Insert saved data. If no data, insert a break block at 12 pm
                # SAVED DATA FORMAT: (TYPE, NAME ,SEGMENT LENGTH)
        breakFlag = True
        skipCount = 0

        try:
            for savedBlock in saved:
                inputs = savedBlock.split(",")
                
                if int(inputs[0]) == 0:
                    skipCount += 1
                else:
                    breakFlag = False
                    if len(inputs[1]) < 1:
                        inputs[1] = "Patient"
                    self.insertSaved(int(inputs[0]), skipCount, inputs[1], int(inputs[2]))
                    skipCount += int(inputs[2])
                    # if int(inputs[0]) == 1:
                    #     skipCount += 8
                    # elif int(inputs[0]) == 2:
                    #     skipCount += int(inputs[2])
                    # elif int(inputs[0]) == 3:
                    #     skipCount += 4
                    # elif int(inputs[0]) == 4:
                    #     skipCount += 5
                    # elif int(inputs[0]) == 5:
                    #     skipCount += 6
                
        except Exception as e:
            print("Could not insert saved procedures: ", e)

        if breakFlag:
            # Add breaktime if no saved data
            breakBlockLength = 2
            breakStart = 19
            breakBlock = GraphicsRectItem(0, 0, self.blockWidth, self.blockSize * breakBlockLength, self.timeWidth, self.typeWidth,
                                          self.getTimeText(breakStart, breakStart + int(self.numSubBlocks * breakBlockLength) - 1), 
                                          "Break", "Break", QBrush(BlockColors.BREAK.value))
            breakBlock.setPos(self.timeBoxWidth, self.scene.schedule[breakStart].y)
            breakBlock.setData(0, breakStart)                                     # id of first block segment that break occupies
            breakBlock.setData(1, breakBlockLength * self.numSubBlocks)                         # number of segments that break occupies
            breakBlock.setData(2, ProcedureDicts.procedureIDs["Break"])          # identifier that this is a movable block

            # breakBlock = QGraphicsRectItem(0, 0, 100, self.blockSize * breakBlockLength)
            # breakBlock.setBrush(QBrush(BlockColors.BREAK.value))
            # breakBlock.setPen(QPen(Qt.GlobalColor.black))
            # breakBlock.setPos(80, self.blockSize * 19)
            # breakBlock.setData(0, breakStart)                                     # id of first block segment that break occupies
            # breakBlock.setData(1, 4 * breakBlockLength)                         # number of segments that break occupies
            # breakBlock.setData(2, ProcedureDicts.procedureIDs["Break"])                                            # identifier that this is a movable block
            # breakText = QGraphicsTextItem("Break", breakBlock)
            # breakText.setData(3, 1)
            # breakText.setFont(QFont("Helvetica", 16))
            # timeRect = QGraphicsRectItem(100, 0, 40, self.blockSize * breakBlockLength, breakBlock)
            # timeRect.setBrush(QColor(255, 255, 255, 255))
            # timeRect.setPen(QPen(Qt.GlobalColor.black))

            # timeText = "Time"
            # try:
            #     lastBlockIndex = breakStart + int(4 * breakBlockLength) - 1
            #     timeText = self.scene.schedule[breakStart].beginString + " - " + self.scene.schedule[lastBlockIndex].endString
            # except Exception as e:
            #     print("There was an issue populating break time: ", e)

            # timeRectText = QGraphicsTextItem(timeText, breakBlock)
            # timeRectText.setX(100)
            # timeRectText.setFont(QFont("Helvetica", 10))
            # timeRectText.setTextWidth(50)
            # timeRectText.setData(3, 2)              # identifier for graphics to tell that this is block time text
            
            self.scene.addItem(breakBlock)
            self.scene.procedures.append(breakBlock)
            breakBlock.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            breakBlock.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
            self.fill(breakStart, self.numSubBlocks * breakBlockLength)
            
            # try:
            #     for i in range(4 * breakBlockLength):
            #         self.scene.schedule[breakStart + i].isFull = True
            #         self.scene.schedule[breakStart + i].isBreak = True
            # except:
            #     print("There was an issue")


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
        setBlock.addItems(["Custom", "Break", "Regular", "Laser", "Premium", "Trabeculectomy", 
                           "Vivity", "Toric/ORA", "Goniotomy", "Micropulse", "Canaloplasty", "Stent",
                           "Shunt", "PanOptix", "XEN"])
        setBlock.setCurrentIndex(2)
        setBlock.currentTextChanged.connect(self.text_changed)
        vbox.addWidget(setBlock)

        self.customLength = QDoubleSpinBox()
        self.customLength.setMinimum(0.25)
        self.customLength.setValue(1.00)
        self.customLength.setSingleStep(0.25)
        self.customLength.valueChanged.connect(self.changeCustomLength)
        vbox.addWidget(self.customLength)

        delete = QPushButton("Delete")
        #delete.setIcon(QIcon(os.path.join(self.baseDir, "icons", "lightning.png")))
        delete.clicked.connect(self.delete)
        vbox.addWidget(delete)

        clear = QPushButton("Clear")
        clear.clicked.connect(self.clear)
        vbox.addWidget(clear)

        openFile = QPushButton("Open")
        openFile.clicked.connect(self.openFile)
        vbox.addWidget(openFile)

        # UTILITY BUTTON
        reset = QPushButton("Reset")
        reset.clicked.connect(self.darkenFull)
        vbox.addWidget(reset)

        squish = QPushButton("Collapse")
        squish.clicked.connect(self.squish)
        vbox.addWidget(squish)

        save = QPushButton("Save")
        save.clicked.connect(self.save)
        vbox.addWidget(save)

        download = QPushButton("Download")
        download.clicked.connect(self.download)
        vbox.addWidget(download)

        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        hbox = QHBoxLayout(self)
        hbox.addLayout(vbox)
        hbox.addWidget(self.view)

        self.setLayout(hbox)

        self.darkenFull()
    

    # FUNCTIONS BELOW

            
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
                self.scene.procedures.remove(item)
                if (item.data(2) != 1):
                    self.currentCaseCount -= 1
                    self.caseCountItem.setPlainText("Cases: " + str(self.currentCaseCount))

        self.darkenFull()

    def clear(self):
        """ Clear all blocks in schedule """

        self.currentCaseCount = 0
        self.caseCountItem.setPlainText("Cases: " + str(self.currentCaseCount))
        self.scene.procedures.clear()

        for item in self.scene.items():
            if item.data(2) is not None:
                self.scene.removeItem(item)
        
        for block in self.scene.schedule:
            block.isFull = False

        self.darkenFull()

    def createTimeText(self, firstEmpty, blockType):
        timeText = "Time"
        try:
            lastBlockIndex = firstEmpty + int(self.blockTimes[blockType] * 4) - 1
            timeText = self.scene.schedule[firstEmpty].beginString + " - " + self.scene.schedule[lastBlockIndex].endString
        except:
            print("There was an issue populating times")
        return timeText

    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', self.baseDir)
        if fname[0]:
            print(fname[0])
            self.clear()

            # Define variable to load the dataframe
            dataframe = op.load_workbook(fname[0], data_only=True)
            
            # Define variable to read sheet
            dataframe1 = dataframe.active

            softMaxCol = min(12, dataframe1.max_column)
            softMaxRow = min(50, dataframe1.max_row)
            
            colTime = 0
            colFirstName = 0
            colLastName = 0
            colIOL = 0
            colProcedure = 0
            rowFirst = -1
            rowCount = 1
            #TODO: Add more robustness for detecting name & procedure
            # Find column indices for desired data
            for row in dataframe1.iter_rows(min_row=1, max_col=4, max_row=30):
                for cell in row:
                    if cell.value is not None:
                        val = cell.value.lower()
                        if "time" in val:
                            rowFirst = rowCount + 1
                            break
                if rowFirst != -1:
                    break
                else:
                    rowCount += 1
            
            for row in dataframe1.iter_rows(rowCount, rowCount):
                count = 0
                for cell in row:
                    if cell.value is not None:
                        val = cell.value.lower()
                        
                        if "first" in val:
                            colFirstName = count
                        elif "last" in val:
                            colLastName = count
                        elif "primary iol" in val:
                            colIOL = count
                        elif "special notes" in val:
                            colProcedure = count
                    count += 1
       
            try:
                # Iterate through rows and add procedures to schedule

                for row in dataframe1.iter_rows(rowFirst, softMaxRow):
                    if  row[colFirstName].value is None and row[colLastName].value is None and row[colIOL].value is None:
                        break
          
                    else:
                        firstEmpty = -1
                        firstY = -1
                        blockType = "Regular"
                        customLength = 1

                        if row[colIOL].value is not None and "Surgeon Break" in row[colIOL].value:
                            blockType = "Break"
                            name = "Break"
                        else:
                            name = row[colFirstName].value[0] + ". " + row[colLastName].value
                            procedure = row[colProcedure].value.lower()
                            
                            # check for block type and add it

                            if ("shunt" in procedure):
                                blockType = "Shunt"
                            elif ("xen" in procedure or "trabeculectomy" in procedure):
                                blockType = "Trabeculectomy"
                            elif ("vivity" in procedure or "panoptix" in procedure or
                                "toric" in procedure):
                                blockType = "Premium"
                            elif ("lasik" in procedure or "goniotomy" in procedure or "goniosynechialysis" in procedure or
                                "femto" in procedure or "lensx" in procedure or "/ora" in procedure or "micropulse" in procedure or
                                "canaloplasty" in procedure or "stent" in procedure):
                                blockType = "Laser"
                            elif "phaco" in procedure or "trimox" in procedure:
                                blockType = "Regular"
                            else:
                                blockType = "Custom"

                        if blockType != "Custom":
                            segLength = int(self.blockTimes[blockType] * self.numSubBlocks)
                            length = self.blockTimes[blockType]
                        else:
                            segLength = int(customLength * self.numSubBlocks)
                            length = customLength
                        
                        firstEmpty, firstY = self.findFirstEmpty(segLength)
                        print(name, firstEmpty, segLength, blockType)
                        if (firstEmpty == -1):
                            continue
                        # for i in range(len(self.scene.schedule)):
                        #     try:
                        #         if (self.scene.schedule[i] == False):
                        #             isColliding = False
                        #             for j in range(1, segLength):
                        #                 if (self.scene.schedule[i + j].isFull == True):
                        #                     isColliding = True
                        #                     i = i + j + 1
                        #                     break

                        #                 if (not isColliding):
                        #                     firstEmpty = self.scene.schedule[i].order
                        #                     firstY = self.scene.schedule[i].y
                        #                     break
                                    
                        #     except Exception as e:
                        #         print("Issue checking collisions:", e)
                        #         break

                        # for block in self.scene.schedule:
                            
                        #     try: #this can be optimized to not recheck block segments
                        #         if block.isFull == False:
                        #             isColliding = False
                        #             for i in range(1, segLength):
                        #                 if self.scene.schedule[block.order + i].isFull == True:
                        #                     isColliding = True
                        #                     break
                                    
                        #             if not isColliding:
                        #                 firstEmpty = block.order
                        #                 firstY = block.y
                        #                 break
                        #     except:
                        #         break

                        # try:
                        #     lastBlockIndex = firstEmpty + int(self.blockTimes[blockType] * 4) - 1
                        #     timeText = self.scene.schedule[firstEmpty].beginString + " - " + self.scene.schedule[lastBlockIndex].endString
                        # except:
                        #     print("There was an issue populating times")

                        # if customLength == -1:
                        #     segLength = int(self.blockTimes[blockType] * self.numSubBlocks)
                        #     type = self.blockTimes[blockType]
                        #     timeText = self.getTimeText(firstEmpty, segLength - 1)
                        #     newBlock = GraphicsRectItem(0, 0, self.blockWidth, self.blockSize * self.blockTimes[blockType], self.timeWidth, 
                        #                                 self.typeWidth, timeText, name, blockType, self.blockColors[blockType])
                        #     #newBlock = GraphicsRectItem(0, 0, 100, self.blockSize, self.blockTimes[blockType], timeText, name, blockType)
                        # else:
                        #     segLength = int(customLength * self.numSubBlocks)
                        #     timeText = self.getTimeText(firstEmpty, int(customLength * self.numSubBlocks) - 1)
                        #     newBlock = GraphicsRectItem(0, 0, self.blockWidth, self.blockSize * customLength, self.timeWidth, 
                        #                                 self.typeWidth, timeText, name, "Custom", self.blockColors["Custom"])
                        #     newBlock.setData(1, int(customLength * self.numSubBlocks))     # number of segments that rect occupies
                        #     #newBlock = GraphicsRectItem(0, 0, 100, self.blockSize, customLength, timeText, name, blockType)
                        # #newBlock.setBrush(QBrush(self.blockColors[blockType]))
                        timeText = self.getTimeText(firstEmpty, firstEmpty + segLength - 1)
                        newBlock = GraphicsRectItem(0, 0, self.blockWidth, self.blockSize * length, self.timeWidth, self.typeWidth, 
                                                    timeText, name, blockType, self.blockColors[blockType], segLength)
                        newBlock.setPos(self.timeBoxWidth, firstY)
                        newBlock.setData(0, firstEmpty)                            # id of first block segment that rect occupies
                        newBlock.setData(1, segLength)                             # length that of procedure
                        newBlock.setData(2, ProcedureDicts.procedureIDs[blockType])   # identifier for graphics to tell that this is a rect

                        # # Define the pen (line)
                        # pen = QPen(Qt.GlobalColor.black)
                        # newBlock.setPen(pen)
                        self.scene.procedures.append(newBlock)
                        self.scene.addItem(newBlock)
                        self.fill(firstEmpty, segLength)
                        # try:
                        #     for i in range(int(self.blockTimes[blockType] * 4)):
                        #         self.scene.schedule[firstEmpty + i].isFull = True
                            
                        # except:
                        #     print("There was an issue")
                        newBlock.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
                        newBlock.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
                        if (ProcedureDicts.procedureIDs[blockType] != 1):
                            self.currentCaseCount += 1
                self.caseCountItem.setPlainText("Cases: " + str(self.currentCaseCount))
                self.darkenFull()
                        

            except Exception as e:
                print("Could not read schedule", e)
                



            # for row in range(0, softMaxRow):
            #     for col in dataframe1.iter_cols(1, softMaxCol):
            #         if col[row].value is not None:
            #             print(col[row].value)

            # f = open(fname[0], 'r')

            # with f:

            #     data = f.read()
            #     print(data)
    
    def squish(self):
        self.scene.squish(0, len(self.scene.schedule) -1 )
        self.darkenFull()
        return

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
                                scheduleNames[item.data(0)] = "," + subItem.toPlainText() + "," + str(item.data(1))

                for i in range(len(schedule)):
                    if schedule[i][0] == 0 and schedule[i][1] != 1:
                        scheduleStr += "0\n"
                    elif schedule[i][0] != 0:
                        scheduleStr += (str(int(schedule[i][0])) + scheduleNames[i] + "\n")

                scheduleFile.write(scheduleStr)
                print("Saved schedule")
        except:
            print("Could not save schedule")

    def download(self):
        try:
            pix = QPixmap(self.canvasWidth, self.canvasHeight)
            painter = QPainter(pix)
            self.scene.render(painter)
            painter.end()
            pix.save("schedule-" + str(date.today()) + ".jpg", "JPG")
        except Exception as e:
            print("Could not save:", e)

    def darkenFull(self):
        """ Utility function to visualize which segments are currently full """

        # print("Procedures: ", len(self.scene.procedures))

        for item in self.scene.items():
            if item.data(4) is not None:
                if self.scene.schedule[item.data(0)].isFull == True:
                    item.setBrush(QColor(0, 0, 0, 125))
                    item.update()
                else: 
                    item.setBrush(QColor(0, 0, 0, 0))
                    item.update()
        return

    
    def insertSaved(self, inputType = -1, skip = 0, name = "Patient", segLength = -1):
        """" Insert a new schedule block for saved schedule"""
        
        if inputType == 0:
            return
        # elif inputType == 1:
        #     blockType = "Break"
        # elif inputType == 2:
        #     blockType = "Custom"
        # elif inputType == 3:
        #     blockType = "Regular"
        # elif inputType == 4:
        #     blockType = "Laser"
        # elif inputType == 5:
        #     blockType = "Premium"
        else:
            #blockType = self.blockType
            blockType = ProcedureDicts.procedureList[inputType]
        # Find first empty block in scene that can accommodate new insertion
        if blockType == "Custom":
            length = segLength / (1.0 * self.numSubBlocks)
        else:
            length = self.blockTimes[blockType]

        firstEmpty = -1
        firstY = -1
        if (skip < len(self.scene.schedule) and skip + segLength - 1 < len(self.scene.schedule)):
            firstEmpty = skip
            firstY = self.scene.schedule[firstEmpty].y
        # for block in self.scene.schedule:
        #     if numSkips > 0:
        #         numSkips -= 1
        #     else:
        #         # try: #this can be optimized to not recheck block segments that are filled probably
        #         #     if block.isFull == False:
        #         #         isColliding = False
        #         #         for i in range(1, int(blockLength * 4)):
        #         #             if self.scene.schedule[block.order + i].isFull == True:
        #         #                 isColliding = True
        #         #                 break
                        
        #         #         if not isColliding:
        #         #             firstEmpty = block.order
        #         #             firstY = block.y
        #         #             break
        #         # except:
        #         #     break

        if firstEmpty != -1:
            timeText = self.getTimeText(firstEmpty, firstEmpty + segLength - 1)
            rect = GraphicsRectItem(0, 0, self.blockWidth, self.blockSize * length, self.timeWidth, self.typeWidth, 
                                    timeText, name, blockType, self.blockColors[blockType], segLength)
            rect.setPos(self.timeBoxWidth, firstY)
            rect.setData(0, firstEmpty)                            # id of first block segment that rect occupies
            rect.setData(1, segLength)                             # length that of procedure
            rect.setData(2, ProcedureDicts.procedureIDs[blockType])   # identifier for graphics to tell that this is a rect

            self.scene.procedures.append(rect)
            self.scene.addItem(rect)
            self.fill(firstEmpty, segLength)

            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
            


            # # Draw a rectangle item, setting the dimensions and location corresponding to empty block.
            # rect = QGraphicsRectItem(0, 0, 100, self.blockSize * blockLength)
            # rect.setBrush(QBrush(self.blockColors[blockType]))
            # rect.setPos(80, firstY)
            # rect.setData(0, firstEmpty)                                     # id of first block segment that rect occupies
            # rect.setData(1, int(blockLength * 4))     # number of segments that rect occupies
            # rect.setData(2, ProcedureDicts.procedureIDs[blockType])   # identifier for graphics to tell that this is a rect
            
            # timeFontSize = 10
            # nameFontSize = 13
            # if blockType == "Break":
            #     rectText = QGraphicsTextItem("Break", rect)
            # else:
            #     rectText = QGraphicsTextItem(name, rect)
            # rectText.setData(3, 1)              # identifier for graphics to tell that this is block text


            # timeRect = QGraphicsRectItem(100, 0, 40, self.blockSize * blockLength, rect)
            # timeRect.setBrush(QColor(255, 255, 255, 255))
            # timeRect.setPen(QPen(Qt.GlobalColor.black))

            # timeText = "Time"
            # try:
            #     lastBlockIndex = firstEmpty + int(blockLength * 4) - 1
            #     timeText = self.scene.schedule[firstEmpty].beginString + " - " + self.scene.schedule[lastBlockIndex].endString
            # except:
            #     print("There was an issue populating times")

            # timeRectText = QGraphicsTextItem(timeText, rect)
            # timeRectText.setX(100)
            # timeRectText.setTextWidth(50)
            # timeRectText.setData(3, 2)              # identifier for graphics to tell that this is block time text

            # if blockType == "Custom":
            #     if blockLength == .75:
            #         timeFontSize = 8
            #         timeRectText.setY(-2)
            #     elif blockLength == .5:
            #         timeFontSize = 6
            #         nameFontSize = 10
            #         rectText.setY(-2)
            #         timeRectText.setX(98)
            #     elif blockLength == .25:
            #         timeFontSize = 4
            #         nameFontSize = 5
            #         rectText.setY(-3)
            #         timeRectText.setY(-2)
            # rectText.setFont(QFont("Helvetica", nameFontSize))
            # timeRectText.setFont(QFont("Helvetica", timeFontSize))
            

            # # Define the pen (line)
            # pen = QPen(Qt.GlobalColor.black)
            # rect.setPen(pen)
            # rect.setZValue(5.0)
            # self.scene.addItem(rect)
            # self.scene.procedures.append(rect)
            # try:
            #     for i in range(int(blockLength * 4)):
            #         self.scene.schedule[firstEmpty + i].isFull = True
                
            # except:
            #     print("There was an issue")
            # rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            # rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

            
            if (ProcedureDicts.procedureIDs[blockType] != 1):
                self.currentCaseCount += 1
                self.caseCountItem.setPlainText("Cases: " + str(self.currentCaseCount))
    

    def insert(self):
        """" Insert a new schedule block """
        
        blockType = self.blockType
        # Find first empty block in scene that can accommodate new insertion
        # firstEmpty = -1
        # firstY = -1

        # for block in self.scene.schedule:
            
        #     try: #this can be optimized to not recheck block segments
        #         if block.isFull == False:
        #             isColliding = False
        #             for i in range(1, int(self.blockTimes[blockType] * 4)):
        #                 if self.scene.schedule[block.order + i].isFull == True:
        #                     isColliding = True
        #                     break
                    
        #             if not isColliding:
        #                 firstEmpty = block.order
        #                 firstY = block.y
        #                 break
        #     except:
        #         break
        
        segLength = int(self.blockTimes[blockType] * self.numSubBlocks)
        
        firstEmpty, firstY = self.findFirstEmpty(segLength)

        if firstEmpty != -1:
            if blockType == "Break":
                rectText = "Break"
            else:
                rectText = self.blockName
            timeText = self.getTimeText(firstEmpty, firstEmpty + segLength - 1)
            rect = GraphicsRectItem(0, 0, self.blockWidth, self.blockSize * self.blockTimes[blockType], self.timeWidth, self.typeWidth, 
                                    timeText, rectText, blockType, self.blockColors[blockType], segLength)
            rect.setPos(self.timeBoxWidth, firstY)
            rect.setData(0, firstEmpty)                            # id of first block segment that rect occupies
            rect.setData(1, segLength)                             # length that of procedure
            rect.setData(2, ProcedureDicts.procedureIDs[blockType])   # identifier for graphics to tell that this is a rect

            self.scene.procedures.append(rect)
            self.scene.addItem(rect)
            self.fill(firstEmpty, segLength)

            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)




            # # Draw a rectangle item, setting the dimensions and location corresponding to empty block.
            # rect = QGraphicsRectItem(0, 0, 100, self.blockSize * self.blockTimes[blockType])
            # rect.setBrush(QBrush(self.blockColors[blockType]))
            # rect.setPos(80, firstY)
            # rect.setData(0, firstEmpty)                                     # id of first block segment that rect occupies
            # rect.setData(1, int(self.blockTimes[blockType] * 4))     # number of segments that rect occupies
            # rect.setData(2, ProcedureDicts.procedureIDs[blockType])   # identifier for graphics to tell that this is a rect

            # timeFontSize = 10
            # nameFontSize = 13
            # if blockType == "Break":
            #     rectText = QGraphicsTextItem("Break", rect)
            # else:
            #     rectText = QGraphicsTextItem(self.blockName, rect)
            # rectText.setData(3, 1)              # identifier for graphics to tell that this is block text

            # #print("FONT")
            # curFontSize = rectText.font().pointSize()
            # #print(curFontSize)
            # #print(rectText.font().pixelSize())
            # #print(rectText.font().pointSize())

            # timeRect = QGraphicsRectItem(100, 0, 40, self.blockSize * self.blockTimes[blockType], rect)
            # timeRect.setBrush(QColor(255, 255, 255, 255))
            # timeRect.setPen(QPen(Qt.GlobalColor.black))

            # timeText = "Time"
            # try:
            #     lastBlockIndex = firstEmpty + int(self.blockTimes[blockType] * 4) - 1
            #     timeText = self.scene.schedule[firstEmpty].beginString + " - " + self.scene.schedule[lastBlockIndex].endString
            # except:
            #     print("There was an issue populating times")

            # timeRectText = QGraphicsTextItem(timeText, rect)
            # timeRectText.setX(100)
            # timeRectText.setTextWidth(50)
            # timeRectText.setData(3, 2)              # identifier for graphics to tell that this is block time text

            # if blockType == "Custom":
            #     if self.blockTimes["Custom"] == .75:
            #         timeFontSize = 8
            #         timeRectText.setY(-2)
            #     elif self.blockTimes["Custom"] == .5:
            #         timeFontSize = 6
            #         nameFontSize = 10
            #         rectText.setY(-2)
            #         timeRectText.setX(98)
            #     elif self.blockTimes["Custom"] == .25:
            #         timeFontSize = 4
            #         nameFontSize = 5
            #         rectText.setY(-3)
            #         timeRectText.setY(-2)
            # rectText.setFont(QFont("Helvetica", nameFontSize))
            # timeRectText.setFont(QFont("Helvetica", timeFontSize))

            # # Define the pen (line)
            # pen = QPen(Qt.GlobalColor.black)
            # rect.setPen(pen)
            # self.scene.addItem(rect)
            # self.scene.procedures.append(rect)
            # try:
            #     for i in range(int(self.blockTimes[blockType] * 4)):
            #         self.scene.schedule[firstEmpty + i].isFull = True
                
            # except:
            #     print("There was an issue")
            # rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            # rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        if (ProcedureDicts.procedureIDs[blockType] != 1):
            self.currentCaseCount += 1
            self.caseCountItem.setPlainText("Cases: " + str(self.currentCaseCount))
        self.darkenFull()

    def getTimeText(self, startIndex, endIndex):
        try:
            return self.scene.schedule[startIndex].beginString + " - " + self.scene.schedule[endIndex].endString
        except Exception as e:
            print("There was an issue populating break time:", e)
            return "Time"
    
    def fill(self, startIndex, segLength):
        try:
            for i in range(segLength):
                self.scene.schedule[startIndex + i].isFull = True
                self.scene.schedule[startIndex + i].isBreak = True
        except Exception as e:
            print("There was an issue:", e)

    def findFirstEmpty(self, segLength, startIndex = 0, endIndex = 1000000):
        endIndex = min(len(self.scene.schedule), endIndex + 1)
        #print(startIndex, endIndex)
        for i in range(startIndex, endIndex):
            try:
                if (i + segLength >= endIndex):
                    break
                if (self.scene.schedule[i].isFull == False):
                    isColliding = False
                    
                    for j in range(1, segLength):
                        if (self.scene.schedule[i + j].isFull == True):
                            isColliding = True
                            i = i + j + 1
                            break

                    if (not isColliding):
                        return self.scene.schedule[i].order, self.scene.schedule[i].y
                    
            except Exception as e:
                print("Issue checking collisions:", e)
                break
        return -1, -1

    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        """ Change the stored procedure type when combobox is updated """
        self.blockType = s
    
    def changeCustomLength(self, i):
        #print("YUH", i)
        self.blockTimes["Custom"] = i
        self.customBlockLength = i

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
