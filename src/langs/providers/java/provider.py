# -*- coding: utf-8 -*-
import re
import subprocess
from django.conf import settings
from .utils import TmpFiles
from ..base import BaseProvider
from src.tasks.models import Task
from src.utils.editor import clear_text


class Provider(BaseProvider):

    @classmethod
    def _get_decoded(cls, stdout: bytes, stderr: bytes) -> tuple:
        output = stdout.decode()
        error = re.sub(r'.*.java:', "", stderr.decode()) if stderr else ''
        return output, error

    @classmethod
    def debug(cls, input: str, content: str) -> dict:
        stdin = input.encode('utf-8')
        tmp = TmpFiles(content=content)
        p1 = subprocess.Popen(
            args=['java', tmp.file_java_dir],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=settings.TMP_DIR
        )
        stdout, stderr = p1.communicate(input=stdin)
        p1.kill()
        output, error = cls._get_decoded(stdout=stdout, stderr=stderr)

        tmp.remove_file_java()

        return {
            'output': output,
            'error': error,
        }

    @classmethod
    def check_tests(cls, content: str, task: Task) -> dict:
        tmp = TmpFiles(clear_text(content))

        compare_method_name = f'_compare_{task.output_type}'
        compare_method = getattr(cls, compare_method_name)

        tests_data = []
        tests_num_success = 0
        for test in task.tests:
            p1 = subprocess.Popen(
                args=['java', tmp.file_java_dir],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=settings.TMP_DIR
            )

            stdin = test['input'].encode('utf-8')
            stdout, stderr = p1.communicate(input=stdin)
            p1.kill()
            output, error = cls._get_decoded(stdout, stderr)

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

        tmp.remove_file_java()

        tests_num = len(task.tests)

        return {
            'num': tests_num,
            'num_success': tests_num_success,
            'data': tests_data,
            'success': tests_num == tests_num_success
        }
