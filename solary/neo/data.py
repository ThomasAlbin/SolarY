import urllib.request
import os
import time

def download(filename='_data/neo_data_neodys.cat', integrity_chk=True):
    
    downl_file_path, _ = \
        urllib.request.urlretrieve(url='https://newton.spacedys.com/~neodys2/neodys.cat', \
                                   filename=filename)
    
    system_time = time.time()
    file_mod_time = os.path.getmtime(downl_file_path)
    
    file_mod_diff = file_mod_time - system_time
    if file_mod_diff < 5:
        dl_status = 'OK'
    else:
        dl_status = 'ERROR'
    
    return dl_status