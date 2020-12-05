import sqlite3

import pytest
import solary

def test__get_neodys_neo_nr():
    
    neo_nr = solary.neo.data._get_neodys_neo_nr()
    assert type(neo_nr) == int
    assert neo_nr >= 0

def test_download():
    
    dl_status, _ = solary.neo.data.download()
    assert dl_status == 'OK'

    dl_status, row_exp = solary.neo.data.download(row_exp=True)
    assert dl_status == 'OK'
    assert type(row_exp) == int
    assert row_exp >= 0
    
def test_read_neodys():
    
    neo_dict_data = solary.neo.data.read_neodys()
    assert neo_dict_data[0]['Name'] == '433'
    assert pytest.approx(neo_dict_data[0]['SemMajAxis_AU'], abs=1e-2) == 1.46
    assert pytest.approx(neo_dict_data[0]['Ecc_'], abs=1e-2) == 0.22

def test_NEOdysDatabase():
    
    neo_sqlite = solary.neo.data.NEOdysDatabase(new=True)
    
    assert type(neo_sqlite.con) == sqlite3.Connection
    assert type(neo_sqlite.cur) == sqlite3.Cursor

    neo_sqlite.create()
    
    query_res_cur = neo_sqlite.cur.execute('SELECT Name, SemMajAxis_AU, ECC_ ' \
                                            'FROM main WHERE Name = "433"')
    query_res = query_res_cur.fetchone()

    assert query_res[0] == '433'
    assert pytest.approx(query_res[1], abs=1e-2) == 1.46
    assert pytest.approx(query_res[2], abs=1e-2) == 0.22

    neo_sqlite.create_deriv_orb()

    query_res_cur = neo_sqlite.cur.execute('SELECT Name, Aphel_AU, Perihel_AU ' \
                                            'FROM main WHERE Name = "433"')
    query_res = query_res_cur.fetchone()

    assert query_res[0] == '433'
    assert pytest.approx(query_res[1], abs=1e-3) == 1.783
    assert pytest.approx(query_res[2], abs=1e-3) == 1.133

    neo_sqlite.close()

def test_download_granvik2018():

    md5_hash = solary.neo.data.download_granvik2018()
    assert md5_hash == '521ddfdc18545c736fee36dbc4879d5e'

def test_read_granvik2018():
    
    neo_dict_data = solary.neo.data.read_granvik2018()
    assert pytest.approx(neo_dict_data[0]['SemMajAxis_AU']) == 2.57498121
    assert pytest.approx(neo_dict_data[0]['Ecc_']) == 0.783616960
    assert pytest.approx(neo_dict_data[0]['Incl_deg']) == 33.5207634
    assert pytest.approx(neo_dict_data[0]['LongAscNode_deg']) == 278.480591
    assert pytest.approx(neo_dict_data[0]['ArgP_deg']) == 75.9520569
    assert pytest.approx(neo_dict_data[0]['MeanAnom_deg']) == 103.833748
    assert pytest.approx(neo_dict_data[0]['AbsMag_']) == 21.0643673

def test_Granvik2018Database():
    
    gravnik2018_sqlite = solary.neo.data.Granvik2018Database(new=True)
    
    assert type(gravnik2018_sqlite.con) == sqlite3.Connection
    assert type(gravnik2018_sqlite.cur) == sqlite3.Cursor

    gravnik2018_sqlite.create()
    
    query_res_cur = gravnik2018_sqlite.cur.execute('SELECT ID, SemMajAxis_AU, ECC_ ' \
                                                    'FROM main WHERE ID = 1')
    query_res = query_res_cur.fetchone()

    assert query_res[1] == 2.57498121
    assert query_res[2] == 0.783616960

    gravnik2018_sqlite.create_deriv_orb()

    query_res_cur = gravnik2018_sqlite.cur.execute('SELECT ID, Aphel_AU, Perihel_AU ' \
                                                    'FROM main WHERE ID = 1')
    query_res = query_res_cur.fetchone()

    assert query_res[1] == 4.592780157837321
    assert query_res[2] == 0.5571822621626783

    gravnik2018_sqlite.close()