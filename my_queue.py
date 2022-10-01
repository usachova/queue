from vars import *
class MyQueue:
    def __init__(self, subjects, subj_dict, namesofsubjs, slovechki, tsit_num, tsit_people):
        self.subjects = subjects
        self.subj_dict = subj_dict
        self.namesofsubjs = namesofsubjs
        self.slovechki = slovechki
        self.tsit_num = tsit_num
        self.tsit_people = tsit_people

    def read_list_from_file(self, filename):
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

    def update_file(self, filename, list1, list2):
        f = open(filename + '.txt', 'w')
        for line in list1:
            f.write(line)
        f.write("...\n")
        for line in list2:
            f.write(line)
        f.close()

    def write_queue(self, list1, list2, s):
        for line in enumerate(list1):
            s += str(line[0] + 1) + '. ' + line[1]
        if list2:
            s += '...\n'
            for line in enumerate(list2):
                s += 'n-' + str(len(list2) - line[0] - 1) + '. ' + line[1]
        return s

    def check_words(self, msg):
        words = ['!очистить', '!запись', '!удалиться', '!очередь ', '!дима', '!тейлор', '!рашид', '!команды']
        tests_commands = ['!!очиститьвсё', '!!смотретьвсё']
        words += tests_commands
        words += self.slovechki.keys()
        for word in words:
            if word in msg:
                return True
        return False

    def record(self, text, name, mes):
        to_first_list = True
        l = text.split()[1:]
        if l and l[0] == 'последним':
            l = l[1:]
            to_first_list = False

        if l and l[0] in self.subj_dict:
            number = self.subj_dict[l[0]]

            # # тсит
            # if number == 2:
            #     name = self.tsit_num[self.tsit_people[name.split()[1]]]

            # if number == 1:
            #     name = self.tsit_num[self.tsit_people[name.split()[1]]]

            if number == 2:
                name = svi_num[svi_people[name.split()[1]]]

            listFirstPart, listSecondPart = self.read_list_from_file(self.subjects[number])

            if listFirstPart.count(name + '\n') or listSecondPart.count(name + '\n'):
                mes = 'вы уже записаны в очередь на ' + self.namesofsubjs[number] + ' !'
            else:
                if to_first_list:
                    listFirstPart.append(name + '\n')
                    mes = 'вы добавлены в очередь на ' + self.namesofsubjs[number]
                else:
                    listSecondPart.reverse()
                    listSecondPart.append(name + '\n')
                    listSecondPart.reverse()
                    mes = 'вы добавлены в очередь на ' + self.namesofsubjs[number] + ' последним'

            self.update_file(self.subjects[number], listFirstPart, listSecondPart)
        return mes

    def show_queue(self, text, mes):
        l = text.split()[1:]
        if l and l[0] in self.subj_dict:
            number = self.subj_dict[l[0]]
            listFirstPart, listSecondPart = self.read_list_from_file(self.subjects[number])
            mes = 'пожилая очередь на ' + self.namesofsubjs[number] + ':\n'
            mes = self.write_queue(listFirstPart, listSecondPart, mes)
        return mes

    def clear_queue(self, text, mes):
        l = text.split()[1:]
        if l and l[0] in self.subj_dict:
            number = self.subj_dict[l[0]]
            listFirstPart, listSecondPart = self.read_list_from_file(self.subjects[number])
            listFirstPart.clear()
            listSecondPart.clear()
            mes = 'очередь на ' + self.namesofsubjs[number] + ' очищена'
            self.update_file(self.subjects[number], listFirstPart, listSecondPart)
        return mes

    def remove_from_queue(self, text, name, mes):
        l = text.split()[1:]
        if l and l[0] in self.subj_dict:
            number = self.subj_dict[l[0]]

            # тсит
            if number == 2:
                name = self.tsit_num[self.tsit_people[name.split()[1]]]

            listFirstPart, listSecondPart = self.read_list_from_file(self.subjects[number])
            if listFirstPart.count(name + '\n'):
                listFirstPart.remove(name + '\n')
            if listSecondPart.count(name + '\n'):
                listSecondPart.remove(name + '\n')
            mes = 'вы удалены из очереди на ' + self.namesofsubjs[number]
            self.update_file(self.subjects[number], listFirstPart, listSecondPart)
        return mes

    def remove_all(self):
        mes = ''
        for subj in self.subjects:
            listFirstPart, listSecondPart = self.read_list_from_file(subj)
            listFirstPart.clear()
            listSecondPart.clear()
            mes += 'очередь на ' + subj + ' очищена\n'
            self.update_file(subj, listFirstPart, listSecondPart)
        return mes

    def show_all(self):
        mes = ''
        for subj in self.subjects:
            listFirstPart, listSecondPart = self.read_list_from_file(subj)
            mes += 'пожилая очередь на ' + subj + ':\n'
            mes = self.write_queue(listFirstPart, listSecondPart, mes)
        return mes