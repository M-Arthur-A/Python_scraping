from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
import pandas as pd
import time
import random

header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}


# pd.set_option("display.max_rows", None, "display.max_columns", None)


def get_price(p):
    # print(p, '->', end=' ')
    min_price = None
    max_price = None
    currency = None
    if p != 'None':  # если в последнем блоке, отделенном пробелом, нет числа -> это валюта
        if not p.split()[-1][0].isnumeric() and p.split()[-1] != 'договорённости':
            currency = p.split()[-1]  # определяем валюту
            p = ' '.join(p.split()[:-1])  # отсекаем валюту

        if not p.split()[0][0].isnumeric():  # если в первом блоке, отделенном пробелом, нет числа -> это "от" / "до"
            border = p.split()[0]  # определяем границу
            p = ' '.join(p.split()[1:])  # отсекаем границу
            if border == 'до':
                max_price = p
            elif border == 'от':
                min_price = p
        elif '-' in p:
            min_price = p.split('-')[0]
            max_price = p.split('-')[1]
        elif ' — ' in p:
            min_price = p.split(' — ')[0]
            max_price = p.split(' — ')[1]
        else:
            min_price = p
            max_price = p
    # print('min:', min_price, ', max:', max_price, ', cur:', currency)
    return [min_price, max_price, currency]


def clear_txt(txt_gen):
    list_of_txt = list(txt_gen)
    txt = ''
    for t in list_of_txt:
        try:
            html_text = t.getText()
            txt = txt + html_text
        except AttributeError:
            txt = txt + t
    return txt


def hh_scrab(vacancy, df):
    main_link = 'https://hh.ru'
    add_link = '/search/vacancy'
    params = {'clusters': 'true', 'enable_snippets': 'true', 'search_field': 'name', 'text': vacancy,
              'L_save_area': 'true',
              'area': '1', 'from': 'cluster_area', 'showClusters': 'false'}
    page = 1  # счетчик страниц
    # vacancies = [['source', 'name', 'href', 'min_price', 'max_price', 'currency', 'employer', 'city',
    #               'responsibility', 'requirement', 'page']]
    while page >= 1:
        response = requests.get(f'{main_link + add_link}', headers=header, params=params)
        if response.ok:
            soup = bs(response.text, 'lxml')
            jobs = soup.find_all('div', {'class': 'vacancy-serp-item'})
            for job in jobs:
                source = 'hh'
                name = job.find('a').getText()
                href = job.find('a').get('href')
                try:
                    price = get_price(job.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText())
                    min_price = price[0]
                    max_price = price[1]
                    currency = price[2]
                except AttributeError:
                    min_price, max_price, currency = None, None, None
                try:
                    employer = job.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).getText()
                except AttributeError:
                    employer = None
                city = job.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).getText()
                responsibility = job.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).getText()
                requirement = job.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).getText()
                # vacancies.append([source, name, href, min_price, max_price, currency, employer, city,
                #                   responsibility, requirement, page])
                new_df = pd.DataFrame([[source, name, href, min_price, max_price, currency, employer, city,
                                        responsibility, requirement, page]], columns=cols)
                df = pd.concat([df, new_df])
        else:
            print('404')
        print(source, page)
        page += 1
        # сохраняем pd.DataFrame на случай бана
        df.to_pickle('JobDataSet.pickle')
        # проверяем есть ли еще страницы, если есть -> добавляем в параметры новую страницу
        try:
            next_page = soup.find('a', {'class': 'HH-Pager-Controls-Next'}).get('href').split('=')[-1]
            params['page'] = next_page
            time.sleep(random.randrange(1, 5))
        except AttributeError:
            break
    return df  # vacancies


def sj_scrab(vacancy, df):
    main_link = 'https://www.superjob.ru'
    add_link = '/vacancy/search/'
    params = {'keywords': vacancy, 'geo[t][0]': 4}
    page = 1  # счетчик страниц
    # vacancies = [['source', 'name', 'href', 'min_price', 'max_price', 'currency', 'employer', 'city',
    #               'responsibility', 'requirement', 'page']]
    while page >= 1:
        response = requests.get(f'{main_link + add_link}', headers=header, params=params)
        if response.ok:
            soup = bs(response.text, 'lxml')
            jobs = soup.find_all('div', {'class': 'f-test-vacancy-item'})
            for job in jobs:
                source = 'sj'
                name = job.find('a', {'class': 'icMQ_'}).getText()
                href = main_link + job.find('a', {'class': 'icMQ_'}).get('href')
                try:
                    price = get_price(job.find('span', {'class': '_2Wp8I'}).getText())
                    min_price = price[0]
                    max_price = price[1]
                    currency = price[2]
                except AttributeError:
                    min_price, max_price, currency = None, None, None
                employer = job.find('a', {'class': '_205Zx'}).getText()
                city = job.find('span', {'class': 'clLH5'}).parent.get_text()
                city = city.split(' • ')[1]
                br = job.find('span', {'class': '_38T7m'}).find('br')
                responsibility = clear_txt(br.previous_siblings)
                requirement = clear_txt(br.next_siblings)
                # vacancies.append([source, name, href, min_price, max_price, currency, employer, city,
                #                   responsibility, requirement, page])
                new_df = pd.DataFrame([[source, name, href, min_price, max_price, currency, employer, city,
                                        responsibility, requirement, page]], columns=cols)
                df = pd.concat([df, new_df])
        else:
            print('404')
        print(source, page)
        page += 1
        # сохраняем pd.DataFrame на случай бана
        df.to_pickle('JobDataSet.pickle')
        # проверяем есть ли еще страницы, если есть -> добавляем в параметры новую страницу
        try:
            next_page = soup.find('a', {'class': 'f-test-button-dalshe'}).get('href').split('=')[-1]
            params['page'] = next_page
            time.sleep(random.randrange(1, 5))
        except AttributeError:
            break
    return df  # vacancies


if __name__ == '__main__':
    vacancy = input(f'Введите вакансию\n-> : ')
    # vacancy = 'аналитик'

    # создаем шаблон pd.DataFrame
    cols = ['source', 'name', 'href', 'min_price', 'max_price', 'currency', 'employer', 'city',
            'responsibility', 'requirement', 'page']
    df = pd.DataFrame(columns=cols)

    # добавляем в DataFrame данные hh
    df = hh_scrab(vacancy, df)
    # сохраняем
    df.reset_index(drop=True, inplace=True)
    df.to_json('JobDataSet.json')
    df.to_excel('JobDataSet.xls')

    # добавляем в DataFrame данные sj
    df = sj_scrab(vacancy, df)

    # сохраняем
    df.reset_index(drop=True, inplace=True)
    df.to_json('JobDataSet.json')
    df.to_excel('JobDataSet.xls')
