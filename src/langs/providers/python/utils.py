import os
import uuid
from django.conf import settings


class DebugFiles:

    def __init__(self, data_in: str, data_py: str):
        _uuid = uuid.uuid4()
        self.filename_py = f'{_uuid}.py'
        self.filename_in = f'{_uuid}.in'
        self.path_py = os.path.join(settings.PY_TMP_DIR, self.filename_py)
        self.path_in = os.path.join(settings.PY_TMP_DIR, self.filename_in)

        with open(self.path_py, 'w') as file_py, open(self.path_in, 'w') as file_in:
            file_py.write(data_py)
            file_in.write(data_in)

    def remove(self):
        os.remove(self.path_py)
        os.remove(self.path_in)


class TestsFiles:

    def __init__(self, data_py: str):
        self._uuid = uuid.uuid4()
        self.filename_py = f'{self._uuid}.py'
        self.path_py = os.path.join(settings.PY_TMP_DIR, self.filename_py)
        self.paths_in = []

        with open(self.path_py, 'w') as file_py:
            file_py.write(data_py)

    def create_file_in(self, data_in: str):
        filename = f'{self._uuid}-{len(self.paths_in)}.in'
        path = os.path.join(settings.PY_TMP_DIR, filename)
        with open(path, 'w') as file:
            file.write(data_in)
        self.paths_in.append(path)
        return filename

    def remove(self):
        os.remove(self.path_py)
        while self.paths_in:
            os.remove(self.paths_in.pop())
