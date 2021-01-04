"""
telescope.py

Script that contains telescope classes that mostly consists of base classes (e.g., optical systems
                                                                             cameras, etc.)

"""

# Import standard libraries
import math

# Import solary
import solary

# Import the camera and optics script from the same directory
from . import camera
from . import optics


def comp_fov(sensor_dim, focal_length):
    """
    Compute the Field-Of-View (FOV) depending on a camera's chip size and telescope's focal length.
    See [1].

    Parameters
    ----------
    sensor_dim : float
        Sensor size (e.g., x or y dimension). Given in mm.
    focal_length : float
        Focal length of the telescope. Given in mm.

    Returns
    -------
    fov_arcsec : float
        Resulting FOV. Given in arcsec.

    References
    ----------
    [1] https://www.celestron.com/blogs/knowledgebase/
        how-do-i-determine-the-field-of-view-for-my-ccd-chip-and-telescope; 04.Jan.2021

    """

    # Compute the FOV. The equation, provided by [1], has been converted from imperial to SI.
    fov_arcsec = (3436.62 * sensor_dim / focal_length) * 60.0

    return fov_arcsec


class ReflectorCCD(optics.Reflector, camera.CCD):

    def __init__(self, optics_config, ccd_config):
        """
        Init function.

        Parameters
        ----------
        optics_config : dict
            Reflector config.
        ccd_config : dict
            CCD config.

        Returns
        -------
        None.
        
        See also
        --------
        solary.instruments.optics.Reflector :
            The Reflector base class that contains the optics attributes and properties.
        solary.instruments.camera.CCD : 
            The CCD base class that contains the camera attributes and properties.

        """

        # Init the optics and camera classes accordingly
        optics.Reflector.__init__(self, optics_config)
        camera.CCD.__init__(self, ccd_config)

        # Load the constants config file and get the photon flux (Given in m^-2 * s^-1)
        config = solary.auxiliary.config.get_constants()
        self._photon_flux_v = float(config['photometry']['photon_flux_V'])


    @property
    def fov(self):
        """
        Get the Field-Of-View (FOV) of the telescope in x and y dimensions.

        Returns
        -------
        fov_res : list
            FOV values (x and y dimension of the CCD chip). Given in arcsec.

        """

        # Placholder list for the results
        fov_res = []

        # Iterate through the chip size list (given in mm) and multiply the focal length that is
        # given in meters with 1000 to convert it to mm.
        for chip_dim in self.chip_size:
            fov_res.append(comp_fov(sensor_dim=chip_dim, focal_length=self.focal_length*1000.0))

        return fov_res


    @property
    def ifov(self):
        """
        Get the individual Field-Of-View (iFOV). The iFOV is the FOV that applies for each pixel.

        Returns
        -------
        ifov_res : list
            iFOV values (x and y dimension of the CCD chip). Given in arcsec / pixel.

        """

        # Placeholder list for the iFOV results
        ifov_res = []

        # Iterate through the FOV values and number of pixels. Divide the FOV dimension by the
        # corresponding number of pixels
        for fov_dim, pixel_dim in zip(self.fov, self.pixels):
            ifov_res.append(fov_dim / pixel_dim)

        return ifov_res


    @property
    def aperture(self):
        """
        Get the aperture.

        Returns
        -------
        float
            Photometry aperture. Given in arcsec.

        """

        return self._aperture


    @aperture.setter
    def aperture(self, apert):
        """
        Set the aperture

        Parameters
        ----------
        apert : float
            Aperture for photometric / astrometric purposes. Given in arcsec.

        Returns
        -------
        None.

        """

        self._aperture = apert


    @property
    def hfdia(self):
        """
        Get the half flux diameter of an object / star.

        Returns
        -------
        float
            Half Flux Diameter. Given in arcsec.

        """

        return self._hfdia


    @hfdia.setter
    def hfdia(self, halfflux_dia):
        """
        Set the half flux diameter of an object / star.

        Parameters
        ----------
        halfflux_dia : float
            Half Flux Diameter. Given in arcsec.

        Returns
        -------
        None.

        """

        self._hfdia = halfflux_dia


    @property
    def exposure_time(self):
        """
        Get the exposure time.

        Returns
        -------
        float
            Exposure time. Given in s.

        """

        return self._exposure_time


    @exposure_time.setter
    def exposure_time(self, exp_time):
        """
        Set the exposure time.

        Parameters
        ----------
        exp_time : float
            Exposure time. Given in s.

        Returns
        -------
        None.

        """

        self._exposure_time = exp_time


    @property
    def pixels_in_aperture(self):
        """
        

        Returns
        -------
        pixels_in_aperture : TYPE
            DESCRIPTION.

        """
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
