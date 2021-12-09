import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import random
import os
from datetime import datetime, date

from my_queue import MyQueue


class Server:
    def __init__(self, token, group_id):
        self.vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.vk_session, group_id)
        self.vk = self.vk_session.get_api()

    def get_name(self, event):
        user_get = self.vk.users.get(user_ids=str(event.object.from_id))
        full_name = user_get[0]['first_name'] + " " + user_get[0]['last_name']
        return full_name

    def send_mes_group(self):
        pass

    def send_img_group(self):
        pass

    def send_mes_user(self, user_id, message, keyboard=None):
        post = {
            "user_id": user_id,
            "message": message,
            "random_id": 0
        }
        if keyboard is not None:
            post["keyboard"] = open(keyboard, "r", encoding="UTF-8").read()
        self.vk_session.method("messages.send", post)

    def start(self, subjects, subj_dict, namesofsubjs, slovechki):
        queue = MyQueue(subjects, subj_dict, namesofsubjs, slovechki)
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_chat:
                    text = event.object['text'].lower()
                    if queue.check_words(text):
                        mes = 'чево'
                        name = self.get_name(event)

                        if '!запись' in text:
                            mes = queue.record(text, name, mes)

                        if '!очередь' in text:
                            mes = queue.show_queue(text, mes)

                        if '!очистить' in text:
                            mes = queue.clear_queue(text, mes)

                        if '!удалиться' in text:
                            mes = queue.remove_from_queue(text, name, mes)

                        if '!дима' in text:
                            l = text.split()[1:]
                            if l:
                                if l[0] == 'не':
                                    f = open('prikol/dima.txt', 'r')
                                    last_date_str = f.readline()
                                    last_date = [int(x) for x in last_date_str.rstrip().split('-')]
                                    record = int(f.readline().rstrip().split(" ")[1])
                                    cnt = datetime.today().date() - date(last_date[0], last_date[1], last_date[2])
                                    mes = 'опять?..😢 \n дней без димы в вузе: ' + str(cnt.days).split()[0] + '..😵'
                                    f.close()
                                    if int(cnt.days) > record:
                                        f = open('prikol/dima.txt', 'w')
                                        f.write(last_date_str + 'рекорд: ' + str(cnt.days))
                                        f.close()
                                elif l[0] == 'пришёл':
                                    f = open('prikol/dima.txt', 'r')
                                    last_date = f.readline().rstrip()
                                    record = f.readline()
                                    f.close()
                                    f = open('prikol/dima.txt', 'w')
                                    f.write(str(datetime.today().date()) + '\n' + record)
                                    mes = 'во дела😳🤯 \n дней без димы в вузе: 0'
                                    f.close()
                                elif l[0] == 'рекорд':
                                    f = open('prikol/dima.txt', 'r')
                                    last_date = f.readline().rstrip()
                                    record = f.readline().rstrip().split(" ")[1]
                                    mes = 'рекорд дней без димы в вузе: ' + record + '..😤'
                                    f.close()
                            else:
                                mes = 'клоун'

                        for slov in queue.slovechki:
                            if slov in text:
                                mes = queue.slovechki[slov]

                        if '!тейлор' in text:
                            dir_name = 'taylor/'
                            taylor_list = os.listdir(dir_name)
                            upload = vk_api.VkUpload(self.vk)
                            photo = upload.photo_messages(
                                dir_name + taylor_list[random.randint(0, len(taylor_list) - 1)])
                            owner_id = photo[0]['owner_id']
                            photo_id = photo[0]['id']
                            access_key = photo[0]['access_key']
                            attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                            self.vk.messages.send(
                                key=('0578ac1069eec95d993b7d9b479e82d61829fa26'),
                                server=('https://lp.vk.com/wh200850856'),
                                ts=('1'),
                                random_id=get_random_id(),
                                message="",
                                attachment=attachment,
                                chat_id=event.chat_id
                            )
                            continue

                        if '!!очиститьвсё' in text:
                            mes = queue.remove_all()

                        if '!!смотретьвсё' in text:
                            mes = queue.show_all()

                        if '!команды' in text:
                            f = open('text_files/commands.txt', 'r')
                            mes = ''.join(f.readlines())
                            f.close()

                        self.vk.messages.send(
                            key=('0578ac1069eec95d993b7d9b479e82d61829fa26'),
                            server=('https://lp.vk.com/wh200850856'),
                            ts=('1'),
                            random_id=get_random_id(),
                            message=mes,
                            chat_id=event.chat_id
                        )

                elif event.from_user:
                    text = event.object['text'].lower()
                    user_id = event.object.peer_id
                    if '!начать' in text:
                        self.send_mes_user(user_id, "вы студент или преподаватель?", "keyboards/keyboard_who.json")
                    elif 'студент' in text:
                        self.send_mes_user(user_id, "выберите действие", "keyboards/keyboard_student.json")
                    elif 'преподаватель' in text:
                        self.send_mes_user(user_id, "выберите действие", "keyboards/keyboard_teacher.json")
                    elif 'добавить слоты' in text:
                        self.send_mes_user(user_id, "..", "keyboards/keyboard_none.json")
