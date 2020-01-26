import re
import subprocess
import os
import uuid
from django.conf import settings


class TmpFile:

    def __init__(self, content):
        self.filename = "%s.py" % (uuid.uuid4())
        self.filedir = os.path.join(settings.TMP_DIR, self.filename)

        file = open(self.filedir, "wb")
        file.write(bytes(content, 'utf-8'))
        file.close()

    def remove(self):
        os.remove(self.filedir)
        return True


def debug(input, content):
    stdin = bytes(input, 'utf-8')
    tmp_file = TmpFile(content)
    proc = subprocess.Popen(
        args=[settings.PYTHON_PATH, tmp_file.filename],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=settings.TMP_DIR,
    )

    stdout, stderr = proc.communicate(stdin)
    tmp_file.remove()
    proc.kill()
    return {
        'output': stdout.decode("utf-8"),
        'error': re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))
    }


def normalize_fract_part(python_out, test_out, limit=8):

    """
        Нормирование дробных частей (ДЧ) теста и вывода питона
        1. Приведение ДЧ к единому виду: добавление нуля в дробную часть если ее нет  1 => 1.0
        2. Ограничение дробной части в limit символов
        3. Если в ДЧ вывода питона > ДЧ теста: округляем вывод питона до того же кол-ва разрядов в дробной части:
    """

    t_parts = test_out.split('.')
    if len(t_parts) < 2:
        t_parts.append('0')
    else:
        t_parts[1] = t_parts[1][:limit]
    t_digig = float('.'.join(t_parts))

    p_parts = python_out.split('.')
    if len(p_parts) < 2:
        p_parts.append('0')
    else:
        p_parts[1] = p_parts[1][:limit]
    p_digit = float('.'.join(p_parts))

    if len(p_parts[1]) > len(t_parts[1]):
        p_digit = round(p_digit, len(t_parts[1]))

    return p_digit, t_digig


def check_test(python_out, test_out):

    """ Проверка вывода программы на тесте
        Нормализация:
            - удаление спец. символов возврата каректи и пробелов в начале и конце
            - для дробных чисел проверка только до восьмого символа дробной части
            - для дробных числе 1.0 == 1
    """

    p_out = python_out.replace('\r', '').strip()
    t_out = test_out.replace('\r', '').strip()
    is_fract_test = t_out.find('.') > -1 and t_out.replace('.', '').isdigit()
    if is_fract_test:
        p_out, t_out = normalize_fract_part(p_out, t_out)
    return p_out == t_out


def tests(content, tests):
    tmp_file = TmpFile(content)
    args = [settings.PYTHON_PATH, tmp_file.filename]
    tests_data = []
    tests_num = len(tests)
    tests_num_success = 0
    for i in range(len(tests)):
        proc = subprocess.Popen(
            args=args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=settings.TMP_DIR,
        )
        stdin = bytes(tests[i]['input'], 'utf-8')
        stdout, stderr = proc.communicate(stdin)
        output = stdout.decode("utf-8")
        error = re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))
        if error:
            success = False
        else:
            success = check_test(output, tests[i]['output'])

        if success:
            tests_num_success += 1

        tests_data.append({
            "output": output,
            "error": error,
            "success": success
        })
        proc.kill()

    tmp_file.remove()

    return {
        'num': tests_num,
        'num_success': tests_num_success,
        'data': tests_data,
        'success': bool(tests_num == tests_num_success),
    }


__all__ = [
    'debug',
    'tests'
]