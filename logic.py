# -*- coding: utf-8 -*-
import codecs
import xml.etree.ElementTree as etr
import json
from os import system as system_call
import sys
'''
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

reload(sys)
sys.setdefaultencoding('utf-8')
'''

from platform import system as system_name
from os import system as system_call


def ping(host):
    parameters = "-n 1" if system_name().lower()=="windows" else "-c 1"
    return system_call("ping " + parameters + " " + host) == 0


def get_date(ip):
    files = ['Users19.xml', 'Users101.xml', 'Users61.xml']
    for file in files:
        tree = etr.parse(file)
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
