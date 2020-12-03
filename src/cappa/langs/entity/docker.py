import os
from dataclasses import dataclass
from django.conf import settings


@dataclass
class ContainerConf:

    """
    name - уникальный идентификатор контейнера
    prefix - идентификатор окружения (dev/prod)
    user - пользователь от имени которого совершаются операции в контейнере
    max_zombie_procs - макс. кол-во мертвых процессов, при котром нужно перезагружать контейнер
    timeout - ограниечение на время выполнения скрипта в песочнице
    cpuset_cpus - номера ядер, занимаемые конейнером
    cpu_quota - максимум нагрузки на занимаемые ядра  (-1 это использование до 100%)
    cpu_shares - относительное количество циклов процессора (относительно 1024)
    mem_reservation - мягкое ограничение на память
    mem_limit -  жесткое ограничение на память
    memswap_limit - ограничение на файл подкачки
    """

    name: str
    prefix: str = settings.DOCKER_PREFIX
    user: str = 'sandbox'
    max_zombie_procs: int = 500
    timeout: int = 5
    cpuset_cpus: int = settings.CORES_FOR_DOCKER
    cpu_quota: int = -1
    cpu_shares: int = 512
    mem_reservation: str = '256m'
    mem_limit: str = '512m'
    memswap_limit: str = '512m'

    @property
    def dockerfile_dir(self):
        return os.path.join(settings.PROVIDERS_DIR, self.name)

    @property
    def tmp_files_dir(self):
        return os.path.join(settings.TMP_DIR, self.name)

    def __post_init__(self):
        os.makedirs(self.tmp_files_dir, mode=0o744, exist_ok=True)

    @property
    def image_tag(self):
        return f'{self.prefix}-{self.name}-image'

    @property
    def container_name(self):
        return f'{self.prefix}-{self.name}-container'