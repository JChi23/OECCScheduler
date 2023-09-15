from enum import Enum  
from PyQt6.QtGui import QColor

class BlockColors(Enum):
    REGULAR = QColor(69, 166, 171)
    LASER = QColor(198, 120, 117)
    PREMIUM = QColor(221, 152, 41)
    CUSTOM = QColor(121, 168, 121)
    BREAK = QColor(145, 146, 97)
    TRABECULECTOMY = QColor(158, 121, 173)
    VIVITY = QColor(194, 193, 122)
    TORIC_ORA = QColor(194, 138, 190)
    GONIOTOMY = QColor(107, 130, 90)
    MICROPULSE = QColor(156, 92, 161)
    CANALOPLASTY = QColor(118, 158, 184)
    STENT = QColor(119, 189, 181)
    SHUNT = QColor(196, 163, 106)
    PANOPTIX = QColor(178, 142, 232)
    XEN = QColor(212, 70, 93)