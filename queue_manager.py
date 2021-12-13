class QueueManager:
    def __init__(self, subjects=None):
        if subjects is None:
            subjects = ['uml', 'ml']
        self.subjects = subjects
        self.filenames = {}
        for subject in subjects:
            self.filenames[subject] = 'subjs/' + subject + '_.txt'

    def show_slots(self, subject):
        mes = ""
        f = open(self.filenames[subject], 'r')
        for line in f:
            slot = line.split(' ', 1)
            if len(slot) == 1:
                mes += line
        f.close()
        if mes == "":
            return "список пуст"
        return mes

    def add_to_queue(self, subject, name, text):
        slot = text.split()[1]
        f = open(self.filenames[subject], 'r')
        lines = f.readlines()
        f = open(self.filenames[subject], 'w')
        for line in lines:
            if line.split()[0] == slot:
                f.write(slot + ' ' + name + '\n')
            else:
                f.write(line)
        f.close()

    def remove_student_from_queue(self, subject, name):
        f = open(self.filenames[subject], 'r')
        lines = f.readlines()
        f = open(self.filenames[subject], 'w')
        for line in lines:
            line_ = line.split(' ', 1)
            if len(line_) > 1 and line_[1] == name + '\n':
                f.write(line_[0] + '\n')
            else:
                f.write(line)
        f.close()

    def clear_queue(self, subject):
        f = open(self.filenames[subject], 'w')
        f.close()

    def add_slots(self, text, subject):
        slots = text.split()[1:]
        f = open(self.filenames[subject], 'a')
        for slot in slots:
            f.write(slot + '\n')
        f.close()

    def show_list_of_slots(self, name):
        mes = ""
        for subject in self.subjects:
            f = open(self.filenames[subject], 'r')
            for line in f:
                line_ = line.split(' ', 1)
                if len(line_) > 1 and line_[1] == name + '\n':
                    mes += subject + ' ' + line
            f.close()
        if mes == "":
            return "список пуст"
        return mes

    def show_the_queue(self, subject):
        mes = ""
        for subject in self.subjects:
            f = open(self.filenames[subject], 'r')
            for line in f:
                slot = line.split(' ', 1)
                if len(slot) != 1:
                    mes += line
            f.close()
        if mes == "":
            return "список пуст"
        return mes
