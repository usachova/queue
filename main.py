from server import Server
import os
from collections import defaultdict

if os.path.exists("secret.txt"):
    f = open("secret.txt", "r")
    my_token = f.readline()[:-1]
    my_group_id = f.readline()
    f.close()
else:
    my_token = os.environ.get("MY_TOKEN")
    my_group_id = os.environ.get("MY_GROUP_ID")

# my_subjects = ["subjs/web", "subjs/linux", "subjs/primat", "subjs/uml", "subjs/ml"]
# my_subj_dict = {"веб": 0, "web": 0, "линукс": 1, "linux": 1, "примат": 2, "uml": 3, "юмл": 3, "ml": 4, "мл": 4}
# my_namesofsubjs = ["веб", "линукс", "примат", "юмл", "мл"]
my_subjects = ["subjs/web", "subjs/archIS", "subjs/TSIT"]
my_subj_dict = {"веб": 0, "web": 0, "беб": 0, "архитектура ис": 1, "архитектура": 1, "ис": 1, "тсит": 2,
                "телекоммуникационные системы и технологии": 2, "сети": 2}
my_namesofsubjs = ["веб", "архитектура ис", "телекоммуникационные системы и технологии"]
my_slovechki = {'!спасибо': 'пожалуста!!!!!!!!!!!!',
             '!прости': 'пососи',
             'мой.': 'факт!',
             'наш.': 'наш максимально!',
             'наш)': 'наш максимально!',
             'мой)': 'факт!',
             '!отчислить диму': 'дим димович димыч отчислен с позором😤',
             '!сайт': 'https://usachova.github.io/ITMO-WEB/',
             '!удалиться из жизни': 'только после маши .'}


tsit_num = {1: "Сесин Сергей, Жуков Максим, Александр Великодный (М33081)",
            2: "Храповицкий Даниил, Усачёва Мария, Маслов Михаил",
            3: "Иванов Евгений, Иванов Анатолий (М33011), Шарифов Сардорбек",
            4: "Зябирова Алина, Федотенко Николай (M33122), Кукулиди Дмитрий (M33122)",
            5: "Тимофеев Захар, Чулков Руслан, Лещиков Дмитрий",
            6: "Галеев Абдерашид, Севастьянов Юрий, Шукшина Ирина",
            7: "Трутнев Севастьян, Кузьмук Павел",
            8: "Тарасов Денис, Гридинарь Николай",
            9: "Дымчикова Аюна, Казаков Никита, Деляну Кирилл (M33081)",
            10: "Зенович Артем, Мещерская Елизавета"
}
tsit_people = {"Сесин": 1, "Жуков": 1,
               "Храповицкий": 2, "Усачёва": 2, "Маслов": 2,
               "Иванов": 3, "Шарифов": 3,
               "Зябирова": 4, "Федотенко": 4,
               "Тимофеев": 5, "Чулков": 5, "Лещиков": 5,
               "Галеев": 6, "Лайтов": 6, "Шукшина": 6,
               "Трутнев": 7, "Кузьмук": 7,
               "Измайлова": 8, "Коперник": 8,
               "Алесанова": 9, "Казаков": 9,
               "Зенович": 10, "Мещерская": 10
}

my_server = Server(my_token, my_group_id)
my_server.start(my_subjects, my_subj_dict, my_namesofsubjs, my_slovechki, tsit_num, tsit_people)


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
