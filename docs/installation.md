# Инструкция по развертке среды разработчика

### Зависимости:
- Python >= 3.6 + Pipenv
- Postgresql >= 9.6
- Docker >= 19
- Git

### Пример установки на ОС Ubuntu 18.04 LTS

Предполагается что ОС установлена и настроена, развертка проекта будет осуществляться через терминал.
Редактирование кода, развертка вирт. окружения и работа с git будут производиться на примере [IDE Pycharm](https://www.jetbrains.com/ru-ru/pycharm/download/#section=linux).

**1. Подготовка среды**

```bash
# python уже предустановлен, можно проверить командой
python3 --version
# установка git
sudo apt install git
# установка pipenv
sudo apt install python3-pip python3-dev
pip3 install --user pipenv
echo "PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
```

**2. Скачать проект из git-репозитория**

- Настроить глобальный git config [по инструкции](https://git-scm.com/book/ru/v2/%D0%92%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%B8%D0%B5-%D0%9F%D0%B5%D1%80%D0%B2%D0%BE%D0%BD%D0%B0%D1%87%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0-Git).
- Зарегистрироваться на [github.com](https://github.com/).
- Сделать форк данного репозитория.
- Склонировать репозиторий.
- Далее все манипуляции будут осуществляться на базе склонированного проекта.

**3. Подготовка проекта к запуску**

- Открыть проект в IDE Pycharm (рекомендуется).
- Создать файл локальных настроек в проекте по адресу ``cappa/src/settings/local.py``. 
- Для первоначального запуска используем базу данных sqlite3.

```python
SECRET_KEY = 'wp-8k64@_1aqkag-7mwgk)=f2irdv32#4y$0bhuxa7i03m802r'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "tests/db.sqlite3",
    }
}
```

**4. Установка Python пакетов**

Создать и активировать виртуальное окружение pipenv:
- Первый вариант: через интерфейс pycharm (в настройках интерпретатора)
- Второй вариант: через терминал, находясь в корне проекта ввести команды:
```
pipenv install
pipenv shell
```
**5. Запустить локальный сервер на тестовой базе данных**

- Находясь в корне проекта выполнить команду:
```
python3 manage.py runserver
```
После этого сайт должен запустится на локальном сервере.
- Открыть в браузере адрес [http://localhost:8000](http://localhost:8000/)

- Для входа в административный интерфейс перейдите по адресу [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Данные для входа: логин: user, пароль: user

**6. Подключение базы данных postgresql**

База данных sqlite3 подходит только для ознакомления с проектом, переключаем проект на Postgresql

6.1. Установка Postgresql:
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
6.2. Удалить из файла локальных настрек ``cappa/src/settings/local.py`` настройку тестовой базы данных: DATABASES (добавленную в пункте 3)

6.3. Создать базу данных в postgresql с именем, пользователем и паролем: "cappa", например через терминал, командами:

```bash
createdb --owner cappa cappa
su postgresql
psql
create role "cappa" WITH NOSUPERUSER CREATEDB NOCREATEROLE INHERIT LOGIN NOREPLICATION PASSWORD 'cappa';
GRANT ALL PRIVILEGES ON DATABASE cappa TO cappa;
```
6.4. Загрузить тествый дамп базы, команда в консоли:
```bash
psql -U cappa -h localhost cappa < tests/pg.dump 
```
Дамп содержит учетную запись суперпользователя: логин: user, пароль: user

6.5. Запустить локальный сервер
```bash 
python manage.py runserver
``` 
Проверяем что сайт поднялся [http://localhost:8000](http://localhost:8000/)

**7. Установка Docker**

Docker используется как песочница для выполнения учебных программ и скриптов. После установки Docker убедитесь в его работоспособности.

```bsah
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
 
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo docker run hello-world
 
# Для запуска команд без sudo добавить текущего пользователя (напримем "root") в группу "docker"
sudo usermod -aG docker root
```

Нужные контейнеры будут развернуты автоматически при первом обращении к песочнице.

Открыть в браузере [тестовую интерактивную страницу](http://localhost:8000/courses/python/vvod-i-vyvod-dannyh/) и запустить на отладку любой блок кода.
В случае если запрос вернет 500 ошибку - попробовать запустить контейнеры вручную.

#### Процесс совместной работы
- Все доработки делать в новой git-ветке (например с именем: feature/branch_name);
- В конце разработки ветка будет слита в основной репозиторий через pull-request.
