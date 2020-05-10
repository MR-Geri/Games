from Code.Person import Data_pers, Action
from Save_Loading.save_loading import save, load


def home_screen():
    global persons
    text = input('new game/save game/load game\n')
    if text == 'new game':
        persons = Data_pers()
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


persons = None
home_screen()
print(persons)
