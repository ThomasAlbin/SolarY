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
    
# def test_neo_sqlite_db():
    
#     neo_sqlite = solary.neo.data.neodys_database()
    
#     neo_sqlite.close()