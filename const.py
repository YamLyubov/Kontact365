# -*- coding: utf-8 -*-
from logic import get_button
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

vk_token = '705848ce54dd5994b7a60f04badbd790bf865ae217b1960acee583641c07faeff74da562a1775f610f4df'
tg_token = '750626699:AAELeCDkbY3exPYhKk7nhw2aSXUkna2S-dA'
wb_id = -255631997
nasa_id = -193913096
group_id = 129298566
vk_keyboard = {
    "one_time": False,
    "buttons": [
     [get_button(label="📅 Дата окончания оплаты", color='primary'),
      get_button(label="💳 Сбербанк ОнЛ@йн", color='positive')],
     [get_button(label="🏄🌏 Есть Интернет?", color='primary'),
      get_button(label="👦Вызов оператора", color='primary')],
     [get_button(label="⏳ обновить клавиатуру 💡", color='default')]
     ]
}
vk_keyboard = json.dumps(vk_keyboard, ensure_ascii=False).encode('utf-8')
vk_keyboard = str(vk_keyboard.decode('utf-8'))
