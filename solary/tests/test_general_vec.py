import math

import pytest
import solary

def test_norm():

    vec_norm_res1 = solary.general.vec.norm(vector=[1.0, 0.0])
    assert vec_norm_res1 == 1.0

    vec_norm_res2 = solary.general.vec.norm(vector=[1.0, 1.0])
    assert vec_norm_res2 == math.sqrt(2)

    vec_norm_res3 = solary.general.vec.norm(vector=[5.0, 4.0])
    assert vec_norm_res3 == math.sqrt(41)

    vec_norm_res4 = solary.general.vec.norm(vector=[1.0, 1.0, 1.0])
    assert vec_norm_res4 == math.sqrt(3)

    vec_norm_res5 = solary.general.vec.norm(vector=[2.0, 4.0, -5.0, 6.0])
    assert vec_norm_res5 == 9.0

def test_unify():
    
    unit_vec1 = solary.general.vec.unify(vector=[1.0, 0.0, 0.0])
    assert unit_vec1 == [1.0, 0.0, 0.0]
    
    unit_vec2 = solary.general.vec.unify(vector=[5.0, 0.0, 0.0])
    assert unit_vec2 == [1.0, 0.0, 0.0]
    
    unit_vec3 = solary.general.vec.unify(vector=[5.0, 5.0, 5.0])
    assert pytest.approx(unit_vec3) == [1.0 / math.sqrt(3), 1.0 / math.sqrt(3), 1.0 / math.sqrt(3)]