import vk
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

vk_session = vk_api.VkApi(token='..')

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

longpoll = VkBotLongPoll(vk_session, '..')
vk = vk_session.get_api()
from vk_api.longpoll import VkLongPoll, VkEventType


def UpdList(filename, flag1, flag2):
    listto = []
    f = open(filename + '.txt', 'r')
    for line in f:
        if (flag1 == flag2 and line != "...\n"):
            listto.append(line)
        if (line == "...\n"):
            flag1 = 1
    return listto


def UpdFile(filename, listto, flag):
    f = open(filename + '.txt', flag)
    if flag == 'a':
        f.write("...\n")
    for i in listto:
        f.write(i)


def GetName():
    vk = vk_session.get_api()
    id = str(event.object.from_id)
    user_get = vk.users.get(user_ids=(id))
    user_get = user_get[0]
    first_name = user_get['first_name']
    last_name = user_get['last_name']
    full_name = first_name + " " + last_name
    return full_name


def WriteLists(lst, list_last):
    s = ''
    for i in range(len(lst)):
        s += str(i + 1) + '. '
        s += lst[i]
    if len(list_last):
        s += '...\n'
    for i in range(len(list_last)):
        s += 'n-' + str(len(list_last) - i - 1) + '. '
        s += list_last[i]
    return s

lists = [[], [], []]
lists_last = [[], [], []]
subjects = ["subj1", "subj2", "fizeka"]
truenamesofsubjs = ["виндовс", "исрпо", "физика"]
namesofsubjs = ["виндовс", "исрпо", "повешение"]

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if '!прости' in str(event) or '!спасибо' in str(event) or '!очистить' in str(event) or '!запись' in str(event) or '!удалиться' in str(event) or '!очередь ' in str(event) or 'мой.' in str(event) or 'наш.' in str(event) or 'наш)' in str(event) or 'мой)' in str(event):
            if event.from_chat:
                mes = 'чево'
                for i in range(len(lists)):
                    lists[i] = UpdList(subjects[i], 0, 0)
                    lists_last[i] = UpdList(subjects[i], 0, 1)
                number = -1

                if '!спасибо' in str(event):
                    mes = 'пожалуста!!!!!!!!!!!!'

                if '!прости' in str(event):
                    mes = 'пососи'

                if '!очистить' in str(event):
                    for i in range(len(truenamesofsubjs)):
                        if '!очистить ' + truenamesofsubjs[i] in str(event):
                            number = i
                            break
                    if number != -1:
                        lists[number].clear()
                        lists_last[number].clear()
                        mes = 'очередь на ' + namesofsubjs[number] + ' очищена'

                if '!запись' in str(event):
                    for i in range(len(truenamesofsubjs)):
                        if '!запись ' + truenamesofsubjs[i] in str(event):
                            number = i
                            break
                    if number != -1:
                        if lists[number].count(GetName() + '\n') or lists_last[number].count(GetName() + '\n'):
                            mes = 'вы уже записаны в очередь на ' + namesofsubjs[number] + ' !'
                        else:
                            lists[number].append(GetName() + '\n')
                            mes = 'вы добавлены в очередь на ' + namesofsubjs[number]

                if '!запись последним' in str(event):
                    for i in range(len(truenamesofsubjs)):
                        if '!запись последним ' + truenamesofsubjs[i] in str(event):
                            number = i
                            break
                    if number != -1:
                        if lists[number].count(GetName() + '\n') or lists_last[number].count(GetName() + '\n'):
                            mes = 'вы уже записаны в очередь на ' + namesofsubjs[number] + '!!'
                        else:
                            lists_last[number].reverse()
                            lists_last[number].append(GetName() + '\n')
                            lists_last[number].reverse()
                            mes = 'вы добавлены в очередь на ' + namesofsubjs[number] + ' последним'

                if '!удалиться' in str(event):
                    for i in range(len(truenamesofsubjs)):
                        if '!удалиться' + truenamesofsubjs[i] in str(event):
                            number = i
                            break
                    if number != -1:
                        if lists[number].count(GetName() + '\n'):
                            lists[number].remove(GetName() + '\n')
                        if lists_last[number].count(GetName() + '\n'):
                            lists_last[number].remove(GetName() + '\n')
                        mes = 'вы удалены из очереди на ' + namesofsubjs[number]

                if '!очередь ' in str(event):
                    for i in range(len(truenamesofsubjs)):
                        if '!очередь ' + truenamesofsubjs[i] in str(event):
                            number = i
                            break
                    if number != -1:
                        mes = 'пожилая очередь на ' + namesofsubjs[number] + ':\n'
                        mes += WriteLists(lists[number], lists_last[number])

                if 'мой.' in str(event) or 'наш.' in str(event) or 'наш)' in str(event) or 'мой)' in str(event):
                    mes = 'факт!'

                for i in range(len(lists)):
                    UpdFile(subjects[i], lists[i], 'w')
                    UpdFile(subjects[i], lists_last[i], 'a')

                vk.messages.send(
                    key=('..'),
                    server=('..'),
                    ts=('1'),
                    random_id=get_random_id(),
                    message=mes,
                    chat_id=event.chat_id
                )
