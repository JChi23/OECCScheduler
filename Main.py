import sys, os

from Scheduler import Window
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    basedir = os.path.dirname(__file__)


    app = QApplication(sys.argv)

    try:
        with open(os.path.join(basedir, "resources", "SavedSchedule.txt"), "r+") as scheduleFile:
            savedSchedule = scheduleFile.read().splitlines()
    except:
        print("Could not open file")
        savedSchedule = ['0']

    w = Window(saved=savedSchedule, baseDir=basedir)
    w.show()

    app.exec()