# -*- coding: utf-8 -*-
import re
import time

from .utils import DebugFiles, TestsFiles
from ..base import DockerProvider
from src.tasks.models import Task
from src.utils import msg as msg_utils
from src.utils.editor import clear_text
from src.langs.entity.docker import ContainerConf


class Provider(DockerProvider):

    conf = ContainerConf(name='cpp')

    @classmethod
    def _process_error_msg(cls, msg: str):

        """ Обработка текста сообщения об ошибке """

        result = clear_text(
            re.sub(pattern='.*.[out|cpp]{1}:', repl="", string=msg)
        )
        if 'Terminated' in result:
            result = msg_utils.CPP__02
        if 'Read-only file system' in result:
            result = msg_utils.CPP__01
        if 'the monitored command dumped core' in result:
            result = msg_utils.CPP__03
        return result

    @classmethod
    def _get_decoded(cls, stdout: bytes, stderr: bytes) -> tuple:

        """ Преобразует bytes (вывод компилятора) в unicode, удаляет лишние символы из вывода """

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
        error = cls._process_error_msg(msg=error)
        return output, error

    @classmethod
    def debug(cls, input: str, content: str) -> dict:
        files = DebugFiles(
            data_in=clear_text(input),
            data_cpp=clear_text(content),
            tmp_dir=cls.conf.tmp_files_dir
        )
        container = cls._get_docker_container()
        try:
            exit_code, result = container.exec_run(
                cmd=f'bash -c "timeout {cls.conf.timeout} c++ {files.filename_cpp} -o {files.path_out}"',
                user=cls.conf.user, stream=True, demux=True
            )
            try:
                stdout, stderr = next(result)
                output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
            except StopIteration:
                output, error = '', ''
            if not error:
                time.sleep(1)
                exit_code, result = container.exec_run(
                    cmd=f'bash -c "timeout {cls.conf.timeout} {files.path_out} < {files.filename_in}"',
                    user=cls.conf.user, stream=True, demux=True
                )
                try:
                    stdout, stderr = next(result)
                    output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
                except StopIteration:
                    output, error = '', ''
        finally:
            exit_code, _ = container.exec_run(
                cmd=f'bash -c "rm {files.path_out}"',
                user=cls.conf.user, stream=True, demux=True
            )
            files.remove()
        return {
            'output': output,
            'error': error,
        }

    @classmethod
    def check_tests(cls, content: str, task: Task) -> dict:

        """ Запускает код на наборе тестов в docker-песочнице и возвращает результаты тестирования """

        compare_method_name = f'_compare_{task.output_type}'
        compare_method = getattr(cls, compare_method_name)
        files = TestsFiles(
            data_cpp=clear_text(content),
            tmp_dir=cls.conf.tmp_files_dir
        )
        container = cls._get_docker_container()
        tests_data = []
        tests_num_success = 0
        tests_num = len(task.tests)
        try:
            exit_code, result = container.exec_run(
                cmd=f'bash -c "timeout {cls.conf.timeout} c++ {files.filename_cpp} -o {files.path_out}"',
                user=cls.conf.user, stream=True, demux=True
            )
            try:
                stdout, stderr = next(result)
                output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
            except StopIteration:
                output, error = '', ''
            if error:
                for test in task.tests:
                    tests_data.append({
                        "output": output,
                        "error": error,
                        "success": False
                    })
                result = {
                    'num': tests_num,
                    'num_success': 0,
                    'data': tests_data,
                    'success': False
                }
            else:
                time.sleep(1)
                for test in task.tests:
                    filename_in = files.create_file_in(data_in=clear_text(test['input']))
                    exit_code, result = container.exec_run(
                        cmd=f'bash -c "timeout {cls.conf.timeout} {files.path_out} < {filename_in}"',
                        user=cls.conf.user, stream=True, demux=True
                    )
                    try:
                        stdout, stderr = next(result)
                        output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
                    except StopIteration:
                        output, error = '', ''
                    if error:
                        success = False
                    else:
                        success = compare_method(
                            etalon=clear_text(test['output']),
                            val=clear_text(output)
                        )
                    tests_num_success += success
                    tests_data.append({
                        "output": clear_text(output),
                        "error": error,
                        "success": success
                    })
                result = {
                    'num': tests_num,
                    'num_success': tests_num_success,
                    'data': tests_data,
                    'success': tests_num == tests_num_success,
                }

        finally:
            exit_code, _ = container.exec_run(
                cmd=f'bash -c "rm {files.path_out}"',
                user=cls.conf.user, stream=True, demux=True
            )
            files.remove()
        return result
