import math

import solary

def test_tisserand():
    
    tisserand_parameter1 = solary.general.astrodyn.tisserand(sem_maj_axis_obj = 5.0, \
                                                             inc = 0.0, \
                                                             ecc = 0.0)
    assert tisserand_parameter1 == 3.001200087241328

    tisserand_parameter2 = solary.general.astrodyn.tisserand(sem_maj_axis_obj = 4.0, \
                                                             inc = 0.0, \
                                                             ecc = 0.65)
    assert tisserand_parameter2 == 2.633422691976387
    
    tisserand_parameter3 = solary.general.astrodyn.tisserand(sem_maj_axis_obj = 4.0, \
                                                             inc = math.radians(30.0), \
                                                             ecc = 0.65)
    assert tisserand_parameter3 == 2.454890564710888

    tisserand_parameter4 = solary.general.astrodyn.tisserand(sem_maj_axis_obj = 4.0, \
                                                             inc = math.radians(30.0), \
                                                             ecc = 0.65, \
                                                             sem_maj_axis_planet = 3.0)
    assert tisserand_parameter4 == 2.2698684153570663