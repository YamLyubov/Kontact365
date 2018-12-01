import xml.etree.ElementTree as etr
import json


def get_date(ip):
    tree = etr.parse('UsersTest.xml')
    root = tree.getroot()
    for elem in root:
        current_ip = elem.attrib['UserIPAddr']
        print(current_ip)
        if current_ip == ip:
            preresult = elem.attrib['Date2']
            result = preresult[8:10] + '.' \
                     + preresult[5:7] + '.' \
                     + preresult[:4]
            return result
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
    [
    get_button(label="Узнать дату", color='positive')
    ]
    ]
}
vk_keyboard = json.dumps(vk_keyboard, ensure_ascii=False).encode('utf-8')
vk_keyboard = str(vk_keyboard.decode('utf-8'))