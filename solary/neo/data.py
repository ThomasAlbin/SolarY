import gzip
import hashlib
import urllib.parse
import urllib.request
import os
import re
import shutil
import sqlite3
import time

import solary

def _comp_md5(file_name):

    hash_md5 = hashlib.md5()
    
    with open(file_name, 'rb') as f_temp:
        for _seq in iter(lambda: f_temp.read(65536), b''):
            hash_md5.update(_seq)

    return hash_md5.hexdigest()


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


def read_neodys(path=None):
    
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
                             'Epoch_MJD': float(neo_data_line[1]), \
                             'SemMajAxis_AU': float(neo_data_line[2]), \
                             'Ecc_': float(neo_data_line[3]), \
                             'Incl_deg': float(neo_data_line[4]), \
                             'LongAscNode_deg': float(neo_data_line[5]), \
                             'ArgP_deg': float(neo_data_line[6]), \
                             'MeanAnom_deg': float(neo_data_line[7]), \
                             'AbsMag_': float(neo_data_line[8]), \
                             'SlopeParamG_': float(neo_data_line[9])})

    return neo_dict


class neodys_database:
    
    def __init__(self, db_filepath=None, new=False):

        if not db_filepath:
    
            module_path = os.path.dirname(__file__)
            self.db_filename = os.path.join(module_path, '_databases', 'neo_neodys.db')
    
        else:
            
            self.db_filename = os.path.join(os.getcwd(), db_filepath, 'neo_neodys.db')

        
        if new and os.path.exists(self.db_filename):
            os.remove(self.db_filename)

        self.con = sqlite3.connect(self.db_filename)
        self.cur = self.con.cursor()

    def _create_col(self, table, col_name, col_type):
        
        sql_col_create = f'ALTER TABLE {table} ADD COLUMN {col_name} {col_type}'
        
        try:
            self.cur.execute(sql_col_create)
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def create(self, neodys_path):
        
        self.cur.execute('CREATE TABLE IF NOT EXISTS main(Name TEXT PRIMARY KEY, ' \
                                                         'Epoch_MJD FLOAT, ' \
                                                         'SemMajAxis_AU FLOAT, ' \
                                                         'Ecc_ FLOAT, ' \
                                                         'Incl_deg FLOAT, ' \
                                                         'LongAscNode_deg FLOAT, ' \
                                                         'ArgP_deg FLOAT, ' \
                                                         'MeanAnom_deg FLOAT, ' \
                                                         'AbsMag_ FLOAT, ' \
                                                         'SlopeParamG_ FLOAT)')

        self.con.commit()

        _neo_data = read_neodys(neodys_path)

        self.cur.executemany('INSERT OR IGNORE INTO main(Name, ' \
                                                        'Epoch_MJD, ' \
                                                        'SemMajAxis_AU, ' \
                                                        'Ecc_, ' \
                                                        'Incl_deg, ' \
                                                        'LongAscNode_deg, ' \
                                                        'ArgP_deg, ' \
                                                        'MeanAnom_deg, ' \
                                                        'AbsMag_, ' \
                                                        'SlopeParamG_) ' \
                                                    'VALUES (:Name, ' \
                                                            ':Epoch_MJD, ' \
                                                            ':SemMajAxis_AU, ' \
                                                            ':Ecc_, ' \
                                                            ':Incl_deg, ' \
                                                            ':LongAscNode_deg, ' \
                                                            ':ArgP_deg, ' \
                                                            ':MeanAnom_deg, ' \
                                                            ':AbsMag_, ' \
                                                            ':SlopeParamG_)', \
                             _neo_data)
        self.con.commit()

    def create_deriv_orb(self):
        
        self._create_col('main', 'Aphel_AU', 'FLOAT')
        self._create_col('main', 'Perihel_AU', 'FLOAT')

        self.cur.execute('SELECT Name, SemMajAxis_AU, Ecc_ FROM main')

        _neo_data = self.cur.fetchall()
        
        _neo_deriv_param_dict = []
        for _neo_data_line_f in _neo_data:
            _neo_deriv_param_dict.append({'Name': _neo_data_line_f[0], \
                                          'Aphel_AU': \
                                              solary.general.astrodyn.kep_apoapsis( \
                                                                sem_maj_axis=_neo_data_line_f[1], \
                                                                ecc=_neo_data_line_f[2] \
                                                                                  ), \
                                          'Perihel_AU': \
                                              solary.general.astrodyn.kep_periapsis( \
                                                                sem_maj_axis=_neo_data_line_f[1], \
                                                                ecc=_neo_data_line_f[2] \
                                                                                  )})
                
        self.cur.executemany('UPDATE main SET Aphel_AU = :Aphel_AU, Perihel_AU = :Perihel_AU ' \
                             'WHERE Name = :Name', _neo_deriv_param_dict)
        self.con.commit()

    def close(self):
        
        self.con.close()


def download_gravnik2018(download_path=None, comp_md5=True):

    FILENAME = r'Granvik+_2018_Icarus.dat.gz'

    if not download_path:

        module_path = os.path.dirname(__file__)
        download_filename = os.path.join(module_path, '_data', FILENAME)
        
    else:

        download_filename = os.path.join(os.getcwd(), download_path, FILENAME)

    url_location = 'https://www.mv.helsinki.fi/home/mgranvik/data/' \
                   'Granvik+_2018_Icarus/Granvik+_2018_Icarus.dat.gz'
    
    downl_file_path, _ = \
        urllib.request.urlretrieve(url=url_location, \
                                   filename=download_filename)
    
    system_time = time.time()
    file_mod_time = os.path.getmtime(downl_file_path)
    
    file_mod_diff = file_mod_time - system_time
    
    if file_mod_diff < 5:
        dl_status = 'OK'
    else:
        dl_status = 'ERROR'

    unzip_file_path = downl_file_path[:-3]
    with gzip.open(downl_file_path, 'r') as f_in, open(unzip_file_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    os.remove(downl_file_path)

    md5_hash = _comp_md5(unzip_file_path)
    
    return dl_status, md5_hash

def read_granvik2018(path=None):
    
    FILENAME = 'Granvik+_2018_Icarus.dat'

    if not path:

        module_path = os.path.dirname(__file__)
        path_filename = os.path.join(module_path, '_data', FILENAME)

    else:
        
        path_filename = os.path.join(os.getcwd(), path, FILENAME)

    neo_dict = []
    with open(path_filename) as f_temp:
        neo_data = f_temp.readlines()
        
        for neo_data_line_f in neo_data:
            neo_data_line = neo_data_line_f.split()
            neo_dict.append({'SemMajAxis_AU': float(neo_data_line[0]), \
                             'Ecc_': float(neo_data_line[1]), \
                             'Incl_deg': float(neo_data_line[2]), \
                             'LongAscNode_deg': float(neo_data_line[3]), \
                             'ArgP_deg': float(neo_data_line[4]), \
                             'MeanAnom_deg': float(neo_data_line[5]), \
                             'AbsMag_': float(neo_data_line[6])})

    return neo_dict

class gravnik2018_database:
    
    def __init__(self, db_filepath=None, new=False):

        if not db_filepath:
    
            module_path = os.path.dirname(__file__)
            self.db_filename = os.path.join(module_path, '_databases', 'neo_gravnik2018.db')
    
        else:
            
            self.db_filename = os.path.join(os.getcwd(), db_filepath, 'neo_gravnik2018.db')

        if new and os.path.exists(self.db_filename):
            os.remove(self.db_filename)

        self.con = sqlite3.connect(self.db_filename)
        self.cur = self.con.cursor()

    def _create_col(self, table, col_name, col_type):
        
        sql_col_create = f'ALTER TABLE {table} ADD COLUMN {col_name} {col_type}'
        
        try:
            self.cur.execute(sql_col_create)
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def create(self, granvik2018_path):
        
        self.cur.execute('CREATE TABLE IF NOT EXISTS main(ID INTEGER PRIMARY KEY, ' \
                                                         'SemMajAxis_AU FLOAT, ' \
                                                         'Ecc_ FLOAT, ' \
                                                         'Incl_deg FLOAT, ' \
                                                         'LongAscNode_deg FLOAT, ' \
                                                         'ArgP_deg FLOAT, ' \
                                                         'MeanAnom_deg FLOAT, ' \
                                                         'AbsMag_ FLOAT)')

        self.con.commit()
     
        _neo_data = read_granvik2018(granvik2018_path)

        self.cur.executemany('INSERT OR IGNORE INTO main(SemMajAxis_AU, ' \
                                                        'Ecc_, ' \
                                                        'Incl_deg, ' \
                                                        'LongAscNode_deg, ' \
                                                        'ArgP_deg, ' \
                                                        'MeanAnom_deg, ' \
                                                        'AbsMag_) ' \
                                                    'VALUES (:SemMajAxis_AU, ' \
                                                            ':Ecc_, ' \
                                                            ':Incl_deg, ' \
                                                            ':LongAscNode_deg, ' \
                                                            ':ArgP_deg, ' \
                                                            ':MeanAnom_deg, ' \
                                                            ':AbsMag_)', \
                             _neo_data)
        self.con.commit()

    def create_deriv_orb(self):
        
        self._create_col('main', 'Aphel_AU', 'FLOAT')
        self._create_col('main', 'Perihel_AU', 'FLOAT')

        self.cur.execute('SELECT ID, SemMajAxis_AU, Ecc_ FROM main')

        _neo_data = self.cur.fetchall()
        
        _neo_deriv_param_dict = []
        for _neo_data_line_f in _neo_data:
            _neo_deriv_param_dict.append({'ID': _neo_data_line_f[0], \
                                          'Aphel_AU': \
                                              solary.general.astrodyn.kep_apoapsis( \
                                                                sem_maj_axis=_neo_data_line_f[1], \
                                                                ecc=_neo_data_line_f[2] \
                                                                                  ), \
                                          'Perihel_AU': \
                                              solary.general.astrodyn.kep_periapsis( \
                                                                sem_maj_axis=_neo_data_line_f[1], \
                                                                ecc=_neo_data_line_f[2] \
                                                                                  )})
                
        self.cur.executemany('UPDATE main SET Aphel_AU = :Aphel_AU, Perihel_AU = :Perihel_AU ' \
                             'WHERE ID = :ID', _neo_deriv_param_dict)
        self.con.commit()

    def close(self):
        
        self.con.close()