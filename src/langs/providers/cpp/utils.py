import os
import uuid
from django.conf import settings


class DebugFiles:

    def __init__(self, data_in: str, data_cpp: str, tmp_dir: str):
        _uuid = uuid.uuid4()
        self.filename_cpp = f'{_uuid}.cpp'
        self.filename_in = f'{_uuid}.in'
        self.path_cpp = os.path.join(tmp_dir, self.filename_cpp)
        self.path_in = os.path.join(tmp_dir, self.filename_in)
        self.path_out = f'/tmp/{_uuid}.out'

        with open(self.path_cpp, 'w') as file_cpp, \
                open(self.path_in, 'w') as file_in:
            file_cpp.write(data_cpp)
            file_in.write(data_in)

    def remove(self):
        os.remove(self.path_cpp)
        os.remove(self.path_in)


class TestsFiles:

    def __init__(self, data_cpp: str, tmp_dir: str):
        self.tmp_dir = tmp_dir
        self._uuid = uuid.uuid4()
        self.filename_cpp = f'{self._uuid}.cpp'
        self.path_cpp = os.path.join(self.tmp_dir, self.filename_cpp)
        self.paths_in = []

        with open(self.path_cpp, 'w') as file_cpp:
            file_cpp.write(data_cpp)

    def create_file_in(self, data_in: str):
        filename = f'{self._uuid}-{len(self.paths_in)}.in'
        path = os.path.join(self.tmp_dir, filename)
        with open(path, 'w') as file:
            file.write(data_in)
        self.paths_in.append(path)
        return filename

    def remove(self):
        os.remove(self.path_cpp)
        while self.paths_in:
            os.remove(self.paths_in.pop())
