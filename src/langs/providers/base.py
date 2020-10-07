import docker
import uuid
from abc import abstractmethod
from django.conf import settings
from docker import errors
from src.tasks.models import Task


class BaseProvider(object):

    """ Реализует обязательные методы провайдера языка программирования """

    @classmethod
    def _compare_str(cls, etalon: str, val: str) -> bool:

        """ Сравнение двух строковых значений построчно """

        result = True
        new_line = '\n'
        if new_line not in etalon:
            result = etalon == val
        else:
            e_list = etalon.split(new_line)
            v_list = val.split(new_line)
            if len(e_list) != len(v_list):
                result = False
            else:
                for e, v in zip(e_list, v_list):
                    if e != v:
                        result = False
                        break
        return result

    @classmethod
    def _compare_int(cls, etalon: str, val: str) -> bool:

        """ Сравнение двух целочисленных значений

            :param etalon: str - эталонное значение для сравнения
            :param val: str - сравниваемое с эталоном значение

            Перед сравнением:
            - проверить, если эталон это несколько значений, каждое с новой строки, то сравнивать построчно
        """

        def compare(etalon: str, val: str) -> bool:

            """ Сравнивает две строки как целые числа

             если строка не является целым числом (а возможно float) то это ошибка """

            if val.isdigit() and etalon.isdigit():
                return int(etalon) == int(val)
            else:
                return False

        result = True
        new_line = '\n'
        if new_line not in etalon:
            result = compare(etalon, val)
        else:
            e_list = etalon.split(new_line)
            v_list = val.split(new_line)
            if len(e_list) != len(v_list):
                result = False
            else:
                for e, v in zip(e_list, v_list):
                    if not compare(e, v):
                        result = False
                        break
        return result

    @classmethod
    def _compare_float(cls, etalon: str, val: str) -> bool:

        """ Сравнение двух значений с плавающей точкой

            :param etalon: str - эталонное значение для сравнения
            :param val: str - сравниваемое с эталоном значение

            Перед сравнением:
            - проверить, если эталон это несколько значений, каждое с новой строки, то сравнивать построчно
            - перевести число из экспоненциальной в десятичную форму
            - привести кол-во разрядов в дробной часи чисел к общему значению

            Если etalon - некорректное значение то будет возбуждено исключение ValueError
        """

        def compare(etalon: str, val: str) -> bool:
            try:
                if 'e' in etalon:
                    etalon = format(float(etalon), 'f')
                if 'e' in val:
                    val = format(float(val), 'f')

                parts = etalon.split('.')
                if len(parts) == 1:
                    sign_part_len = 0
                elif len(parts) == 2:
                    sign_part_len = len(parts[1])
                else:
                    raise ValueError()
                result = round(float(val), sign_part_len) == float(etalon)
            except ValueError:
                result = False
            return result

        result = True
        new_line = '\n'
        if new_line not in etalon:
            result = compare(etalon, val)
        else:
            e_list = etalon.split(new_line)
            v_list = val.split(new_line)
            if len(e_list) != len(v_list):
                result = False
            else:
                for e, v in zip(e_list, v_list):
                    if not compare(e, v):
                        result = False
                        break
        return result

    @abstractmethod
    def debug(self, input: str, content: str) -> dict:

        """
        return {
            "output": "str",
            "error": "str"
        }

        """
        pass

    @abstractmethod
    def check_tests(cls, content: str, task: Task) -> dict:

        """
          return {
            'num': "int",
            'num_success': "int",
            'success': "bool",
            'tests_data': [
                {
                    "output": "str",
                    "error": "str,
                    "success": "bool"
                },
                {
                    "output": "str",
                    "error": "str,
                    "success": "bool"
                },
                # ...
            ]
          }

        """
        pass


class DockerProvider(BaseProvider):

    prefix = settings.DOCKER_CONF['prefix']
    client = docker.from_env()

    @property
    @abstractmethod
    def provider_name(self):
        pass

    @property
    def conf(self):
        return settings.DOCKER_CONF[self.provider_name]

    @classmethod
    def _get_docker_image(cls):

        """ Создает и возвращает docker-образ python песочницы """

        image_tag = cls.prefix + cls.conf['image_tag']
        try:
            image = cls.client.images.get(name=image_tag)
        except errors.ImageNotFound:
            image, logs = cls.client.images.build(
                path=cls.conf['path'],
                tag=image_tag
            )
        return image

    @classmethod
    def _get_docker_container(cls):

        """ Запускает и возвращает docker-контейнер python песочницы """

        container_id = cls.prefix + cls.conf["container_name"]
        try:
            container = cls.client.containers.get(container_id=container_id)
        except errors.NotFound:
            image = cls._get_docker_image()
            try:
                container = cls.client.containers.run(
                    image=image,
                    name=container_id,
                    detach=True, auto_remove=True,
                    stdin_open=True, stdout=True, stderr=True,
                    cpuset_cpus=cls.conf['cpuset_cpus'],
                    cpu_quota=cls.conf['cpu_quota'],
                    cpu_shares=cls.conf['cpu_shares'],
                    mem_reservation=cls.conf['mem_reservation'],
                    mem_limit=cls.conf['mem_limit'],
                    memswap_limit=cls.conf['memswap_limit'],
                    volumes={cls.conf['dir']: {'bind': f'/home/{cls.conf["user"]}/', 'mode': 'ro'}}
                )
            except errors.APIError:  # На случай если другой процесс создал контейнер быстрее
                container = cls.client.containers.get(container_id=container_id)
        return container

    @classmethod
    def _stop_docker_container(cls):

        """ Мягкая остановка контейнера

            Перерменование и только затем остановка, необходимо для того чтобы
            другие процессы не успевали подключиться к выключаемому контейнеру.
            Вместо этого они будут инициировать старт нового контейнера.
        """
        container_id = cls.prefix + cls.conf["container_name"]
        container = cls.client.containers.get(container_id=container_id)
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
            stream=True, demux=True, user=cls.conf['user']
        )
        stdout, stderr = next(result)
        count_zombie_procs = int(stdout.decode())
        if count_zombie_procs > cls.conf['max_zombie_procs']:
            cls._stop_docker_container()
