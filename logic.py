import xml.etree.ElementTree as etr
import json


vk_token = '705848ce54dd5994b7a60f04badbd790bf865ae217b1960acee583641c07faeff74da562a1775f610f4df'
tg_token = '750626699:AAELeCDkbY3exPYhKk7nhw2aSXUkna2S-dA'
def get_date(ip):
    tree = etr.parse('UsersTest.xml')
    root = tree.getroot()
    for elem in root:
        current_ip = elem.attrib['UserIPAddr']
        if current_ip == ip:
            try:
                preresult = elem.attrib['Date2']
                result = preresult[8:10] + '.' \
                        + preresult[5:7] + '.' \
                        + preresult[:4]
                return result
            except KeyError:
                return ''
    return ''


def save_matching(id, ip):
    with open('IP.json', 'r+', encoding='utf-8') as IP:
        data = json.load(IP)
        data[id] = ip
        IP.seek(0)
        json.dump(data, IP)
        IP.truncate()


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


vk_keyboard = {
    "one_time": False,
    "buttons": [
     [get_button(label="Узнать дату", color='positive')],
     [get_button(label="Оплата через сбербанк онлайн", color='primary')],
     [get_button(label="Есть ли проблемы со связью", color='primary')]
     ]
}
vk_keyboard = json.dumps(vk_keyboard, ensure_ascii=False).encode('utf-8')
vk_keyboard = str(vk_keyboard.decode('utf-8'))