from Code.Person import Data_pers


def save(data_save):
    f = open('Save_Loading/save.text', 'w')
    for pers in data_save.personalities:
        f.write(f'{pers.name}/{pers.surname}/{pers.age}/')
        for i in [pers.special, pers.skills, pers.buff, pers.de_buff]:
            temp = '|'.join(i)
            temp = 'NONE' if len(temp) == 0 else temp
            f.write(f'{temp}/')
        f.write(f'{pers.hp}/{pers.hunger}/{pers.water}/')
        f.write(f'{pers.control}/{pers.stress}/')
        f.write(f'{pers.left_arm}/{pers.right_arm}/{pers.back}/')
        f.write('|'.join([i if i is not None else 'None' for i in pers.pockets]))
        f.write(f'//')
    f.close()


def load():
    f = open('Save_Loading/save.text', 'r')
    data_load = f.read().split('//')
    data = Data_pers(len(data_load[:-1]))
    for line in range(len(data_load[:-1])):
        data_pers = data_load[line].split('/')
        data.personalities[line].name, data.personalities[line].surname = data_pers[0], data_pers[1]
        data.personalities[line].age = data_pers[2]
        t = [data.personalities[line].special, data.personalities[line].skills,
             data.personalities[line].buff, data.personalities[line].de_buff]
        for i in range(4):
            t[i] = set(data_pers[i + 3].split('|')) if data_pers[i + 3] != 'NONE' else set()
        data.personalities[line].hp, data.personalities[line].hunger = data_pers[7], data_pers[8]
        data.personalities[line].water = data_pers[9]
        data.personalities[line].control, data.personalities[line].stress = data_pers[10], data_pers[11]
        data.personalities[line].left_arm = None if data_pers[12] == 'None' else data_pers[12]
        data.personalities[line].right_arm = None if data_pers[13] == 'None' else data_pers[13]
        data.personalities[line].back = None if data_pers[14] == 'None' else data_pers[14]
        for i in range(4):
            data.personalities[line].pockets[i] = None if data_pers[15].split('|')[i] == 'None' else \
                data_pers[15].split('|')[i]
    f.close()
    return data
