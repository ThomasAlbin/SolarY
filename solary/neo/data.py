"""
data.py

NEO data download, parsing and database creation functions are part of this sub-module.

"""

# Import standard libraries
import gzip
import urllib.parse
import urllib.request
import os
import re
import shutil
import sqlite3
import time

# Import SolarY
import solary

def _get_neodys_neo_nr():
    """
    This function gets the number of currently known NEOs from the NEODyS webpage. The information
    is obtained by a Crawler-like script that may need frequent maintenance.

    Returns
    -------
    neodys_nr_neos : int
        Number of catalogued NEOs in the NEODyS database.

    """

    # Open the NEODyS link, where the current number of NEOs is shown
    http_response = urllib.request.urlopen('https://newton.spacedys.com/neodys/index.php?pc=1.0')

    # Get the HTML response and read its content
    html_content = http_response.read()

    # Extract the number of NEOs from a specific HTML position, using a regular expression. The
    # number is displayed in bold like "[...] <b>1000 objects</b> in the NEODys [...]"
    neodys_nr_neos = int(re.findall(r'<b>(.*?) objects</b> in the NEODyS', str(html_content))[0])

    return neodys_nr_neos


def download(row_exp=None):
    """
    This function downloads a file with the orbital elements of currently all known NEOs from the
    NEODyS database. The file has the ending .cat and is basically a csv / ascii formatted file
    that can be read by any editor.

    Parameters
    ----------
    row_exp : bool, optional
        Boolean value. If the input is set to True the number of NEOs that are listed in the
        downloaded file are compared with the number of expected NEOs (number of NEOs listed on the
        NEODyS page). The default is None.

    Returns
    -------
    dl_status : str
        Human-readable status report that returns 'OK' or 'ERROR', depending on the download's
        success.
    neodys_neo_nr : int
        Number of NEOs (from the NEODyS page and thus optional). This value can be compared with
        the content of the downloaded file to determine whether entries are missing or not. Per
        default None is returned.

    """

    # Set the complete filepath. The file is stored in the user's home directory
    download_filename = solary.auxiliary.parse.setnget_file_path('solary_data/neo/data', \
                                                                 'neodys.cat')

    # Download the file
    downl_file_path, _ = \
        urllib.request.urlretrieve(url='https://newton.spacedys.com/~neodys2/neodys.cat', \
                                   filename=download_filename)

    # To check whether the file has been successfully updated (if a file was present before) one
    # needs to compare the "last modification time" of the file with the current system's time. If
    # the deviation is too high, it is very likely that no new file has been downloaded and
    # consequently updated
    system_time = time.time()
    file_mod_time = os.path.getmtime(downl_file_path)
    file_mod_diff = file_mod_time - system_time

    # Set status message, if the file has been updated or not. A time difference of less than 5 s
    # shall indicate whether the file is new or not
    if file_mod_diff < 5:
        dl_status = 'OK'
    else:
        dl_status = 'ERROR'

    # Optional: Get the number of expected NEOs from the NEODyS webpage
    neodys_neo_nr = None
    if row_exp:
        neodys_neo_nr = _get_neodys_neo_nr()

    return dl_status, neodys_neo_nr


def read_neodys():
    """
    Read the content of the downloaded NEODyS file and return a dictionary with its content.

    Returns
    -------
    neo_dict : dict
        Dictionary that contains the NEO data from the NEODyS download.

    """

    # Set the download file path. The file shall be stored in the home direoctry
    path_filename = solary.auxiliary.parse.setnget_file_path('solary_data/neo/data', 'neodys.cat')

    # Set a placeholder dictionary where the data will be stored
    neo_dict = []

    # Open the NEODyS file. Ignore the header (first 6 rows) and iterate through the file row-wise.
    # Read the content adn save it in the dictionary
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


class NEOdysDatabase:

    def __init__(self, new=False):

        self.db_filename = solary.auxiliary.parse.setnget_file_path('solary_data/neo/databases', \
                                                                    'neo_neodys.db')


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

    def create(self):

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

        _neo_data = read_neodys()

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


def download_granvik2018():

    download_filename = solary.auxiliary.parse.setnget_file_path('solary_data/neo/data', \
                                                                 'Granvik+_2018_Icarus.dat.gz')

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

    md5_hash = solary.auxiliary.parse.comp_md5(unzip_file_path)

    return dl_status, md5_hash

def read_granvik2018():

    path_filename = solary.auxiliary.parse.setnget_file_path('solary_data/neo/data', \
                                                             'Granvik+_2018_Icarus.dat')

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

class Granvik2018Database:

    def __init__(self, new=False):

        self.db_filename = solary.auxiliary.parse.setnget_file_path('solary_data/neo/databases', \
                                                                    'neo_granvik2018.db')

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

    def create(self):

        self.cur.execute('CREATE TABLE IF NOT EXISTS main(ID INTEGER PRIMARY KEY, ' \
                                                         'SemMajAxis_AU FLOAT, ' \
                                                         'Ecc_ FLOAT, ' \
                                                         'Incl_deg FLOAT, ' \
                                                         'LongAscNode_deg FLOAT, ' \
                                                         'ArgP_deg FLOAT, ' \
                                                         'MeanAnom_deg FLOAT, ' \
                                                         'AbsMag_ FLOAT)')

        self.con.commit()

        _neo_data = read_granvik2018()

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
