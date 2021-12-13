class QueueManager:
    def __init__(self, subjects=None):
        if subjects is None:
            subjects = ['uml', 'ml']
        self.subjects = subjects
        self.filenames = {}
        for subject in subjects:
            self.filenames[subject] = subject + '_.txt'

    def add_to_queue(self, subject):
        pass

    def remove_student_from_queue(self):
        pass

    def clear_queue(self, subject):
        f = open(self.filenames[subject], 'w')
        f.close()

    def add_slots(self, text, subject):
        slots = text.split()[1:]
        f = open(self.filenames[subject], 'a')
        for slot in slots:
            f.write(slot)
        f.close()

    def show_list_of_slots(self):
        pass

    def show_the_queue(self):
        pass
