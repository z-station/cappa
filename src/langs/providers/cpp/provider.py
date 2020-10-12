# -*- coding: utf-8 -*-
import re
import time

from .utils import DebugFiles
from ..base import DockerProvider
from src.tasks.models import Task
from src.utils.editor import clear_text
from src.langs.entity.docker import ContainerConf


class Provider(DockerProvider):

    conf = ContainerConf(name='cpp')

    @classmethod
    def _get_decoded(cls, stdout: bytes, stderr: bytes) -> tuple:

        """ Преобразует bytes (вывод компилятора) в unicode, удаляет лишние смиволы из вывода """

        if isinstance(stdout, bytes):
            output = stdout.decode()
        elif stdout is None:
            output = ''
        else:
            output = stdout

        if isinstance(stderr, bytes):
            error = stderr.decode()
        elif stderr is None:
            error = ''
        else:
            error = stderr
        error = re.sub(pattern='.*.out:', repl="", string=error)
        return output, error

    @classmethod
    def debug(cls, input: str, content: str) -> dict:
        files = DebugFiles(
            data_in=clear_text(input),
            data_cpp=clear_text(content),
            tmp_dir=cls.conf.tmp_files_dir
        )
        container = cls._get_docker_container()
        exit_code, _ = container.exec_run(
            cmd=f'bash -c "timeout {cls.conf.timeout} c++ {files.filename_cpp} -o {files.path_out}"',
            user=cls.conf.user, stream=True, demux=True
        )
        time.sleep(1)
        exit_code, result = container.exec_run(
            cmd=f'bash -c "timeout {cls.conf.timeout} {files.path_out} < {files.filename_in}"',
            user=cls.conf.user, stream=True, demux=True
        )
        try:
            stdout, stderr = next(result)
        except StopIteration:
            output, error = '', ''
        else:
            output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
        finally:
            exit_code, _ = container.exec_run(
                cmd=f'bash -c "rm {files.path_out}"',
                user=cls.conf.user, stream=True, demux=True
            )
            files.remove()
        cls._check_zombie_procs()
        return {
            'output': output,
            'error': error,
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

