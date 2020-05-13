from Code.Person import Data_pers, Action
from Save_Loading.save_loading import save, load


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
        f = open('Save_Loading/save.text', 'r')
        if f.read() == '':
            print('Ошибка. Нет сохранения, начните новую игру.')
        else:
            persons = load()
            print('Игра загружена.')
        f.close()
    elif text == 'out':
        print(persons)


def test():
    home_screen('new game')
    home_screen('out')


def main():
    while True:
        home_screen()


if __name__ == '__main__':
    persons = None
    test()
