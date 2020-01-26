import re
import subprocess
import os
import uuid
from django.conf import settings


class TmpFiles:

    def __init__(self, content):
        filename = uuid.uuid4()
        self.filename_cpp = '%s.cpp' % filename
        self.filename_out = '%s.out' % filename
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


def debug(input, content):
    stdin = bytes(input, 'utf-8')
    tmp = TmpFiles(content)
    p1 = subprocess.Popen(
        args=['c++', tmp.file_cpp_dir, '-o', tmp.filename_out],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=settings.TMP_DIR,
    )
    stdout, stderr = p1.communicate(stdin)
    p1.wait()
    error = re.sub(r'.*.cpp:', "", stderr.decode("utf-8"))
    output = stdout.decode("UTF-8")
    p1.kill()

    if not re.findall(r'error', error):
        p2 = subprocess.Popen(
            args=[tmp.file_out_dir],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=settings.TMP_DIR,
        )
        try:
            stdout, stderr = p2.communicate(stdin)
            error = stderr.decode('utf-8')
            output = stdout.decode('utf-8')
        except subprocess.TimeoutExpired:
            output = ""
            error = "Timeout Error!"
        finally:
            p2.kill()

    tmp.remove_file_cpp()
    tmp.remove_file_out()
    return {
        'output': output,
        'error': error,
    }


def tests(content, tests):
    tmp = TmpFiles(content)
    tests_data = []
    tests_num = len(tests)
    tests_num_success = 0
    for i in range(len(tests)):
        p1 = subprocess.Popen(
            args=['c++', tmp.file_cpp_dir, '-o', tmp.filename_out],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=settings.TMP_DIR,
        )

        stdin = bytes(tests[i]['input'], 'utf-8')
        stdout, stderr = p1.communicate(stdin)
        p1.wait()
        error = re.sub(r'.*.cpp:', "", stderr.decode("UTF-8"))
        output = stdout.decode("UTF-8")
        p1.kill()

        if not re.findall(r'error', error):
            p2 = subprocess.Popen(
                args=[tmp.file_out_dir],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=settings.TMP_DIR,
            )
            try:
                stdout, stderr = p2.communicate(stdin)
                error = stderr.decode('UTF-8')
                output = stdout.decode("UTF-8")
                tmp.remove_file_out()
            except subprocess.TimeoutExpired:
                stdout, stderr = p2.communicate()
                output = ""
                error = "Timeout Error!"
            finally:
                p2.kill()

        if error:
            success = False
        else:
            success = tests[i]['output'] == output

        if success:
            tests_num_success += 1

        tests_data.append({
            "output": output,
            "error": error,
            "success": success
        })

    tmp.remove_file_cpp()
    tmp.remove_file_out()

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