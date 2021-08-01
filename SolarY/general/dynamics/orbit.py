from dataclasses import dataclass, field
import dataclasses
import datetime
import typing as t

import spiceypy

from . import properties
from ... import auxiliary

naif_ids = {'SSB': 0,
            'Sun': 10}

class Orbit:
    
    def __init__(self, rp, ecc, inc, lnode, argp, ref, center, grav_param):
        self.rp = rp
        self.ecc = ecc
        self.inc = inc
        self.lnode = lnode
        self.argp = argp
        
        self.ref = ref
        self.center = center
        self.grav_param = grav_param
    
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


class State():
    
    def __init__(self, orbit: Orbit, m0, t0, et) -> None:
    
        auxiliary.config.load_spice_kernels(ktype="generic")    
    
        self._orbit = orbit
        self._m0 = m0
        self._t0 = t0
        self._et = et
        
    @property
    def orbit(self) -> Orbit:
        """Get the CCD Orbit instance."""
        return self._orbit
        
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

    @property
    def et(self) -> float:
        
        return self._et
  

    @et.setter
    def et(self, value: str) -> None:

        self._et = value  
  
    @property
    def et_ephem(self):
        
        _et_ephem = properties.time2et(self.et)
    
        return _et_ephem

    @property
    def state_vec(self):


        _state_vec = spiceypy.conics(elts=[self._orbit.rp, \
                                      self.orbit.ecc, \
                                      self.orbit.inc, \
                                      self.orbit.lnode, \
                                      self.orbit.argp, \
                                      self.m0, \
                                      self.t0_ephem, \
                                      self.orbit.grav_param,],
                                     et=self.et_ephem)

        return _state_vec
        
        
        