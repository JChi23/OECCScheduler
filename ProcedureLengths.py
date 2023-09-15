from enum import Enum  

class Procedures(Enum):
    PHACO = "Regular" #1.0
    LASIK = "Laser"
    GONIOTOMY = "Laser"
    GONIOSYNECHIALYSIS = "Laser"
    FEMTO = "Laser" #FEMTO, LENSX, LASIK are all the same (laser)
    LENSX = "Laser"
    ORA = "Laser" #.25
    CANALOPLASTY = "Laser"
    STENT = "Laser"
    PANOPTIX = "Premium"
    MICROPULSE = "Premium"
    VIVITY = "Premium"
    TORIC = "Premium"
    XEN_GEL_STENT = "Custom 3.0"
    TRABECULECTOMY = "Custom 3.0"
    SHUNT = "Custom 4.0"

class ProcedureIDs(Enum):
    EMPTY = 0
    BREAK = 1
    CUSTOM = 2
    REGULAR = 3
    LASER = 4
    PREMIUM = 5