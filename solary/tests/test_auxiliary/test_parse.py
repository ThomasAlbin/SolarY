import os

import solary

def test_comp_md5():
    
    mockup_file = 'mockup.txt'
    open(mockup_file, 'wb').close()
    
    md5_mockup = solary.auxiliary.parse.comp_md5(mockup_file)
    
    assert 'd41d8cd98f00b204e9800998ecf8427e' == md5_mockup

    os.remove(mockup_file)
