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

# Get the file paths
PATH_CONFIG = solary.auxiliary.config.get_paths()

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
    that can be read by any editor. See -1-

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

    References
    ----------
    -1- Link to the NEODyS data: https://newton.spacedys.com/neodys/index.php?pc=1.0

    """

    # Set the complete filepath. The file is stored in the user's home directory
    download_filename = \
        solary.auxiliary.parse.setnget_file_path(PATH_CONFIG['neo']['neodys_raw_dir'], \
                                                 PATH_CONFIG['neo']['neodys_raw_file'])

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
    neo_dict : list
        List of dictionaries that contains the NEO data from the NEODyS download.

    """

    # Set the download file path. The file shall be stored in the home direoctry
    path_filename = solary.auxiliary.parse.setnget_file_path(PATH_CONFIG['neo']['neodys_raw_dir'], \
                                                             PATH_CONFIG['neo']['neodys_raw_file'])

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
    """
    Class to create, update and read an SQLite based database that contains NEO data (raw and
    derived parameters) based on the NEODyS data.

    Attributes
    ----------
    db_filename : str
        Absolute path to the SQLite NEODyS database
    con : sqlite3.Connection
        Connection to the SQLite NEODyS database
    cur: sqlite3.Cursor
        Cursor to the SQLite NEODyS database

    Methods
    -------
    __init__(new=False)
        Init function at the class call. Allows one to re-create a new SQLite database from
        scratch.
    create()
        Create the main table of the SQLite NEODyS database (contains only the raw input data, no
        derived parameters).
    create_deriv_orb()
        Compute derived orbital elements from the raw input data.
    close()
        Close the SQLite database.

    See also
    --------
    solary.neo.data.download(row_exp=None)
    solary.neo.data.read_neodys()

    """


    def __init__(self, new=False):
        """
        Init. function of the NEODySDatabase class. This method creates a new database or opens an
        existing one (if applicable) and sets a cursor.

        Parameters
        ----------
        new : bool, optional
            If True: a new database will be created from scratch. WARNING: this will delete any
            previously built SQLite database with the name "neo_neodys.db" in the home directory.
            The default is False.

        """

        # Set / Get an SQLite database path + filename
        self.db_filename = \
            solary.auxiliary.parse.setnget_file_path(PATH_CONFIG['neo']['neodys_db_dir'], \
                                                     PATH_CONFIG['neo']['neodys_db_file'])

        # Delete any existing database, if requested
        if new and os.path.exists(self.db_filename):
            os.remove(self.db_filename)

        # Connect / Build database and set a cursor
        self.con = sqlite3.connect(self.db_filename)
        self.cur = self.con.cursor()


    def _create_col(self, table, col_name, col_type):
        """
        Private method to create new columns in tables

        Parameters
        ----------
        table : str
            Table name, where a new column shall be added.
        col_name : str
            Column name.
        col_type : str
            SQLite column type (FLOAT, INT, TEXT, etc.).

        """

        # Generic f-string that represents an SQLite command to alter a table (adding a new column
        # with its dtype).
        sql_col_create = f'ALTER TABLE {table} ADD COLUMN {col_name} {col_type}'

        # Try to create a new column. If is exists an sqlite3.OperationalError weill raise. Pass
        # this error.
        #TODO: change the error passing
        try:
            self.cur.execute(sql_col_create)
            self.con.commit()
        except sqlite3.OperationalError:
            pass


    def create(self):
        """
        Method to create the NEODyS main table, read the downloaded content and fill the database
        with the raw data.

        """

        # Create the main table
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

        # Read the NEODyS raw data
        _neo_data = read_neodys()

        # Insert the raw data into the database
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
        """
        Method to compute and insert derived orbital elements into the SQLite database.

        """

        # Add new columns in the main table
        self._create_col('main', 'Aphel_AU', 'FLOAT')
        self._create_col('main', 'Perihel_AU', 'FLOAT')

        # Get orbital elements to compute the derived parameters
        self.cur.execute('SELECT Name, SemMajAxis_AU, Ecc_ FROM main')

        # Fetch the data
        _neo_data = self.cur.fetchall()

        # Iterate throuh the results, compute the derived elements and put them in a list of
        # dicitionaries
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

        # Insert the data into the main table
        self.cur.executemany('UPDATE main SET Aphel_AU = :Aphel_AU, Perihel_AU = :Perihel_AU ' \
                             'WHERE Name = :Name', _neo_deriv_param_dict)
        self.con.commit()


    def update(self):
        """
        Update the NEODyS Database with all content.

        """

        # Call the create functions that insert new data
        self.create()
        self.create_deriv_orb()


    def close(self):
        """
        Close the SQLite NEODyS database.

        """

        self.con.close()


def download_granvik2018():
    """
    Function to download the model data from Granvik et al. (2018) -1-. The data can be found in
    -2-.

    Returns
    -------
    md5_hash : str
        MD5 hash of the downloaded file.

    References
    ----------
    -1- Granvik, Morbidelli, Jedicke, Bolin, Bottke, Beshore, Vokrouhlicky, Nesvorny, and Michel
        (2018). Debiased orbit and absolute-magnitude distributions for near-Earth objects.
        Accepted for publication in Icarus.
    -2- https://www.mv.helsinki.fi/home/mgranvik/data/Granvik+_2018_Icarus/
    """

    # Set the download path to the home directory
    download_filename = \
        solary.auxiliary.parse.setnget_file_path(PATH_CONFIG['neo']['granvik2018_raw_dir'], \
                                                 PATH_CONFIG['neo']['granvik2018_raw_file'])

    # Set the downlaod URL
    url_location = 'https://www.mv.helsinki.fi/home/mgranvik/data/' \
                   'Granvik+_2018_Icarus/Granvik+_2018_Icarus.dat.gz'

    # Retrieve the data (download)
    downl_file_path, _ = urllib.request.urlretrieve(url=url_location, \
                                                    filename=download_filename)

    # Get the file name (without the gzip ending). Open the gzip file and move the .dat file out.
    unzip_file_path = downl_file_path[:-3]
    with gzip.open(downl_file_path, 'r') as f_in, open(unzip_file_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    # Delete the gzip file
    os.remove(downl_file_path)

    # Compute the MD5 hash
    md5_hash = solary.auxiliary.parse.comp_md5(unzip_file_path)

    return md5_hash


def read_granvik2018():
    """
    Read the content of the downloaded Granvik et al. (2018) NEO model data file and return a
    dictionary with its content.

    Returns
    -------
    neo_dict : list
        List of dictionaries that contains the NEO data from the downloaded model data.

    """

    # Set the download path of the model file
    path_filename = \
        solary.auxiliary.parse.setnget_file_path(PATH_CONFIG['neo']['granvik2018_raw_dir'], \
                                                 PATH_CONFIG['neo']['granvik2018_unzip_file'])

    # Iterate through the downloaded file and write the content in a list of dictionaries. Each
    # dictionary contains an individual simulated NEO
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
    """
    Class to create, update and read an SQLite based database that contains the Granvik et al.
    (2018) NEO model data (raw and derived parameters)

    Attributes
    ----------
    db_filename : str
        Absolute path to the SQLite Granvik et al. (2018) database
    con : sqlite3.Connection
        Connection to the SQLite Granvik et al. (2018) database
    cur: sqlite3.Cursor
        Cursor to the SQLite Granvik et al. (2018) database

    Methods
    -------
    __init__(new=False)
        Init function at the class call. Allows one to re-create a new SQLite database from
        scratch.
    create()
        Create the main table of the SQLite Granvik et al. (2018) database (contains only the raw
        input data, no derived parameters).
    create_deriv_orb()
        Compute derived orbital elements from the raw input data.
    close()
        Close the SQLite database.

    See also
    --------
    solary.neo.data.download_granvik2018()
    solary.neo.data.read_granvik2018()

    """


    def __init__(self, new=False):
        """
        Init. function of the Granvik2018Database class. This method creates a new database or
        opens an existing one (if applicable) and sets a cursor.

        Parameters
        ----------
        new : bool, optional
            If True: a new database will be created from scratch. WARNING: this will delete any
            previously built SQLite database with the name "neo_granvik2018.db" in the home
            directory. The default is False.

        """

        # Set the database path to the home directory
        self.db_filename = \
            solary.auxiliary.parse.setnget_file_path(PATH_CONFIG['neo']['granvik2018_db_dir'], \
                                                     PATH_CONFIG['neo']['granvik2018_db_file'])

        # Delete any existing database, if requested
        if new and os.path.exists(self.db_filename):
            os.remove(self.db_filename)

        # Establish a connection and set a cursor to the database
        self.con = sqlite3.connect(self.db_filename)
        self.cur = self.con.cursor()


    def _create_col(self, table, col_name, col_type):
        """
        Private method to create new columns in tables

        Parameters
        ----------
        table : str
            Table name, where a new column shall be added.
        col_name : str
            Column name.
        col_type : str
            SQLite column type (FLOAT, INT, TEXT, etc.).

        """

        # Generic f-string that represents an SQLite command to alter a table (adding a new column
        # with its dtype).
        sql_col_create = f'ALTER TABLE {table} ADD COLUMN {col_name} {col_type}'

        # Try to create a new column. If is exists an sqlite3.OperationalError weill raise. Pass
        # this error.
        #TODO: change the error passing and merge with the same method in NEODySDatabase
        try:
            self.cur.execute(sql_col_create)
            self.con.commit()
        except sqlite3.OperationalError:
            pass


    def create(self):
        """
        Method to create the Granvik et al. (2018) main table, read the downloaded content and fill
        the database with the raw data.

        """

        # Create main table for the raw data
        self.cur.execute('CREATE TABLE IF NOT EXISTS main(ID INTEGER PRIMARY KEY, ' \
                                                         'SemMajAxis_AU FLOAT, ' \
                                                         'Ecc_ FLOAT, ' \
                                                         'Incl_deg FLOAT, ' \
                                                         'LongAscNode_deg FLOAT, ' \
                                                         'ArgP_deg FLOAT, ' \
                                                         'MeanAnom_deg FLOAT, ' \
                                                         'AbsMag_ FLOAT)')
        self.con.commit()

        # Read the Granvik et al. (2018) data
        _neo_data = read_granvik2018()

        # Insert the raw Granvik et al. (2018) data into the SQLite database
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
        """
        Method to compute and insert derived orbital elements into the SQLite database.

        """

        # Create new columns
        self._create_col('main', 'Aphel_AU', 'FLOAT')
        self._create_col('main', 'Perihel_AU', 'FLOAT')

        # Get all relevant information from the database
        self.cur.execute('SELECT ID, SemMajAxis_AU, Ecc_ FROM main')
        _neo_data = self.cur.fetchall()


        # Iterate through the results and compute the derived orbital parameters
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

        # Insert the derived paramters into the database
        self.cur.executemany('UPDATE main SET Aphel_AU = :Aphel_AU, Perihel_AU = :Perihel_AU ' \
                             'WHERE ID = :ID', _neo_deriv_param_dict)
        self.con.commit()


    def close(self):
        """
        Close the Granvik et al. (2018) database.

        """

        self.con.close()
