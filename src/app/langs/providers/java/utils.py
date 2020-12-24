import os
import uuid
from django.conf import settings


class TmpFiles:

    def __init__(self, content):
        self.filename_java = 'program.java'
        self.file_java_dir = os.path.join(settings.TMP_DIR, self.filename_java)

        file = open(self.file_java_dir, "wb")
        file.write(bytes(content, 'utf-8'))
        file.close()

    def remove_file_java(self):
        try:
            os.remove(self.file_java_dir)
        except:
            pass
