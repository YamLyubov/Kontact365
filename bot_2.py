# -*- coding: utf-8 -*-
import vk
from requests import post
from logic import get_date, save_matching, ping
from const import vk_keyboard, tg_token, vk_token, wb_id, nasa_id, group_id
import json
import telebot
from time import sleep
from text import greeting, return_date, get_ip, sber, no_ip
from datetime import datetime
import sys
import codecs

def setup_console(sys_enc="utf-8"):
    reload(sys)
    try:
        # для win32 вызываем системную библиотечную функцию
        if sys.platform.startswith("win"):
            import ctypes
            enc = "cp%d" % ctypes.windll.kernel32.GetOEMCP() #TODO: проверить на win64/python64
        else:
            # для Linux всё, кажется, есть и так
            enc = (sys.stdout.encoding if sys.stdout.isatty() else
                        sys.stderr.encoding if sys.stderr.isatty() else
                            sys.getfilesystemencoding() or sys_enc)

        # кодировка для sys
        sys.setdefaultencoding(sys_enc)

        # переопределяем стандартные потоки вывода, если они не перенаправлены
        if sys.stdout.isatty() and sys.stdout.encoding != enc:
            sys.stdout = codecs.getwriter(enc)(sys.stdout, 'replace')

        if sys.stderr.isatty() and sys.stderr.encoding != enc:
            sys.stderr = codecs.getwriter(enc)(sys.stderr, 'replace')

    except:
        pass # Ошибка? Всё равно какая - работаем по-старому...


users = []
bot = telebot.TeleBot(tg_token)
session = vk.Session(access_token=vk_token)
api = vk.API(session, v='5.85')
longPoll = api.groups.getLongPollServer(group_id=group_id)
server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']
url = "https://api.telegram.org/bot{}/".format(tg_token)
while True:
    longPoll = post('%s'%server, data={'act': 'a_check',
                                       'key': key,
                                       'ts': ts,
                                       'wait': 90}).json()
    print(longPoll)
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
                elif text == '📅 Узнать дату окончания оплаты 📍':
                    id = str(update['object']['user_id'])
                    with open('IP.json', 'r+', encoding='utf-8') as IP:
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
                elif '10.10.' in text and update['object']['user_id'] in users:
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
                    else:
                        api.messages.send(peer_id=update['object']['user_id'],
                                          message=no_ip)
                elif text == '💳 Оплата через Сбербанк ОнЛ@йн 💰':
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message=sber,
                        attachment='photo-129298566_456239067,'
                                   'photo-129298566_456239068,'
                                   'photo-129298566_456239069,'
                                   'photo-129298566_456239070,'
                                   'photo-129298566_456239071,'
                                   'photo-129298566_456239072,'
                                   'photo-129298566_456239073,'
                                   'photo-129298566_456239074')

                elif text == '🏄🌏 Есть Интернет? 🚀🌖':
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
                    else:
                        sleep(3)
                        api.messages.send(
                            peer_id=update['object']['user_id'],
                            message='В данным момент имеются проблемы 🚧 со'
                                    ' связью. Приносим извинения😔.')
                else:
                    tg_text = '👀   ' + time + ' \n ' + '👃   ' + name \
                              + ' ' + last_name + ' \n ' + '👅   ' + text
                    post(url + "sendMessage", data={'chat_id': nasa_id,
                                                    'text': tg_text})


        ts = longPoll['ts']
