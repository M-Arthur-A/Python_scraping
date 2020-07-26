import requests
from pprint import pprint

main_link = 'https://api.github.com/'
header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
user = 'M-Arthur-A'
response = requests.get(f'{main_link}users/{user}/repos', headers=header)

if response.ok:
    # Читаем
    data = response.json()
    pprint(data)

    # сохраняем файл
    with open('1_GithubRepos.json', 'w') as f:
        f.write(response.text)
        print('Файл сохранён!')
