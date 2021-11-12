import random
import os
import vk_api
from vk_api.utils import get_random_id
from datetime import datetime, date
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk_session = vk_api.VkApi(token='828d15350ed7aabdb944a2defc9f780bc8b0ed16ddaf94f97e2a79574e953cbeb586c460709098852f6fd')
longpoll = VkBotLongPoll(vk_session, '200850856')
vk = vk_session.get_api()

subjects = ["subjs/web", "subjs/linux", "subjs/primat", "subjs/uml", "subjs/ml"]
subj_dict = {"веб": 0, "web": 0, "линукс": 1, "linux": 1, "примат": 2, "uml": 3, "юмл": 3, "ml": 4, "мл": 4}
namesofsubjs = ["веб", "линукс", "примат", "юмл", "мл"]
slovechki = {'!спасибо': 'пожалуста!!!!!!!!!!!!',
             '!прости': 'пососи',
             'мой.': 'факт!',
             'наш.': 'наш максимально!',
             'наш)': 'наш максимально!',
             'мой)': 'факт!',
             '!коля': '1С+++++ монстррр',
             '!отчислить диму': 'дим димович димыч отчислен с позором😤',
             '!сайт': 'https://usachova.github.io/ITMO-WEB/'}


def read_list_from_file(filename):
    list1, list2 = [], []
    f = open(filename + '.txt', 'r')
    is_first_part = True
    for line in f:
        if line == "...\n":
            is_first_part = False
            continue
        if is_first_part:
            list1.append(line)
        else:
            list2.append(line)
    f.close()
    return list1, list2


def update_file(filename, list1, list2):
    f = open(filename + '.txt', 'w')
    for line in list1:
        f.write(line)
    f.write("...\n")
    for line in list2:
        f.write(line)
    f.close()


def write_queue(list1, list2, s):
    for line in enumerate(list1):
        s += str(line[0] + 1) + '. ' + line[1]
    if list2:
        s += '...\n'
        for line in enumerate(list2):
            s += 'n-' + str(len(list2) - line[0] - 1) + '. ' + line[1]
    return s


def get_name():
    user_get = vk.users.get(user_ids=str(event.object.from_id))
    full_name = user_get[0]['first_name'] + " " + user_get[0]['last_name']
    return full_name


def check_words(msg):
    words = ['!очистить', '!запись', '!удалиться', '!очередь ', '!дима', '!тейлор', '!команды']
    tests_commands = ['!!очиститьвсё', '!!смотретьвсё']
    words += tests_commands
    words += slovechki.keys()
    for word in words:
        if word in msg:
            return True
    return False


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.object['text'].lower()
        if check_words(text) and event.from_chat:
            mes = 'чево'

            if '!запись' in text:
                to_first_list = True
                l = text.split()[1:]
                if l and l[0] == 'последним':
                    l = l[1:]
                    to_first_list = False

                if l and l[0] in subj_dict:
                    number = subj_dict[l[0]]

                    listFirstPart, listSecondPart = read_list_from_file(subjects[number])

                    if listFirstPart.count(get_name() + '\n') or listSecondPart.count(get_name() + '\n'):
                        mes = 'вы уже записаны в очередь на ' + namesofsubjs[number] + ' !'
                    else:
                        if to_first_list:
                            listFirstPart.append(get_name() + '\n')
                            mes = 'вы добавлены в очередь на ' + namesofsubjs[number]
                        else:
                            listSecondPart.reverse()
                            listSecondPart.append(get_name() + '\n')
                            listSecondPart.reverse()
                            mes = 'вы добавлены в очередь на ' + namesofsubjs[number] + ' последним'

                    update_file(subjects[number], listFirstPart, listSecondPart)

            if '!очередь' in text:
                l = text.split()[1:]
                if l and l[0] in subj_dict:
                    number = subj_dict[l[0]]
                    listFirstPart, listSecondPart = read_list_from_file(subjects[number])
                    mes = 'пожилая очередь на ' + namesofsubjs[number] + ':\n'
                    mes = write_queue(listFirstPart, listSecondPart, mes)

            if '!очистить' in text:
                l = text.split()[1:]
                if l and l[0] in subj_dict:
                    number = subj_dict[l[0]]
                    listFirstPart, listSecondPart = read_list_from_file(subjects[number])
                    listFirstPart.clear()
                    listSecondPart.clear()
                    mes = 'очередь на ' + namesofsubjs[number] + ' очищена'
                    update_file(subjects[number], listFirstPart, listSecondPart)

            if '!удалиться' in text:
                l = text.split()[1:]
                if l and l[0] in subj_dict:
                    number = subj_dict[l[0]]
                    listFirstPart, listSecondPart = read_list_from_file(subjects[number])
                    if listFirstPart.count(get_name() + '\n'):
                        listFirstPart.remove(get_name() + '\n')
                    if listSecondPart.count(get_name() + '\n'):
                        listSecondPart.remove(get_name() + '\n')
                    mes = 'вы удалены из очереди на ' + namesofsubjs[number]
                    update_file(subjects[number], listFirstPart, listSecondPart)

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

            for slov in slovechki:
                if slov in text:
                    mes = slovechki[slov]

            if '!тейлор' in text:
                dir_name = 'taylor/'
                taylor_list = os.listdir(dir_name)
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages(dir_name + taylor_list[random.randint(0, len(taylor_list) - 1)])
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(
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
                mes = ''
                for subj in subjects:
                    listFirstPart, listSecondPart = read_list_from_file(subj)
                    listFirstPart.clear()
                    listSecondPart.clear()
                    mes += 'очередь на ' + subj + ' очищена\n'
                    update_file(subj, listFirstPart, listSecondPart)

            if '!!смотретьвсё' in text:
                mes = ''
                for subj in subjects:
                    listFirstPart, listSecondPart = read_list_from_file(subj)
                    mes += 'пожилая очередь на ' + subj + ':\n'
                    mes = write_queue(listFirstPart, listSecondPart, mes)

            if '!команды' in text:
                f = open('text_files/commands.txt', 'r')
                mes = ''.join(f.readlines())
                f.close()

            vk.messages.send(
                key=('0578ac1069eec95d993b7d9b479e82d61829fa26'),
                server=('https://lp.vk.com/wh200850856'),
                ts=('1'),
                random_id=get_random_id(),
                message=mes,
                chat_id=event.chat_id
            )


# Automatically launch when terminating (for Heroku)
def thread_function():
    while True:
        try:
            time.sleep(1200)
        except:
            pass


if __name__ == "__main__":
    x1 = threading.Thread(target=thread_function, args=())
    x1.start()
