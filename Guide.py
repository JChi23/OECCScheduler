""" Represents the layout for the scheduler help guide """
from PyQt6.QtWidgets import (
    QGroupBox, 
    QLabel, 
    QVBoxLayout, 
    QWidget, 
    QFormLayout,
)

from random import randint


class HelpGuide(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scheduler Help")
        layout = QVBoxLayout()

        insertHelp = QGroupBox("How to Insert a Procedure")
        insertHelpLayout = QFormLayout()
        insertHelpLayout.addRow(QLabel("Step 1: Go to Insert Procedure box in menu"))
        insertHelpLayout.addRow(QLabel("Step 2: Type in a name/title (or leave field empty for name to be 'Patient') into the text box"))
        insertHelpLayout.addRow(QLabel("Step 3: Select a procedure type from the procedure list"))
        insertHelpLayout.addRow(QLabel("Step 4: Click the 'Insert' button to insert the new procedure in the earliest available slot"))
        insertHelpLayout.addRow(QLabel("""NOTE: If you are creating a custom-length procedure, select 'Custom' from the procedure list and 
        use the length scale below to adjust how long you want the procedure to be. The scale
        increments by factors of .25 where 1.0 is equal to the length of one block (15 minutes)"""))
        
        insertHelpLayout.setSizeConstraint(QFormLayout.SizeConstraint.SetFixedSize)
        insertHelp.setLayout(insertHelpLayout)
        layout.addWidget(insertHelp)

        modifyHelp = QGroupBox("How to Modify a Procedure")
        modifyHelpLayout = QFormLayout()
        modifyHelpLayout.addRow(QLabel("Step 1: Click on which procedure you wish to modify"))
        modifyHelpLayout.addRow(QLabel("Step 2: Go to Modify Procedure box in menu"))
        modifyHelpLayout.addRow(QLabel("Step 3: If you wish to delete the procedure, click the 'Delete' button"))
        modifyHelpLayout.addRow(QLabel("""Step 4: If you wish to rename the procedure, type in a name/title (or leave field empty for 
        name to be 'Patient') into the text box and click the 'Change Name' button"""))
        modifyHelpLayout.addRow(QLabel("NOTE: If multiple procedures are selected, all procedures will be renamed"))
        
        modifyHelpLayout.setSizeConstraint(QFormLayout.SizeConstraint.SetFixedSize)
        modifyHelp.setLayout(modifyHelpLayout)
        layout.addWidget(modifyHelp)

        otherHelp = QGroupBox("Other Functionality")
        otherHelpLayout = QFormLayout()
        otherHelpLayout.addRow(QLabel("Block Select: Hold shift and select two procedures to select every procedure within them as well"))
        otherHelpLayout.addRow(QLabel("Multi Select: Hold command (control on windows) and click however many procedures you wish to select"))
        otherHelpLayout.addRow(QLabel("Clear: Deletes all procedures and blocks from schedule"))
        otherHelpLayout.addRow(QLabel("Open: Allows you to open an .xlsx file to read and input into the scheduler"))
        otherHelpLayout.addRow(QLabel("Collapse: Removes all whitespace between procedures and blocks (i.e. 'squishes' schedule)"))
        otherHelpLayout.addRow(QLabel("Save: Saves current schedule so that closing and reopening the program will keep the current schedule"))
        otherHelpLayout.addRow(QLabel("Download: Downloads the current schedule as a .jpg image to your computer"))
        
        otherHelpLayout.setSizeConstraint(QFormLayout.SizeConstraint.SetFixedSize)
        otherHelp.setLayout(otherHelpLayout)
        layout.addWidget(otherHelp)

        self.setLayout(layout)