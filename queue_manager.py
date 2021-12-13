class SlotRegister:
    def __init__(self, subjects=None):
        self.listOfSlotsByIDs = []
        self.listOfSlotsBySubjects = []
        if subjects is None:
            subjects = ['uml', 'ml']
        self.subjects = subjects
        self.filenames = {}
        for subject in subjects:
            self.filenames[subject] = 'subjs/' + subject + '_.txt'

    def get_filename(self, subject):
        return self.filenames[subject]

    def get_subjects(self):
        return self.subjects


class Slot:
    def __init__(self, time='', student_name='', name_of_subject='', teachers_name='', is_occupied=False):
        self.time = time
        self.student_name = student_name
        self.name_of_subject = name_of_subject
        self.teachers_name = teachers_name
        self.is_occupied = is_occupied

    def to_string(self):
        if self.student_name == '':
            return self.time + '\n'
        return self.time + ' ' + self.student_name + '\n'

    def add_to_register(self):
        pass

    def remove_from_register(self):
        pass


class QueueManager:
    def __init__(self, subjects=None):
        self.slot_register = SlotRegister(subjects)

    def show_slots(self, subject):
        mes = ""
        filename = self.slot_register.get_filename(subject)
        f = open(filename, 'r')
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
        filename = self.slot_register.get_filename(subject)
        f = open(filename, 'r')
        lines = f.readlines()
        f = open(filename, 'w')
        for line in lines:
            if line.split()[0] == slot:
                slot_ = Slot(slot, name)
                f.write(slot_.to_string())
            else:
                f.write(line)
        f.close()

    def remove_student_from_queue(self, subject, name):
        filename = self.slot_register.get_filename(subject)
        f = open(filename, 'r')
        lines = f.readlines()
        f = open(filename, 'w')
        for line in lines:
            line_ = line.split(' ', 1)
            if len(line_) > 1 and line_[1] == name + '\n':
                slot_ = Slot(line_[0])
                f.write(slot_.to_string())
            else:
                f.write(line)
        f.close()

    def clear_queue(self, subject):
        filename = self.slot_register.get_filename(subject)
        f = open(filename, 'w')
        f.close()

    def add_slots(self, text, subject):
        filename = self.slot_register.get_filename(subject)
        slots = text.split()[1:]
        f = open(filename, 'a')
        for slot in slots:
            slot_ = Slot(slot)
            f.write(slot_.to_string())
        f.close()

    def show_list_of_slots(self, name):
        mes = ""
        subjects = self.slot_register.get_subjects()
        for subject in subjects:
            filename = self.slot_register.get_filename(subject)
            f = open(filename, 'r')
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
        filename = self.slot_register.get_filename(subject)
        f = open(filename, 'r')
        for line in f:
            slot = line.split(' ', 1)
            if len(slot) != 1:
                mes += line
        f.close()
        if mes == "":
            return "список пуст"
        return mes
