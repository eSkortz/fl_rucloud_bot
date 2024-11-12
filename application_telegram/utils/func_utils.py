import requests
from aiogram.types import Message

import io
import base64
from PIL import Image
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

from sqlalchemy.orm import session, sessionmaker

from db.oop.alchemy_di_async import DBWorkerAsync
from config import engine_async, engine
from db.orm.schema_public import Users, Groups

db_worker = DBWorkerAsync(engine_async)

base_url = 'https://nextcloud.prosto-web.agency'
admin_username = 'admin'
admin_password = 'admin'
Session = sessionmaker(bind=engine)


async def get_files_list(nextcloud_login: str, nextcloud_password: str, directory_name='') -> list:
    # Данные для подключения к вашему серверу Nextcloud
    url = base_url + f'/remote.php/dav/files/{nextcloud_login}/{directory_name}'
    if not url.endswith('/'):
        url += '/'

    # Заголовки, необходимые для запроса WebDAV
    headers = {
        'Depth': '1',  # Глубина запроса. 1 означает, что мы получим только содержимое корневой директории.
    }

    # Выполняем запрос PROPFIND для получения списка файлов
    response = requests.request("PROPFIND", url, headers=headers, auth=HTTPBasicAuth(nextcloud_login, nextcloud_password))

    files = []

    if response.status_code == 207:
        root = ET.fromstring(response.content)

        for response_elem in root.findall('{DAV:}response'):
            href = response_elem.find('{DAV:}href').text
            propstat = response_elem.find('{DAV:}propstat')
            prop = propstat.find('{DAV:}prop')

            displayname_elem = prop.find('{DAV:}displayname')
            displayname = displayname_elem.text if displayname_elem is not None else href
            if displayname.endswith('/'):
                filename = displayname.split('/')[-2].replace('%20', ' ')
            else:
                filename = displayname.split('/')[-1].replace('%20', ' ')

            resourcetype_elem = prop.find('{DAV:}resourcetype')
            is_collection = resourcetype_elem.find(
                '{DAV:}collection') is not None if resourcetype_elem is not None else False

            if filename == '' or filename == directory_name.strip('/'):
                continue

            if is_collection:
                files.append('dir ' + filename)
            else:
                files.append(filename)
            print ("ok")
    else:
        print(f"Failed to retrieve files. Status code: {response.status_code}")
        print("Response text:", response.text)

    return files


async def upload_file(nextcloud_login: str, nextcloud_password: str, local_file_path, remote_file_name):
    url = base_url + f'/remote.php/dav/files/{nextcloud_login}/'

    # Открываем файл и выполняем PUT-запрос для его загрузки на сервер
    with open(local_file_path, 'rb') as file:
        response = requests.put(url + remote_file_name, data=file, auth=HTTPBasicAuth(nextcloud_login, nextcloud_password))

    # Проверяем статус ответа
    if response.status_code == 201:
        print(f"File '{remote_file_name}' has been successfully uploaded.")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print("Response text:", response.text)


async def download_file(nextcloud_login, nextcloud_password, local_file_path, remote_file_name):
    url = base_url + f'/remote.php/dav/files/{nextcloud_login}/'

    # Выполняем GET-запрос для скачивания файла с сервера
    response = requests.get(url + remote_file_name, auth=HTTPBasicAuth(nextcloud_login, nextcloud_password))

    # Проверяем статус ответа и сохраняем файл
    if response.status_code == 200:
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        print(f"File '{remote_file_name}' has been successfully downloaded.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        print("Response text:", response.text)


async def remove_file(nextcloud_login: str, nextcloud_password: str, remote_file_name):
    # Данные для подключения к вашему серверу Nextcloud
    url = base_url + f'/remote.php/dav/files/{nextcloud_login}/'

    # Имя файла на сервере для удаления
    remote_file_name = remote_file_name

    # Выполняем DELETE-запрос для удаления файла с сервера
    response = requests.delete(url + remote_file_name, auth=HTTPBasicAuth(nextcloud_login, nextcloud_password))

    # Проверяем статус ответа
    if response.status_code == 204:
        print(f"File '{remote_file_name}' has been successfully deleted.")
    else:
        print(f"Failed to delete file. Status code: {response.status_code}")
        print("Response text:", response.text)


def list_directory(directory_name:str, username: str, password: str):
    url = f"{base_url}/remote.php/dav/files/admin/{directory_name}/"
    response = requests.request('PROPFIND', url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 207:
        print(f"Содержимое директории '{directory_name}':")
        print(response.text)
    else:
        print(f"Ошибка при получении содержимого директории '{directory_name}': {response.status_code} {response.text}")


async def group_list(telegram_id: int) -> list:
    # Данные для подключения к вашему серверу Nextcloud
    user_credits = await db_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == telegram_id]
    )
    user_credits: Users = user_credits[0]
    login, password = user_credits.nextcloud_login, user_credits.nextcloud_password

    url = base_url + f'/ocs/v1.php/cloud/users/{login}'
    user_id = 'admin'

    # Заголовки, необходимые для запроса OCS API
    headers = {
        'OCS-APIRequest': 'true',
    }

    # Выполняем GET-запрос к API для получения списка групп пользователя
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(login, password))

    group_names = []

    # Проверяем статус ответа
    if response.status_code == 200:
        try:
            # Парсим XML-ответ
            root = ET.fromstring(response.content)

            # Находим все элементы группы
            groups = root.findall('.//groups/element')

            # Выводим список групп
            print("List of groups for user", {user_id})
            for group in groups:
                print(group.text)
                group_names.append(group.text)
        except ET.ParseError as e:
            print("Error parsing XML response:", e)
    else:
        print(f"Failed to retrieve groups. Status code: {response.status_code}")
        print("Response text:", response.text)

    return group_names


async def add_user_to_group():
    # Данные для подключения к вашему серверу Nextcloud
    username = 'admin'
    password = 'admin'
    url = 'https://nextcloud.prosto-web.agency/ocs/v1.php/cloud/users/admin/groups'
    user_id = 'vlad'
    group_name = 'test_group2'

    # Заголовки, необходимые для запроса OCS API
    headers = {
        'OCS-APIRequest': 'true',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Данные для тела запроса
    data = {
        'groupid': group_name
    }

    # Выполняем POST-запрос к API для добавления пользователя в группу
    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(username, password), data=data)

    # Проверяем статус ответа
    if response.status_code == 200:
        try:
            # Парсим XML-ответ
            root = ET.fromstring(response.content)

            # Извлекаем статус и сообщение
            status = root.find('.//meta/status').text
            message = root.find('.//meta/message').text

            if status == 'ok':
                print(f"User '{user_id}' has been successfully added to group '{group_name}'.")
            else:
                print(f"Failed to add user '{user_id}' to group '{group_name}'. Message: {message}")
        except ET.ParseError as e:
            print("Error parsing XML response:", e)
    else:
        print(f"Failed to add user to group. Status code: {response.status_code}")
        print("Response text:", response.text)


async def add_new_user(username, password):
    url = base_url + '/ocs/v1.php/cloud/users'

    # Данные для создания пользователя
    new_user_data = {
        'userid': username,
        'password': password
    }

    # Заголовки, необходимые для запроса OCS API
    headers = {
        'OCS-APIRequest': 'true',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Выполняем POST-запрос к API для создания пользователя
    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(admin_username, admin_password),
                             data=new_user_data)

    # Проверяем статус ответа
    if response.status_code == 200:
        try:
            # Парсим XML-ответ
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)

            # Извлекаем статус и сообщение
            status = root.find('.//status').text
            message = root.find('.//message').text

            if status == 'ok':
                print(f"User '{new_user_data['userid']}' has been successfully created.")
            else:
                print(f"Failed to create user '{new_user_data['userid']}'. Message: {message}")
        except ET.ParseError as e:
            print("Error parsing XML response:", e)
    else:
        print(f"Failed to create user. Status code: {response.status_code}")
        print("Response text:", response.text)


async def get_rucloud_groups_list(telegram_id: int) -> list:
    groups_list = await db_worker.custom_orm_select(
        cls_from=Groups,
        where_params=[Groups.telegram_id == telegram_id]
    )
    group_names = []

    for index in range(len(groups_list)):
        group_name: Groups = groups_list[index]
        group_names.append("ru " + str(group_name.group_name))

    return group_names


async def create_group(username: str, password: str, group_name: str) -> None:
    url = base_url + f"/remote.php/dav/files/{username}/group_directory/{group_name}"

    response = requests.request('MKCOL', url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 201:
        print("Директория успешно создана")
    else:
        print(f"Ошибка при создании директории: {response}")

async def change_password(nextcloud_login: str, password: str):
    endpoint = f'{base_url}/ocs/v1.php/cloud/users/{nextcloud_login}/password'
    headers = {'OCS-APIRequest': 'true'}

    data = {'password': password}

    response = requests.put(endpoint, auth=HTTPBasicAuth(admin_username, admin_password), headers=headers, data=data)

    if response.status_code == 200:
        print("Пароль успешно изменен")
    else:
        print(f"Ошибка при смене пароля: {response.status_code} - {response.text}")
