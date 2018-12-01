import vk
from requests import *
from logic import get_date, save_matching, get_button, vk_keyboard
import json

session = vk.Session(access_token = '705848ce54dd5994b7a60f04badbd790bf865ae217b1960acee583641c07faeff74da562a1775f610f4df')
api = vk.API(session, v='5.85')
longPoll = api.groups.getLongPollServer(group_id = 129298566)
server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']
while True:
    longPoll = post('%s'%server, data={'act': 'a_check',
                                         'key': key,
                                         'ts': ts,
                                         'wait': 25}).json()
    print(longPoll)
    if len(longPoll['updates']) != 0:
        for update in longPoll['updates']:
            if update['type'] == 'message_new':
                api.messages.markAsRead(peer_id=update['object']['user_id'])
                text = update['object']['body'].lower()
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
                                        ':\n ip:10.10.0.00\nСвой IP можно узнать'
                                        ' по телефону 8512485.')

                elif 'ip' in text:
                    ip = text[3:]
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
    ts = longPoll['ts']
