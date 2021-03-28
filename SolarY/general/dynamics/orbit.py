from dataclasses import dataclass
import datetime
import typing as t

from . import properties

@dataclass
class Orbit:
    
    rp: float
    ecc: float
    inc: float
    lnode: float
    argp: float
#    m0: float
#    t0: t.Union[float, str, datetime.datetime]
    
    ref: str
    grav_param: float
    
    @property
    def semi_maj_axis(self) -> float:
        
        _semi_maj_axis = self.peri / (1.0 - self.ecc)

        return _semi_maj_axis

    @property    
    def apo(self) -> float:
        
        _apo = properties.kep_apoapsis(sem_maj_axis=self.semi_maj_axis, ecc=self.ecc)
        
        return _apo
    
@dataclass
class State:
    
    pos_x: float
    pox_y: float
    pos_z: float
    vel_x: float
    vel_y: float
    vel_z: float
    
    t0: t.Union[float, str, datetime.datetime]

    ref: str
    grav_param: float