import solary

def test__get_neodys_neo_nr():
    
    neo_nr = solary.neo.data._get_neodys_neo_nr()
    assert type(neo_nr) == int
    assert neo_nr >= 0

def test_download():
    
    dl_status = solary.neo.data.download()
    assert dl_status == 'OK'
    
# def test_neo_sqlite_db():
    
#     neo_sqlite = solary.neo.data.neodys_database()
    
#     neo_sqlite.close()