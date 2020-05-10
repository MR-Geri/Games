from Code.Person import Data_pers


def save(data_save):
    f = open('Save_Loading/save.text', 'w')
    var = {'mom': data_save.mom, 'dad': data_save.dad, 'son': data_save.son, 'dau': data_save.dau}
    for pers in ['mom', 'dad', 'son', 'dau']:
        f.write(f'{var[pers].name}/{var[pers].surname}/{var[pers].age}/')
        for i in [var[pers].special, var[pers].skills, var[pers].buff, var[pers].de_buff]:
            temp = '|'.join(i)
            temp = 'NONE' if len(temp) == 0 else temp
            f.write(f'{temp}/')
        f.write(f'{var[pers].hp}/{var[pers].hunger}/{var[pers].water}/')
        f.write(f'{var[pers].control}/{var[pers].stress}//')
    f.close()


def load():
    data = Data_pers()
    var = {0: data.mom, 1: data.dad, 2: data.son, 3: data.dau}
    f = open('Save_Loading/save.text', 'r')
    data_load = f.read().split('//')
    for line in range(4):
        data_pers = data_load[line].split('/')
        var[line].name, var[line].surname, var[line].age = data_pers[0], data_pers[1], data_pers[2]
        t = [var[line].special, var[line].skills, var[line].buff, var[line].de_buff]
        for i in range(4):
            t[i] = set(data_pers[i + 3].split('|')) if data_pers[i + 3] != 'NONE' else set()
        var[line].hp, var[line].hunger, var[line].water = data_pers[7], data_pers[8], data_pers[9]
        var[line].control, var[line].stress = data_pers[10], data_pers[11]
    f.close()
    return data
