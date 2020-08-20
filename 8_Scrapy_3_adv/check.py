from pymongo import MongoClient


def followers_query(db, user):
    '''
    список подписчиков только указанного пользователя
    '''

    for i in db.find({'$and': [
        {'username': user},
        {'follower_data': {"$exists": True}}
    ]}):
        print(i['follower_data'])


def follow_query(db, user):
    '''
    список профилей, на кого подписан указанный пользователь
    '''
    for i in db.find({'$and': [
        {'username': user},
        {'following_data': {"$exists": True}}
    ]}):
        print(i['following_data'])


if __name__ == '__main__':
    client = MongoClient('192.168.1.3', 27017)
    mongo_base = client.insta
    collection = mongo_base['profiles']

    # for n in collection.find({}):
    #     print(n)

    users = ['_lena_volkova_', 'cg_boost']
    followers_query(collection, users[0])
    print()
    print('-----------------------------------------------------------------------------------------------------------')
    print()
    follow_query(collection, users[1])
