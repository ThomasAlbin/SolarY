import hashlib
import pathlib
import os

def comp_md5(file_name):

    hash_md5 = hashlib.md5()

    with open(file_name, 'rb') as f_temp:
        for _seq in iter(lambda: f_temp.read(65536), b''):
            hash_md5.update(_seq)

    return hash_md5.hexdigest()

def setnget_file_path(dl_path, filename):

    home_dir = os.path.expanduser('~')

    compl_dl_path = os.path.join(home_dir, dl_path)

    pathlib.Path(compl_dl_path).mkdir(parents=True, exist_ok=True)

    file_path = os.path.join(compl_dl_path, filename)

    return file_path