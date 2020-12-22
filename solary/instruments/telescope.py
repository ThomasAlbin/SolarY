"""
TBD

"""

import json

# Import solary
import solary


def read_optical_config(config_filepath):
    
    with open(config_filepath) as temp_obj:
        optics_config = json.load(temp_obj)

    return optics_config


class Optical:
    
    
    def __init__(self, optics_config):
        
        valid_keys = ['main_mirror_dia', 'sec_mirror_dia', 'optical_throughput', 'focal_length']
        for key in valid_keys:
            setattr(self, key, optics_config.get(key))


    @property
    def main_mirror_area(self):
        
        return solary.general.geometry.circle_area(self.main_mirror_dia / 2.0)


    @property
    def sec_mirror_area(self):
        
        return solary.general.geometry.circle_area(self.sec_mirror_dia / 2.0)


    @property
    def collect_area(self):
        
        return self.main_mirror_area - self.sec_mirror_area