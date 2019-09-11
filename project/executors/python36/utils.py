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
    args = [settings.PYTHON_PATH, filename]
    proc = subprocess.Popen(
        args=args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=TMP_DIR,
    )

    stdout, stderr = proc.communicate(stdin, timeout=code.timeout)
    # status = proc.returncode
    tmp_file.remove()

    output = stdout.decode("utf-8")
    error = re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))
    return output, error


def normalize_fract_part(val1, val2, limit=8):
    parts1 = val1.split('.')
    if len(parts1) < 2:
        parts1.append('0')

    parts2 = val2.split('.')
    if len(parts2) < 2:
        parts2.append('0')

    parts1[1] = parts1[1][:limit]
    parts2[1] = parts2[1][:limit]

    return '.'.join(parts1), '.'.join(parts2)


def check_test(output, error, test):

    """ Проверка вывода программы на тесте
        Нормализация:
            - удаление спец. символов возврата каректи и пробелов в начале и конце
            - для дробных чисел проверка только до восьмого символа дробной части
            - для дробных числе 1.0 == 1
    """
    if error:
        return False
    else:
        out = output.rstrip('\r\n').replace('\r', '').strip()
        t_out = test.output.replace('\r', '').strip()
        if t_out.replace('.', '').isdigit():
            out, t_out = normalize_fract_part(out, t_out)
        return t_out == out


def check_tests(code, content, tests):
    tmp_file = TmpFile()
    filename = tmp_file.create(content)
    args = [settings.PYTHON_PATH, filename]
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
        output = stdout.decode("utf-8")
        error = re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))
        success = check_test(output, error, test)
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
