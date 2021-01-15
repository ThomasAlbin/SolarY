"""
reader.py

Auxiliary reader for miscellaneous files.

"""

# Import standard libraries
import json

def read_orbit(orbit_path):
    """
    Function to read an orbit properties file.

    Parameters
    ----------
    orbit_path : str
        File path of the JSON file that contains the properties information.

    Returns
    -------
    orbit_values : dict
        Orbit values.
    orbit_units : dict
        Orbit units.

    """

    # Open the file path and load / read it as a JSON
    with open(orbit_path) as temp_obj:
        orbit_compl = json.load(temp_obj)

    #TODO: check if values and units are in json and then check if the keys are correct

    # Get the values and units dictionaries within the JSON file
    orbit_values = orbit_compl['values']
    orbit_units = orbit_compl['units']

    return orbit_values, orbit_units
