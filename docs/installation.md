#### Инструкция по развертке среды разработчика


1. Установить на рабочей машине требуемое ПО:
- python >= 3.6
- pipenv
- pycharm
- git

Допустимо использовать любую популярную OC (Windows, Mac, Linux)
Установка на примере Linux Ubuntu 18.04 LTS:
```bash
# python уже будет предустановлен
# установка git
sudo apt install git
# установка pipenv
sudo apt install python3-pip python3-dev
pip3 install --user pipenv
echo "PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
```
pycharm устанавливается через менеджер приложений.

2. Развернуть git-репозиторий проекта

- зарегистрироваться на github;
- сделать форк репозитория;
- настроить глобальный git config;
- склонировать репозиторий на машину разработчика;

3. Подготовка проекта
- открыть склонированный проект в pycharm;
- создать файл локальных настроек проекта ``cappa/src/settings/local.py`` со следующим содержимым:
```python
SECRET_KEY = 'wp-8k64@_1aqkag-7mwgk)=f2irdv32#4y$0bhuxa7i03m802r'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "test_db",
    }
}
```
4. Установка python зависимостей

Создать и активировать виртуальное окружение pipenv:
- Первый вариант: через интерфейс pycharm (в настройках интерпретатора)
- Второй вариант: через консоль, находясь в корне проекта ввести команды:
```
pipenv install
pipenv shell
```
5. Запустить локальный сервер на тестовой базе данных.

- Находясь в корне проекта выполнить команду:
``python manage.py runserver``. После этого сайт должен запустится на локальном сервере. Открыть в браузере адрес ``http://localhost:8000/``

- Для входа в административный интерфейс перейдите по адресу ``http://localhost:8000/admin/``, логин / пароль суперпользователя: admin / 1


6. Подключение базы данных postgresql

Тестовая база данных sqlite3 не может обеспечить требуемый функционал, потому подходит только для ознакомления с проектом.

- установить последний postgresql;

Установка на примере Linux Ubuntu 18.04 LTS:
```bash
sudo add-apt-repository "deb https://apt.postgresql.org/pub/repos/apt bionic-pgdg main"
wget --quiet -O - https://postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add
sudo apt-get update

sudo apt install postgresql postgresql-contrib postgresql-server-dev-12
sudo dpkg --get-selections | grep postgres
sudo pg_ctlcluster 12 main start
sudo passwd postgres
# Ввести пароль: 1
su postgres
# создать пользователя postgres одноименного пользователю системы
createuser --interactive <user>
# применить изменения
sudo systemctl restart postgresql

```

- удалить из ``cappa/src/settings/local.py`` настройки тестовой базы данных:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "test_db",
    }
}
```
- создать postgresql базу данных с именем "cappa";
- применить файлы миграций, создать суперпользователя и запустить локальный сервер командами:
```bash 
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
- Открыть в браузере адрес ``http://localhost:8000/``

#### Процесс работы
- Все доработки делать в новой git-ветке (например с именем: feature/php);
- В конце разработки ветка будет слита в основной репозиторий через pull-request.
