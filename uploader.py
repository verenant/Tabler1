from restraunt import Restraunt

from tablerObject import TablerObject
import json
import re

#Перевод координат в float
def prepareCoord(x):
    return float(x)

def prepareCheck(check):
    if check == "no_avg_check":
        return "no_avg_check"
    pos = check.index(" ")
    if pos < 0:
        return int(check)
    return int(check[:pos])

def prepareSchedule(timetable):
    # Подготовка расписания делаем паттерн на цифр+буква (идеальный вариант)
    # затем проходим по расписанию и берем разбиение до следующего изменения расписания
    # после заполнения списка week его надо будет разбить на словарь с началом рабочего дня и концом рабочего дня
    pattern = r'\d+[А-Я]+'
    #pattern= r'[a-я][А-Я]+'

    week=[]
    # если изменение происходит в четверг. сделать и для других дней
    # циклом заполняем все дни с начала этапа и до конца этапа
    if timetable[3:5] == "чт" or timetable[3:5] == "ЧТ" or timetable[3:5] == "Чт":
        pos = 0
        for i in range(0,4):
            match = re.findall(pattern,timetable)
            if len(match) == 0:
                # особенный паттерн если работает до последнего гостя
                pattern = r'[a-я][А-Я]+'
                match = re.findall(pattern, timetable)
            pos = timetable.find(match[0])
            week.append(timetable[7:pos+1])
            pass
        timetable = timetable[pos+1:]
    elif timetable[3:5] == "ВС" or timetable[3:5] == "вс" or timetable[3:5] == "Вс":
        # циклом заполняем все дни с начала этапа и до конца этапа
        for i in range(0, 7):
            match = re.findall(pattern, timetable)
            pos = 0
            if len(match) == 0:
                pattern = r'[a-я][А-Я]+'
            match = re.findall(pattern, timetable)

            if len(match) > 0:
                pos = timetable.find(match[0])
                week.append(timetable[7:pos + 1])
            else:
                week.append(timetable[7:])
                pos = len(timetable)
            timetable = timetable[pos + 1:]
            pass


    pass

rest = Restraunt("","flamingo-3.json","",1)
tObj = TablerObject()
rest.avg_check = prepareCheck(rest.avg_check)
rest.lon = prepareCoord(rest.Coordinates[1])
rest.lat = prepareCoord(rest.Coordinates[0])
prepareSchedule(rest.timetable)





pass