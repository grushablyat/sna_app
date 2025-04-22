import vk_api
import vk_api.requests_pool

from config import ACCESS_TOKEN, ID


def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as e:
        print(e)
        return

    vk = vk_session.get_api()

    response = vk.wall.get(count=1)

    if response['items']:
        print(response['items'][0])


if __name__ == '__main__':
    main()
