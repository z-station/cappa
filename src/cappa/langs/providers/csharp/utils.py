# -*- coding: utf-8 -*-
import os
import uuid
from django.conf import settings


class TmpFiles:

    def __init__(self, content):
        filename = uuid.uuid4()
        self.filename_cpp = '%s.cs' % filename
        self.filename_out = '%s.exe' % filename
        self.file_cpp_dir = os.path.join(settings.TMP_DIR, self.filename_cpp)
        self.file_out_dir = os.path.join(settings.TMP_DIR, self.filename_out)

        file = open(self.file_cpp_dir, "wb")
        file.write(bytes(content, 'utf-8'))
        file.close()

    def remove_file_cpp(self):
        try:
            os.remove(self.file_cpp_dir)
        except:
            pass

    def remove_file_out(self):
        try:
            os.remove(self.file_out_dir)
        except:
            pass