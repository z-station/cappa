# -*- coding: utf-8 -*-
import os
import uuid
from django.conf import settings


class TmpFiles:

    def __init__(self, content, input):
        filename = uuid.uuid4()
        self.filename_php = '%s.php' % filename
        self.file_php_dir = os.path.join(settings.TMP_DIR, self.filename_php)

        file = open(self.file_php_dir, "wb")
        input_tag = f'<?php {input} ?>'
        content_tag = f'<?php {content} ?>'
        file.write(bytes(input_tag, 'utf-8'))
        file.write(bytes(content_tag, 'utf-8'))
        file.close()

    def remove_file_php(self):
        try:
            os.remove(self.file_php_dir)
        except:
            pass



