import solary

def test_get_constants():
    
    constant_config = solary.auxiliary.config.get_constants()
    
    constant_config_sections = constant_config.sections()
    
    assert 'constants' in constant_config_sections

def test_get_paths():
    
    paths_config = solary.auxiliary.config.get_paths()
    
    paths_config_sections = paths_config.sections()
    
    assert 'neo' in paths_config_sections