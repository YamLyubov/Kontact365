import vk
import requests
from logic import get_date, save_matching
from logic import vk_keyboard, tg_token, vk_token
import json
import telebot
from ping import ping
from requests.auth import HTTPProxyAuth

'''
auth = HTTPProxyAuth("vkbot", "vkbot13042000")
proxy = {"http": "socks5://80.211.242.87:3180"}
'''
bot = telebot.TeleBot(tg_token)
session = vk.Session(access_token=vk_token)
api = vk.API(session, v='5.85')
longPoll = api.groups.getLongPollServer(group_id=129298566)
server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']
url = "https://api.telegram.org/bot{}/".format(tg_token)
while True:
    longPoll = requests.post('%s'%server, data={'act': 'a_check',
                                       'key': key,
                                       'ts': ts,
                                       'wait': 25}).json()
    print(longPoll)
    if len(longPoll['updates']) != 0:
        for update in longPoll['updates']:
            if update['type'] == 'message_new':
                api.messages.markAsRead(peer_id=update['object']['user_id'])
                text = update['object']['body'].lower()
                '''
                response = requests.post('%s' %url + 'sendMessage', proxies=dict(http='socks5://vkbot:vkbot13042000@80.211.242.87:3180',
                                 https='socks5://vkbot:vkbot13042000@80.211.242.87:3180'),
                                data={'chat_id': 255631997, 'text': text}, verify=False)
                '''
                if text == 'начать':
                    name = api.users.get(user_ids=update['object']['user_id'])[0]['first_name']
                    api.messages.send(peer_id=update['object']['user_id'],
                                      message='Здравствуйте, %s. ' % name,
                                      keyboard=vk_keyboard)
                elif text == 'узнать дату':
                    id = str(update['object']['user_id'])
                    with open('IP.json', 'r+', encoding='utf-8') as IP:
                        data = json.load(IP)
                        if id in data:
                            date = get_date(data[id])
                            api.messages.send(
                                peer_id=update['object']['user_id'],
                                message='Доступ к интернету будет'
                                        ' прекращен в полночь %s ' % date)
                        else:
                            api.messages.send(
                                peer_id=update['object']['user_id'],
                                message='Пожалуйста введите IP адресс в формате'
                                        ':\n 10.10.0.00\nСвой IP можно узнать'
                                        ' по телефону 8512485.')
                elif text == 'оплата через сбербанк онлайн':
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message='Если будете платить через приложение в телефоне\n'
                                'Следуйте пунктам:\n1. Платежи/Переводы\n'
                                '2. Остальные услуги\n3. Поиск: ПК ОИС\n'
                                '[Получатель: ПК ОИС-Ивангород\n'
                                'ИНН/СЧЁТ: 4707024525 / 40703810855300000095]\n'
                                '*И заполните:\nФИО: Фамилия Имя Отчество\n'
                                'Адрес: Ивангород\nУлица Дом-Квартира\n'
                                'Назначение:\nЧленские взносы 200\n'
                                '(вместо 200 указать своё 400 или 500)')
                elif '10.10.' in text:
                    ip = text
                    date = get_date(ip)
                    if date != '':
                        id = update['object']['user_id']
                        save_matching(id, ip)
                        api.messages.send(peer_id=update['object']['user_id'],
                                          message='Доступ к интернету будет'
                                                ' прекращен в полночь %s ' % date)
                    else:
                        api.messages.send(peer_id=update['object']['user_id'],
                                          message='К сожалению, информации про'
                                                  ' пользователя с таким IP '
                                                  'нет. Проверьте, правильно '
                                                  'ли вы ввели данные или'
                                                  ' обратитесь за помощью к '
                                                  'нашему сотруднику.')
                elif text == 'есть ли проблемы со связью':
                    if ping('194.105.212.27'):
                        api.messages.send(
                            peer_id=update['object']['user_id'],
                            message='Всё норм! Проблем нет!')
                    else:
                        api.messages.send(
                            peer_id=update['object']['user_id'],
                            message='Есть проблемка!')
    ts = longPoll['ts']
