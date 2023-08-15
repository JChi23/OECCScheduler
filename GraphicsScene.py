""" Represents custom scene that contains the schedule and inherits from QGraphicsScene """

from PyQt6.QtWidgets import (
    QGraphicsScene,
)

class GraphicsScene(QGraphicsScene):

    schedule = []
    selectedOrder = 0
    oldSelected = []
    blockSelected = False

    def __init__(self, parent=None):
        super().__init__(parent)
    
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)

    def mousePressEvent(self, event):
        """ Add overloaded functionality to make selection apparent and set block fullness when a time block is selected """

        self.blockSelected = False
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

            item.setOpacity(0.5)
            item.update()

            if item.data(1) is not None:
                if not self.blockSelected:
                    self.blockSelected = True
                    try:
                        self.parent().changeNameChange(True)
                    except:
                        print("could not enable parent button")
                for i in range(item.data(1)):
                        self.schedule[item.data(0) + i].isFull = False
            
            if item.data(2) is not None:
                subItems = item.childItems()
                for subItem in subItems:
                    if subItem.data(3) is not None and subItem.data(3) == 1:
                        self.parent().changeInputPatientName(subItem.toPlainText())
        
        if not self.blockSelected:
            try:
                self.parent().changeNameChange()
            except:
                print("could not disable parent button")

    def changeName(self, name="Patient"):
        """ Change the name of the selected block """
        items = self.selectedItems()

        for item in items:
            if item.data(2) is not None:
                subItems = item.childItems()
                for subItem in subItems:
                    if subItem.data(3) is not None and subItem.data(3) == 1:
                        subItem.setPlainText(name)



    def mouseReleaseEvent(self, event):
        """ Add overloaded functionality to correctly snap and place time blocks when mouse released """

        items = self.selectedItems()

        super().mouseReleaseEvent(event)
        
        for item in items:

            newBlock = 0
            if item.data(0) is not None:
                newBlock = item.data(0)
            newY = 0
            for block in self.schedule: # can be optimized to only check for colliding things
                try:
                    if (block.isFull != True and
                        abs(block.y - item.y()) <= abs(newY - item.y())):
                        isColliding = False

                        for i in range(1, item.data(1)):
                            if self.schedule[block.order + i].isFull == True:
                                isColliding = True
                                break
                        
                        if not isColliding:
                            newY = block.y
                            newBlock = block.order
                            
                except:
                    print("there was an issue with block collision")
                    break
            
            item.setPos(80, newY)
            try:
                for i in range(item.data(1)):
                    self.schedule[newBlock + i].isFull = True

                for subItem in item.childItems():
                    if subItem.data(3) is not None and subItem.data(3) == 2:
                        timeText = "Time"
                        lastBlockIndex = newBlock + item.data(1) - 1
                        timeText = self.schedule[newBlock].beginString + " - " + self.schedule[lastBlockIndex].endString
                        subItem.setPlainText(timeText)
            
                
                item.setData(0, newBlock)
                
            except:
                print("there was an issue with updating times")
                break