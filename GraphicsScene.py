""" Represents custom scene that contains the schedule and inherits from QGraphicsScene """

from PyQt6.QtWidgets import (
    QGraphicsScene,
)

class GraphicsScene(QGraphicsScene):

    schedule = []
    selectedOrder = 0
    oldSelected = []

    def __init__(self, parent=None):
        super().__init__(parent)
    
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)

    def mousePressEvent(self, event):
        """ Add overloaded functionality to make selection apparent and set block fullness when a time block is selected """

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
                for i in range(item.data(1)):
                        self.schedule[item.data(0) + i].isFull = False


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
            try:

                for i in range(item.data(1)):
                    self.schedule[newBlock + i].isFull = True
                
                item.setData(0, newBlock)
                
            except:
                break