import configparser
import math

def tisserand(sem_maj_axis_obj, inc, ecc, sem_maj_axis_planet=None):

    if not sem_maj_axis_planet:
        config = configparser.ConfigParser()
        config.read('_config/constants.ini')
        sem_maj_axis_planet = float(config['planets']['sem_maj_axis_jup'])
    
    tisserand_parameter = (sem_maj_axis_planet / sem_maj_axis_obj) + 2.0 * math.cos(inc) \
                          * math.sqrt((sem_maj_axis_obj / sem_maj_axis_planet) * (1.0 - ecc**2.0))
                          
    return tisserand_parameter