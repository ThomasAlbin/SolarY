from dataclasses import dataclass, field
import dataclasses
import datetime
import typing as t

import spiceypy

from . import properties

naif_ids = {'SSB': 0,
            'Sun': 10}


@dataclass
class Orbit:
    
    rp: float
    ecc: float
    inc: float
    lnode: float
    argp: float
    
    ref: str
    center: str
    grav_param: float
    
    @classmethod
    def from_instance(cls, instance):
        return cls(**dataclasses.asdict(instance))

    @property
    def semi_maj_axis(self) -> float:
        
        _semi_maj_axis = self.rp / (1.0 - self.ecc)

        return _semi_maj_axis

    @property    
    def apo(self) -> float:
        
        _apo = properties.kep_apoapsis(sem_maj_axis=self.semi_maj_axis, ecc=self.ecc)
        
        return _apo
    
    @property
    def center_id(self) -> int:
        
        _center_id = naif_ids.get(self.center, None)
        
        return _center_id


@dataclass
class State:
    
    position_vec: [float, float, float]
    velocity_vec: [float, float, float]
    
    t0: t.Union[float, str, datetime.datetime]

    ref: str
    grav_param: float



@dataclass
class Object(Orbit):
    
    m0: float
    _m0: float = field(init=False, repr=False)
    t0: str
    _t0: str = field(init=False, repr=False)

    @property
    def m0(self) -> float:
        
        return self._m0

    @m0.setter
    def m0(self, value: float) -> None:

        self._m0 = value

    @property
    def t0(self) -> float:
        
        return self._t0
  

    @t0.setter
    def t0(self, value: str) -> None:

        self._t0 = value  
  
    @property
    def t0_ephem(self):
        
        _t0_ephem = properties.time2et(self.t0)
    
        return _t0_ephem

    # @property
    # def state_vec(self, m0, t0):
        
    #     _state_vec = spiceypy.conics()
        
    #     return _state_vec
        
        
        