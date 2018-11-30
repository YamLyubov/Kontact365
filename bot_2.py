import vk
from requests import *
from const import vk_keybord
from logic import get_date, save_matching

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
                if 'привет' in text:
                    name = api.users.get(user_ids=update['object']['user_id'])[0]['first_name']
                    api.messages.send(peer_id=update['object']['user_id'],
                                      message='Привет, %s ' % name)
                if 'ip' in text:
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
