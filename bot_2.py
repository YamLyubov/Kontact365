import vk
import requests
from logic import get_date, save_matching
from logic import vk_keyboard, tg_token, vk_token
import json
import telebot
from ping import ping
import time
from text import return_date, get_ip, sber, no_ip
from datetime import datetime


users = []
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
                                                'wait': 90}).json()
    print(longPoll)
    if len(longPoll['updates']) != 0:
        time = str(datetime.now())[:16]
        for update in longPoll['updates']:
            if update['type'] == 'message_new':
                api.messages.markAsRead(peer_id=update['object']['user_id'])
                text = update['object']['body'].lower()
                name = api.users.get(user_ids=update['object']['user_id'])[0]['first_name']
                last_name = api.users.get(user_ids=update['object']['user_id'])[0]['last_name']
                tg_text = time + ' ' + name + ' ' + last_name + ': ' + text
                requests.post(url + "sendMessage", data={'chat_id': -255631997,
                                                         'text': tg_text})
                if text == 'начать':
                    api.messages.send(peer_id=update['object']['user_id'],
                                      message='Здравствуйте, %s, это бот'% name,
                                      keyboard=vk_keyboard)
                elif text == 'узнать дату':
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
                elif text == 'оплата через сбербанк онлайн':
                    api.messages.send(
                        peer_id=update['object']['user_id'],
                        message=sber)
                elif '10.10.' in text and update['object']['user_id'] in users:
                    ip = text
                    date = get_date(ip)
                    if date != '':
                        id = update['object']['user_id']
                        message = return_date + date
                        users.remove(update['object']['user_id'])
                        save_matching(id, ip)
                        api.messages.send(peer_id=update['object']['user_id'],
                                          message=message)
                    else:
                        api.messages.send(peer_id=update['object']['user_id'],
                                          message=no_ip)
                elif text == 'есть ли проблемы со связью':
                    if ping('194.105.212.27'):
                        time.sleep(3)
                        api.messages.send(
                            peer_id=update['object']['user_id'],
                            message='Всё норм! Проблем нет!')
                    else:
                        time.sleep(3)
                        api.messages.send(
                            peer_id=update['object']['user_id'],
                            message='Есть проблемка!')
    ts = longPoll['ts']
