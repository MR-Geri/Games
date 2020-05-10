def save(data_save):
    f = open('save.text', 'w')
    var = {'mom': data_save.mom, 'dad': data_save.dad, 'son': data_save.son, 'dau': data_save.dau}
    for pers in ['mom', 'dad', 'son', 'dau']:
        f.write(f'{var[pers].name}/{var[pers].surname}/{var[pers].age}/')
        f.write(f'{var[pers].special}/{var[pers].skills}/')
        f.write(f'{var[pers].buff}/{var[pers].de_buff}/')
        f.write(f'{var[pers].hp}/{var[pers].hunger}/{var[pers].water}/')
        f.write(f'{var[pers].control}/{var[pers].stress}//')
