import re
import uuid
import docker
from docker import errors
from django.conf import settings
from .utils import DebugFiles, TestsFiles
from ..base import BaseProvider
from src.tasks.models import Task
from src.utils import msg as msg_utils
from src.utils.editor import clear_text

conf = settings.DOCKER_CONF['python']
client = docker.from_env()


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
            image = client.images.get(name=conf['image_tag'])
        except errors.ImageNotFound:
            image, logs = client.images.build(
                path=conf['path'],
                tag=conf['image_tag']
            )
        return image

    @classmethod
    def _get_docker_container(cls):

        """ Запускает и возвращает docker-контейнер python песочницы """

        try:
            container = client.containers.get(container_id=conf["container_name"])
        except errors.NotFound:
            image = cls._get_docker_image()
            try:
                container = client.containers.run(
                    image=image,
                    name=conf['container_name'],
                    detach=True, auto_remove=True,
                    stdin_open=True, stdout=True, stderr=True,
                    cpuset_cpus=conf['cpuset_cpus'],
                    cpu_quota=conf['cpu_quota'],
                    cpu_shares=conf['cpu_shares'],
                    mem_reservation=conf['mem_reservation'],
                    mem_limit=conf['mem_limit'],
                    memswap_limit=conf['memswap_limit'],
                    volumes={conf['dir']: {'bind': f'/home/{conf["user"]}/', 'mode': 'ro'}}
                )
            except errors.APIError:  # На случай если другой процесс создал контейнер быстрее
                container = client.containers.get(container_id=conf["container_name"])
        return container

    @classmethod
    def _stop_docker_container(cls):

        """ Мягкая остановка контейнера
            Перерменование и только затем остановка, необходимо для того чтобы
            другие процессы не успевали подключиться к выключаемому контейнеру.
            Вместо этого они будут инициировать старт нового контейнера.
        """

        container = client.containers.get(container_id=conf["container_name"])
        container.rename(name=f'trash-{uuid.uuid1()}')
        container.stop()

    @classmethod
    def _check_zombie_procs(cls):

        """ Проверяет количество мертвых процессов в контейнере и если нужно останавливает его
            Команда timeout контролирует время выполнения кода в песочнице, но
            пораждает мертвые процессы в контейнере (возможно характерно только для linux Alpine),
            которые можно убить только остановив контейнер.
        """

        container = cls._get_docker_container()
        exit_code, result = container.exec_run(
            cmd=f'bash -c "ps axu | grep -c timeout"',
            stream=True, demux=True, user=conf['user']
        )
        stdout, stderr = next(result)
        count_zombie_procs = int(stdout.decode())
        if count_zombie_procs > conf['max_zombie_procs']:
            cls._stop_docker_container()

    @classmethod
    def debug(cls, input: str, content: str) -> dict:

        """ Запускает код в docker-песочнице и возвращает результаты """

        files = DebugFiles(data_in=clear_text(input), data_py=clear_text(content))
        container = cls._get_docker_container()
        exit_code, result = container.exec_run(
            cmd=f'bash -c "timeout {conf["timeout"]} python {files.filename_py} < {files.filename_in}"',
            stream=True, demux=True, user=conf['user']
        )
        try:
            stdout, stderr = next(result)
        except StopIteration:
            output, error = '', ''
        else:
            output, error = cls._get_decoded(stdout=stdout, stderr=stderr)
        files.remove()
        cls._check_zombie_procs()
        return {
            'output': output,
            'error': error
        }

    @classmethod
    def check_tests(cls, content: str, task: Task) -> dict:

        """ Запускает код на наборе тестов в docker-песочнице и возвращает результаты тестирования """

        compare_method_name = f'_compare_{task.output_type}'
        compare_method = getattr(cls, compare_method_name)
        files = TestsFiles(data_py=clear_text(content))
        container = cls._get_docker_container()
        tests_data = []
        tests_num_success = 0
        for test in task.tests:
            filename_in = files.create_file_in(data_in=clear_text(test['input']))
            exit_code, result = container.exec_run(
                cmd=f'bash -c "timeout {conf["timeout"]} python {files.filename_py} < {filename_in}"',
                stream=True, demux=True, user=conf['user']
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
        cls._check_zombie_procs()
        return {
            'num': tests_num,
            'num_success': tests_num_success,
            'data': tests_data,
            'success': tests_num == tests_num_success,
        }