import random
from datetime import datetime
from Data.ins_data import sel_prop_data
import requests
from token import GROUP_TOKEN, personal_token  # персональный токен

access_token = personal_token


coincidence = []


class VKinder_get_info:
    def __init__(self, sex, age, city):
        if sex == 'ж':
            sex = 1
        elif sex == 'м':
            sex = 2
        else:
            sex = 0
        self.vk_url = 'https://api.vk.com/method/'
        self.params = {
            "access_token": access_token,
            "v": 5.131,
            'oauth': 1,
            'count': 10,
            'offset': random.randrange(0, 100),
            'sort': 0,
            "fields": 'sex, city, photo_id, has_photo, screen_name, can_write_private_message',
            "age_from": age - 3,
            "age_to": age + 3,
            "sex": sex,
            "hometown": city.title(),
            "status": 1,
            "album_id": "profile"
        }

    """Получаем информацию для запроса урла фото"""

    def get_all_result(self):
        url_get_info = self.vk_url + "users.search?"
        req = requests.get(url_get_info, params=self.params).json()
        all_result_list = [req['response']['items']]
        return all_result_list

    def get_inf(self, user_id):
        try:
            all_result_list = self.get_all_result()
            for items in all_result_list:
                for i in range(len(items)):
                    item = items[i]
                    if item['is_closed'] is False and item['can_write_private_message'] == 1 and item['has_photo'] == 1:
                        if item['id'] not in # должна быть ссылка на функцию из бд(user_id):
                            result = item['first_name'], item['last_name'], item[
                                'id'], f"https://vk.com/{item['screen_name']}"
                            coincidence.append(f"{user_id}-{item['id']}")
                            print(coincidence)
                            return result
                    else:
                        continue
        except KeyError:
            KeyError("Проверьте правильность набора!")
            return None


class VKinder_get_photo:
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.vk_url = 'https://api.vk.com/method/'
        self.params = {
            "access_token": access_token,
            "v": 5.131,
            'oauth': 1,
            "owner_id": owner_id,
            "album_id": "profile",
            "photo_sizes": 1,
            "extended": 1
        }

    def get_photo_url(self):
        url_photos_get = self.vk_url + "photos.get?"
        req = requests.get(url_photos_get, params=self.params).json()
        attachment = []
        if 'response' in req.keys() and len(req['response']['items']) != 0:
            photos = sorted(req['response']['items'], key=lambda k: k['likes']['count'], reverse=True)
            if len(photos) > 3:
                photos = photos[:3]
            for item in photos:
                attachment.append(f'photo{self.owner_id}_{item["id"]}')
        return attachment


class MessagesSend:

    def __init__(self, user_id, item):
        self.vk_url = 'https://api.vk.com/method/'
        self.user_id = user_id
        self.params = {
            "access_token": GROUP_TOKEN,
            "user_id": self.user_id,
            "peer_id": self.user_id,
            "attachment": item,
            "v": 5.131,
            "random_id": 0
        }

    def send_photo(self):
        url_send_message = self.vk_url + "messages.send?"
        req = requests.post(url_send_message, params=self.params).json()
        return req


def get_user_param(user):
    params = {
        "access_token": access_token,
        "v": 5.131,
        "user_id": user,
        "fields": 'sex, bdate, city, age'
    }
    req = requests.get("https://api.vk.com/method/users.get?", params=params).json()
    user_param = req['response'][0]
    request = f"{user_param['city']['title'].split('/')[0].strip()}, " \
              f"{datetime.now().year - datetime.strptime(user_param['bdate'], '%d.%m.%Y').year}, " \
              f"{'ж' if user_param['sex'] == 2 else 'м'}"  # противоположный пол

    return request
