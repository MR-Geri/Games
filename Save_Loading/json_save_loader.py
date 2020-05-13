import json
from Code.Person import Data_pers
import os


def save(data_save):
    try:
        os.remove('Save_Loading/save.json')
    except:
        pass
    open('Save_Loading/save.json', 'tw').close()
    for pers in data_save.personalities:
        temp = [pers.name, pers.surname, pers.age, list(pers.special), list(pers.skills), list(pers.buff),
                list(pers.de_buff), pers.hp, pers.hunger, pers.water, pers.control, pers.stress,
                pers.left_arm, pers.right_arm, pers.back, pers.pockets]
        try:
            data = json.load(open('Save_Loading/save.json'))
        except:
            data = []
        data.append(temp)
        with open('Save_Loading/save.json', 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


def load():
    temp = json.load(open('Save_Loading/save.json'))
    data = Data_pers(len(temp), True)
    for pers in range(len(temp)):
        data.personalities[pers].name, data.personalities[pers].surname = temp[pers][0], temp[pers][1]
        data.personalities[pers].age = temp[pers][2]
        data.personalities[pers].special, data.personalities[pers].skills = set(temp[pers][3]), set(temp[pers][4])
        data.personalities[pers].buff, data.personalities[pers].de_buff = set(temp[pers][5]), set(temp[pers][6])
        data.personalities[pers].hp = temp[pers][7]
        data.personalities[pers].hunger, data.personalities[pers].water = temp[pers][8], temp[pers][9]
        data.personalities[pers].control, data.personalities[pers].stress = temp[pers][10], temp[pers][11]
        data.personalities[pers].left_arm, data.personalities[pers].right_arm = temp[pers][12], temp[pers][13]
        data.personalities[pers].back, data.personalities[pers].pockets = temp[pers][14], temp[pers][15]
    return data
