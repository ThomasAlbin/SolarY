"""
test_data.py

Testing suite for solary/neo/data.py

"""

# Import standard libraries
import sqlite3

# Import installed libraries
import pytest

# Import solary
import solary


def test__get_neodys_neo_nr():
    """
    Testing the hidden function that gets the current number of known NEOs from the NEODyS webpage.

    Returns
    -------
    None.

    """

    # Call the function to get the number of currently known NEOs.
    neo_nr = solary.neo.data._get_neodys_neo_nr()

    # Check of the result is an integer
    assert isinstance(neo_nr, int)

    # Since the number of NEOs can change daily this assertion test check only if the number is
    # larger than 0
    assert neo_nr >= 0


def test_download():
    """
    Testing the NEODyS download function

    Returns
    -------
    None.

    """

    # Execute the download function and check if the download status was "OK"
    dl_status, _ = solary.neo.data.download()
    assert dl_status == 'OK'

    # Execute the donwload a second time get also the row expectation (internally it compares the
    # results with the _get_neodys_neo_nr function)
    dl_status, row_exp = solary.neo.data.download(row_exp=True)
    assert dl_status == 'OK'
    assert isinstance(row_exp, int)
    assert row_exp >= 0


def test_read_neodys():
    """
    Test the reading functionality of the downloaded NEODyS data

    Returns
    -------
    None.

    """

    # Read the data
    neo_dict_data = solary.neo.data.read_neodys()

    # The first entry must be (433) Erors; with its semi-major axis givne in AU and the
    # eccentricity
    assert neo_dict_data[0]['Name'] == '433'
    assert pytest.approx(neo_dict_data[0]['SemMajAxis_AU'], abs=1e-2) == 1.46
    assert pytest.approx(neo_dict_data[0]['Ecc_'], abs=1e-2) == 0.22


def test_NEOdysDatabase():
    """
    Test the NEODyS database.

    Returns
    -------
    None.

    """

    # Create the database and check if the connection is established and the cursor is set
    neo_sqlite = solary.neo.data.NEOdysDatabase(new=True)

    assert isinstance(neo_sqlite.con, sqlite3.Connection)
    assert isinstance(neo_sqlite.cur, sqlite3.Cursor)

    # Create the table and content
    neo_sqlite.create()

    # Get now the data of (433) Eros
    query_res_cur = neo_sqlite.cur.execute('SELECT Name, SemMajAxis_AU, ECC_ ' \
                                           'FROM main WHERE Name = "433"')
    query_res = query_res_cur.fetchone()

    # Perform assertion tests on Eros' data
    assert query_res[0] == '433'
    assert pytest.approx(query_res[1], abs=1e-2) == 1.46
    assert pytest.approx(query_res[2], abs=1e-2) == 0.22

    # Compute the derived orbital elements and the the aphelion and perihelion data of Eros
    neo_sqlite.create_deriv_orb()
    query_res_cur = neo_sqlite.cur.execute('SELECT Name, Aphel_AU, Perihel_AU ' \
                                           'FROM main WHERE Name = "433"')
    query_res = query_res_cur.fetchone()

    # Perform assertion tests on Eros' derived results
    assert query_res[0] == '433'
    assert pytest.approx(query_res[1], abs=1e-3) == 1.783
    assert pytest.approx(query_res[2], abs=1e-3) == 1.133

    # Now the test check if the update functionality works. For this purpose, the first row from the
    # database is deleted; the update function is executed and then the number of rows is compared
    # with the expectation.
    # First: get the current number of rows from the database
    query_res_cur = neo_sqlite.cur.execute('SELECT COUNT(*) FROM main')
    original_count = query_res_cur.fetchone()[0]

    # Delete Eros and get the number of rows
    neo_sqlite.cur.execute('DELETE FROM main WHERE Name="433"')
    neo_sqlite.con.commit()
    query_res_cur = neo_sqlite.cur.execute('SELECT COUNT(*) FROM main')
    manip_count = query_res_cur.fetchone()[0]

    # The modified database should have 1 entry less than before
    assert manip_count == original_count-1

    # Update the database and get the number of counts
    neo_sqlite.update()
    query_res_cur = neo_sqlite.cur.execute('SELECT COUNT(*) FROM main')
    update_count = query_res_cur.fetchone()[0]

    # Now the updated database must have the same number of rows as before
    assert update_count == original_count

    # Close the database
    neo_sqlite.close()


def test_download_granvik2018():
    """
    Testing the download of the Granvik et al. (2018) NEO data.

    Returns
    -------
    None.

    """

    # Download the data and compare the MD5 hash of the downloaded file with the expectation
    md5_hash = solary.neo.data.download_granvik2018()
    assert md5_hash == '521ddfdc18545c736fee36dbc4879d5e'


def test_read_granvik2018():
    """
    Test the reader function of the Granvik et al. (2018) data.

    Returns
    -------
    None.

    """

    # Read the data and perform some assertions (expectations for the very first entry that has
    # been inspected before)
    neo_dict_data = solary.neo.data.read_granvik2018()
    assert pytest.approx(neo_dict_data[0]['SemMajAxis_AU']) == 2.57498121
    assert pytest.approx(neo_dict_data[0]['Ecc_']) == 0.783616960
    assert pytest.approx(neo_dict_data[0]['Incl_deg']) == 33.5207634
    assert pytest.approx(neo_dict_data[0]['LongAscNode_deg']) == 278.480591
    assert pytest.approx(neo_dict_data[0]['ArgP_deg']) == 75.9520569
    assert pytest.approx(neo_dict_data[0]['MeanAnom_deg']) == 103.833748
    assert pytest.approx(neo_dict_data[0]['AbsMag_']) == 21.0643673


def test_Granvik2018Database():
    """
    Test the Granvik et al. (2018) SQLite database

    Returns
    -------
    None.

    """

    # Create the database
    granvik2018_sqlite = solary.neo.data.Granvik2018Database(new=True)

    # Check if a connection has been established and if a cursor has been set
    assert isinstance(granvik2018_sqlite.con, sqlite3.Connection)
    assert isinstance(granvik2018_sqlite.cur, sqlite3.Cursor)

    # Create the main table, get the first entry and verify the results
    granvik2018_sqlite.create()
    query_res_cur = granvik2018_sqlite.cur.execute('SELECT ID, SemMajAxis_AU, ECC_ ' \
                                                    'FROM main WHERE ID = 1')
    query_res = query_res_cur.fetchone()
    assert query_res[1] == 2.57498121
    assert query_res[2] == 0.783616960

    # Create the dervied orbital elements and perform a verfication step
    granvik2018_sqlite.create_deriv_orb()
    query_res_cur = granvik2018_sqlite.cur.execute('SELECT ID, Aphel_AU, Perihel_AU ' \
                                                    'FROM main WHERE ID = 1')
    query_res = query_res_cur.fetchone()
    assert query_res[1] == 4.592780157837321
    assert query_res[2] == 0.5571822621626783

    # Close the Granvik database
    granvik2018_sqlite.close()
