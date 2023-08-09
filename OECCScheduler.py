
import sys
import numpy as np

from typing import List

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPen, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,

)

class GraphicsScene(QGraphicsScene):

    schedule = []
    selectedOrder = 0
    oldSelected = []

    def __init__(self, parent=None):
        super().__init__(parent)
        print("noo")
    
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)
        print("noo1")

    # def mouseMoveEvent(self, event):
    #     self.posX = event.scenePos().x()
    #     self.parent().parent().setPosition(event.scenePos().x()) # <-- crawl up the ancestry
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        items = self.selectedItems()
        for item in self.oldSelected:
            try:
                if item not in items:
                    item.setOpacity(1)
                    item.update()
            except:
                print("there was an error with updating opacity")
        
        self.oldSelected = items

        for item in items:
            # print("SELECTED ITEM2")
            # print(item.pos().x(), item.pos().y())
            # print(item.scenePos().x(), item.scenePos().y())

            item.setOpacity(0.5)
            item.update()
            # for cItem in item.collidingItems():
            #     print("NEW ITEM")
            #     print(cItem.x())
            #     print(cItem.y())
            if item.data(1) is not None:
                for i in range(item.data(1)):
                        self.schedule[item.data(0) + i].isFull = False

        

        # for block in self.schedule:
        #         try:
        #             if (block.isFull == True and
        #                 abs(block.y - item.y()) < abs(newY - item.y())):
        #                 newY = block.y
        #                 newBlock = block.order
        #         except:
        #             break
        print("Mouse press event in graphic")

    def mouseReleaseEvent(self, event):
        items = self.selectedItems()
        # for item in items:
        #     print("SELECTED ITEM")
        #     print(item.x())
        #     print(item.y())
            
        #     newX = 80
        #     newY = 0
        #     for block in self.schedule:
        #         try:
        #             if abs(block.y - item.y()) < abs(newY - item.y()):
        #                 newY = block.y
        #         except:
        #             break


        super().mouseReleaseEvent(event)
        print("Mouse Release Event in Graphic")

        for item in items:
            # print("SELECTED ITEM")
            # print(item.pos().x(), item.pos().y())
            # print(item.scenePos().x(), item.scenePos().y())

            newBlock = 0
            if item.data(0) is not None:
                newBlock = item.data(0)
            #newX = 0
            newY = 0
            for block in self.schedule: # can be optimized to only check for colliding things
                try:
                    if (block.isFull != True and
                        abs(block.y - item.y()) < abs(newY - item.y())):
                        isColliding = False

                        for i in range(1, item.data(1)):
                            if self.schedule[block.order + i].isFull == True:
                                isColliding = True
                                break
                        
                        if not isColliding:
                            newY = block.y
                            newBlock = block.order
                            
                except:
                    break
            
            item.setPos(80, newY)
            #item.setY(newY)
            try:
                # self.schedule

                #self.schedule[newBlock].isFull = True

                for i in range(item.data(1)):
                    #self.schedule[item.data(0) + i].isFull = False
                    self.schedule[newBlock + i].isFull = True
                
                item.setData(0, newBlock)
                
            except:
                break


class GraphicsView(QGraphicsView):
    def __init__(self, parent=None, blockSize=24):
        super(GraphicsView, self).__init__(parent)
        #super().__init__(parent)
        print("noo2")
        
class BlockSegment():
    
    def __init__(self, order=0, y=0, prev=None, next=None, blocks=[]):
        self.order = order
        self.blocks = blocks
        self.y = y
        self.prev = prev
        self.next = next
        self.isFull = False
        self.isBreak = False


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

    def __init__(self, saved=None):
        super().__init__()

        # Defining scene and adding basic layout elements to scene
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

            #self.schedule.append(Block(i, self.blockSize * i + (self.blockSize / 2)))
            #self.scene.schedule.append(BlockSegment(i * 4, self.blockSize * i))

            timeBox = QGraphicsRectItem(0, 0, 80, self.blockSize)
            timeBox.setBrush(QColor(255, 0, 0, 0))
            timeBox.setPen(QPen(Qt.GlobalColor.black))
            timeBox.setPos(0, self.blockSize * i)
            self.scene.addItem(timeBox)
            # for j in range(1,4):
            #     blockLine = QGraphicsLineItem(80, (self.blockSize * i) + ((self.blockSize / 4) * j), 
            #                                   260, (self.blockSize * i) + ((self.blockSize / 4) * j))
            #     blockLine.setPen(QPen(Qt.GlobalColor.gray))
            #     self.scene.addItem(blockLine)
            #     self.scene.schedule.append(BlockSegment(i * 4 + j, (self.blockSize * i) + ((self.blockSize / 4) * j)))
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

        # # Draw a rectangle item, setting the dimensions.
        # rect = QGraphicsRectItem(0, 0, 200, 50)
        # rect.setPos(50, 20)
        # brush = QBrush(Qt.GlobalColor.red)
        # rect.setBrush(brush)

        # # Define the pen (line)
        # pen = QPen(Qt.GlobalColor.cyan)
        # pen.setWidth(10)
        # rect.setPen(pen)

        # ellipse = QGraphicsEllipseItem(0, 0, 100, 100)
        # ellipse.setPos(75, 30)

        # brush = QBrush(Qt.GlobalColor.blue)
        # ellipse.setBrush(brush)

        # pen = QPen(Qt.GlobalColor.green)
        # pen.setWidth(5)
        # ellipse.setPen(pen)

        # # Add the items to the scene. Items are stacked in the order they are added.
        # self.scene.addItem(ellipse)
        # self.scene.addItem(rect)

        # # Set all items as moveable and selectable.
        # for item in self.scene.items():
        #     item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        #     item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)



        # Define our layout.
        vbox = QVBoxLayout()

        insert = QPushButton("Insert")
        insert.clicked.connect(self.insert)
        vbox.addWidget(insert)

        setBlock = QComboBox()
        setBlock.addItems(["Regular", "Laser", "Premium"])

        # Sends the current index (position) of the selected item.
        #blockType.currentIndexChanged.connect( self.index_changed )

        # There is an alternate signal to send the text.
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

        # listItems = QPushButton("List")
        # listItems.clicked.connect(self.listItems)
        # vbox.addWidget(listItems)

        # EXISTING CODE
        # up = QPushButton("Up")
        # up.clicked.connect(self.up)
        # vbox.addWidget(up)

        # down = QPushButton("Down")
        # down.clicked.connect(self.down)
        # vbox.addWidget(down)

        # rotate = QSlider()
        # rotate.setRange(0, 360)
        # rotate.valueChanged.connect(self.rotate)
        # vbox.addWidget(rotate)

        #view = QGraphicsView(self.scene)
        #self.view = GraphicsView(self.scene)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        hbox = QHBoxLayout(self)
        hbox.addLayout(vbox)
        hbox.addWidget(self.view)

        self.setLayout(hbox)
    
    def listItems(self):
        for item in self.scene.items():
        #for item in self.view.scene.items():
            print("NEW ITEM")
            print(item.x())
            print(item.y())
            
    def delete(self):
        for item in self.scene.selectedItems():
            if item.data(0) is not None and item.data(1) is not None:
                for cItem in item.collidingItems():
                    if (cItem.data(0) is not None and
                        item.data(0) == cItem.data(0)):
                        for i in range(item.data(1)):
                            self.scene.schedule[item.data(0) + i].isFull = False
            self.scene.removeItem(item)

    def clear(self):
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
        try:
            with open("SavedSchedule.txt", "w") as scheduleFile:
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
        """" Insert a new schedule block """
        
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
            # pen.setWidth(10)
            rect.setPen(pen)
            self.scene.addItem(rect)
            try:
                for i in range(int(self.blockTimes[blockType] * 4)):
                    self.scene.schedule[firstEmpty + i].isFull = True
                
            except:
                print("There was an issue")
            #self.view.scene.addItem(rect)
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
            # pen.setWidth(10)
            rect.setPen(pen)
            self.scene.addItem(rect)
            try:
                for i in range(int(self.blockTimes[blockType] * 4)):
                    self.scene.schedule[firstEmpty + i].isFull = True
                
            except:
                print("There was an issue")
            #self.view.scene.addItem(rect)
            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

    #def selectItem(self):

    # def mousePressEvent(self, event):

    #     if event.button() == Qt.LeftButton:
    #         # handle left mouse button here
    #     else:
    #         # pass on other buttons to base class
    #         QCheckBox.mousePressEvent(event)

    # def mouseReleaseEvent(self, event):
    #     print("Mouse Release Event")
        

    def index_changed(self, i): # i is an int
        print(i)

    def text_changed(self, s): # s is a str
        self.blockType = s
        print(self.blockType)

    def up(self):
        """ Iterate all selected items in the view, moving them forward. """
        items = self.scene.selectedItems()
        for item in items:
            z = item.zValue()
            item.setZValue(z + 1)

    def down(self):
        """ Iterate all selected items in the view, moving them backward. """
        items = self.scene.selectedItems()
        for item in items:
            z = item.zValue()
            item.setZValue(z - 1)

    def rotate(self, value):
        """ Rotate the object by the received number of degrees. """
        items = self.scene.selectedItems()
        for item in items:
            item.setRotation(value)


app = QApplication(sys.argv)

try:
    with open("SavedSchedule.txt", "r+") as scheduleFile:
        savedSchedule = scheduleFile.read().splitlines()
except:
    print("Could not open file")
    savedSchedule = ['0']

w = Window(saved=savedSchedule)
w.show()

app.exec()