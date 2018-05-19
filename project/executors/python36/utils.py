# -*- coding utf:8 -*-
from django.conf import settings
import subprocess
import os
import uuid
import re
from project.executors.models import EXEC_FOLDERS, PYTHON36

TMP_DIR = os.path.join(settings.CODE_TMP_DIR, EXEC_FOLDERS[PYTHON36])

try:
    os.stat(TMP_DIR)
except:
    os.mkdir(TMP_DIR)


class TmpFile:

    TMP_DIR = os.path.join(settings.CODE_TMP_DIR, EXEC_FOLDERS[PYTHON36])

    def __init__(self, extension="py"):
        self.filename = "%s.%s" % (uuid.uuid4(), extension)
        self.filedir = os.path.join(TMP_DIR, self.filename)

    def create(self, file_content):
        file = open(self.filedir, "wb")
        file.write(bytes(file_content, 'utf-8'))
        file.close()
        return self.filename

    def remove(self):
        os.remove(self.filedir)
        return True


def execute_code(code, content, input):
    stdin = bytes(input, 'utf-8')
    tmp_file = TmpFile()
    filename = tmp_file.create(content)
    args = ["python", filename]
    proc = subprocess.Popen(
        args=args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=TMP_DIR,
        # preexec_fn=set_process_limits,
    )

    stdout, stderr = proc.communicate(stdin, timeout=30)
    # status = proc.returncode
    tmp_file.remove()

    output = stdout.decode("utf-8")
    error = re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))
    return output, error


def check_tests(code, content, tests):
    tmp_file = TmpFile()
    filename = tmp_file.create(content)
    args = ["python", filename]
    tests_result = []
    for test in tests:
        proc = subprocess.Popen(
            args=args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=TMP_DIR,
            # preexec_fn=set_process_limits,
        )

        stdin = bytes(test.input, 'utf-8')
        stdout, stderr = proc.communicate(stdin, timeout=30)
        # status = proc.returncode
        output = stdout.decode("utf-8").rstrip('\r\n')
        error = re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))

        success = True if (test.output == output) and not error else False
        tests_result.append({
            "id": test.id,
            "input": test.input,
            "output": test.output,
            "user_output": output,
            "error": error,
            "success": success
        })

    tmp_file.remove()
    return tests_result
