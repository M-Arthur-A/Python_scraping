from pymongo import MongoClient
from pathlib import Path
import json


def mongodb_creation(job):
    '''
    Функция, записывающая собранные вакансии в созданную БД
    '''

    dataset_path = 'NewsDataSet.json'
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)  # загружаем JSON с данными

        job.insert_many(dataset)  # вставка подготовленных данных
        print('данные успешно добавлены в MongoDB')


def main():
    ### Подготовка базы данных
    client = MongoClient('192.168.1.3', 27017)  # подключение к виртуальной машине
    db = client['news']  # указание базы данных
    news = db.news  # указание коллекции
    ###
    mongodb_creation(news)
    # проверка
    for n in news.find({}):
        print(n)


if __name__ == '__main__':
    main()

# вывод консоли:
'''данные успешно добавлены в MongoDB
{'_id': ObjectId('5f2ab8baf64151a58f708dfb'), 'source': 'rbc', 'name': 'МОЭК подала иск к Дому моды Вячеслава Зайцева более чем на 700 тыс. руб.', 'href': 'https://www.rbc.ru/rbcfreenews/5f2a9b649a79473deec39a54?from=newsfeed', 'date': '2020-08-05 16:33'}
{'_id': ObjectId('5f2ab8baf64151a58f708dfc'), 'source': 'rbc', 'name': 'Проректора МГУ Гришина задержали и отправили в Саранск', 'href': 'https://www.rbc.ru/society/05/08/2020/5f2ab1fd9a79474b6a398fdf?from=newsfeed', 'date': '2020-08-05 16:24'}
{'_id': ObjectId('5f2ab8baf64151a58f708dfd'), 'source': 'rbc', 'name': 'Павлюченкова отказалась от участия в US Open из-за коронавируса', 'href': 'https://sportrbc.ru/news/5f2ab0649a79474a01f1676d?from=newsfeed', 'date': '2020-08-05 16:20'}
{'_id': ObjectId('5f2ab8baf64151a58f708dfe'), 'source': 'rbc', 'name': 'Пандемия коронавируса. Самое актуальное на 5 августа', 'href': 'https://www.rbc.ru/society/05/08/2020/5e2fe9459a79479d102bada6?from=newsfeed', 'date': '2020-08-05 16:19'}
{'_id': ObjectId('5f2ab8baf64151a58f708dff'), 'source': 'rbc', 'name': 'Forbes назвал Керимова самым богатым миллиардером России', 'href': 'https://www.rbc.ru/business/05/08/2020/5f2aaecc9a7947491b7cd505?from=newsfeed', 'date': '2020-08-05 16:18'}
{'_id': ObjectId('5f2ab8baf64151a58f708e00'), 'source': 'rbc', 'name': 'Акции Sony на максимуме с 2001 года. Аналитики ждут роста благодаря PS5', 'href': 'https://quote.rbc.ru/news/article/5f2aa7fc9a79474517d8fffd?from=newsfeed', 'date': '2020-08-05 16:17'}
{'_id': ObjectId('5f2ab8baf64151a58f708e01'), 'source': 'rbc', 'name': 'Взрыв в порту Бейрута. Главное', 'href': 'https://www.rbc.ru/society/05/08/2020/5f299ec49a79476520783341?from=newsfeed', 'date': '2020-08-05 16:13'}
{'_id': ObjectId('5f2ab8baf64151a58f708e02'), 'source': 'rbc', 'name': 'Соцсети делают бизнес по-новому: дайджест иностранных СМИ', 'href': 'https://pro.rbc.ru/news/5f2a7e519a79472faa9d38cd?from=newsfeed&utm_source=rbc.ru&utm_medium=inhouse_media&utm_campaign=newsfeed&utm_content=5f2a7e519a79472faa9d38cd', 'date': '2020-08-05 16:12'}
{'_id': ObjectId('5f2ab8baf64151a58f708e03'), 'source': 'rbc', 'name': 'Медведев предупредил белорусов о последствиях из-за «образа врага»', 'href': 'https://www.rbc.ru/rbcfreenews/5f2aa4ef9a7947434d3aef32?from=newsfeed', 'date': '2020-08-05 16:06'}
{'_id': ObjectId('5f2ab8baf64151a58f708e04'), 'source': 'rbc', 'name': 'Лукашенко пообещал сотрудничество с Москвой и Киевом по делу «боевиков»', 'href': 'https://www.rbc.ru/rbcfreenews/5f2aa7669a7947437e759803?from=newsfeed', 'date': '2020-08-05 16:05'}
{'_id': ObjectId('5f2ab8baf64151a58f708e05'), 'source': 'rbc', 'name': 'В Молдавии ответили на сообщения о судне со взорвавшимся в Бейруте грузом', 'href': 'https://www.rbc.ru/rbcfreenews/5f2a908a9a7947377ecb402d?from=newsfeed', 'date': '2020-08-05 16:02'}
{'_id': ObjectId('5f2ab8baf64151a58f708e06'), 'source': 'rbc', 'name': 'ФАС обвинила «Открытие» в нарушении закона о защите конкуренции', 'href': 'https://www.rbc.ru/business/05/08/2020/5f2aa6fa9a7947422bff9ffb?from=newsfeed', 'date': '2020-08-05 15:59'}
{'_id': ObjectId('5f2ab8baf64151a58f708e07'), 'source': 'rbc', 'name': 'В ВТБ предупредили о спаде доходности вкладов. 3 альтернативы в биткоине', 'href': 'https://www.rbc.ru/crypto/news/5f2aa1f59a7947412e08533f?from=newsfeed', 'date': '2020-08-05 15:46'}
{'_id': ObjectId('5f2ab8baf64151a58f708e08'), 'source': 'rbc', 'name': 'Губернатор Бейрута сообщил о гибели десяти пожарных при взрыве', 'href': 'https://www.rbc.ru/rbcfreenews/5f2a9c159a79473cf1a37e54?from=newsfeed', 'date': '2020-08-05 15:43'}
{'_id': ObjectId('5f2ab8baf64151a58f708e09'), 'source': 'kommersant', 'name': 'Участник митинга в поддержку Фургала задержан в Хабаровске', 'href': 'https://www.kommersant.ru/doc/4442911', 'date': '2020-08-05 16:35'}
{'_id': ObjectId('5f2ab8baf64151a58f708e0a'), 'source': 'kommersant', 'name': 'Павлюченкова отказалась от участия в US Open', 'href': 'https://www.kommersant.ru/doc/4442962', 'date': '2020-08-05 16:31'}
{'_id': ObjectId('5f2ab8baf64151a58f708e0b'), 'source': 'kommersant', 'name': 'Бывший сотрудник Google приговорен к 18 месяцам тюрьмы за кражу информации', 'href': 'https://www.kommersant.ru/doc/4442907', 'date': '2020-08-05 16:11'}
{'_id': ObjectId('5f2ab8baf64151a58f708e0c'), 'source': 'kommersant', 'name': 'Набсовет РУСАДА рекомендовал уволить Гануса', 'href': 'https://www.kommersant.ru/doc/4442945', 'date': '2020-08-05 16:07'}
{'_id': ObjectId('5f2ab8baf64151a58f708e0d'), 'source': 'kommersant', 'name': 'ФАС возбудила дело против банка «Открытие» из-за выплат клиентам меньше обещанного', 'href': 'https://www.kommersant.ru/doc/4442937', 'date': '2020-08-05 16:02'}
{'_id': ObjectId('5f2ab8baf64151a58f708e0e'), 'source': 'kommersant', 'name': 'Минюст получил уведомление от ЕСПЧ о жалобе Нидерландов по делу MH17', 'href': 'https://www.kommersant.ru/doc/4442929', 'date': '2020-08-05 15:47'}
{'_id': ObjectId('5f2ab8baf64151a58f708e0f'), 'source': 'kommersant', 'name': 'Список богатейших россиян впервые возглавила семья Керимова', 'href': 'https://www.kommersant.ru/doc/4442927', 'date': '2020-08-05 15:41'}
{'_id': ObjectId('5f2ab8baf64151a58f708e10'), 'source': 'kommersant', 'name': 'Медведев назвал отношения Москвы и Минска разменной монетой в избирательной кампании', 'href': 'https://www.kommersant.ru/doc/4442914', 'date': '2020-08-05 15:40'}
{'_id': ObjectId('5f2ab8baf64151a58f708e11'), 'source': 'kommersant', 'name': 'Медведев назвал акции в поддержку Фургала явлением, с которым государству надо считаться', 'href': 'https://www.kommersant.ru/doc/4442918', 'date': '2020-08-05 15:30'}
{'_id': ObjectId('5f2ab8baf64151a58f708e12'), 'source': 'kommersant', 'name': 'SpaceX провела успешное испытание ракеты Starship', 'href': 'https://www.kommersant.ru/doc/4442878', 'date': '2020-08-05 15:23'}
{'_id': ObjectId('5f2ab8baf64151a58f708e13'), 'source': 'kommersant', 'name': 'Глава Калмыкии Хасиков госпитализирован с коронавирусом', 'href': 'https://www.kommersant.ru/doc/4442885', 'date': '2020-08-05 15:16'}
{'_id': ObjectId('5f2ab8baf64151a58f708e14'), 'source': 'kommersant', 'name': 'В смертельном ДТП на «Тавриде» обвинили уставшего водителя и перевозчика', 'href': 'https://www.kommersant.ru/doc/4442869', 'date': '2020-08-05 15:07'}
{'_id': ObjectId('5f2ab8baf64151a58f708e15'), 'source': 'kommersant', 'name': 'Зеленский попросил Лукашенко выдать задержанных россиян', 'href': 'https://www.kommersant.ru/doc/4442899', 'date': '2020-08-05 15:05'}
{'_id': ObjectId('5f2ab8baf64151a58f708e16'), 'source': 'kommersant', 'name': '«РИА Новости»: в Москве обокрали коттедж Тинькова', 'href': 'https://www.kommersant.ru/doc/4442888', 'date': '2020-08-05 15:04'}
{'_id': ObjectId('5f2ab8baf64151a58f708e17'), 'source': 'kommersant', 'name': '«Ростелеком» создает новый портал госуслуг', 'href': 'https://www.kommersant.ru/doc/4442887', 'date': '2020-08-05 15:00'}
{'_id': ObjectId('5f2ab8baf64151a58f708e18'), 'source': 'kommersant', 'name': 'Защита Шамсутдинова подала ходатайство о рассмотрении дела присяжными', 'href': 'https://www.kommersant.ru/doc/4442870', 'date': '2020-08-05 14:56'}
{'_id': ObjectId('5f2ab8baf64151a58f708e19'), 'source': 'kommersant', 'name': '«Голос» направил в ЦИК предложения по улучшению досрочного голосования', 'href': 'https://www.kommersant.ru/doc/4442877', 'date': '2020-08-05 14:46'}
{'_id': ObjectId('5f2ab8baf64151a58f708e1a'), 'source': 'kommersant', 'name': 'Число въехавших в Россию иностранцев в первом полугодии сократилось на 60%', 'href': 'https://www.kommersant.ru/doc/4442876', 'date': '2020-08-05 14:38'}
{'_id': ObjectId('5f2ab8baf64151a58f708e1b'), 'source': 'kommersant', 'name': 'В Москве посетителям театров, концертных залов и цирков будут измерять температуру', 'href': 'https://www.kommersant.ru/doc/4442872', 'date': '2020-08-05 14:35'}
{'_id': ObjectId('5f2ab8baf64151a58f708e1c'), 'source': 'kommersant', 'name': 'Россия предложила Нидерландам пересмотреть налоговое соглашение', 'href': 'https://www.kommersant.ru/doc/4442863', 'date': '2020-08-05 14:11'}
{'_id': ObjectId('5f2ab8baf64151a58f708e1d'), 'source': 'kommersant', 'name': 'Выручка платежного сервиса Square от операций с биткойном выросла на 600%', 'href': 'https://www.kommersant.ru/doc/4442862', 'date': '2020-08-05 14:08'}
{'_id': ObjectId('5f2ab8baf64151a58f708e1e'), 'source': 'kommersant', 'name': 'Гендиректор «Аэрофлота» Савельев не исключает банкротств авиакомпаний осенью', 'href': 'https://www.kommersant.ru/doc/4442861', 'date': '2020-08-05 13:58'}
{'_id': ObjectId('5f2ab8baf64151a58f708e1f'), 'source': 'kommersant', 'name': 'Дело адвокатов из КБР передали в окружное управление', 'href': 'https://www.kommersant.ru/doc/4442849', 'date': '2020-08-05 13:53'}
{'_id': ObjectId('5f2ab8baf64151a58f708e20'), 'source': 'kommersant', 'name': 'Чистый спрос на наличную валюту в мае упал на 42%', 'href': 'https://www.kommersant.ru/doc/4442859', 'date': '2020-08-05 13:53'}
{'_id': ObjectId('5f2ab8baf64151a58f708e21'), 'source': 'kommersant', 'name': 'Власти Молдавии: судно, груз с которого взорвался в Бейруте, давно не под нашим флагом', 'href': 'https://www.kommersant.ru/doc/4442844', 'date': '2020-08-05 13:41'}
{'_id': ObjectId('5f2ab8baf64151a58f708e22'), 'source': 'kommersant', 'name': 'Подразделение Alibaba провело в Гонконге крупнейшее FPO с 2015 года', 'href': 'https://www.kommersant.ru/doc/4442841', 'date': '2020-08-05 13:24'}
{'_id': ObjectId('5f2ab8baf64151a58f708e23'), 'source': 'kommersant', 'name': 'Обыски у экс-президента «Интеко» связаны с уголовным делом о мошенничестве', 'href': 'https://www.kommersant.ru/doc/4442840', 'date': '2020-08-05 13:22'}
{'_id': ObjectId('5f2ab8baf64151a58f708e24'), 'source': 'kommersant', 'name': 'Зампред ВТБ предупредил о риске снижения доходов от вкладов до уровня 90-х', 'href': 'https://www.kommersant.ru/doc/4442833', 'date': '2020-08-05 13:10'}
{'_id': ObjectId('5f2ab8baf64151a58f708e25'), 'source': 'kommersant', 'name': 'ЦИК России не будет отправлять наблюдателей на выборы в Белоруссию', 'href': 'https://www.kommersant.ru/doc/4442827', 'date': '2020-08-05 13:00'}
{'_id': ObjectId('5f2ab8baf64151a58f708e26'), 'source': 'kommersant', 'name': 'Авиакомпания Virgin Atlantic объявила о банкротстве в США', 'href': 'https://www.kommersant.ru/doc/4442815', 'date': '2020-08-05 12:54'}
{'_id': ObjectId('5f2ab8baf64151a58f708e27'), 'source': 'vedomosti', 'name': 'Компания Глеба Франка предложила правительству реформу рыбной отрасли', 'href': 'https://www.vedomosti.ru/business/articles/2020/08/04/835961-kompaniya-gleba-franka-predlozhila-pravitelstvu-reformu-ribnoi-otrasli', 'date': '2020-08-04 21:07'}
{'_id': ObjectId('5f2ab8baf64151a58f708e28'), 'source': 'vedomosti', 'name': 'Адвокат заявил о возможной фальсификации доказательств по делу Ефремова', 'href': 'https://www.vedomosti.ru/society/news/2020/08/05/835998-o-falsifikatsii-dokazatelstv-po-delu-efremova', 'date': '2020-08-05 12:26'}
{'_id': ObjectId('5f2ab8baf64151a58f708e29'), 'source': 'vedomosti', 'name': 'Германия отпраздновала день свободы от пандемии', 'href': 'https://www.vedomosti.ru/opinion/articles/2020/08/04/835974-germaniya-otprazdnovala', 'date': '2020-08-04 23:53'}
{'_id': ObjectId('5f2ab8baf64151a58f708e2a'), 'source': 'vedomosti', 'name': '«Никогда не видел, чтобы казаки что-то делали»', 'href': 'https://www.vedomosti.ru/opinion/articles/2020/08/04/835972-kazaki-delali', 'date': '2020-08-04 23:52'}
{'_id': ObjectId('5f2ab8baf64151a58f708e2b'), 'source': 'vedomosti', 'name': 'Медведев заявил о необходимости властей считаться со сторонниками Фургала', 'href': 'https://www.vedomosti.ru/politics/news/2020/08/05/836013-medvedev-zayavil-o-neobhodimosti-vlasti-schitatsya-so-storonnikami-furgala', 'date': '2020-08-05 15:38'}
{'_id': ObjectId('5f2ab8baf64151a58f708e2c'), 'source': 'vedomosti', 'name': 'В Москве открылся ресторан с роботом-поваром', 'href': 'https://www.vedomosti.ru/business/articles/2020/08/05/835993-v-moskve-otkrilsya-restoran-s-robotom-povarom', 'date': '2020-08-05 10:30'}
{'_id': ObjectId('5f2ab8baf64151a58f708e2d'), 'source': 'vedomosti', 'name': 'В порту Бейрута произошел взрыв', 'href': 'https://www.vedomosti.ru/society/articles/2020/08/04/835958-v-portu-beiruta-proizoshel-moschnii-vzriv', 'date': '2020-08-04 20:26'}
{'_id': ObjectId('5f2ab8baf64151a58f708e2e'), 'source': 'vedomosti', 'name': 'Россия предложила Нидерландам пересмотреть налоговое соглашение', 'href': 'https://www.vedomosti.ru/economics/news/2020/08/05/836009-rossiya-predlozhila-niderlandam-izmenit-nalogovie-soglasheniya', 'date': '2020-08-05 15:29'}
{'_id': ObjectId('5f2ab8baf64151a58f708e2f'), 'source': 'vedomosti', 'name': 'В России за сутки выявили 5204 больных коронавирусом', 'href': 'https://www.vedomosti.ru/society/articles/2020/08/05/835988-v-rossii-viyavili-5-204-bolnih', 'date': '2020-08-05 10:50'}
{'_id': ObjectId('5f2ab8baf64151a58f708e30'), 'source': 'vedomosti', 'name': 'Президент Белоруссии продолжает обвинять граждан России во вмешательстве в выборы', 'href': 'https://www.vedomosti.ru/politics/articles/2020/08/04/835969-prezident-belorussii', 'date': '2020-08-04 23:38'}
{'_id': ObjectId('5f2ab8baf64151a58f708e31'), 'source': 'vedomosti', 'name': 'В Турции увеличилось количество случаев COVID-19 после открытия границ', 'href': 'https://www.vedomosti.ru/society/news/2020/08/05/836003-v-turtsii-rezko-uvelichilos-chislo-zarazhenii-korornavirusom-posle-otkritiya-granits', 'date': '2020-08-05 13:57'}
{'_id': ObjectId('5f2ab8baf64151a58f708e32'), 'source': 'vedomosti', 'name': 'Систему распознавания лиц в вагонах московского метро развернет «Максимателеком»', 'href': 'https://www.vedomosti.ru/technology/articles/2020/08/04/835976-sistemu-raspoznavaniya', 'date': '2020-08-04 23:50'}
{'_id': ObjectId('5f2ab8baf64151a58f708e33'), 'source': 'vedomosti', 'name': 'МВД пошло навстречу гражданам в исчислении сроков для повторных штрафов', 'href': 'https://www.vedomosti.ru/society/articles/2020/08/04/835965-mvd-poshlo', 'date': '2020-08-04 23:42'}
{'_id': ObjectId('5f2ab8baf64151a58f708e34'), 'source': 'vedomosti', 'name': 'Что вы знаете о голосовых роботах?', 'href': 'https://www.vedomosti.ru/partner/test/2020/07/30/835169-chto-robotah', 'date': '2020-07-30 10:51'}
{'_id': ObjectId('5f2ab8baf64151a58f708e35'), 'source': 'vedomosti', 'name': 'Военнослужащие дефицитных специальностей получат доплаты', 'href': 'https://www.vedomosti.ru/politics/articles/2020/08/04/835967-voennosluzhaschie-defitsitnih', 'date': '2020-08-04 23:43'}
{'_id': ObjectId('5f2ab8baf64151a58f708e36'), 'source': 'vedomosti', 'name': 'Российские покупатели резко активизировались', 'href': 'https://www.vedomosti.ru/economics/articles/2020/08/04/835968-rossiiskie-pokupateli', 'date': '2020-08-04 23:44'}
{'_id': ObjectId('5f2ab8baf64151a58f708e37'), 'source': 'vedomosti', 'name': 'Что о вас знают в социальных сетях', 'href': 'https://www.vedomosti.ru/career/articles/2020/08/04/835980-znayut-sotsialnih', 'date': '2020-08-04 23:50'}
{'_id': ObjectId('5f2ab8baf64151a58f708e38'), 'source': 'vedomosti', 'name': 'Российская экономика становится венчуром', 'href': 'https://www.vedomosti.ru/economics/articles/2020/08/04/835970-ekonomika-venchurom', 'date': '2020-08-04 23:46'}
{'_id': ObjectId('5f2ab8baf64151a58f708e39'), 'source': 'vedomosti', 'name': 'Около порта в Бейруте прогремел мощный взрыв. Фотографии', 'href': 'https://www.vedomosti.ru/society/galleries/2020/08/04/835956-okolo-porta-v-beirute-progremel-moschnii-vzriv-fotografii', 'date': '2020-08-04 20:38'}
{'_id': ObjectId('5f2ab8baf64151a58f708e3a'), 'source': 'vedomosti', 'name': '«Норникель» представил план ликвидации последствий аварии в Норильске', 'href': 'https://www.vedomosti.ru/business/articles/2020/08/04/835957-nornikel-predstavil-plan-likvidatsii-posledstvii-avarii-v-norilske', 'date': '2020-08-04 19:17'}
{'_id': ObjectId('5f2ab8baf64151a58f708e3b'), 'source': 'vedomosti', 'name': 'Кипр по двойному тарифу', 'href': 'https://www.vedomosti.ru/economics/articles/2020/08/03/835884-kipr-dvoinomu', 'date': '2020-08-04 00:14'}
{'_id': ObjectId('5f2ab8baf64151a58f708e3c'), 'source': 'vedomosti', 'name': 'Booking уволит почти четверть персонала из-за пандемии', 'href': 'https://www.vedomosti.ru/business/news/2020/08/04/835945-booking-sokratit-chetvert-personala', 'date': '2020-08-04 16:32'}
{'_id': ObjectId('5f2ab8baf64151a58f708e3d'), 'source': 'vedomosti', 'name': 'Вдова Дмитрия Босова заявила о попытке рейдерского захвата «Сибантрацита»', 'href': 'https://www.vedomosti.ru/business/articles/2020/08/04/835931-vdova-dmitriya-bosova-zayavila-o-popitke-reiderskogo-zahvata', 'date': '2020-08-04 14:59'}
{'_id': ObjectId('5f2ab8baf64151a58f708e3e'), 'source': 'vedomosti', 'name': 'Tekta Group покупает жилой проект на юго-западе Москвы', 'href': 'https://www.vedomosti.ru/realty/articles/2020/08/04/835905-tekta-group-pokupaet-zhiloi-proekt', 'date': '2020-08-04 10:54'}
{'_id': ObjectId('5f2ab8baf64151a58f708e3f'), 'source': 'vedomosti', 'name': 'Поверят ли российские туристы президенту Танзании', 'href': 'https://www.vedomosti.ru/society/articles/2020/08/03/835872-prezidentu-tanzanii', 'date': '2020-08-04 11:15'}
'''