
import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("noo")
    
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)
        print("noo1")

    # def mouseMoveEvent(self, event):
    #     self.posX = event.scenePos().x()
    #     self.parent().parent().setPosition(event.scenePos().x()) # <-- crawl up the ancestry
    def mouseReleaseEvent(self, event):
        items = self.selectedItems()
        for item in items:
            print("SELECTED ITEM")
            print(item.x())
            print(item.y())
        super().mouseReleaseEvent(event)
        print("Mouse Release Event in Graphic")


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None, blockSize=24):
        super(GraphicsView, self).__init__(parent)
        #super().__init__(parent)
        print("noo2")
        

class Window(QWidget):

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

        # Defining a scene rect of 400x200, with it's origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.setWindowTitle("Scheduler")
        #self.scene = QGraphicsScene(0, 0, 400, 800)
        self.scene = GraphicsScene(0, 0, 400, 800)
        # self.Layout = QtWidgets.QVBoxLayout()
        # self.gw = GraphicsView(self) # <-- pass self here


        # List out time slots
        numHours = 8
        startHour = 7
        startMinute = 30
        AMPMTag = "AM"

        for i in range(0,4 * numHours):
            if startHour < 10:
                textHour = "0" + str(startHour)
            else:
                textHour = str(startHour)
            
            if startMinute == 0:
                textMinute = "00"
            else:
                textMinute = str(startMinute)
            
            textitem = self.scene.addText( textHour + ":" + textMinute + " " + AMPMTag)
            textitem.setPos(0, self.blockSize * i)

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
        print("hello")


        # Draw a rectangle item, setting the dimensions.
        rect = QGraphicsRectItem(0, 0, 100, self.blockSize * self.blockTimes[self.blockType])
        rect.setPos(50, 20)
        brush = QBrush(Qt.GlobalColor.red)
        rect.setBrush(brush)
        

        # Define the pen (line)
        pen = QPen(Qt.GlobalColor.cyan)
        pen.setWidth(10)
        rect.setPen(pen)
        self.scene.addItem(rect)
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

    def mouseReleaseEvent(self, event):
        print("Mouse Release Event")
        

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