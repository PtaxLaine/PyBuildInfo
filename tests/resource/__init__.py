import os
import tempfile
import tarfile
import shutil


class Repo:
    def __init__(self, name):
        self.name = name
        r = os.path.dirname(__file__)
        r = os.path.abspath(r)
        r = os.path.join(r, '{}.tar.gz'.format(name))
        assert os.path.isfile(r)
        self.path = r
        self.tmp_path = None

    def __del(self):
        if self.tmp_path:
            shutil.rmtree(self.tmp_path)

    def __enter__(self):
        self.tmp_path = tempfile.mkdtemp()
        try:
            tar = tarfile.open(self.path)
            tar.extractall(self.tmp_path)
        except Exception as ex:
            self.__del()
            raise ex
        return self.tmp_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del()
