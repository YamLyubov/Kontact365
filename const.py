# -*- coding: utf-8 -*-
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

from logic import get_button
import json

vk_token = '705848ce54dd5994b7a60f04badbd790bf865ae217b1960acee583641c07faeff74da562a1775f610f4df'
tg_token = '750626699:AAELeCDkbY3exPYhKk7nhw2aSXUkna2S-dA'
wb_id = -255631997
nasa_id = -193913096
group_id = 129298566
vk_keyboard = {
    "one_time": False,
    "buttons": [
     [get_button(label="📅 Узнать дату окончания оплаты 📍", color='primary')],
     [get_button(label="💳 Оплата через Сбербанк ОнЛ@йн 💰", color='positive')],
     [get_button(label="🏄🌏 Есть Интернет? 🚀🌖", color='primary')],
     [get_button(label="Призвать живого👦оператора", color='primary')],
     [get_button(label="⏳ обновить клавиатуру 💡", color='default')]
     ]
}
vk_keyboard = json.dumps(vk_keyboard, ensure_ascii=False).encode('utf-8')
vk_keyboard = str(vk_keyboard.decode('utf-8'))
