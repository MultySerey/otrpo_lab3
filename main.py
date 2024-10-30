import requests
import json
import argparse

COMMON_PARAMS = {
    "access_token": "",
    "v": "5.199",
    "lang": "ru"
}


def get_user_name(user_id: int) -> str:
    params = {
        "user_id": user_id,
    }
    response = requests.get("https://api.vk.com/method/users.get",
                            params=(COMMON_PARAMS | params))

    response = json.loads(response.content)['response'][0]
    return f"{response['first_name']} {response['last_name']}"


def get_group_name(group_id: int):
    params = {
        "group_id": group_id,
        "fields": "name"
    }
    response = requests.get("https://api.vk.com/method/groups.getById",
                            params=(COMMON_PARAMS | params))

    response = json.loads(response.content)['response']
    return response['groups'][0]['name']


def get_followers(user_id: int) -> list[int]:
    params = {
        "user_id": user_id
    }
    response = requests.get("https://api.vk.com/method/users.getFollowers",
                            params=(COMMON_PARAMS | params))

    response = json.loads(response.content)['response']
    return response['items']


def get_subscriptions(user_id: int) -> dict[str, list[int]]:
    params = {
        "user_id": user_id
    }
    response = requests.get("https://api.vk.com/method/users.getSubscriptions",
                            params=(COMMON_PARAMS | params))

    response = json.loads(response.content)['response']
    response_dict = {
        "users": response['users']['items'],
        "groups": response['groups']['items']
    }

    return response_dict


def main(user_id: int):
    print("Получаем пользователя")
    name: str = get_user_name(user_id)

    print("Получаем подписчиков")
    follows: list[int] = get_followers(user_id)
    follow_names: dict[int, str] = {
        follow: get_user_name(follow) for follow in follows
    }

    print("Получаем подписки")
    subs: dict[str, list[int]] = get_subscriptions(user_id)
    user_names: dict[int, str] = {
        user: get_user_name(user) for user in subs['users']
    }
    group_names: dict[int, str] = {
        group: get_group_name(group) for group in subs['groups']
    }

    print("Заканчиваем")
    result = {
        user_id: {
            "name": name,
            "followers": follow_names,
            "subscriptions": {
                "users": user_names,
                "groups": group_names
            }
        }
    }

    with open("result.json", "w", encoding="utf-8") as w:
        json.dump(result, w, ensure_ascii=False, indent=2)
    print("Готово")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='OTRPO Lab 3',
        description='Лабораторная работа 3 по ОТРПО'
    )
    parser.add_argument(
        'user_id',
        type=int,
        help='Идентификатор пользователя (число)'
    )
    parser.add_argument(
        'service_key',
        type=str,
        help='Сервисный ключ API VK'
    )
    args = parser.parse_args()
    COMMON_PARAMS["access_token"] = args.service_key
    main(args.user_id)
