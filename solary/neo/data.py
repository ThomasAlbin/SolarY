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

        download_filename = os.path.join(os.getcwd(), download_path, FILENAME)

        
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

def read(path=None):
    
    FILENAME = 'neodys.cat'

    if not path:

        module_path = os.path.dirname(__file__)
        path_filename = os.path.join(module_path, '_data', FILENAME)

    else:
        
        path_filename = os.path.join(os.getcwd(), path, FILENAME)

    neo_dict = []
    with open(path_filename) as f_temp:
        neo_data = f_temp.readlines()[6:]
        
        for neo_data_line_f in neo_data:
            neo_data_line = neo_data_line_f.split()
            neo_dict.append({'Name': neo_data_line[0].replace('\'', ''), \
                             'Epoch_[MJD]': float(neo_data_line[1]), \
                             'Sem-Maj_Axis_[AU]': float(neo_data_line[2]), \
                             'Ecc_[]': float(neo_data_line[3]), \
                             'Incl_[deg]': float(neo_data_line[4]), \
                             'Long_Asc_Node_[deg]': float(neo_data_line[5]), \
                             'Arg_P_[deg]': float(neo_data_line[6]), \
                             'Mean_Anom_[deg]': float(neo_data_line[7]), \
                             'Abs_Mag_[]': float(neo_data_line[8]), \
                             'Slope_Param_G_[]': float(neo_data_line[9])})

    return neo_dict

class neodys_database:
    
    def __init__(self, db_name):
        
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        
    def close(self):
        
        self.con.close()