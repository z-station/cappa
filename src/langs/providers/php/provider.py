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
        output = ''
        error = ''
        tmp = TmpFiles(content=content, input=input)
        stdin = input.encode('utf-8')
        try:
            p = subprocess.Popen(['php', tmp.file_php_dir],
                                 stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 cwd=settings.TMP_DIR)
            stdout, stderr = p.communicate(input=stdin, timeout=3)
            output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
        except subprocess.TimeoutExpired:
            output, error = '', msg.PHP__02
        finally:
            p.kill()
            tmp.remove_file_php()
        return {
            'output': output,
            'error': error,
        }

    @classmethod
    def check_tests(cls, content: str, task: Task) -> dict:

        compare_method_name = f'_compare_{task.output_type}'
        compare_method = getattr(cls, compare_method_name)

        tests_data = []

        tests_num_success = 0
        for test in task.tests:
            tmp = TmpFiles(content=content, input=test['input'])

            try:
                p1 = subprocess.Popen(['php', tmp.file_php_dir],
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      cwd=settings.TMP_DIR)
                stdin = test['input'].encode('utf-8')
                stdout, stderr = p1.communicate(input=stdin, timeout=3)
                output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
            except subprocess.TimeoutExpired:
                output, error = '', msg.PHP__02
                tmp.remove_file_php()
            finally:
                p1.kill()


            if error:
                success = False
            else:
                success = compare_method(etalon=clear_text(test['output']),
                                         val=clear_text(output))


            tests_num_success += success

            tests_data.append({
                "output": output,
                "error": error,
                "success": success
            })

        tmp.remove_file_php()
        tests_num = len(task.tests)

        return {
            'num': tests_num,
            'num_success': tests_num_success,
            'data': tests_data,
            'success': tests_num == tests_num_success,
        }

