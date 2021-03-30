from dataclasses import dataclass
import dataclasses
import datetime
import typing as t

from . import properties
from ... import auxiliary as solary_auxiliary

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
    
    def state_vec(self, m0, t0):
        
        generic_kernel_info = solary_auxiliary.config.get_spice_kernels('generic')