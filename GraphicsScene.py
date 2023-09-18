""" Represents custom scene that contains the schedule and inherits from QGraphicsScene """

#from PyQt6 import QtGui
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
)
from PyQt6.QtGui import (
    QTransform,
    QKeyEvent,
)

class GraphicsScene(QGraphicsScene):
    
    schedule = []
    selectedOrder = 0
    oldSelected = []
    blockSelected = False
    allowDeselect = False
    count = 0
    pressBegan = False
    allowMultiSelect = False

    def __init__(self, parent=None):
        super().__init__(parent)
    
    def __init__(self, x, y, width, height, parent=None):
        super().__init__(x, y, width, height, parent)
        #print(Qt.Key.Key_Shift.value)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_Shift.value:
            self.allowMultiSelect = True

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        super().keyReleaseEvent(event)
        if event.key() == Qt.Key.Key_Shift.value:
            self.allowMultiSelect = False

    def mousePressEvent(self, event):
        """ Add overloaded functionality to make selection apparent and set block fullness when a time block is selected """

        self.allowDeselect = False
        self.blockSelected = False
        self.pressBegan = True
        self.count = 0

        multiItemGuard = self.itemAt(event.scenePos().x(), event.scenePos().y(), QTransform())
        multiItemParent = multiItemGuard
        while(multiItemParent.parentItem()):
            multiItemParent = multiItemParent.parentItem()
        if multiItemParent and multiItemParent.isSelected():
            self.allowDeselect = True

        oldItems = self.selectedItems()


        super().mousePressEvent(event)

        if multiItemParent:
            multiItemParent.setSelected(True)

        items = self.selectedItems()

        if self.allowMultiSelect:
            try:
                tempCombined = oldItems + items
                tempCombined.sort(key=lambda e: e.data(0))
                earliest = tempCombined[0].data(0)
                latest = tempCombined[len(tempCombined) - 1].data(0)

                for item in self.items():
                    if (item.data(2) is not None and
                        item.data(0) >= earliest and
                        item.data(0) <= latest):
                        item.setSelected(True)
                for item in oldItems:
                    item.setSelected(True)
                items = self.selectedItems()
            except:
                print("Unable to get ordering from items")


        for item in oldItems:   # Change opacity of old selected items to opaque
            try:
                if item not in items:
                    item.setOpacity(1)
                    item.update()
            except:
                print("there was an error with updating opacity")
        
        for item in items:  # Change patient names and block fullness

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

        self.parent().darkenFull()

    def changeName(self, name="Patient"):
        """ Change the name of the selected block """

        items = self.selectedItems()
        for item in items:
            if item.data(2) is not None:
                subItems = item.childItems()
                for subItem in subItems:
                    if subItem.data(3) is not None and subItem.data(3) == 1:
                        subItem.setPlainText(name)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        """ Add overloaded functionality to allow for single click selection + deselection """

        super().mouseMoveEvent(event)
        if self.allowDeselect and self.count >= 10:
            self.allowDeselect = False
            self.count = 0
        elif self.pressBegan:
            self.count += 1

    def mouseReleaseEvent(self, event):
        """ Add overloaded functionality to correctly snap and place time blocks when mouse released """

        items = self.selectedItems()
        super().mouseReleaseEvent(event)

        try:
            items.sort(key=lambda e: e.data(0))
        except:
            print("Unable to get ordering from items")
        
        for item in items:

            # Check for collisions and find earliest block to put in procedure

            newBlock = 0
            isOldFull = False

            if item.data(0) is not None:
                newBlock = item.data(0)

            if self.doesCollide(item, newBlock):  # If old spot is occupied, need to find a new default spot
                isOldFull = True
            
            if not item.isSelected():
                item.setSelected(True)

            prevBlocksEmpty = 0
            newBlocksEmpty = 0
        
                # this will insert the block into the first available space without moving anything else
            # for block in self.schedule: # can be optimized to only check for colliding things
            #     try:
            #         if (item.data(1) + block.order > len(self.schedule)):
            #             break

            #         if (block.isFull == False):
            #             prevBlocksEmpty += 1

            #             if (abs(block.y - item.y()) <= abs(self.schedule[newBlock].y - item.y()) or isOldFull):
            #                 if not self.doesCollide(item, block.order):
            #                     newBlock = block.order
            #                     newBlocksEmpty = prevBlocksEmpty
            #                     if isOldFull:
            #                         isOldFull = False
            #     except Exception as e:
            #         print("there was an issue with block collision", e)
            #         break


                # this will insert the block as close as possible to where it is dropped, shifting other blocks around
            lpointer = 0
            rpointer = len(self.schedule) - 1
            mpointer = (lpointer + rpointer) // 2
            try:
                while (lpointer <= rpointer):
                    if (rpointer - lpointer == 1): # two elements remaining
                        if (abs(self.schedule[lpointer].y - item.y()) > abs(self.schedule[rpointer].y - item.y())):
                            if (abs(self.schedule[mpointer].y - item.y()) > abs(self.schedule[rpointer].y - item.y())):
                                mpointer = rpointer
                            break
                        else:                    
                            if (abs(self.schedule[mpointer].y - item.y()) > abs(self.schedule[lpointer].y - item.y())):
                                mpointer = lpointer
                            break
                    mpointer = (lpointer + rpointer) // 2
                    if (rpointer - lpointer == 2): # three elements remaining
                        if (self.schedule[mpointer].y > item.y()):
                            if (abs(self.schedule[mpointer].y - item.y()) > abs(self.schedule[rpointer].y - item.y())):
                                mpointer = rpointer
                            break
                        else:                    
                            if (abs(self.schedule[mpointer].y - item.y()) > abs(self.schedule[lpointer].y - item.y())):
                                mpointer = lpointer
                            break
                    
                                                        #binary search
                    if (self.schedule[mpointer].y == item.y()):
                        break
                    else:
                        if (self.schedule[mpointer].y > item.y()):
                            rpointer = mpointer - 1
                        else:
                            lpointer = mpointer + 1
                print("MID: ", mpointer)
                    
                newBlock = self.schedule[mpointer].order

                for i in range(newBlock + (item.data(1) // 2) - 1, -1, -1):
                    if (self.schedule[i].isFull == False):
                        prevBlocksEmpty += 1

                    if (prevBlocksEmpty == item.data(1)):
                        self.squish(i, newBlock + item.data(1) - 1)
                        break
                
                if (prevBlocksEmpty != item.data(1)):
                    prevBlocksEmpty = 0
                    for i in range(newBlock + (item.data(1) // 2), len(self.schedule)):
                        if (self.schedule[i].isFull == False):
                            prevBlocksEmpty += 1
                        
                        if (prevBlocksEmpty == item.data(1)):
                            self.squish(newBlock, i, False)
                            break
            
                    
            except Exception as e:
                print("there was an issue with block collision", e)
                break
     
            # Update procedure time and location with new block
            self.move(item, item.data(0), newBlock)

        multiItemGuard = self.itemAt(event.scenePos().x(), event.scenePos().y(), QTransform())
        if multiItemGuard and self.allowDeselect:
            tempItem = multiItemGuard
            while(tempItem.parentItem()):
                tempItem = tempItem.parentItem()
            tempItem.setSelected(False)
            tempItem.setOpacity(1)
            tempItem.update()
            self.allowDeselect = False
        
        self.pressBegan = False
        self.parent().darkenFull()

    def doesCollide(self, item, block = 0) -> bool:
        """ Check if item at block in schedule would have any collisions """

        try:
            isColliding = False
            
            for i in range(item.data(1)):
                if self.schedule[block + i].isFull == True:
                    isColliding = True
                    break
            
            return isColliding
        except Exception as e:
            print("Could not check for collisions: ", e)
            return True
        
    def squish(self, startingIndex, endingIndex, squishUp = True):
        print("squishing")
        if squishUp:
            bpointer = startingIndex
            while (self.schedule[bpointer].isFull == True and bpointer < endingIndex):
                bpointer += 1
            fpointer = bpointer

            print(fpointer)

            while (fpointer < endingIndex):
                if (self.schedule[fpointer].isFull == True):
                    for item in self.items():
                        if (item.data(2) is not None and item.data(0) == self.schedule[fpointer].order):
                            self.move(item, item.data(0), self.schedule[bpointer].order)
                            bpointer = bpointer + item.data(1) - 1
                            fpointer = max(fpointer + 1, bpointer)
                            break
                else:
                    fpointer += 1
                    
        else:
            fpointer = endingIndex
            bpointer = endingIndex

        print("finished squishing")

    def move(self, movedItem, oldBlock = 0, newBlock = 0):
        """ Move movedItem from oldBlock in schedule to newBlock """
        
        try:
            movedItem.setPos(80, self.schedule[newBlock].y)
            
            # for i in range(movedItem.data(1)):
            #     self.schedule[oldBlock + i].isFull = False
            for i in range(movedItem.data(1)):
                self.schedule[newBlock + i].isFull = True

            if oldBlock == newBlock:
                return

            for subItem in movedItem.childItems():
                if subItem.data(3) is not None and subItem.data(3) == 2:
                    timeText = "Time"
                    lastBlockIndex = newBlock + movedItem.data(1) - 1
                    timeText = self.schedule[newBlock].beginString + " - " + self.schedule[lastBlockIndex].endString
                    subItem.setPlainText(timeText)

            movedItem.setData(0, newBlock)
        except:
            print("Could not move item")