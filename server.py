import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import random
import os
from datetime import datetime, date

from my_queue import MyQueue
from queue_manager import QueueManager


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
        manager = QueueManager()
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
                    last_action = ''
                    last_subj = ''
                    last_user = ''
                    if '!начать' in text:
                        self.send_mes_user(user_id, "вы студент или преподаватель?", "keyboards/keyboard_who.json")
                    elif 'студент' == text:
                        self.send_mes_user(user_id, "выберите действие", "keyboards/keyboard_student.json")
                        last_user = 'студент'
                    elif 'преподаватель' == text:
                        self.send_mes_user(user_id, "выберите действие", "keyboards/keyboard_teacher.json")
                        last_user = 'преподаватель'
                    elif 'добавить слоты' == text or 'очередь на предмет' == text or 'очистить очередь' == text\
                            or 'записаться на сдачу' == text or 'удалить себя из очереди' == text\
                            or 'список своих слотов' == text:
                        self.send_mes_user(user_id, "выберите предмет", "keyboards/keyboard_subjects.json")
                        last_action = text
                    elif text == 'uml' or text == 'ml':
                        if last_action == 'добавить слоты':
                            mes = "перечислите слоты в формате '!слоты: 14:20 14:40'"
                            self.send_mes_user(user_id, mes, "keyboards/keyboard_none.json")
                            last_subj = text
                        elif last_action == 'очередь на предмет':
                            mes = manager.show_the_queue(text)
                            if last_user == 'преподаватель':
                                self.send_mes_user(user_id, mes, "keyboards/keyboard_teacher.json")
                            elif last_user == 'студент':
                                self.send_mes_user(user_id, mes, "keyboards/keyboard_student.json")
                        elif last_action == 'очистить очередь':
                            manager.clear_queue(text)
                            self.send_mes_user(user_id, "очередь очищена", "keyboards/keyboard_teacher.json")
                        elif last_action == 'записаться на сдачу':
                            name = self.get_name(event)
                            manager.add_to_queue(text, name)
                            self.send_mes_user(user_id, "вы записаны на сдачу", "keyboards/keyboard_student.json")
                        elif last_action == 'удалить себя из очереди':
                            name = self.get_name(event)
                            manager.remove_student_from_queue(text, name)
                            self.send_mes_user(user_id, "вы удалены из очереди", "keyboards/keyboard_student.json")
                        elif last_action == 'список своих слотов':
                            name = self.get_name(event)
                            mes = manager.show_list_of_slots(text, name)
                            self.send_mes_user(user_id, mes, "keyboards/keyboard_student.json")
                    elif '!слоты:' in text:
                        manager.add_slots(text, last_subj)
                        self.send_mes_user(user_id, "слоты записаны", "keyboards/keyboard_teacher.json")
