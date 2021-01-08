# -*- coding: utf-8 -*-
import re

from .utils import DebugFiles, TestsFiles
from ..base import DockerProvider
from src.tasks.models import Task
from src.utils import msg as msg_utils
from src.utils.editor import clear_text
from src.langs.entity.docker import ContainerConf


class Provider(DockerProvider):

    conf = ContainerConf(name='java')

    @classmethod
    def _process_error_msg(cls, msg: str):

        """ Обработка текста сообщения об ошибке """

        result = clear_text(
            re.sub(pattern='program.java',  repl="", string=msg)
        )
        if 'Terminated' in result:
            result = msg_utils.JAVA__02
        if 'Read-only file system' in result:
            result = msg_utils.JAVA__01
        return result

    @classmethod
    def _get_decoded(cls, stdout: bytes, stderr: bytes) -> tuple:

        """ Преобразует bytes (вывод интерпретатора) в unicode, удаляет лишние символы из вывода """

        output = '' if stdout is None else stdout.decode()
        if stderr is None:
            error = ''
        else:
            error = cls._process_error_msg(msg=stderr.decode())
        return output, error

    @classmethod
    def debug(cls, input: str, content: str) -> dict:

        """ Запускает код в docker-песочнице и возвращает результаты """

        files = DebugFiles(
            data_in=clear_text(input),
            data_java=clear_text(content),
            tmp_dir=cls.conf.tmp_files_dir
        )
        container = cls._get_docker_container()
        exit_code, result = container.exec_run(
            cmd=f'bash -c "timeout {cls.conf.timeout} java {files.filename_java} < {files.filename_in}"',
            stream=True, demux=True, user=cls.conf.user
        )
        try:
            stdout, stderr = next(result)
        except StopIteration:
            output, error = '', ''
        else:
            output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
        files.remove()
        return {
            'output': output,
            'error': error
        }

    @classmethod
    def check_tests(cls, content: str, task: Task) -> dict:

        """ Запускает код на наборе тестов в docker-песочнице и возвращает результаты тестирования """

        compare_method_name = f'_compare_{task.output_type}'
        compare_method = getattr(cls, compare_method_name)
        files = TestsFiles(
            data_java=clear_text(content),
            tmp_dir=cls.conf.tmp_files_dir
        )
        container = cls._get_docker_container()
        tests_data = []
        tests_num_success = 0
        for test in task.tests:
            filename_in = files.create_file_in(data_in=clear_text(test['input']))
            exit_code, result = container.exec_run(
                cmd=f'bash -c "timeout {cls.conf.timeout} java {files.filename_java} < {filename_in}"',
                stream=True, demux=True, user=cls.conf.user
            )
            try:
                stdout, stderr = next(result)
            except StopIteration:
                output, error = '', ''
            else:
                output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
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

        files.remove()

        tests_num = len(task.tests)
        return {
            'num': tests_num,
            'num_success': tests_num_success,
            'data': tests_data,
            'success': tests_num == tests_num_success,
        }
