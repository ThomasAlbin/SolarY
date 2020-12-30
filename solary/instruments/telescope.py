"""
TBD

"""

import json

# Import solary
import solary

from . import camera
from . import optics

def comp_fov(sensor_dim, focal_length):
    
    # https://www.celestron.com/blogs/knowledgebase/
    # how-do-i-determine-the-field-of-view-for-my-ccd-chip-and-telescope
    
    return (3436.62 * sensor_dim / focal_length) * 60.0
    

class ReflectorCCD(optics.Reflector, camera.CCD):
    
    def __init__(self, optics_config, ccd_config):
        
        optics.Reflector.__init__(self, optics_config)
        camera.CCD.__init__(self, ccd_config)
    
    @property
    def fov(self):
        
        fov_res = []
        for chip_dim in self.chip_size:
            fov_res.append(comp_fov(sensor_dim=chip_dim, focal_length=self.focal_length*1000.0))
        
        return fov_res
    
    @property
    def ifov(self):
        
        ifov_res = []
        for fov_dim, pixel_dim in zip(self.fov, self.pixels):
            ifov_res.append(fov_dim / pixel_dim)
        
        return ifov_res
    
    @property
    def aperture(self):
        
        return self._aperture
        
    @aperture.setter
    def aperture(self, apert):
        
        self._aperture = apert
        
    @property
    def exposure_time(self):
        
        return self._exposure_time
    
    @exposure_time.setter
    def exposure_time(self, exp_time):
        self._exposure_time = exp_time
    
    # def _comp_electrons_total(self, mag):
        
        
    
    