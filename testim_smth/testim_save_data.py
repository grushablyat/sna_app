import codecs
import json

from time import sleep
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import ID, ACCESS_TOKEN
from user import User
from testim_visual import visualize_graph_vis


# Отправка HTTP-запроса
def send_request(url, fields):
    try:
        request = Request(url, urlencode(fields).encode())
        with urlopen(request) as response:
            return response.read().decode()
    except KeyError as e:
        print(e)


def get_user_data(id):
    url = 'https://api.vk.com/method/users.get'
    fields = {
        'user_ids': id,
        'fields': 'bdate',
        'access_token': ACCESS_TOKEN,
        'v': '5.199',
    }

    str_user = send_request(url, fields)
    dict_user = json.loads(str_user)

    user = None

    try:
        user_data = dict_user['response'][0]
        user = User(user_data['id'], user_data['first_name'], user_data['last_name'])
    except KeyError as e:
        pass
    finally:
        return user


# Извлечение данных о списке друзей, формирование сета объектов User
def extract(id):
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
    dict_friends = json.loads(str_friends)

    friends = set()
    relations = set()

    try:
        for friend in dict_friends['response']['items']:
            friends.add(User(
                friend['id'],
                friend['first_name'],
                friend['last_name']
            ))
            relations.add((min(id, friend['id']), max(id, friend['id'])))
    except KeyError as e:
        # print(e)
        if dict_friends['error']:
            pass

    return friends, relations, str_friends


def json_to_object(id, str_friends, adding):
    dict_friends = json.loads(str_friends)

    friends = set()
    relations = set()

    try:
        for friend in dict_friends['response']['items']:
            if adding:
                friends.add(User(
                    friend['id'],
                    friend['first_name'],
                    friend['last_name']
                ))
            relations.add((min(id, friend['id']), max(id, friend['id'])))
    except KeyError as e:
        # print(e)
        if dict_friends['error']:
            pass

    return friends, relations


def make_dump_json(id):
    friends, relations, str_friends = extract(id)

    file = codecs.open(f"friends_{id}.json", "w", "utf-8")
    file.write(str_friends + '\n')

    for friend in list(friends):
        sleep(0.34)
        friend_friends, friend_relations, str_friend_friends = extract(friend.id)
        file.write(str_friend_friends + '\n')


def import_from_dump(id, adding):
    user = get_user_data(id)
    users = {user}
    users_ids = {user.id}

    file = codecs.open(f'friends_{id}.json', 'r', 'utf-8')

    str_friends = file.readline()
    friends, relations = json_to_object(id, str_friends, True)
    users = users.union(friends)
    users_ids = users_ids.union([friend.id for friend in friends])

    for friend in friends:
        friend_friends = file.readline()
        friend_friends, friend_relations = json_to_object(friend.id, friend_friends, adding)
        users = users.union(friend_friends)
        for relation in friend_relations:
            print(relation)
            if relation[1] in users_ids:
                relations.add(relation)

    return users, relations


def test_graph():
    nodes = ['alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf']
    nodes = [1, 2, 3, 4, 5]
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5), (2, 4), (1, 4), (3, 5)]

    return set(nodes), set(edges)
