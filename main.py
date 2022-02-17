from server import Server
import os

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
my_subj_dict = {"веб": 0, "web": 0, "архитектура ис": 1, "архитектура": 1, "ис": 1, "тсит": 2,
                "телекоммуникационные системы и технологии": 2}
my_namesofsubjs = ["веб", "архитектура ис", "телекоммуникационные системы и технологии"]
my_slovechki = {'!спасибо': 'пожалуста!!!!!!!!!!!!',
             '!прости': 'пососи',
             'мой.': 'факт!',
             'наш.': 'наш максимально!',
             'наш)': 'наш максимально!',
             'мой)': 'факт!',
             '!отчислить диму': 'дим димович димыч отчислен с позором😤',
             '!сайт': 'https://usachova.github.io/ITMO-WEB/',
             '!стасик': 'клоун + уебан'}


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
