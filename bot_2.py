# -*- coding: utf-8 -*-
import vk
from requests import post
from logic import get_date, save_matching, ping
from const import vk_keyboard, tg_token, vk_token, wb_id, nasa_id, group_id
import json
import telebot
from time import sleep
from text import greeting, return_date, get_ip, no_ip, operator
from text import sber_0, sber_1, sber_2, sber_3, sber_4
from datetime import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
users = []
bot = telebot.TeleBot(tg_token)
session = vk.Session(access_token=vk_token)
api = vk.API(session, v='5.85')
longPoll = api.groups.getLongPollServer(group_id=group_id)
server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']
url = "https://api.telegram.org/bot{}/".format(tg_token)
while True:
    longPoll = post('%s' % server, data={'act': 'a_check',
                                         'key': key,
                                         'ts': ts,
                                         'wait': 90}).json()
    if len(longPoll['updates']) != 0:
        time = str(datetime.now())[:16]
        for update in longPoll['updates']:
            if update['type'] == 'message_new':
                api.messages.markAsRead(peer_id=update['object']['user_id'])
                text = update['object']['body']
                user = api.users.get(user_ids=update['object']['user_id'])
                name = user[0]['first_name']
                last_name = user[0]['last_name']
                tg_text = '👀   ' + time + ' \n ' + '👃   ' + name \
                          + ' ' + last_name + ' \n ' + '👅   ' + text
                post(url + "sendMessage", data={'chat_id': wb_id,
                                                'text': tg_text})
                if text == 'Начать' or text == '⏳ обновить клавиатуру 💡':
                    api.messages.send(peer_id=update['object']['user_id'],
                                      message=greeting,
                                      keyboard=vk_keyboard)
                elif text == '📅 Дата окончания оплаты':
                    id = str(update['object']['user_id'])
                    with open('IP.json', 'r+') as IP:
                        data = json.load(IP)
                        if id in data:
                            date = get_date(data[id])
                            message = return_date + date
                            api.messages.send(
                                peer_id=update['object']['user_id'],
                                message=message)
                        else:
                            users.append(update['object']['user_id'])
                            api.messages.send(
                                peer_id=update['object']['user_id'],
                                message=get_ip)
                elif '10.10.' in text or update['object']['user_id'] in users:
                    users.remove(update['object']['user_id'])
                    ip = text
                    date = get_date(ip)
                    if date != '':
                        id = update['object']['user_id']
                        message = return_date + date
                        save_matching(id, ip)
                        api.messages.send(
                                peer_id=update['object']['user_id'],
                                message=message)
                        api.messages.send(
                            peer_id=update['object']['user_id'],
                            message='IP сохранен. Больше писать его не нужно😊')
                    else:
                        api.messages.send(peer_id=update['object']['user_id'],
                                          message=no_ip)
                        api.messages.send(peer_id=update['object']['user_id'],
                                          attachment='doc-129298566_483539786')
                elif text == '💳 Сбербанк ОнЛ@йн':
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message=sber_0)
                    sleep(2)
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message=sber_1,
                        attachment='photo-129298566_456239068')
                    sleep(5)
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message=sber_2,
                        attachment='photo-129298566_456239070')
                    sleep(5)
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message=sber_3,
                        attachment='photo-129298566_456239071')
                    sleep(5)
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message=sber_4,
                        attachment='photo-129298566_456239074')

                elif text == '🏄🌏 Есть Интернет?':
                    sleep(1)
                    api.messages.send(peer_id=update['object']['user_id'],
                                      message='Запускаем квантово🔨карпаскуляр'
                                              'ный тест соединения')
                    sleep(1)
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message='💨')
                    sleep(1)
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message='💨💨💨')
                    sleep(1)
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message='💨💨💨💨💨')
                    sleep(1)
                    if ping('194.105.212.27'):
                        api.messages.send(
                            peer_id=update['object']['user_id'],
                            message='✨Проблем со связью не обнаружено 👌.'
                                    ' Приятного дня!✨')
                        api.messages.send(peer_id=update['object']['user_id'],
                                          attachment='doc-129298566_483539744')
                    else:
                        sleep(3)
                        api.messages.send(
                            peer_id=update['object']['user_id'],
                            message='В данным момент имеются проблемы 🚧 со'
                                    ' связью. Приносим извинения😔.')
                elif update['object']['user_id'] not in users:
                    tg_text = '👀   ' + time + ' \n ' + '👃   ' + name \
                              + ' ' + last_name + ' \n ' + '👅   ' + text
                    post(url + "sendMessage", data={'chat_id': nasa_id,
                                                    'text': tg_text})
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message=operator)

        ts = longPoll['ts']
