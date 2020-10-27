import sqlite3

import pytest
import solary

# def test__get_neodys_neo_nr():
    
#     neo_nr = solary.neo.data._get_neodys_neo_nr()
#     assert type(neo_nr) == int
#     assert neo_nr >= 0

# def test_download():
    
#     dl_status, _ = solary.neo.data.download()
#     assert dl_status == 'OK'

#     dl_status, _ = solary.neo.data.download(download_path='tests/_temp')
#     assert dl_status == 'OK'

#     dl_status, row_exp = solary.neo.data.download(row_exp=True)
#     assert dl_status == 'OK'
#     assert type(row_exp) == int
#     assert row_exp >= 0
    
def test_read():
    
    neo_dict_data = solary.neo.data.read()
    assert neo_dict_data[0]['Name'] == '433'
    assert pytest.approx(neo_dict_data[0]['SemMajAxis_AU'], abs=1e-2) == 1.46
    assert pytest.approx(neo_dict_data[0]['Ecc_'], abs=1e-2) == 0.22

    neo_dict_data = solary.neo.data.read(path='tests/_temp')
    assert neo_dict_data[0]['Name'] == '433'
    assert pytest.approx(neo_dict_data[0]['SemMajAxis_AU'], abs=1e-2) == 1.46
    assert pytest.approx(neo_dict_data[0]['Ecc_'], abs=1e-2) == 0.22

def test_neo_sqlite_db():
    
    neo_sqlite = solary.neo.data.neodys_database(new=True)
    
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