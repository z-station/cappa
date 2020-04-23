import re
import docker
from docker import errors
from django.conf import settings
from .utils import DebugFiles, TestsFiles
from ..base import BaseProvider
from src.tasks.models import Task
from src.utils import msg as msg_utils
from src.utils.editor import clear_text

docker_conf = settings.DOCKER_CONF['python']
client = docker.from_env()
api_client = docker.APIClient()


class Provider(BaseProvider):

    @classmethod
    def _process_error_msg(cls, msg: str):

        """ Обработка текста сообщения об ошибке """

        result = clear_text(re.sub(r'\s*File.+.py",', "", msg))
        if 'Terminated' in result:
            result = msg_utils.PYTHON__02
        if 'Read-only file system' in result:
            result = msg_utils.PYTHON__01
        return result

    @classmethod
    def _get_decoded(cls, stdout: bytes, stderr: bytes) -> tuple:

        """ Преобразует bytes (вывод интерпретатора) в unicode, удаляет лишние смиволы из вывода """

        output = '' if stdout is None else stdout.decode()
        if stderr is None:
            error = ''
        else:
            error = cls._process_error_msg(msg=stderr.decode())
        return output, error

    @classmethod
    def _get_docker_image(cls):

        """ Создает и возвращает docker-образ python песочницы """

        try:
            image = client.images.get(name=docker_conf['image_tag'])
        except errors.ImageNotFound:
            image, logs = client.images.build(
                path=docker_conf['path'],
                tag=docker_conf['image_tag']
            )
        return image

    @classmethod
    def _get_docker_container(cls):

        """ Запускает и возвращает docker-контейнер python песочницы """

        try:
            container = client.containers.get(container_id=docker_conf["container_name"])
        except errors.NotFound:
            image = cls._get_docker_image()
            container = client.containers.run(
                image=image,
                name=docker_conf['container_name'],
                detach=True, auto_remove=True,
                stdin_open=True, stdout=True, stderr=True,
                cpuset_cpus=docker_conf['cpuset_cpus'],
                cpu_quota=docker_conf['cpu_quota'],
                cpu_shares=docker_conf['cpu_shares'],
                mem_reservation=docker_conf['mem_reservation'],
                mem_limit=docker_conf['mem_limit'],
                memswap_limit=docker_conf['memswap_limit'],
                volumes={docker_conf['dir']: {'bind': f'/home/{docker_conf["user"]}/', 'mode': 'ro'}}
            )
        return container

    @classmethod
    def debug(cls, input: str, content: str) -> dict:
        files = DebugFiles(data_in=clear_text(input), data_py=clear_text(content))
        container = cls._get_docker_container()
        exit_code, result = container.exec_run(
            cmd=f'bash -c "timeout {docker_conf["timeout_duration"]} python {files.filename_py} < {files.filename_in}"',
            stream=True, demux=True, user=docker_conf['user']
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
        compare_method_name = f'_compare_{task.output_type}'
        compare_method = getattr(cls, compare_method_name)
        files = TestsFiles(data_py=clear_text(content))
        container = cls._get_docker_container()
        tests_data = []
        tests_num_success = 0
        for test in task.tests:
            filename_in = files.create_file_in(data_in=clear_text(test['input']))
            exit_code, result = container.exec_run(
                cmd=f'bash -c "timeout {docker_conf["timeout_duration"]} python {files.filename_py} < {filename_in}"',
                stream=True, demux=True, user=docker_conf['user']
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
