#!/usr/bin/python3
import os
import pickle
import vk_api
import random
import datetime
import time
import threading
from vk_api.longpoll import VkLongPoll,VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

#ЗАГРУЖАЕМ ТОКЕН
path = os.getcwd() +'/'
print(path)
token = open(path +'token').readline().rstrip()
print('\nToken:\t',token)
print('Variables creating...')
#СОЗДАЕМ ПЕРЕМЕННУЮ С ВРЕМЕННЫМИ ДАННЫМИ ПОЛЬЗОВАТЕЛЯ
idtemp = {'action':'intro','langs':{}}
#РЕДАКТИРОВАТЬ --> текст клавиатуры
chname, addlan, dellan = 'Я поменяль имя','Добавить язык','Удалить язык'
chlang, ediwor, delwor  = 'Очепятка в языке','Изменить слово','Удалить слово'
icmind = 'Я передумаль, Фиби=('
love,evol = 'Любовь-Love','Love-Любовь'
print('Keyboards creating...')
#СОЗДАЕМ КЛАВИАТУРУ СТОП
stopk = VkKeyboard(one_time=False)
stopk.add_button('Стоп!',color=VkKeyboardColor.NEGATIVE)
#СОЗДАЕМ КЛАВИАТУРУ ГЛАВНОГО МЕНЮ
adwords,shwords,chwords,edwords = 'Пополнить словарь','Покажи мой словарь','Проверь слова, Фиби!=)','Редактировать'
Mkeyboard = VkKeyboard(one_time=False)
Mkeyboard.add_button(adwords,color=VkKeyboardColor.POSITIVE)
Mkeyboard.add_button(shwords,color=VkKeyboardColor.POSITIVE)
Mkeyboard.add_line()
Mkeyboard.add_button(chwords,color=VkKeyboardColor.POSITIVE)
Mkeyboard.add_line()
Mkeyboard.add_button(edwords,color=VkKeyboardColor.NEGATIVE)
#СОЗДАЕМ КЛАВИАТУРУ МЕНЮ РЕДАКТИРОВАНИЯ
editk = VkKeyboard(one_time=False)
editk.add_button(chname,color=VkKeyboardColor.POSITIVE)
editk.add_line()
editk.add_button(addlan,color=VkKeyboardColor.POSITIVE)
editk.add_button(dellan,color=VkKeyboardColor.NEGATIVE)
editk.add_line()
editk.add_button(chlang,color=VkKeyboardColor.POSITIVE)
editk.add_line()
editk.add_button(adwords,color=VkKeyboardColor.POSITIVE)
editk.add_button(delwor,color=VkKeyboardColor.NEGATIVE)
editk.add_line()
editk.add_button(icmind,color=VkKeyboardColor.NEGATIVE)
#СОЗДАЕМ КЛАВИАТУРУ ВЫБОРА ТИПА ПРОВЕРКИ
chtkey = VkKeyboard(one_time=False)
chtkey.add_button(love,color=VkKeyboardColor.POSITIVE)
chtkey.add_line()
chtkey.add_button(evol,color=VkKeyboardColor.POSITIVE)
chtkey.add_line()
chtkey.add_button('Стоп!',color=VkKeyboardColor.NEGATIVE)
#СОЗДАЕМ КЛАВИАТУРУ ВЫБОРА СЛОВ ДЛЯ ПРОВЕРКИ
chtkey2 = VkKeyboard(one_time=False)
chtkey2.add_button('Все слова',color=VkKeyboardColor.POSITIVE)
chtkey2.add_line()
chtkey2.add_button('Последние n',color=VkKeyboardColor.POSITIVE)
chtkey2.add_line()
chtkey2.add_button('Стоп!',color=VkKeyboardColor.NEGATIVE)
print('Connecting...')
#ПОДКЛЮЧАЕМСЯ К VK
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
print('Function initialization...')

class WriteFirst:#СОЗДАЕМ ОТДЕЛЬНЫЙ ПОТОК ДЛЯ ФУНКЦИИ "ПИШУ ПЕРВОЙ"
    def __init__(self,interval = 3600):
        self.interval = interval
        thread = threading.Thread(target=self.chkTi,args=())
        thread.daemon = True
        thread.start()

    def chkTi(self):
        while True:
            try:
                wtf = pload('writefirst')
                print('LAST ACTIVITY DB LOADED')
                nowt = datetime.datetime.now()
                dtm = [nowt.month,nowt.day]
                if nowt.hour >=21:
                    for uid in wtf.keys():
                        if (abs(dtm[0]-wtf[uid][0])+abs(dtm[1]-wtf[uid][1]))>=1:
                            wtf[uid]=dtm
                            pdump('writefirst',wtf)
                            tempu = pload(uid)
                            tempu['%'], tempu['chkt'],tempu['chch'] = 0,1,'!!!ВСЕ!!!'
                            tempu['action'] = 'chwords1'
                            pdump(uid,tempu)
                            x = tempu['langs'][min(tempu['langs'])]
                            out = 'Мы не общались больше суток, %s! Я тебе больше не нужна?=(\nСыграем? Загадай число от 1 до %d'%(tempu['uname'],len(x))
                            newmes(uid,out,stopk)
            except:
                print('NO DB YET')
            time.sleep(self.interval)

def formdict(uid,idtemp, i=0,out =''): #ПОСТРОЕНИЕ МАССИВА СЛОВ ДЛЯ ОПРОСА
    try:
        idtemp['dict'] = []
        for language in idtemp['langs']:
            if idtemp['chch'] != '!!!ВСЕ!!!': language = idtemp['chch']
            for elem in enumerate(idtemp['langs'][language][::-1]):
                if i and i==elem[0]: break
                elem2 = elem[1][:]
                elem2.append(language)
                idtemp['dict'].append(elem2)
            if idtemp['chch'] != '!!!ВСЕ!!!':break
        #ПОДГОТОВКА К ИГРЕ И ФОРМИРОВАНИЕ ОТВЕТА
        if not i: out = 'Любишь сложнее, да, %s?\n'%idtemp['uname']
        random.shuffle(idtemp['dict'])
        idtemp['stlen'],idtemp['action'] = len(idtemp['dict']),'PLAYN'
        out += 'Я буду писать тебе слово, ты будешь писать ответ, мы подсчитаем процент правильных ответов вместе! Ты сможешь!)'
        out +='\nВсего слов: %s'%idtemp['stlen']
        newmes(uid,out,stopk)
        newmes(uid, 'Я начинаю: %s(%s)'%(idtemp['dict'][0][idtemp['chkt']],idtemp['dict'][0][2]) ,stopk)
    except:
        idtemp['action']='mainmenu'
        newmes(uid,'Oops... Broken x(',Mkeyboard)
    return idtemp

def formanswer(uid,message): #ФУНКЦИЯ ФОРМИРОВАНИЯ ОТВЕТОВ
    try:
        global idtemp
        print("\nUser ID: \t" + str(uid) +"\nUser message:\n" + message)
        #ПЫТАЕМСЯ ЗАГРУЗИТЬ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ С ЛОКАЛЬНОГО ХРАНИЛИЩА
        try: idtemp = pload(uid)
        except: pass
        #ОБНУЛЕНИЕ ИГРОВЫХ ПЕРЕМЕННЫХ
        if idtemp['action'] == 'mainmenu':
            idtemp['chkt'],idtemp['%'],idtemp['stlen'],idtemp['chch'] = 2,0,0,'NONE'
            idtemp['dict'] = []
        #ЗНАКОМСТВО
        if message.lower() in ['start','начать','привет']:
            idtemp['action'],idtemp['uid'] = 'intro0',uid
            out = ('Привет, меня зовут Фиби и я буду твоим персональным помощником в изучении языка. ' +
                    'Мы с тобой будем учить слова и с этого дня я от тебя не отцеплюсь! =)' +
                    'Я представилась, а как обращаться к тебе?)')
            newmes(uid,out)
        #ПОКАЖИ МОЙ СЛОВАРЬ
        elif message == shwords:
            out = 'Хорошо, вот твой словарь, %s:\n'%idtemp['uname']
            for lang in idtemp['langs'].keys():
                out+='\n'
                out += '%s:\n'%lang
                for word in idtemp['langs'][lang]:
                    out += '%s-%s\n'%(word[0],word[1])
            newmes(uid,out)
        #ПОПОЛНИТЬ СЛОВАРЬ
        elif message == adwords:
            idtemp['action'] = 'adwords'
            newmes(uid,'Окей, но всё по порядку, %s =) Какой язык?'%idtemp['uname'],buildkey(1,idtemp['langs']))
        #ПОПОЛНИТЬ СЛОВАРЬ|УДАЛИТЬ СЛОВАРЬ|ИЗМЕНИТЬ СЛОВАРЬ|ИЗМЕНИТЬ СЛОВО --> ВЫБОР СЛОВАРЯ
        elif (message in idtemp['langs'].keys() or message =='!!!ВСЕ!!!') and idtemp['action'] in ('adwords','dellan','chlang','chwords0'):
            #ПОПОЛНИТЬ
            if idtemp['action'] == 'adwords':
                res,temp = message,stopk
                out = 'Хорошо, отправляй мне по одному слову за сообщение, вот пример: Похмелье-Hang over. Не отделяй тире пробелами, пожалуйста=)'
            #УДАЛИТЬ
            elif idtemp['action'] == 'dellan':
                idtemp['langs'].pop(message)
                res,out,temp = 'mainmenu','Удалила =)',Mkeyboard
            #ИЗМЕНИТЬ
            elif idtemp['action'] == 'chlang':
                out,temp,res = 'На что меняем?',Mkeyboard,'chlang0'+message
            #ПРОВЕРКА
            elif idtemp['action'] == 'chwords0':
                out,res,temp = 'Замечательный выбор!','chwords1',chtkey2
                idtemp['chch'] = message
            idtemp['action'] = res
            newmes(uid,out,temp)
        #ПОПОЛНИТЬ СЛОВАРЬ| ПРОВЕРЬ МЕНЯ --> ВЫХОД В ГЛАВНОЕ МЕНЮ
        elif message in (icmind,'Стоп!') and idtemp['action'] in ('adwords','chwords','chwords0','chwords1','PLAYN','edwords0','dellan','chlang'):
            #ВЫХОД В ГЛАВНОЕ МЕНЮ
            if idtemp['action'] in ('adwords','chwords','edwords0'):
                res,out,temp = 'mainmenu','Окей, я готова двигаться дальше!=)',Mkeyboard
            #ВЫХОД В МЕНЮ РЕДАКТИРОВАНИЯ
            elif idtemp['action'] in ('dellan','chlang'):
                res,out,temp = 'edwords0','Ок, вернулись=)',editk
            #ПРОВЕРЬ МЕНЯ --> ВЫХОД В МЕНЮ ВЫБОРА ТИПА ПРОВЕРКИ
            elif idtemp['action'] == 'chwords0':
                res,out,temp = 'chwords','Ладно, шаг назад.',chtkey
            #ПРОВЕРЬ МЕНЯ --> ВЫХОД В МЕНЮ ВЫБОРА ЯЗЫКА
            elif idtemp['action'] == 'chwords1':
                res,out,temp = 'chwords0','Серьезно?=(',buildkey(0,idtemp['langs'])
            #ПРОВЕРЬ МЕНЯ -->ВЫХОД ИЗ ИГРЫ
            elif idtemp['action'] == 'PLAYN':
                res,out,temp = 'chwords1','Ладно.',chtkey2
            idtemp['action'] = res
            newmes(uid,out ,temp)
        #РЕДАКТИРОВАТЬ
        elif message == edwords:
            idtemp['action'] = 'edwords0'
            newmes(uid,'Что меняем, %s?'%idtemp['uname'],editk)
        #РЕДАКТИРОВАТЬ --> ПОМЕНЯЙ ИМЯ
        elif message == chname and idtemp['action'] == 'edwords0':
            idtemp['action'] = 'introO'
            newmes(uid,'Как теперь мне тебя называть?=)',Mkeyboard)
        #РЕДАКТИРОВАТЬ --> ДОБАВИТЬ ЯЗЫК
        elif message == addlan and idtemp['action'] == 'edwords0':
            idtemp['action'] = 'introI'
            out = ('Давай добавим, %s! '%idtemp['uname'] +
                    'Напиши пожалуйста каждый язык через пробел, например: Английский Испанский Японский')
            newmes(uid,out,Mkeyboard)
        #РЕДАКТИРОВАТЬ --> УДАЛИТЬ ЯЗЫК|ОПЕЧАТКА В НАЗВАНИИ ЯЗЫКА
        elif message in (dellan,chlang) and idtemp['action'] == 'edwords0':
            idtemp['action'] = 'dellan' if message == dellan else 'chlang'
            newmes(uid,'Какой язык удаляем?' if message == dellan else 'Какой язык изменяем, %s?'%idtemp['uname']
                    ,buildkey(1,idtemp['langs']))
        #РЕДАКТИРОВАТЬ --> УДАЛИТЬ СЛОВО
        elif message == delwor and idtemp['action'] == 'edwords0':
            idtemp['action'] = 'delwor'
            newmes(uid,'Хорошо, %s, что мне удалить? Напиши по примеру: Похмелье-Hang over'%idtemp['uname'],Mkeyboard)
        #ПРОВЕРЬ МЕНЯ
        elif message == chwords:
            idtemp['action'] = 'chwords'
            newmes(uid,'Ок, %s. Как реализуем проверку? Есть два варианта:\n1) Я пишу тебе слово, а ты мне перевод.(любовь-love)\n2) Я пишу перевод, а ты мне слово.(love-любовь).'%idtemp['uname'],chtkey)
        #ПРОВЕРЬ МЕНЯ --> ВЫБОР ЯЗЫКА
        elif message in (love,evol) and idtemp['action'] == 'chwords':
            idtemp['chkt'] = 0 if message==love else 1
            idtemp['action'] = 'chwords0'
            newmes(uid,'Какой язык?',buildkey(0,idtemp['langs']))
        #ПРОВЕРЬ МЕНЯ --> ВЫБОР КОЛ-ВА слов
        elif (message in ('Все слова','Последние n') or message.isdigit()) and idtemp['action'] == 'chwords1':
            if message == 'Все слова': idtemp = formdict(uid,idtemp)
            elif message == 'Последние n':
                x = idtemp['langs'][min(idtemp['langs'])] if idtemp['chch'] == '!!!ВСЕ!!!' else idtemp['langs'][idtemp['chch']]
                out = 'Отличный выбор, %s!\nСколько слов? ответь цифрой 1 до %d'%(idtemp['uname'],len(x))
                newmes(uid,out,stopk)
            elif message.isdigit(): idtemp = formdict(uid,idtemp,int(message))


        elif message == 'show1': #ВЫВОД НА ТЕРМИНАЛ ДАННЫХ ПОЛЬЗОВАТЕЛЯ
            for language in idtemp['langs']:
                for words in enumerate(idtemp['langs'][language]):
                    idtemp['langs'][language][words[0]] = [words[1][0].lower(),words[1][1].lower()]
            print(idtemp)
            try:
                print('\nUser id:\t%s'%idtemp['uid'])
                print('User name:\t%s'%idtemp['uname'])
                print('Current action:\t%s'%idtemp['action'])
                print('Check type:\t%s'%idtemp['chkt'])
                print('CheckN lan:\t%s'%idtemp['chch'])
                out=''
                for lang in idtemp['langs'].keys():
                    out+='\n'
                    out += '%s:\n'%lang
                    for word in idtemp['langs'][lang]:
                        out += '%s-%s\n'%(word[0],word[1])
                print('Dictionary:\n%s'%out)
                out = ''
                if idtemp:
                    for word in idtemp['dict']:
                        out+='%s\t%s\n'%(word[0],word[1])
                print('CheckN dict:\n%s'%out)
                t = pload('writefirst')
                print('\n\nDB "SHE WRITES FIRST":')
                for key in t.keys():
                    print('%s:\t%d.%d'%(key,t[key][1],t[key][0]))
                print()
            except: print('Oops...')
        elif message == 'restart1': #ПЕРЕЗАГРУЗКА
            idtemp['action'] = 'mainmenu'
            newmes(uid,'Чинюсь...')
            newmes(uid,'Исправление пространства времени...')
            newmes(uid,'Найдена доступная ячейка, подгружаюсь...')
            newmes(uid,'ASDmiqwjfndasiuNASUYHDLWdoasmdofmaoedwSSSASDWЙЦвыфываЯЛДФЫ')
            newmes(uid,'!!!OK!!!',Mkeyboard)

        else:
            #ЗНАКОМСТВО|РЕДАКТИРОВАТЬ --> ПРОСИМ ВВЕСТИ ПОЛЬЗОВАТЕЛЯ ИЗУЧАЕМЫЕ ЯЗЫКИ|СОХРАНЯЕМ ИМЯ
            if idtemp['action'] in ('intro0','introO'):
                idtemp['uname'] =  message
                if idtemp['action'] == 'intro0':
                    idtemp['action'] = 'intro1'
                    out = ('Очень приятно, %s, Какие языки мы будем изучать?'%idtemp['uname'] +
                        'Напиши пожалуйста каждый язык через пробел, например: Английский Испанский Японский')
                else:
                    idtemp['action'] = 'mainmenu'
                    out = 'Хорошо, %s'%idtemp['uname']
                newmes(uid,out)
            #ЗНАКОМСТВО|РЕДАКТИРОВАТЬ --> СОХРАНЯЕМ ЯЗЫКИ КОТОРЫЕ ИЗУЧАЕТ ПОЛЬЗОВАТЕЛЬ
            elif idtemp['action'] in ('intro1','introI'):
                for lang in message.split(' '):idtemp['langs'][lang] = []
                out = 'Замечательный выбор, а теперь смотри что я умею!' if idtemp['action']=='intro1' else 'Добавила =)'
                idtemp['action'] = 'mainmenu'
                newmes(uid,out ,Mkeyboard)
            #ПОПОЛНЕНИЕ СЛОВ
            elif idtemp['action'] in idtemp['langs'].keys():
                #ПОПОЛНЕНИЕ СЛОВ --> ПОЛЬЗОВАТЕЛЬ ЗАКОНЧИЛ ПОПОЛНЯТЬ СЛОВА
                if message == 'Стоп!':
                    idtemp['action'] = 'adwords'
                    newmes(uid,'Добавим для другого языка, или всё?',buildkey(1,idtemp['langs']))
                #ПОПОЛНЕНИЕ СЛОВ --> ДОБАВЛЯЕМ СЛОВА В СПИСОК
                else:
                    idtemp['langs'][idtemp['action']].append([message.split('-')[0].lower(), message.split('-')[1].lower()])
                    newmes(uid,'Zzz...',stopk)
            #РЕДАКТИРОВАТЬ --> ИСПРАВЛЯЕМ НАЗВАНИЕ ЯЗЫКА
            elif idtemp['action'][:7] == 'chlang0':
                idtemp['langs'][message] = idtemp['langs'].pop(idtemp['action'][7:])
                idtemp['action'] = 'mainmenu'
                newmes(uid,'Готово!=)',Mkeyboard)
            #РЕДАКТИРОВАТЬ --> УДАЛИТЬ СЛОВО
            elif idtemp['action'] == 'delwor':
                for language in idtemp['langs']:
                    try:
                        idtemp['langs'][language].remove(message.lower().split('-'))
                        out = 'Удалила!=)';break
                    except:out = 'Упс=( Не могу найти слова. Напиши точно так же как в твоем словаре, пожалуйста!'
                idtemp['action']='mainmenu'
                newmes(uid,out,Mkeyboard)
            #ПРОВЕРЬ МЕНЯ --> ПОЛЬЗОВАТЕЛЬ ВВОДИТ СЛОВО
            elif idtemp['action'] == 'PLAYN':
                #ПРАВИЛЬНО ОТВЕТИЛ
                if message.lower() in idtemp['dict'][0] and message != idtemp['dict'][0][idtemp['chkt']]:
                    out = 'Правильно!'
                    cur = ((idtemp['stlen']-idtemp['%'])/idtemp['stlen'])*100
                    out += '\nТочность: %.2f'%cur
                    if len(idtemp['dict'])>1:
                        idtemp['dict'].remove(idtemp['dict'][0])
                        out += '\nНовое слово: %s (%s)'%(idtemp['dict'][0][idtemp['chkt']],idtemp['dict'][0][2])
                        newmes(uid,out,stopk)
                    else:
                        idtemp['action']='mainmenu'
                        cur = ((idtemp['stlen']-idtemp['%'])/idtemp['stlen'])*100
                        newmes(uid,'Поздравляю %s, мы закончили!=)\nТвой результат: %.2f'%(idtemp['uname'],cur),Mkeyboard)
                #НЕПРАВИЛЬНО ОТВЕТИЛ
                else:
                    idtemp['%'] +=1
                    cur = ((idtemp['stlen']-idtemp['%'])/idtemp['stlen'])*100
                    out = 'Ошибка! Точность: %.2f'%cur
                    out += '\nПостарайся ещё, слово: %s (%s)'%(idtemp['dict'][0][idtemp['chkt']],idtemp['dict'][0][2])
                    newmes(uid,out,stopk)
        #WRITEFIRST
        now = datetime.datetime.now()
        wtfst ={}
        try:
            wtfst = pload('writefirst')
        except:
            pdump('writefirst',wtfst)
        wtfst[uid] = [now.month,now.day]
        pdump('writefirst',wtfst)

        pdump(uid,idtemp)
    except: print('Oops..');newmes(uid,'Oops...(Try restart1)')

def buildkey(type0,langs=None): #ФУНКЦИЯ ПОСТРОЕНИЯ КЛАВИАТУРЫ
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Стоп!',color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    for x in enumerate(langs.keys()):
        if x[0]%2==0 and x[0]>1: keyboard.add_line()
        keyboard.add_button(x[1],color=VkKeyboardColor.POSITIVE)
    if type0:return keyboard
    keyboard.add_line()
    keyboard.add_button('!!!ВСЕ!!!',color=VkKeyboardColor.POSITIVE)
    return keyboard

def newmes(uid,message,*keyboard): #ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЙ
    if keyboard:
        vk.method('messages.send',{'user_id' :uid,'random_id': get_random_id(),
                                'message':message,
                                'keyboard':keyboard[0].get_keyboard()})
    else:vk.method('messages.send',{'user_id' :uid,'random_id': get_random_id(),'message':message})
    print("SystemID:\tFIBI\nSystem message:\n" + str(message))

def pdump(uid,idtem): #ФУНКЦИЯ СОХРАНЕНИЯ ДАННЫХ ПОЛЬЗОВАТЕЛЯ НА ДИСК
    with open(path + str(uid)+'.pkl','wb') as f: pickle.dump(idtem,f)
    print('DATA SAVED')
def pload(uid): #ФУНКЦИЯ ЗАГРУЗКИ ДАННЫХ ПОЛЬЗОВАТЕЛЯ С ДИСКА
    with open(path + str(uid)+'.pkl','rb') as f: return pickle.load(f)
    print('DATA LOADED')

print('Second thread creating...')
wt=WriteFirst()
#ПОЛУЧАЕМ НОВЫЕ СООБЩЕНИЯ В ЦИКЛЕ
print('SYSTEM STARTED')
while True:
    try:
        for event in longpoll.listen():
            if event.to_me:
                if event.type == VkEventType.MESSAGE_NEW: formanswer(event.user_id,event.text)
    except: print('SYSTEM FUCKED UP')
