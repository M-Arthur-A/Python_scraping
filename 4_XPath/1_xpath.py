import requests
from lxml import html
import pandas as pd
from datetime import date as dt
import json

'''
Новости RBC, Vedomosti, Kommersant
'''


def scrap(df, cols, resource):
    def clear(txt, d=None):
        txt = ''.join(txt)  # преобразование списка в строку
        if txt:
            txt = txt.replace('\n', '')  # удаление переноса строки
            txt = txt.replace('\r', '')  # удаление прочего
            txt = ''.join(txt.split('  '))  # удаление двойных пробелов
            txt = txt[1:] if txt[0] == ' ' else txt  # удалением пробела в начале
            if d:  # обработка даты
                try:
                    txt = txt.split(', ')[1]
                except:
                    pass
                txt = str(dt.today()) + ' ' + txt
        return txt

    def get_key():
        with open('/home/arthur/Project/GeekBrains/Python_scraping/!ADDS/hw4_adds/req.txt', 'r') as f:
            return f.read().replace('\n', '')

    header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'}
    if resource == 'rbc':
        path = 'https://www.rbc.ru/'
        news_xpath = "//div[@class='js-news-feed-list']/a"
        news_title_xpath = ".//span[contains(@class,'news-feed__item__title')]//text()"
        news_href_xpath = "./@href"
        news_date_xpath = ".//span[contains(@class,'news-feed__item__date-text')]//text()"
    elif resource == 'kommersant':
        path = 'https://www.kommersant.ru/archive/news?from=news'
        news_xpath = "//ul[@class='archive_date_result__list']/li"
        news_title_xpath = "./a/text()"
        news_href_xpath = "./a/@href"
        news_date_xpath = "./a/time/text()"
    elif resource == 'vedomosti':
        # не работает из-за java-script
        # path = 'https://www.vedomosti.ru/'
        # news_xpath = "//ul[contains(@class,'waterfall__list')]/li"
        # news_title_xpath = "./a/text()"
        # news_href_xpath = "./a/@href"
        # news_date_xpath = ".//div[contains(@class,'waterfall__item-meta')]/text()"
        header['X-Access-Token'] = get_key()
        path = 'https://api.vedomosti.ru/v2/pages/main/grids/columns2/built'
        response = requests.get(path, headers=header)
        json_get = response.json()
        for data in json_get['cells']:
            if not 'adfox' in data.keys():
                if 'data' in data.keys():
                    if 'title' in data['data'].keys():
                        name = data['data']['title']
                        href = 'https://www.' + data['data']['url']
                        date = data['data']['published_at']
                        date = date.split('T')[0] + ' ' + date.split('T')[1].split('.')[0][:-3]
                        new_df = pd.DataFrame([[resource, name, href, date]], columns=cols)
                        df = pd.concat([df, new_df])
        return df
    response = requests.get(path, headers=header)
    dom = html.fromstring(response.text)
    news = dom.xpath(news_xpath)
    for n in news:
        name = clear(n.xpath(news_title_xpath))
        href = n.xpath(news_href_xpath)[0]
        if resource == 'kommersant':
            href = 'https://www.kommersant.ru' + href
        date = clear(n.xpath(news_date_xpath), 'date')
        # print(name, '|', href, '|', date)
        new_df = pd.DataFrame([[resource, name, href, date]], columns=cols)
        df = pd.concat([df, new_df])
    return df


def main():
    cols = ['source', 'name', 'href', 'date']
    df = pd.DataFrame(columns=cols)
    df = scrap(df, cols, 'rbc')
    df = scrap(df, cols, 'kommersant')
    df = scrap(df, cols, 'vedomosti')

    # сохранение датасета
    df.reset_index(drop=True, inplace=True)
    df.to_excel('JobDataSet.xls')
    to_json = df.to_dict('records')
    with open('NewsDataSet.json', 'w') as f:
        f.write(json.dumps(to_json))


if __name__ == '__main__':
    main()
