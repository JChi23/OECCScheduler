from enum import Enum  

class Procedures(Enum):
    PHACO = "Regular" #1.0
    LASIK = "Laser"
    GONIOTOMY = "Laser"
    GONIOSYNECHIALYSIS = "Laser"
    FEMTO = "Laser"
    LENSX = "Laser"
    ORA = "Laser" #.25
    MICROPULSE = "Premium"
    VIVITY = "Premium"
    TORIC = "Premium"
    XEN_GEL_STENT = "Custom 3.0"
    TRABECULECTOMY = "Custom 3.0"

class ProcedureIDs(Enum):
    EMPTY = 0
    BREAK = 1
    CUSTOM = 2
    REGULAR = 3
    LASER = 4
    PREMIUM = 5