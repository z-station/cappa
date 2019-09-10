# -*- coding utf:8 -*-
from django.conf import settings
import subprocess
import os
import uuid
import re
from project.executors.models import Executor
TMP_DIR = os.path.join(settings.CODE_TMP_DIR, Executor.EXEC_FOLDERS[Executor.PYTHON36])

try:
    os.stat(TMP_DIR)
except:
    os.mkdir(TMP_DIR)


class TmpFile:

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
    args = ["python3.6", filename]
    proc = subprocess.Popen(
        args=args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=TMP_DIR,
        # preexec_fn=set_process_limits,
    )

    stdout, stderr = proc.communicate(stdin, timeout=code.timeout)
    # status = proc.returncode
    tmp_file.remove()

    output = stdout.decode("utf-8")
    error = re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))
    return output, error


def check_tests(code, content, tests):
    tmp_file = TmpFile()
    filename = tmp_file.create(content)
    args = ["python3.6", filename]
    tests_result = {
        "data": [],          # список результатов по каждому тесту
        "num": len(tests),   # количество тестов
        "success_num": 0,    # количество пройденных тестов
    }
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
        stdout, stderr = proc.communicate(stdin, timeout=code.timeout)
        # status = proc.returncode
        output = stdout.decode("utf-8").rstrip('\r\n').replace('\r', '')
        error = re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))
        success = True if (test.output.replace('\r', '') == output) and not error else False
        tests_result["data"].append({
            "id": test.id,            # id теста
            "input": test.input,      # ввод теста
            "output": test.output,    # вывод теста
            "user_output": output,    # вывод исполнителя на основе ввода теста и кода пользователя
            "error": error,           # ошибка от исполнителя (если есть)
            "success": success        # True если output=user_output (полное совпадение)
        })
        if success:
            tests_result["success_num"] += 1
    tmp_file.remove()
    return tests_result
