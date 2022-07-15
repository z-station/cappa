from django.core.management import BaseCommand
from app.tasks.models.source import Source
from app.tasks.models.task import Task
from app.tasks.services import SolutionService
from app.tasks.enums import SolutionType
from app.translators.enums import TranslatorType
from app.training.models import TaskItem
from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):

    help = """
        Скопировать код решений python-задач и
        создать специальный тип решений в базе данных

        Пригоден для запуска только внутри контейнера,
        т.к. работает контейнерной базой

        Пример №1 создание внешнего решения
        python manage.py create_external_solutions
    """

    def _clear_code_from_control_characters(self, code: str) -> str:

        if isinstance(code, str):
            return code.replace('\r', '').rstrip('\n')
        else:
            return code

    def _get_list_of_tasks_from_database(self) -> list:

        list_of_tasks = []

        taskitem = TaskItem.objects.prefetch_related('topic__course')

        for task in taskitem:
            if task.topic.course.title == 'Python':
                list_of_tasks.append(task.title)

        return list_of_tasks

    def _get_titles_and_links(self, list_of_tasks) -> dict:

        url_request = requests.get('http://pyanswer.site/sitemap')
        search_setting = BeautifulSoup(url_request.text, 'html.parser')
        search_result = search_setting.find_all('li', {'class': 'wsp-post'})

        pyanswer_tasks = {}
        titles_and_links = {}

        for html_code in search_result:
            a_tag = html_code.a
            link = a_tag.get('href')
            pyanswer_title = a_tag.text.strip()
            first_quote = pyanswer_title.find('«')
            last_quote = pyanswer_title.find('»')
            title = pyanswer_title[first_quote+1:last_quote]
            processed_title = title.replace(' — ', '-')

            if processed_title == 'Сумма факториалов':
                processed_title = processed_title.replace(
                    'Сумма факториалов',
                    'Лесенка'
                )
            elif processed_title == 'Отрицательная степень':
                processed_title = processed_title.replace(
                    'Отрицательная степень',
                    'Степень'
                )
            elif processed_title == 'Минимальный делитель':
                processed_title = processed_title.replace(
                    'Минимальный делитель',
                    'Наименьший делитель'
                )
            elif processed_title == 'Среднее значение последовательности':
                processed_title = processed_title.replace(
                    'Среднее значение последовательности',
                    'Среднее арифметическое'
                )
            elif processed_title == \
                    'Количество элементов, которые больше предыдущего':
                processed_title = processed_title.replace(
                    'Количество элементов, которые больше предыдущего',
                    'Количество элементов, больших предыдущего'
                )
            elif processed_title == 'Количество различных элементов':
                processed_title = processed_title.replace(
                    'Количество различных элементов',
                    'Количество разных элементов'
                )
            elif processed_title == 'Сколько совпадает чисел':
                processed_title = processed_title.replace(
                    'Сколько совпадает чисел',
                    'Сколько чисел совпадают'
                )
            elif processed_title == 'Дележ яблок':
                processed_title = processed_title.replace(
                    'Дележ яблок',
                    'Делёж яблок'
                )
            elif processed_title == 'Минимум из трех чисел':
                processed_title = processed_title.replace(
                    'Минимум из трех чисел',
                    'Минимум из трёх чисел'
                )
            elif processed_title == 'Разность времен':
                processed_title = processed_title.replace(
                    'Разность времен',
                    'Разность времён'
                )
            elif processed_title == 'Четные индексы':
                processed_title = processed_title.replace(
                    'Четные индексы',
                    'Чётные индексы'
                )
            elif processed_title == 'Четные элементы':
                processed_title = processed_title.replace(
                    'Четные элементы',
                    'Чётные элементы'
                )
            elif processed_title == 'Угадай число-2':
                processed_title = processed_title.replace(
                    'Угадай число-2',
                    'Угадай число - 2'
                )
            pyanswer_tasks.update({processed_title: link})

        pyanswer_task_titles = pyanswer_tasks.keys()

        for task_title in list(pyanswer_task_titles):
            if 'Задача №' in task_title:
                del pyanswer_tasks[task_title]

        for task_title in list_of_tasks:
            for title, link in pyanswer_tasks.items():
                if task_title == title:
                    titles_and_links.update({title: link})

        return titles_and_links

    def _get_titles_and_codes(self, titles_and_links: dict) -> dict:

        titles_and_codes = {}

        for title, link in titles_and_links.items():
            extracted_url = link
            url_request = requests.get(extracted_url)
            search_class = "fusion-syntax-highlighter-textarea"
            search_setting = BeautifulSoup(
                url_request.text, 'html.parser'
            )
            search_result = search_setting.find(
                'textarea', class_=search_class
            )
            pyanswer_code = search_result.text
            code = self._clear_code_from_control_characters(
                pyanswer_code
            )
            titles_and_codes.update({title: code})

        return titles_and_codes

    def handle(self, *args, **options):

        list_of_tasks = self._get_list_of_tasks_from_database()
        titles_and_links = self._get_titles_and_links(list_of_tasks)
        titles_and_codes = self._get_titles_and_codes(titles_and_links)
        task_titles = titles_and_codes.keys()

        pyanswer_source, _ = Source.objects.get_or_create(
            name='PyAnswer',
            description='Решения задач с сайта Питонтьютор'
        )

        tasks = Task.objects.filter(
            title__in=task_titles
        ).prefetch_related('solutions')

        parsed_tasks_counter = 0

        for task in tasks:
            if task.solutions.filter(
                translator=TranslatorType.PYTHON38,
                type=SolutionType.EXTERNAL,
                external_source=pyanswer_source
            ).exists():
                self.stdout.write('Внешнее решение задачи уже существует')
            else:
                link = titles_and_links.get(task.title, '')
                SolutionService.create_external(
                    external_source=pyanswer_source,
                    task=task,
                    description=f'<a target="_blank" href="{link}">{link}</a>' if link else '',
                    content=titles_and_codes[task.title],
                    translator=TranslatorType.PYTHON38
                )
                self.stdout.write(
                    f'Создано внешнее решение задачи "{task.title}"'
                )
                parsed_tasks_counter += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Число распарсенных страниц - {len(titles_and_codes)}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Число созданных внешних решений - {parsed_tasks_counter}'
            )
        )
