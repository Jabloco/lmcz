import requests
import logging
from datetime import datetime
from settings import TOKEN
from settings import AUTH
from settings import DOMAIN


logging.basicConfig(handlers=[logging.FileHandler('error.log', 'a', 'utf-8')],
                    format='%(levelname)s - %(message)s')


class LmczClient:
    # метод для запроса статуса
    def lmcz_status_req(self, comp: str):
        headers = {'Content-Type': 'application/json', 'Authorization': AUTH}
        try:
            req = requests.get(f"http://{comp}:5995/api/v1/status", headers=headers, timeout=2)
            req.raise_for_status()
        except requests.RequestException as error:
            logging.exception(error)
            return
        return req.json()

    # метод для запроса на инициализацию
    def lmcz_init_req(self, comp: str):
        headers = {'Content-Type': 'application/json', 'Authorization': AUTH}
        token = f'{{"token": "{TOKEN}"}}'
        try:
            req = requests.post(f"http://{comp}:5995/api/v1/init", headers=headers, data=token)
            req.raise_for_status()
        except requests.RequestException as error:
            logging.exception(error)
            return
        return req


def check_status_lmcz(comp_name: str) -> str | None:
    """
    Функция проверки статуса ЛМЧЗ

    Принимает на вход имя компа

    Возвращает или None или сам строку с наименованием статуса

    """
    status_req_res = r.lmcz_status_req(comp=comp_name)
    if status_req_res:
        status = status_req_res['status']
        return status
    else:
        return


# проверка версии ЛМЧЗ
def check_version_lmcz(comp_name: str) -> str | None:
    status_req_res = r.lmcz_status_req(comp=comp_name)
    if status_req_res:
        version = status_req_res['version']
        return version
    else:
        return


# проверкаа последнего времени обновления и синхронизации
def check_update_and_sync(comp_name: str) -> dict | None:
    status_req_res = r.lmcz_status_req(comp=comp_name)
    if status_req_res:
        last_update = datetime.utcfromtimestamp(status_req_res['lastUpdate']/1000).strftime('%Y-%m-%d %H:%M:%S')
        last_sync = datetime.utcfromtimestamp(status_req_res['lastSync']/1000).strftime('%Y-%m-%d %H:%M:%S')
        update_and_sync = {'update':last_update, 'sync':last_sync}
        return update_and_sync
    else:
        return


def init_lmcz(comp_name: str) -> str | None:
    """
    Функция для отправки запроса на инициализацию ЛМЧЗ

    Принимает имя компа

    Возвращает или None или строку
    """
    init_req_res = r.lmcz_init_req(comp_name)

    if init_req_res is None:
        print(f"Запрос на инициализацию не отправлен")
    elif init_req_res.status_code == 200:
        print(init_req_res)
        return (f"Отправлен запрос на инициализацию. Код {init_req_res.status_code}")
    else:
        return


def write_logs(file_name: str, msg_text: str):
    """

    Функция для записи в файл.
    Принимаетимя файла и сообщение

    """
    with open(f"{file_name}.txt", "a") as logs_file:
        logs_file.write(msg_text)


def clear_log_files():
    """

    Функция для очистки логов

    """
    file_names = ['log_initialization',
                  'log_not_configure',
                  'log_ready',
                  'log_sync_error',
                  '1.2.0-326',
                  '1.2.1-340',
                  '1.3.1-369'
                  ]
    for file_name in file_names:
        with open(f"{file_name}.txt", "w"):
            pass


def write_lmcz_ver(file_name: str, msg_text: str):
    """

    Функция для создания файла с версией ЛМЧЗ в имени и номерами магазинов внутри

    """
    with open(f"{file_name}.txt", "a") as logs_file:
        logs_file.write(msg_text)


def check_and_update(comp_name: str) -> dict | None:
    """

    Функция для проверки статуса и отправки запроса на инициализацию если \
        статус отличный от ready
    Функция принимает номер магазина, возвращает словарь \
        check_res = {'shop_num':val, 'lmcz_ver':val, 'status':val, 'update':val, 'sync':val}
    Пока  пишем в файл, потом надо переделать в СУБД

    """

    # делаем запрос статуса
    status = check_status_lmcz(comp_name)
    # получаем версию модуля
    version = check_version_lmcz(comp_name)
    update_and_sync = check_update_and_sync(comp_name)
    # обрабатываем возможные ответы
    if status is None:
        # если статус не пришел то возвращаем None
        return
    elif status == 'ready':
        msg = f"{comp_name} модуль ЛМЧЗ инициализирован. Статус: {status}. Версия ЛМЧЗ: {version}.\n\
            \tПоследняя синхронизация {update_and_sync['sync']}. Последняя репликация {update_and_sync['update']}"
        write_logs(file_name="log_ready", msg_text=f"{msg}\n")
        write_lmcz_ver(file_name=str(version), msg_text=f"{str(comp_name)} {status}\n")
    elif status == 'initialization':
        msg = f"{comp_name} модуль ЛМЧЗ в процессе инициализации. Статус: {status}. Версия ЛМЧЗ: {version}.\n\
            \tПоследняя синхронизация {update_and_sync['sync']}. Последняя репликация {update_and_sync['update']}"
        write_logs(file_name="log_initialization", msg_text=f"{msg}\n")
        write_lmcz_ver(file_name=str(version), msg_text=f"{str(comp_name)} {status}\n")
    elif status == 'not_configured':
        msg = f"{comp_name} модуль ЛМЧЗ не инициализирован.Статус: {status}. Версия ЛМЧЗ: {version}.\n\
            \tПоследняя синхронизация {update_and_sync['sync']}. Последняя репликация {update_and_sync['update']}"
        write_logs(file_name="log_not_configure", msg_text=f"{msg}\n")
        write_lmcz_ver(file_name=str(version), msg_text=f"{str(comp_name)} {status}\n")
        send_init_req = init_lmcz(comp_name)
    elif status == 'sync_error':
        msg = f"{comp_name} ошибка синхронизации.Статус: {status}. Версия ЛМЧЗ: {version}.\n\
            \tПоследняя синхронизация {update_and_sync['sync']}. Последняя репликация {update_and_sync['update']}"
        write_logs(file_name="log_sync_error", msg_text=f"{msg}\n")
        write_lmcz_ver(file_name=str(version), msg_text=f"{str(comp_name)} {status}\n")
        send_init_req = init_lmcz(comp_name)
        print(send_init_req)
    else:
        return

    check_res = {'shop_num': shop_num,
                 'lmcz_ver': version,
                 'status': status,
                 'update': update_and_sync['update'],
                 'sync': update_and_sync['sync']
                 }

    return check_res


if __name__ == "__main__":
    r = LmczClient()
    clear_log_files()
    for shop_num in range(2,310):
        # формируем имя компа
        comp_name = f'mag-{shop_num}-zav.{DOMAIN}'
        print(check_and_update(comp_name))
