# Приложение для проверки ЛМЧЗ в сети магазинов

Для запуска надо создать файл settings.py в нем указать

TOKEN = который мы получили для работы с честным знаком
DEBUG = производится отладка Flask-а (True) или нет (False)
AUTH = шифрованую пару логин-пароль для доступа к ЛМЧЗ (см. документацию по ЛМЧЗ)
DOMAIN = домен в котором работает комп с ЛМЧЗ

В нашем конкретном случае имена компа формируются как mag-{номер}-zav.{домен}
Скрипт написан так что по циклу перебираются номера магазинов, формируется имя компа и имя передается в функцию