from server import Server

my_token = '828d15350ed7aabdb944a2defc9f780bc8b0ed16ddaf94f97e2a79574e953cbeb586c460709098852f6fd'
my_group_id = '200850856'

# my_subjects = ["subjs/web", "subjs/linux", "subjs/primat", "subjs/uml", "subjs/ml"]
# my_subj_dict = {"веб": 0, "web": 0, "линукс": 1, "linux": 1, "примат": 2, "uml": 3, "юмл": 3, "ml": 4, "мл": 4}
# my_namesofsubjs = ["веб", "линукс", "примат", "юмл", "мл"]
my_subjects = ["subjs/web", "subjs/archIS", "subjs/TSIT"]
my_subj_dict = {"веб": 0, "web": 0, "архитектура ис": 1, "архитектура": 1, "ис": 1, "тсит": 2,
                "телекоммуникационные системы и технологии": 2}
my_namesofsubjs = ["веб", "архитектура ис", "телекоммуникационные системы и технологии"]
my_slovechki = {'!спасибо': 'пожалуста!!!!!!!!!!!!',
             '!прости': 'пососи',
             'мой.': 'факт!',
             'наш.': 'наш максимально!',
             'наш)': 'наш максимально!',
             'мой)': 'факт!',
             '!коля': '1С+++++ монстррр',
             '!отчислить диму': 'дим димович димыч отчислен с позором😤',
             '!сайт': 'https://usachova.github.io/ITMO-WEB/'}

my_server = Server(my_token, my_group_id)
my_server.start(my_subjects, my_subj_dict, my_namesofsubjs, my_slovechki)


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
