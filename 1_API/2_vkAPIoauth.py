import requests
from pprint import pprint


def get_keys():
    with open('/home/arthur/Project/GeekBrains/Python_scraping/!ADDS/hw1_adds/req.txt', 'r') as f:
        return f.read().splitlines()


header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
app_id = get_keys()[0]
user_id = get_keys()[1]
token = get_keys()[2]
method = 'account.getProfileInfo'
params = {'access_token': token,
          'v': '5.78'}
main_link = f'https://api.vk.com/method/{method}'

response = requests.get(main_link, headers=header, params=params)

if response.ok:
    # Читаем
    data = response.json()
    pprint(data)

    # сохраняем файл
    with open('2_vkAccInfo.json', 'w') as f:
        f.write(response.text)
        print('Файл сохранён!')
