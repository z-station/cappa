import os
import uuid
from django.conf import settings


class TmpFile:

    def __init__(self, ext):
        self.filename = "%s.%s" % (uuid.uuid4(), ext)
        self.filedir = os.path.join(settings.TMP_DIR, self.filename)

    def create(self, file_content):
        file = open(self.filedir, "wb")
        file.write(bytes(file_content, 'utf-8'))
        file.close()
        return self.filename

    def remove(self):
        os.remove(self.filedir)
        return True


#
# class ProviderResponse:
#
#     def __init__(self, error=None, output=None, tests_result=None, msg=None):
#         if error:
#             self.ok = False
#             self.msg = 'Ошибка'
#             self.error = error
#         else:
#             self.ok = True
#             if output:
#                 self.message = 'Готово'
#                 self.output = output
#             elif tests_result:
#                 self.message = 'Пройдено тестов: %s из %s' % (
#                     tests_result['success_num'],
#                     tests_result['num']
#                 )
#                 self.tests_result = tests_result
#         if msg:
#             self.msg = msg

