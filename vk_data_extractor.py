import codecs
import json
import math

from time import sleep, time
from typing import Collection
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import ACCESS_TOKEN, DUMPS
from user import User


TIMING = 0.21
SIMULTANEOUS_APPEALS = 25

# Отправка HTTP-запроса
def send_request(url: str, fields: dict) -> str:
    try:
        request = Request(url, urlencode(fields).encode())
        with urlopen(request) as response:
            return response.read().decode()
    except KeyError as e:
        print(e)
        return ''
    except HTTPError as e:
        return e.read()


# Получение данных пользователя
def get_user_data(id: int) -> User:
    url = 'https://api.vk.com/method/users.get'
    fields = {
        'user_ids': id,
        'fields': 'bdate',
        'access_token': ACCESS_TOKEN,
        'lang': 'ru',
        'v': '5.199',
    }

    str_user = send_request(url, fields)
    dict_user = json.loads(str_user)

    user = None

    try:
        user_data = dict_user['response'][0]
        user = User(user_data['id'], user_data['first_name'], user_data['last_name'], user_data['is_closed'])
    except KeyError as e:
        pass
    finally:
        return user


# Извлечение данных о списке друзей в формате JSON
def extract_friends_json(id: int) -> (str, dict):
    url = f'https://api.vk.com/method/friends.get'
    fields = {
        'user_id': id,
        'order': 'hints',
        # 'count': 20,
        'fields': 'bdate',
        'access_token': ACCESS_TOKEN,
        'lang': 'ru',
        'v': '5.199',
    }

    str_friends = send_request(url, fields)
    str_friends = f'{{"id":{id},{str_friends[1:]}'
    dict_friends = json.loads(str_friends)

    return str_friends


# Ускоренное извлечение данных о списке друзей в формате JSON
# Используется метод execute для выполнения множества обращений в рамках одного запроса
def fast_extract_fr_friends_json(ids: list[int]) -> list[str]:
    url = 'https://api.vk.com/method/execute'
    fields = {
        'code': '',
        'access_token': ACCESS_TOKEN,
        'lang': 'ru',
        'v': '5.199',
    }

    result_jsons = []
    start = time()

    for i in range(math.ceil(len(ids)/SIMULTANEOUS_APPEALS)):
        script = 'return {'
        for j in range(SIMULTANEOUS_APPEALS):
            k = i*SIMULTANEOUS_APPEALS + j
            if k < len(ids):
                script += f'"{ids[k]}": API.friends.get({{"user_id": {ids[k]}, "fields": "bdate"}}),'
        script = script[:-1] + '};'
        fields['code'] = script

        str_resp = send_request(url, fields)
        dict_resp = json.loads(str_resp)

        try:
            result_jsons.extend(
                [f'{{"id":{k},"response":{json.dumps(v, ensure_ascii=False, separators=(",", ":"))}}}'
                 for k, v in dict_resp['response'].items()]
            )
        except KeyError as e:
            print(e)
            print(str_resp)

        extract_time = time() - start
        if extract_time < TIMING:
            sleep(TIMING - extract_time)
        start = time()

    return result_jsons


# Форматирование JSON в users и relations
def json_to_objects(str_friends: str) -> (set[User], set[tuple]):
    dict_friends = json.loads(str_friends)
    friends = set()
    relations = set()

    try:
        user_id = dict_friends['id']
        if dict_friends['response']:
            for friend in dict_friends['response']['items']:
                friends.add(User(
                    friend['id'],
                    friend['first_name'],
                    friend['last_name'],
                    friend['is_closed'],
                ))
                relations.add((min(user_id, friend['id']), max(user_id, friend['id'])))
    except KeyError as e:
        if dict_friends['error']:
            pass

    return friends, relations


# Получение списка друзей с отношениями
def get_friends(id: int) -> (set[User], set[tuple]):
    str_friends = extract_friends_json(id)
    friends, relations = json_to_objects(str_friends)

    user = get_user_data(id)
    friends.add(user)

    return friends, relations


# Получение списка друзей и их друзей с отношениями
def get_friends_and_friends(id: int, add_fr_friends: bool=False) -> (set[User], set[tuple]):
    friends, relations = get_friends(id)
    users_ids = set([friend.id for friend in friends])

    for friend in list(friends):
        sleep(TIMING)
        fr_friends, fr_relations = get_friends(friend.id)
        if add_fr_friends:
            friends.update(fr_friends)
            users_ids.update([fr_friend.id for fr_friend in fr_friends])
            relations.update(fr_relations)
        else:
            for fr_relation in fr_relations:
                if fr_relation[0] in users_ids and fr_relation[1] in users_ids:
                    relations.add(fr_relation)

    return friends, relations


# Ускоренное получение списка друзей с отношениями
def fast_get_friends(id: int) -> (set[User], set[tuple]):
    str_frs = fast_extract_fr_friends_json([id])[0]
    friends, relations = json_to_objects(str_frs)

    opened_users_ids = set()
    for friend in friends:
        if not friend.is_closed:
            opened_users_ids.add(friend.id)

    user = get_user_data(id)
    friends.add(user)

    users_ids = set([friend.id for friend in friends])

    str_frs_frs = fast_extract_fr_friends_json(list(opened_users_ids))

    for str_fr_frs in str_frs_frs:
        fr_friends, fr_relations = json_to_objects(str_fr_frs)
        for fr_relation in fr_relations:
            if fr_relation[0] in users_ids and fr_relation[1] in users_ids:
                relations.add(fr_relation)

    return friends, relations


# Ускоренное получение списка друзей и их друзей с отношениями
def fast_get_friends_and_friends(id: int) -> (set[User], set[tuple]):
    str_frs = fast_extract_fr_friends_json([id])[0]
    friends, relations = json_to_objects(str_frs)

    user = get_user_data(id)
    friends.add(user)

    users_ids = set([friend.id for friend in friends])

    str_frs_frs = fast_extract_fr_friends_json(list(users_ids - {id}))

    for str_fr_frs in str_frs_frs:
        fr_friends, fr_relations = json_to_objects(str_fr_frs)

        fr_frs_ids = [fr_friend.id for fr_friend in fr_friends]
        friends.update(fr_friends)
        users_ids.update(fr_frs_ids)
        relations.update(fr_relations)

        str_fr_frs_frs = fast_extract_fr_friends_json(fr_frs_ids)
        for str_fr_fr_frs in str_fr_frs_frs:
            fr_fr_friends, fr_fr_relations = json_to_objects(str_fr_fr_frs)

            for fr_fr_relation in fr_fr_relations:
                if fr_fr_relation[0] in users_ids and fr_fr_relation[1] in users_ids:
                    relations.add(fr_fr_relation)

    return friends, relations


# Сложный экспорт в JSON друзей и их друзей со ВСЕМИ отношениями
def export_to_json(id: int, connect_fr_friends: bool=False, filename: str=None) -> None:
    if not filename:
        filename = f'friends_{id}.json'

    filename = 'dumps/' + filename

    str_friends = extract_friends_json(id)
    friends, _ = json_to_objects(str_friends)

    file = codecs.open(filename, 'w', encoding='utf-8')
    file.write('{"dump":[\n')
    file.write(str_friends + ',\n')

    for friend in friends:
        sleep(TIMING)
        str_fr_friends = extract_friends_json(friend.id)
        file.write(str_fr_friends + ',\n')

        fr_friends, _ = json_to_objects(str_friends)

        if connect_fr_friends:
            for fr_friend in fr_friends:
                sleep(TIMING)
                str_fr_fr_friends = extract_friends_json(fr_friend.id)
                file.write(str_fr_fr_friends + ',\n')

    file.write(']}')
    file.close()


# Сложный импорт из JSON друзей и их друзей со ВСЕМИ отношениями
# Некорректно работает при добавлении вторичных друзей и тем более их отношений
def import_from_json(id: int, add_fr_friends: bool=False, add_fr_fr_cons: bool=False, filename: str=None) -> (set[User], set[tuple]):
    if not filename:
        filename = f'friends_{id}.json'

    filename = 'dumps/' + filename

    user = get_user_data(id)
    users = {user}

    file = codecs.open(filename, 'r', encoding='utf-8')
    lines = list(map(lambda l: l[:-2], file.readlines()[1:-1]))

    try:
        main_user_friends_count = json.loads(lines[0])['response']['count']
        friends, relations = json_to_objects(lines[0])
        users.update(friends)
        users_ids = set([user.id for user in users])

        print(lines[0])
        print(main_user_friends_count)

        for line in lines[1:main_user_friends_count+1]:
            fr_friends, fr_relations = json_to_objects(line)
            if add_fr_friends:
                users.update(fr_friends)
                users_ids.update([fr_friend.id for fr_friend in fr_friends])
                relations.update(fr_relations)
            else:
                for fr_relation in fr_relations:
                    if fr_relation[0] in users_ids and fr_relation[1] in users_ids:
                        relations.add(fr_relation)

        if add_fr_friends and add_fr_fr_cons:
            for line in lines[main_user_friends_count+1:]:
                _, fr_fr_relations = json_to_objects(line)
                for fr_fr_relation in fr_fr_relations:
                    if fr_fr_relation[0] in users_ids and fr_fr_relation[1] in users_ids:
                        relations.add(fr_fr_relation)
    except Exception as e:
        raise e

    return users, relations


# Простой экспорт в TXT готовых объектов пользователей и отношений
def simple_export(id: int, users: Collection[User], relations: Collection[tuple], filename: str=None) -> None:
    if not filename:
        filename = f'dump_{id}.txt'

    filename = f'{DUMPS}/{filename}'

    file = codecs.open(filename, 'w', encoding='utf-8')
    for user in users:
        file.write(user.__str__() + '\n')
    for relation in relations:
        file.write(relation.__str__() + '\n')

    file.close()


# Простой импорт из TXT готовых объектов пользователей и отношений
def simple_import(id: int, filename: str=None) -> (set[User], set[tuple]):
    if not filename:
        filename = f'dump_{id}.txt'

    filename = f'{DUMPS}/{filename}'

    users = set()
    relations = set()

    file = codecs.open(filename, 'r', encoding='utf-8')
    for line in file.readlines():
        if line.startswith('('):
            relations.add(tuple(map(int, line[1:-2].split(', '))))
        else:
            data = line[:-1].split(' ')
            users.add(User(
                int(data[0]),
                data[1],
                data[2],
                bool(data[3]),
            ))

    file.close()

    return users, relations


if __name__ == '__main__':
    pass
