import re
import subprocess
from django.conf import settings
from .utils import TmpFile
from ..base import BaseProvider
from src.tasks.models import Task
from src.utils import msg
from src.utils.editor import clear_text


class Provider(BaseProvider):

    @classmethod
    def _get_decoded(cls, stdout: bytes, stderr: bytes) -> tuple:

        """ Преобразует bytes (вывод интерпретатора) в unicode, удаляет лишние смиволы из вывода """

        output = stdout.decode()
        error = re.sub(r'\s*File.+.py",', "", stderr.decode()) if stderr else ''
        return output, error

    @classmethod
    def debug(cls, input: str, content: str) -> dict:
        tmp_file = TmpFile(content=content)
        try:
            proc = subprocess.Popen(
                args=[settings.PYTHON_PATH, tmp_file.filename],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=settings.TMP_DIR,
            )
        except FileNotFoundError:
            raise Exception(msg.PYTHON__01)
        except subprocess.TimeoutExpired:
            output, error = '', msg.PYTHON__02
        else:
            stdin = clear_text(input).encode('utf-8')
            stdout, stderr = proc.communicate(input=stdin)
            proc.kill()
            output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
        finally:
            tmp_file.remove()
        return {
            'output': output,
            'error': error
        }

    @classmethod
    def check_tests(cls, content: str, task: Task) -> dict:
        tmp_file = TmpFile(clear_text(content))

        compare_method_name = f'_compare_{task.output_type}'
        compare_method = getattr(cls, compare_method_name)

        tests_data = []
        tests_num_success = 0
        args = [settings.PYTHON_PATH, tmp_file.filename]
        for test in task.tests:
            try:
                proc = subprocess.Popen(
                    args=args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=settings.TMP_DIR,
                )
            except FileNotFoundError:
                raise Exception(msg.PYTHON__01)
            except subprocess.TimeoutExpired:
                success, output, error = False, '', msg.PYTHON__02
            else:
                stdin = clear_text(test['input']).encode('utf-8')
                stdout, stderr = proc.communicate(input=stdin)
                proc.kill()
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

        tmp_file.remove()

        tests_num = len(task.tests)
        return {
            'num': tests_num,
            'num_success': tests_num_success,
            'data': tests_data,
            'success': tests_num == tests_num_success,
        }
