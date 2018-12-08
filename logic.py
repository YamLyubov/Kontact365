# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etr
import json
import sys
from platform import system as system_name
from os import system as system_call

reload(sys)
sys.setdefaultencoding('utf-8')

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
    with open('IP.json', 'r+') as IP:
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
