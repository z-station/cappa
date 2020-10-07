# -*- coding: utf-8 -*-
import re

from django.conf import settings

from .utils import DebugFiles
from ..base import DockerProvider
from src.tasks.models import Task
from src.utils.editor import clear_text


class Provider(DockerProvider):

    conf = settings.DOCKER_CONF['cpp']

    @classmethod
    def _get_decoded(cls, stdout: bytes, stderr: bytes) -> tuple:

        """ Преобразует bytes (вывод компилятора) в unicode, удаляет лишние смиволы из вывода """

        output = stdout.decode()
        error = re.sub(r'.*.cpp:', "", stderr.decode()) if stderr else ''
        return output, error

    @classmethod
    def debug(cls, input: str, content: str) -> dict:
        files = DebugFiles(data_in=clear_text(input), data_cpp=clear_text(content))
        container = cls._get_docker_container()
        exit_code, result = container.exec_run(
            cmd=f'bash -c "timeout {cls.conf["timeout"]} c++ {files.filename_cpp} -o {files.filename_out} < {files.filename_in}"',
            stream=True, demux=True, user=cls.conf['user']
        )
        print('===', exit_code, result)
        #
        # if not error:
        #     p2 = subprocess.Popen(
        #         args=[tmp.file_out_dir],
        #         stdin=subprocess.PIPE,
        #         stdout=subprocess.PIPE,
        #         stderr=subprocess.PIPE,
        #         cwd=settings.TMP_DIR,
        #     )
        #     try:
        #         stdout, stderr = p2.communicate(input=stdin)
        #         output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
        #     except subprocess.TimeoutExpired:
        #         output, error = '', msg.CPP__02
        #     finally:
        #         p2.kill()
        #
        # tmp.remove_file_cpp()
        # tmp.remove_file_out()
        return {
            'output': 'output',
            'error': 'error',
        }

    @classmethod
    def check_tests(cls, content: str, task: Task) -> dict:
        # tmp = TmpFiles(clear_text(content))
        #
        # compare_method_name = f'_compare_{task.output_type}'
        # compare_method = getattr(cls, compare_method_name)
        #
        # tests_data = []
        # tests_num_success = 0
        # args = ['c++', tmp.file_cpp_dir, '-o', tmp.filename_out]
        # for test in task.tests:
        #     p1 = subprocess.Popen(
        #         args=args,
        #         stdin=subprocess.PIPE,
        #         stdout=subprocess.PIPE,
        #         stderr=subprocess.PIPE,
        #         cwd=settings.TMP_DIR,
        #     )
        #
        #     stdin = test['input'].encode('utf-8')
        #     stdout, stderr = p1.communicate(input=stdin)
        #     p1.wait()
        #     p1.kill()
        #     output, error = cls._get_decoded(stdout, stderr)
        #
        #     if not error:
        #         p2 = subprocess.Popen(
        #             args=[tmp.file_out_dir],
        #             stdin=subprocess.PIPE,
        #             stdout=subprocess.PIPE,
        #             stderr=subprocess.PIPE,
        #             cwd=settings.TMP_DIR,
        #         )
        #         try:
        #             stdout, stderr = p2.communicate(stdin)
        #             output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
        #             tmp.remove_file_out()
        #         except subprocess.TimeoutExpired:
        #             output, error = '', msg.CPP__02
        #         finally:
        #             p2.kill()
        #
        #     if error:
        #         success = False
        #     else:
        #         success = compare_method(
        #             etalon=clear_text(test['output']),
        #             val=clear_text(output)
        #         )
        #     tests_num_success += success
        #
        #     tests_data.append({
        #         "output": output,
        #         "error": error,
        #         "success": success
        #     })
        #
        # tmp.remove_file_cpp()
        # tmp.remove_file_out()
        # tests_num = len(task.tests)

        return {
            'num': "tests_num",
            'num_success': "tests_num_success",
            'data': "tests_data",
            'success': "tests_num == tests_num_success"
        }

