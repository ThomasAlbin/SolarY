"""
TBD

"""

import json
import math

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
    
        config = solary.auxiliary.config.get_constants()
        self._photon_flux_v = float(config['photometry']['photon_flux_V'])
    
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
    def hfdia(self):
        
        return self._hfdia
        
    @hfdia.setter
    def hfdia(self, halfflux_dia):
        
        self._hfdia = halfflux_dia
        
    @property
    def exposure_time(self):
        
        return self._exposure_time
    
    @exposure_time.setter
    def exposure_time(self, exp_time):
        self._exposure_time = exp_time
    
    @property
    def pixels_in_aperture(self):

        frac_pixels_in_aperture = math.pi * (0.5 * self.aperture) ** 2.0 / math.prod(self.ifov)
        
        pixels_in_aperture = int(round(frac_pixels_in_aperture, 0))

        return pixels_in_aperture

    @property
    def _ratio_light_aperture(self):
        sigma = solary.general.geometry.fwhm2std(self.hfdia)
        
        _ratio = math.erf(self.aperture / (sigma * math.sqrt(2))) ** 2.0

        return _ratio
    
    def object_esignal(self, mag):

        obj_sig_aper = 10.0 ** (-0.4 * mag) * self._photon_flux_v * self.exposure_time \
            * self.collect_area * self._ratio_light_aperture * self.quantum_eff * self.optical_throughput
        
        obj_sig_aper = round(obj_sig_aper, 0)
        
        return obj_sig_aper

    def sky_esignal(self, mag_arcsec_sq):
        
        total_sky_mag = solary.general.photometry.surmag2intmag(surmag=mag_arcsec_sq, \
                                                                area=math.prod(self.fov))
        
        sky_sig_aper = 10.0 ** (-0.4 * total_sky_mag) * self._photon_flux_v * self.exposure_time \
            * self.collect_area * (self.pixels_in_aperture / math.prod(self.pixels)) \
            * self.quantum_eff * self.optical_throughput

        sky_sig_aper = round(sky_sig_aper, 0)

        return sky_sig_aper
    
    @property
    def dark_esignal_aperture(self):
        
        dark_sig_aper = self.dark_noise * self.exposure_time * self.pixels_in_aperture

        dark_sig_aper = round(dark_sig_aper, 0)

        return dark_sig_aper
    
    def object_snr(self, obj_mag, sky_mag_arcsec_sq):
        
        signal = self.object_esignal(mag=obj_mag)
        noise = math.sqrt(signal + self.sky_esignal(mag_arcsec_sq=sky_mag_arcsec_sq)
                          + self.dark_esignal_aperture)
        
        snr = signal/noise
        
        return snr





