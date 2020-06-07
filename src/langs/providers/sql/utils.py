import os
import uuid
from django.conf import settings


class TmpFile:

    def __init__(self, content):
        print("doing stuff")
      #  self.filename = "%s.py" % (uuid.uuid4())
      #  self.filedir = os.path.join(settings.TMP_DIR, self.filename)

      #  file = open(self.filedir, "wb")
      #  file.write(bytes(content, 'utf-8'))
      #  file.close()

    def remove(self):
        print("removing")
       # os.remove(self.filedir)
        #return True
