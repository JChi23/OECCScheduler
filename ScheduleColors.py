from enum import Enum  
from PyQt6.QtGui import QColor

class BlockColors(Enum):
    REGULAR = QColor(69, 166, 171)
    LASER = QColor(198, 120, 117)
    PREMIUM = QColor(221, 152, 41)
    CUSTOM = QColor(125, 125, 125)
    BREAK = QColor(145, 146, 97)