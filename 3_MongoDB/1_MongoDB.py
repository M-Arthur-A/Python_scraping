from pymongo import MongoClient
from pathlib import Path
import json
from pprint import pprint


def json_to_int(data):  # конвертируем цены в integer
    for i in data.keys():
        try:
            data[i] = int(data[i].replace(' ', ''))
        except AttributeError:
            data[i] = 0


def json_transpose(data):
    dataT = []
    datat = {}
    for i in data['source']:  # итерируем по строкам
        for key in data:  # итерируем по ключам
            datat[key] = data[key][i]  # присваиваем каждому ключу значение
        dataT.append(datat)  # добавляем получившийся словарь в список
        datat = {}  # очищаем словарь (не обязательно)
    return dataT


def mongodb_creation(job):
    '''
    Функция, записывающая собранные вакансии в созданную БД
    '''

    dataset_path = str(Path().absolute().parent) + '/2_BeautifulSoup/JobDataSet.json'
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)  # загружаем JSON с данными
        json_to_int(dataset['min_price'])  # конвертируем цены в integer
        json_to_int(dataset['max_price'])  # конвертируем цены в integer

        dataset_transposed = json_transpose(dataset)  # транспонирование данных

        job.insert_many(dataset_transposed)  # вставка подготовленных данных
        print('данные успешно добавлены в MongoDB')


def mongodb_query(job):
    '''
    Функция производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы.
    Поиск по двум полям (мин и макс зарплату)
    '''

    for j in job.find({'$or': [
                                {'min_price': {'$gte': 150000}},
                                {'max_price': {'$gte': 150000}}
                               ]}):
        print(j['name'], '|', j['href'], '|', j['min_price'], '|', j['max_price'], '|', j['currency'])


def main():
    ### Подготовка базы данных
    client = MongoClient('192.168.1.7', 27017)  # подключение к виртуальной машине
    db = client['jobs']  # указание базы данных
    job = db.job  # указание коллекции
    ###

    mongodb_creation(job)  # 1 задача
    mongodb_query(job)  # 2 задача
    # 3 задача может решаться через сверку хешей ключей _id


if __name__ == '__main__':
    main()
