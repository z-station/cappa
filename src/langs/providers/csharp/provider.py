# -*- coding: utf-8 -*-
import re
import subprocess
from django.conf import settings
from .utils import TmpFiles
from ..base import BaseProvider
from src.tasks.models import Task
from src.utils import msg
from src.utils.editor import clear_text


class Provider(BaseProvider):

    @classmethod
    def _get_decoded(cls, stdout: bytes, stderr: bytes) -> tuple:

        """ Преобразует bytes (вывод компилятора) в unicode, удаляет лишние смиволы из вывода """

        error = re.sub(r'.*.cs', "", stderr.decode("utf-8")) if stderr else ''
        output = re.sub(r'.*.cs:', "", stdout.decode("utf-8")) if stdout else ''
        return output, error

    @classmethod
    def debug(cls, input: str, content: str) -> dict:
        tmp = TmpFiles(content=content)
        p1 = subprocess.Popen(
            args=['mcs', tmp.file_cpp_dir],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=settings.TMP_DIR,
        )
        stdin = input.encode('utf-8')
        stdout, stderr = p1.communicate(input=stdin)
        p1.wait()
        p1.kill()
        output, error = cls._get_decoded(stdout=stdout, stderr=stderr)

        if not error:
            p2 = subprocess.Popen(
                args=['mono', tmp.file_out_dir],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=settings.TMP_DIR,
            )
            try:
                stdout, stderr = p2.communicate(input=stdin)
                output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
            except subprocess.TimeoutExpired:
                output, error = '', msg.CSHARP__02
            finally:
                p2.kill()

        tmp.remove_file_cpp()
        tmp.remove_file_out()
        return {
            'output': output,
            'error': error,
        }

    @classmethod
    def check_tests(cls, content: str, task: Task) -> dict:
        tmp = TmpFiles(content=content)

        compare_method_name = f'_compare_{task.output_type}'
        compare_method = getattr(cls, compare_method_name)

        tests_data = []
        tests_num_success = 0
        args = ['mcs', tmp.file_cpp_dir]
        for test in task.tests:
            p1 = subprocess.Popen(
                args=args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=settings.TMP_DIR,
            )

            stdin = test['input'].encode('utf-8')
            stdout, stderr = p1.communicate(input=stdin)
            p1.wait()
            p1.kill()
            output, error = cls._get_decoded(stdout, stderr)

            if not error:
                p2 = subprocess.Popen(
                    args=['mono', tmp.file_out_dir],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=settings.TMP_DIR,
                )
                try:
                    stdout, stderr = p2.communicate(stdin)
                    output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
                    tmp.remove_file_out()
                except subprocess.TimeoutExpired:
                    output, error = '', msg.CSHARP__02
                finally:
                    p2.kill()

            if error:
                success = False
            else:
                success = compare_method(
                    etalon=clear_text(test['output']),
                    val=clear_text(output)
                )
            tests_num_success += success

            tests_data.append({
                "output": output,
                "error": error,
                "success": success
            })

        tmp.remove_file_cpp()
        tmp.remove_file_out()
        tests_num = len(task.tests)

        return {
            'num': tests_num,
            'num_success': tests_num_success,
            'data': tests_data,
            'success': tests_num == tests_num_success
        }

