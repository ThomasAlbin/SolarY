import solary

def test_download():
    
    # donwload the file and return a check value
    # perform an assertation test on the very first neo: 433 Eros
    # maybe also on neodys: check number of rows with number of numbers on website
    # https://newton.spacedys.com/~neodys2/neodys.cat
    
    dl_status = solary.neo.data.download()
    assert dl_status == 'OK'

    dl_status = solary.neo.data.download(filename='_data/neodys_test.cat')
    assert dl_status == 'OK'