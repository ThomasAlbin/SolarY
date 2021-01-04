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
    """
    Class of a reflector telescope with a CCD camera system. This class loads config files and sets
    attributes of a telescope system. Further, one can set observationsl settings like e.g., the
    exposure time. Functions allow one to compute the Signal-To-Noise ratio of an object.

    Since this class is build on the Reflector and CCD class, please check "See Also" to see the
    class references. These base classes contain more attributes, properties, etc. and can be read
    in the corresponding docstring.

    Attributes
    ----------
    _photo_flux_v : float
        Photon flux of a 0 mag star in V-Band.

    Static Properties
    -----------------
    fov : list
        FOV values (x and y dimension of the CCD chip). Given in arcsec.
    ifov_res : list
        iFOV values (x and y dimension of the CCD chip). Given in arcsec / pixel.

    Dynamic Properties
    ------------------
    aperture : float
        Aperture for photometric / astrometric purposes. Given in arcsec.
    hfdia : float
        Half Flux Diameter. Given in arcsec.
    exposure_time : float
        Exposure time. Given in s.
    pixels_in_aperture : int
        Number of pixels within the aperture (rounded).
    dark_esignal_aperture : float
        Number of dark current electrons.

    Methods
    -------
    object_esignal(mag)
        Compute the number of CCD electrons that are created by the object's brightness within the
        photometric aperture.
    sky_esignal(mag_arcsec_sq)
        Compute the number of CCD electrons that are created by the background sky brighness within
        the photometric aperture (considering only the included pixels).
    object_snr(obj_mag, sky_mag_arcsec_sq)
        Compute the Signal-To-Noise ratio of an object.

    See Also
    --------
    solary.instruments.optics.Reflector
    solary.instruments.camera.CCD

    """


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
        Get the number of pixels within the photometric aperture.

        Returns
        -------
        pixels_in_aperture : int
            Number of pixels within the aperture (rounded).

        """

        # Number of pixels corresponds to the aperture area (assuming a cirlce) divided by the iFOV
        frac_pixels_in_aperture = solary.general.geometry.circle_area(0.5 * self.aperture) \
                                  / math.prod(self.ifov)

        # Round the result
        pixels_in_aperture = int(round(frac_pixels_in_aperture, 0))

        return pixels_in_aperture


    @property
    def _ratio_light_aperture(self):
        """
        Get the ratio of light that is collected within the photometric aperture.
        Assumption: the light of an object is Gaussian distributed (in both directions equally);
                    the ration within the photometric aperture can be perfectly described by the
                    error functon.

        Returns
        -------
        _ratio : float
            Ratio of light within the photometric aperture. Value between 0 and 1.

        """

        # Compute the Gaussian standard deviation of the half flux diameter in arcsec
        sigma = solary.general.geometry.fwhm2std(self.hfdia)

        # Compute the ratio, using the error function, the photometric aperture and half flux
        # diameter corresponding standard deviation
        _ratio = math.erf(self.aperture / (sigma * math.sqrt(2))) ** 2.0

        return _ratio


    def object_esignal(self, mag):
        """
        Function to compute the number of the object's corresponding electrons that are created
        within the photometric aperture on the CCD.

        Parameters
        ----------
        mag : float
            Brightness of the object in V-Band. Given in mag.

        Returns
        -------
        obj_sig_aper : float
            Number of electrons that are created within the aperture.

        """

        # Compute the number of electrons:
        #    1. Scale by the magnitude
        #    2. Multiply by the photon flux in V-band
        #    3. Multiply by the exposure time in seconds
        #    4. Multiply by the telescope's collection area
        #    5. Multiply by the light ratio within the aperture
        #    6. Multiply by the quantum efficiency
        #    7. Multiply by the optical throughput
        obj_sig_aper = 10.0 ** (-0.4 * mag) \
                       * self._photon_flux_v \
                       * self.exposure_time \
                       * self.collect_area \
                       * self._ratio_light_aperture \
                       * self.quantum_eff \
                       * self.optical_throughput

        # Round the result
        obj_sig_aper = round(obj_sig_aper, 0)

        return obj_sig_aper


    def sky_esignal(self, mag_arcsec_sq):
        """
        Function to compute the number of electrons within the photometric aperture caused by the
        background sky brightness.

        Parameters
        ----------
        mag_arcsec_sq : float
            Background sky brightness in V-Band. Given in mag/arcsec^2

        Returns
        -------
        sky_sig_aper : float
            Number of electrons that are created within the aperture.

        """

        # First, convert the sky surface brightness to an integrated brightness (apply the complete
        # telescope's collection area)
        total_sky_mag = solary.general.photometry.surmag2intmag(surmag=mag_arcsec_sq, \
                                                                area=math.prod(self.fov))

        # Compute the number of electrons:
        #    1. Scale by the magnitude
        #    2. Multiply by the photon flux in V-band
        #    3. Multiply by the exposure time in seconds
        #    4. Multiply by the telescope's collection area
        #    5. Multiply by the number of pixels within the aperture w.r.t. the total number of
        #       pixels (discrete ratio)
        #    6. Multiply by the quantum efficiency
        #    7. Multiply by the optical throughput
        sky_sig_aper = 10.0 ** (-0.4 * total_sky_mag) \
                       * self._photon_flux_v \
                       * self.exposure_time \
                       * self.collect_area \
                       * (self.pixels_in_aperture / math.prod(self.pixels)) \
                       * self.quantum_eff \
                       * self.optical_throughput

        # Round the result
        sky_sig_aper = round(sky_sig_aper, 0)

        return sky_sig_aper


    @property
    def dark_esignal_aperture(self):
        """
        Get the number of dark current induced electrons within the aperture

        Returns
        -------
        dark_sig_aper : float
            Number of dark current electrons.

        """

        # Compute the number of dark current electrons (Noise * exposure time * number of pixels
        # within the photometric aperture)
        dark_sig_aper = self.dark_noise * self.exposure_time * self.pixels_in_aperture

        # Round the result
        dark_sig_aper = round(dark_sig_aper, 0)

        return dark_sig_aper


    def object_snr(self, obj_mag, sky_mag_arcsec_sq):
        """
        Compute the Signal-To-Noise ratio (SNR) of an object.

        Parameters
        ----------
        obj_mag : float
            Object brightness. Given in mag.
        sky_mag_arcsec_sq : float
            Background sky brightness. Given in mag/arcsec^2.

        Returns
        -------
        snr : float
            SNR of the object.

        """

        # Compute the signal of the object (electrons within the photometric aperture)
        signal = self.object_esignal(mag=obj_mag)

        # Compute the noise
        noise = math.sqrt(signal
                          + self.sky_esignal(mag_arcsec_sq=sky_mag_arcsec_sq)
                          + self.dark_esignal_aperture)

        # Determine the SNR
        snr = signal/noise

        return snr
