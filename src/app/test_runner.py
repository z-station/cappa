import os

from django.apps import apps
from django.conf import settings
from django.test.runner import DiscoverRunner


class CappaDiscoverRunner(DiscoverRunner):
    """
    Test runner проекта cappa.

    При запуске ``manage.py test`` без аргументов стандартный ``DiscoverRunner``
    ищет тесты от текущей директории (``.``). В этом проекте это приводит к
    ложным импортам модулей вроде ``app.service.admin`` и пропуску тестов из
    пакетов, не зарегистрированных в ``INSTALLED_APPS`` (например,
    ``app.auth.tests``).

    Если метки тестов не переданы, runner собирает модули ``app.<имя>/tests/``
    из ``PROJECT_DIR``. Если таких пакетов нет, используется запасной вариант:
    модули ``tests`` у приложений из ``INSTALLED_APPS`` с префиксом ``app.``.

    Явно указанные метки (``manage.py test app.auth.tests``) обрабатываются
    как обычно.
    """

    def _discover_project_test_modules(self):
        test_labels = []
        for app_name in os.listdir(settings.PROJECT_DIR):
            tests_init = os.path.join(
                settings.PROJECT_DIR,
                app_name,
                'tests',
                '__init__.py',
            )
            if os.path.isfile(tests_init):
                test_labels.append(f'app.{app_name}.tests')
        return test_labels

    def build_suite(self, test_labels=None, extra_tests=None, **kwargs):
        if not test_labels:
            test_labels = self._discover_project_test_modules()
            if not test_labels:
                for app_config in apps.get_app_configs():
                    if not app_config.name.startswith('app.'):
                        continue
                    tests_module = f'{app_config.name}.tests'
                    try:
                        __import__(tests_module)
                    except ImportError:
                        continue
                    test_labels.append(tests_module)
        return super().build_suite(test_labels, extra_tests, **kwargs)
