
import sys

from typing import List

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPen, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGraphicsEllipseItem,
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

class GraphicsScene(QtWidgets.QGraphicsScene):

    schedule = []
    selectedOrder = 0

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
        for item in items:
            print("SELECTED ITEM2")
            print(item.x())
            print(item.y())

        for block in self.schedule:
                try:
                    if (block.isFull == True and
                        abs(block.y - item.y()) < abs(newY - item.y())):
                        newY = block.y
                        newBlock = block.order
                except:
                    break
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
            print("SELECTED ITEM")
            print(item.x())
            print(item.y())
            
            newBlock = 0
            #newX = 0
            newY = 0
            for block in self.schedule:
                try:
                    if (block.isFull != True and
                        abs(block.y - item.y()) < abs(newY - item.y())):
                        newY = block.y
                        newBlock = block.order
                except:
                    break
            
            #item.setPos(newX, newY)
            item.setY(newY)
            try:
                self.schedule
                self.schedule[newBlock].isFull = True
            except:
                break


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None, blockSize=24):
        super(GraphicsView, self).__init__(parent)
        #super().__init__(parent)
        print("noo2")
        
class Block():
    
    def __init__(self, order=0, y=0, prev=None, next=None, blocks=[]):
        self.order = order
        self.blocks = blocks
        self.y = y
        self.prev = prev
        self.next = next
        self.isFull = False


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

    def __init__(self):
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
            self.scene.schedule.append(Block(i, self.blockSize * i))

            timeBox = QGraphicsRectItem(0, self.blockSize * i, 80, self.blockSize)
            timeBox.setBrush(QColor(255, 0, 0, 0))
            timeBox.setPen(QPen(Qt.GlobalColor.black))
            self.scene.addItem(timeBox)
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

        listItems = QPushButton("List")
        listItems.clicked.connect(self.listItems)
        vbox.addWidget(listItems)

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
            

    def insert(self):
        """" Insert a new schedule block """

        # Find first empty block in scene
        firstEmpty = -1
        firstY = -1
        for block in self.scene.schedule:
            try: 
                if block.isFull == False:
                    firstEmpty = block.order
                    firstY = block.y
                    break
            except:
                break

        if firstEmpty != -1:

            # Draw a rectangle item, setting the dimensions and location corresponding to empty block.
            rect = QGraphicsRectItem(80, firstY, 100, self.blockSize * self.blockTimes[self.blockType])
            #rect.setPos(50, 20)
            brush = QBrush(self.blockColors[self.blockType])
            rect.setBrush(brush)
            

            # Define the pen (line)
            pen = QPen(Qt.GlobalColor.black)
            # pen.setWidth(10)
            rect.setPen(pen)
            self.scene.addItem(rect)
            try:
                self.scene.schedule[firstEmpty].isFull = True
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

w = Window()
w.show()

app.exec()