# -*- coding utf:8 -*-
from django.conf import settings
import subprocess
import os
import uuid
import re
from project.executors.models import Executor
TMP_DIR = os.path.join(settings.CODE_TMP_DIR, Executor.EXEC_FOLDERS[Executor.CPP])

try:
    os.stat(TMP_DIR)
except:
    os.mkdir(TMP_DIR)


class TmpFiles:

    def __init__(self, content):
        filename = uuid.uuid4()
        self.filename_cpp = '%s.cpp' % filename
        self.filename_out = '%s.out' % filename
        self.file_cpp_dir = os.path.join(TMP_DIR, self.filename_cpp)
        self.file_out_dir = os.path.join(TMP_DIR, self.filename_out)

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


def execute_code(code, content, input):
    stdin = bytes(input, 'utf-8')
    tmp = TmpFiles(content)
    p1 = subprocess.Popen(
        args=['g++', tmp.file_cpp_dir, '-o', tmp.filename_out],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=TMP_DIR
    )
    stdout, stderr = p1.communicate(stdin, code.timeout)
    p1.wait()
    error = re.sub(r'.*.cpp:', "", stderr.decode("utf-8"))
    output = stdout.decode("UTF-8")

    if not re.findall(r'error', error):
        p2 = subprocess.Popen(
            args=[tmp.file_out_dir],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=TMP_DIR,
        )
        try:
            stdout, stderr = p2.communicate(stdin, timeout=code.timeout)
            error = stderr.decode('UTF-8')
            output = stdout.decode("UTF-8")
            tmp.remove_file_out()
        except subprocess.TimeoutExpired:
            p2.kill()
            stdout, stderr = p2.communicate()
            output=""
            error="Timeout Error!"
            tmp.remove_file_out()
    tmp.remove_file_cpp()
    return output, error


def check_tests(code, content, tests):
    tmp = TmpFiles(content)
    args = ['g++', tmp.file_cpp_dir, '-o', tmp.filename_out],
    tests_result = {
        "data": [],          # список результатов по каждому тесту
        "num": len(tests),   # количество тестов
        "success_num": 0,    # количество пройденных тестов
    }
    for test in tests:
        p1 = subprocess.Popen(
            args=['g++', tmp.file_cpp_dir, '-o', tmp.filename_out],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=TMP_DIR
        )

        stdin = bytes(test.input, "UTF-8")
        stdout, stderr = p1.communicate(stdin, code.timeout)
        p1.wait()
        error = re.sub(r'.*.cpp:', "", stderr.decode("UTF-8"))
        output = stdout.decode("UTF-8")

        if not re.findall(r'error', error):
            p2 = subprocess.Popen(
                args=[tmp.file_out_dir],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=TMP_DIR,
            )
            try:
                stdout, stderr = p2.communicate(stdin, timeout=code.timeout)
                error = stderr.decode('UTF-8')
                output = stdout.decode("UTF-8")
                tmp.remove_file_out()
            except subprocess.TimeoutExpired:
                p2.kill()
                stdout, stderr = p2.communicate()
                output = ""
                error = "Timeout Error!"
                tmp.remove_file_out()

        success = True if (test.output == output) and not error else False
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
    tmp.remove_file_cpp()
    tmp.remove_file_out()
    return tests_result
