import urllib.request
import os
import re
import sqlite3
import time

def _get_neodys_neo_nr():

    http_response = urllib.request.urlopen('https://newton.spacedys.com/neodys/index.php?pc=1.0')

    html_content = http_response.read()

    neodys_nr_neos = int(re.findall(r'<b>(.*?) objects</b> in the NEODyS', str(html_content))[0])

    return neodys_nr_neos

def download(download_path=None, row_exp=None):
    
    FILENAME = 'neodys.cat'

    if not download_path:

        module_path = os.path.dirname(__file__)
        download_filename = os.path.join(module_path, '_data', FILENAME)
        
    else:

        download_filename = os.path.join(download_path, '_data', FILENAME)

        
    downl_file_path, _ = \
        urllib.request.urlretrieve(url='https://newton.spacedys.com/~neodys2/neodys.cat', \
                                   filename=download_filename)
    
    system_time = time.time()
    file_mod_time = os.path.getmtime(downl_file_path)
    
    file_mod_diff = file_mod_time - system_time
    
    if file_mod_diff < 5:
        dl_status = 'OK'
    else:
        dl_status = 'ERROR'

    neodys_neo_nr = None
    if row_exp:
        neodys_neo_nr = _get_neodys_neo_nr()

    return dl_status, neodys_neo_nr

class neodys_database:
    
    def __init__(self, db_name):
        
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        
    def close(self):
        
        self.con.close()