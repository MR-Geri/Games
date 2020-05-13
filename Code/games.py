from Code.Person import Data_pers, Action
from Save_Loading.json_save_loader import save, load
import json


def home_screen(flag=None):
    global persons
    text = input('new game/save game/load game/out\n') if flag is None else flag
    if text == 'new game':
        persons = Data_pers() if flag is None else Data_pers(1)
    elif text == 'save game':
        if persons is None:
            print('Игра не создана')
        else:
            save(persons)
            print('Игра сохранена.')
    elif text == 'load game':
        try:
            temp = json.load(open('Save_Loading/save.json'))
            persons = load()
            print('Игра загружена.')
        except:
            print('Нет сохранения.')
    elif text == 'out':
        print(persons)


def test():
    print(load())


def main():
    while True:
        home_screen()


if __name__ == '__main__':
    persons = None
    main()
