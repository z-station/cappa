import os
import uuid


class DebugFiles:

    def __init__(self, data_in: str, data_java: str, tmp_dir: str):
        _uuid = uuid.uuid4()
        self.filename_java = 'program.java'
        self.filename_in = f'{_uuid}.in'
        self.path_java = os.path.join(tmp_dir, self.filename_java)
        self.path_in = os.path.join(tmp_dir, self.filename_in)

        with open(self.path_java, 'w') as file_java, open(self.path_in, 'w') as file_in:
            file_java.write(data_java)
            file_in.write(data_in)

    def remove(self):
        os.remove(self.path_java)
        os.remove(self.path_in)


class TestsFiles:

    def __init__(self, data_java: str, tmp_dir: str):
        self.tmp_dir = tmp_dir
        self._uuid = uuid.uuid4()
        self.filename_java = 'program.java'
        self.path_java = os.path.join(self.tmp_dir, self.filename_java)
        self.paths_in = []

        with open(self.path_java, 'w') as file_java:
            file_java.write(data_java)

    def create_file_in(self, data_in: str):
        filename = f'{self._uuid}-{len(self.paths_in)}.in'
        path = os.path.join(self.tmp_dir, filename)
        with open(path, 'w') as file:
            file.write(data_in)
        self.paths_in.append(path)
        return filename

    def remove(self):
        os.remove(self.path_java)
        while self.paths_in:
            os.remove(self.paths_in.pop())
