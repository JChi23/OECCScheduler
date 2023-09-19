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
    procedures = []
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
            items.sort(key=lambda e: e.data(0)) # Earliest block should be first
        except Exception as e:
            print("Unable to get ordering from items", e)

        totalProcedureSize = 0
        for item in items:          # Get total block size of blocks being moved
            if item.data(2) is not None:
                totalProcedureSize += item.data(1)
        print("TOTAL SIZE: ", totalProcedureSize)
        newBlock = 0 # Find the desired insertion index of the first block via binary search

        lpointer = 0
        rpointer = len(self.schedule) - 1
        mpointer = (lpointer + rpointer) // 2
        try:
            while (lpointer <= rpointer):
                if (rpointer - lpointer == 1): # two elements remaining
                    if (abs(self.schedule[lpointer].y - items[0].y()) > abs(self.schedule[rpointer].y - items[0].y())):
                        if (abs(self.schedule[mpointer].y - items[0].y()) > abs(self.schedule[rpointer].y - items[0].y())):
                            mpointer = rpointer
                        break
                    else:                    
                        if (abs(self.schedule[mpointer].y - items[0].y()) > abs(self.schedule[lpointer].y - items[0].y())):
                            mpointer = lpointer
                        break
                mpointer = (lpointer + rpointer) // 2
                if (rpointer - lpointer == 2): # three elements remaining
                    if (self.schedule[mpointer].y > items[0].y()):
                        if (abs(self.schedule[mpointer].y - items[0].y()) > abs(self.schedule[rpointer].y - items[0].y())):
                            mpointer = rpointer
                        break
                    else:                    
                        if (abs(self.schedule[mpointer].y - items[0].y()) > abs(self.schedule[lpointer].y - items[0].y())):
                            mpointer = lpointer
                        break
                
                                                    #binary search
                if (self.schedule[mpointer].y == items[0].y()):
                    break
                else:
                    if (self.schedule[mpointer].y > items[0].y()):
                        rpointer = mpointer - 1
                    else:
                        lpointer = mpointer + 1
            print("MID: ", mpointer)
                
            newBlock = self.schedule[mpointer].order

            conflictFlag = False
            for i in range(totalProcedureSize):
                if self.schedule[i].isFull == True:
                    conflictFlag = True
                    break

            if conflictFlag:

                squishIndex = newBlock + (totalProcedureSize // 2) - 1
                squishAddTop = 0
                squishAddBot = 0
                containsBlock = False

                for procedure in self.procedures:
                    if (not procedure.isSelected() and # Find procedures that begin in the anticipated insert size
                        procedure.data(0) >= newBlock and
                        procedure.data(0) <= newBlock + totalProcedureSize - 1):
                        containsBlock = True
                        if (#procedure.data(0) + procedure.data(1) - 1 <= newBlock + totalProcedureSize - 1 and
                            procedure.data(0) <= newBlock + (totalProcedureSize // 2) - 1 and
                            procedure.data(0) + procedure.data(1) - 1 >= newBlock + (totalProcedureSize // 2) - 1): # If procedure is completely encapsulated within insert and contains midpoint
                            # if (procedure.data(0) > newBlock + (totalProcedureSize // 2) - 1):
                            #     squishAddBot += procedure.data(1)
                            # elif (procedure.data(0) + procedure.data(1) - 1 <= newBlock + (totalProcedureSize // 2) - 1):
                            #     squishAddTop += procedure.data(1)
                            # else:
                            if (procedure.data(0) + (procedure.data(1) // 2) - 1 > newBlock + (totalProcedureSize // 2) - 1): # If midpoint of procedure is below midpoint of insert
                                #squishAddBot += procedure.data(1)
                                squishIndex = procedure.data(0) - 1
                            else:
                                #squishAddTop += procedure.data(1)
                                squishIndex = procedure.data(0) + procedure.data(1) - 1

                        else:                                       # If procedure begins in insert but finishes outside
                            if (procedure.data(0) <= newBlock + (totalProcedureSize // 2) - 1):
                                squishIndex = procedure.data(0) - 1
                            squishAddBot += newBlock + totalProcedureSize - procedure.data(0)
                    elif (not procedure.isSelected() and
                        procedure.data(0) + procedure.data(1) - 1 >= newBlock and
                        procedure.data(0) + procedure.data(1) - 1 <= newBlock + totalProcedureSize - 1): # Find procedure that ends in insert
                        containsBlock = True
                        squishAddTop += procedure.data(0) + procedure.data(1) - newBlock

                if not containsBlock:
                    for procedure in self.procedures:
                        if (not procedure.isSelected() and # Find a procedure that completely encapsulates moved procedure and choose to either position above or below
                            procedure.data(0) + procedure.data(1) - 1 > newBlock + totalProcedureSize - 1 and
                            procedure.data(0) < newBlock):
                            if (newBlock > (procedure.data(0) + (procedure.data(1) // 2) - 1)): # Try to fit insert below at index
                                squishAddTop += (procedure.data(1) + procedure.data(1) - newBlock)
                                squishIndex = procedure.data(0) + procedure.data(1) - 1
                            else:                                                               # Try to fit insert above at index
                                squishAddBot += (newBlock + totalProcedureSize - procedure.data(0))
                                squishIndex = procedure.data(0) - 1
                            break

                # Check for spaces and squish above and below
                prevBlocksEmpty = 0
                totalTopSquish = totalProcedureSize + squishAddTop
                totalBotSquish = squishAddBot
                topIndex = 0
                print("BLAH: ", totalTopSquish, squishAddTop, totalBotSquish, squishAddBot, squishIndex)
                if totalTopSquish > 0:
                    for i in range(squishIndex, -1, -1):
                        if (self.schedule[i].isFull == False):
                            prevBlocksEmpty += 1

                        if (prevBlocksEmpty == totalTopSquish):
                            topIndex = i
                            #self.squish(i, squishIndex)
                            break
                    
                    if (prevBlocksEmpty != totalTopSquish):
                        #self.squish(0, squishIndex)
                        newBlock += totalTopSquish - prevBlocksEmpty
                        totalBotSquish += totalTopSquish - prevBlocksEmpty
                    prevBlocksEmpty = 0

                if totalBotSquish > 0:

                    for i in range(squishIndex + 1, len(self.schedule)):
                        if (self.schedule[i].isFull == False):
                            prevBlocksEmpty += 1
                        
                        if (prevBlocksEmpty == totalBotSquish):
                            self.squish(squishIndex + 1, i, False)
                            break

                    if (prevBlocksEmpty != totalBotSquish):
                        self.squish(squishIndex + 1, len(self.schedule) - 1, False)
                        newBlock -= totalBotSquish - prevBlocksEmpty
                        totalTopSquish = totalBotSquish - prevBlocksEmpty
                        prevBlocksEmpty = 0
                        for i in range(topIndex - 1, -1, -1):
                            if (self.schedule[i].isFull == False):
                                prevBlocksEmpty += 1

                            if (prevBlocksEmpty == totalTopSquish):
                                #self.squish(i, squishIndex)
                                topIndex = i
                                break
                        
                        if (prevBlocksEmpty != totalTopSquish):
                            print("NOT ENOUGH SPACE (THIS SHOULD NOT HAPPEN)")
                self.squish(topIndex, squishIndex)



        except Exception as e:
            print("there was an issue with block collision", e)
            
        try:
            for item in items:

                if not item.isSelected():
                    item.setSelected(True)
                
                self.move(item, item.data(0), newBlock, releaseOld=False)
                newBlock += item.data(1)

        except Exception as e:
            print("There was an issue moving items:", e)

        # OLD MOVEMENT METHOD
        # for item in items:

        #     # Check for collisions and find earliest block to put in procedure

        #     newBlock = 0
        #     isOldFull = False

        #     if item.data(0) is not None:
        #         newBlock = item.data(0)

        #     if self.doesCollide(item, newBlock):  # If old spot is occupied, need to find a new default spot
        #         isOldFull = True
            
        #     if not item.isSelected():
        #         item.setSelected(True)

        #     prevBlocksEmpty = 0
        #     newBlocksEmpty = 0
        
        #         # this will insert the block into the first available space without moving anything else
        #     # for block in self.schedule: # can be optimized to only check for colliding things
        #     #     try:
        #     #         if (item.data(1) + block.order > len(self.schedule)):
        #     #             break

        #     #         if (block.isFull == False):
        #     #             prevBlocksEmpty += 1

        #     #             if (abs(block.y - item.y()) <= abs(self.schedule[newBlock].y - item.y()) or isOldFull):
        #     #                 if not self.doesCollide(item, block.order):
        #     #                     newBlock = block.order
        #     #                     newBlocksEmpty = prevBlocksEmpty
        #     #                     if isOldFull:
        #     #                         isOldFull = False
        #     #     except Exception as e:
        #     #         print("there was an issue with block collision", e)
        #     #         break
     
        #     # Update procedure time and location with new block
        #     self.move(item, item.data(0), newBlock)

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
            while (self.schedule[bpointer].isFull == True and bpointer <= endingIndex): #Find first open space
                bpointer += 1
            fpointer = bpointer

            print(fpointer)
            bp = 0
            while (fpointer <= endingIndex and bp < 2000):
                bp += 1
                if (self.schedule[fpointer].isFull == True):
                    for procedure in self.procedures:
                        if (procedure.data(0) == self.schedule[fpointer].order):
                            # for i in range(procedure.data(1)):
                            #     self.schedule[procedure.data(0) + i].isFull = False
                            self.move(procedure, procedure.data(0), self.schedule[bpointer].order)
                            bpointer = bpointer + procedure.data(1)
                            fpointer += procedure.data(1)
                            break
                else:
                    fpointer += 1
                    
        else:
            bpointer = endingIndex
            while (self.schedule[bpointer].isFull == True and bpointer >= startingIndex): #Find first open space
                bpointer -= 1
            fpointer = bpointer

            print(fpointer)
            bp = 0
            while (fpointer >= startingIndex and bp < 2000):
                bp += 1
                if (self.schedule[fpointer].isFull == True):
                    for procedure in self.procedures:
                        if (procedure.data(0) + procedure.data(1) - 1 == self.schedule[fpointer].order):
                            # for i in range(procedure.data(1)):
                            #     self.schedule[procedure.data(0) + i].isFull = False
                            self.move(procedure, procedure.data(0), self.schedule[bpointer - procedure.data(1) + 1].order)
                            bpointer = bpointer - procedure.data(1)
                            fpointer -= procedure.data(1)
                            break
                else:
                    fpointer -= 1

        print("finished squishing")

    def move(self, movedItem, oldBlock = 0, newBlock = 0, releaseOld = True):
        """ Move movedItem from oldBlock in schedule to newBlock """
        
        try:
            movedItem.setPos(80, self.schedule[newBlock].y)
            
            if releaseOld:
                for i in range(movedItem.data(1)):
                    self.schedule[oldBlock + i].isFull = False
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