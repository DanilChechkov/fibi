#!/usr/bin/python3
import os
import os.path
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
wtfst = {}
#РЕДАКТИРОВАТЬ --> текст клавиатуры
chname, addlan, dellan = 'Я поменяль имя','Добавить язык','Удалить язык'
chlang, ediwor, delwor  = 'Очепятка в языке','Изменить слово','Удалить слово'
icmind = 'Я передумаль, Фиби=('
love,evol = 'Любовь-Love','Love-Любовь'
tss = 1
print('Keyboards creating...')
#СОЗДАЕМ КЛАВИАТУРУ СТОП
stopk = VkKeyboard(one_time=False)
stopk.add_button('Стоп!',color=VkKeyboardColor.NEGATIVE)
#СОЗДАЕМ КЛАВИАТУРУ ГЛАВНОГО МЕНЮ
adwords,shwords,chwords,edwords = 'Пополнить словарь','Мой словарь','Проверь слова, Фиби!=)','Редактировать'
reminme = 'Напомни мне'
Mkeyboard = VkKeyboard(one_time=False)
Mkeyboard.add_button(adwords,color=VkKeyboardColor.POSITIVE)
Mkeyboard.add_button(shwords,color=VkKeyboardColor.POSITIVE)
Mkeyboard.add_line()
Mkeyboard.add_button(chwords,color=VkKeyboardColor.POSITIVE)
Mkeyboard.add_line()
Mkeyboard.add_button(reminme,color=VkKeyboardColor.POSITIVE)
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
    def __init__(self,interval = 60):
        self.interval = interval
        thread = threading.Thread(target=self.chkTi,args=())
        thread.daemon = True
        thread.start()

    def chkTi(self):
        global tss
        while True:
            nowt = datetime.datetime.now()
            dtm = [nowt.month,nowt.day,nowt.hour,nowt.minute]
            #WRITEFIRST
            try:
                tss +=1
                wtf = pload('writefirst')
                print('LAST ACTIVITY DB LOADED')
                if tss == 90:
                    newmes(214708790,'All good!');tss =1
                for uid in wtf.keys():
                    if dtm[0]>wtf[uid][0] or dtm[1]>wtf[uid][1]:
                        if dtm[2] >= wtf[uid][2] and dtm[3] > wtf[uid][3]:
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
            #НАПОМИНАНИЯ
            try:
                if os.path.isfile(path + 'reminder.pkl'):
                    tmpr = pload('reminder')
                    for mess in tmpr.keys():
                        if dtm[0]==tmpr[mess][1] and dtm[1]==tmpr[mess][2] and dtm[2]>=tmpr[mess][3] and dtm[3]>=tmpr[mess][4]:
                            for text in ('Эй',mess,'Нужно было напомнить.'):newmes(tmpr[mess][0],text)
                            tmpr.pop(mess,'FUCK')
                            pdump('reminder',tmpr)
                            break
                else: 
                    print('NO REMINDERS YET')
            except:
                print('NO REMINDERS DB')
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
        global idtemp,wtfst
        tempOUT,tempKEY = '', None
        now = datetime.datetime.now()
        ptu = path + str(uid) +'.pkl'
        print("\nUser ID: \t" + str(uid) +"\nUser message:\n" + message)
        #ПЫТАЕМСЯ ЗАГРУЗИТЬ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ С ЛОКАЛЬНОГО ХРАНИЛИЩА
        if os.path.isfile(ptu):idtemp = pload(uid)
        else: idtemp = {'action':'intro','langs':{}}
        
        if idtemp['action'] == 'mainmenu':#ОБНУЛЕНИЕ ИГРОВЫХ ПЕРЕМЕННЫХ
            idtemp['chkt'],idtemp['%'],idtemp['stlen'],idtemp['chch'],idtemp['remi'] = 2,0,0,'NONE',''
            idtemp['dict'] = []
        
        if message.lower() in ['start','начать','привет']:#ЗНАКОМСТВО
            idtemp['action'],idtemp['uid'] = 'intro0',uid
            tempOUT = ('Привет, меня зовут Фиби и я буду твоим персональным помощником в изучении языка. ' +
                    'Мы с тобой будем учить слова и с этого дня я от тебя не отцеплюсь! =)' +
                    'Я представилась, а как обращаться к тебе?)')
        
        elif message == shwords:#ПОКАЖИ МОЙ СЛОВАРЬ
            tempOUT = 'Хорошо, вот твой словарь, %s:\n'%idtemp['uname']
            for lang in idtemp['langs'].keys():
                tempOUT += '\n%s:\n'%lang
                for word in idtemp['langs'][lang]:
                    tempOUT += '%s-%s\n'%(word[0],word[1])

        elif message == adwords:#ПОПОЛНИТЬ СЛОВАРЬ
            idtemp['action'],tempOUT,tempKEY = 'adwords','Окей, но всё по порядку, %s =) Какой язык?'%idtemp['uname'],buildkey(1,idtemp['langs'])
        #ПОПОЛНИТЬ СЛОВАРЬ|УДАЛИТЬ СЛОВАРЬ|ИЗМЕНИТЬ СЛОВАРЬ|ИЗМЕНИТЬ СЛОВО --> ВЫБОР СЛОВАРЯ
        elif (message in idtemp['langs'].keys() or message =='!!!ВСЕ!!!') and idtemp['action'] in ('adwords','dellan','chlang','chwords0'):
            if idtemp['action'] == 'adwords':#ПОПОЛНИТЬ
                res,tempOUT,tempKEY = message,'Хорошо, отправляй мне по одному слову за сообщение, вот пример: Похмелье-Hang over. Не отделяй тире пробелами, пожалуйста=)',stopk
            elif idtemp['action'] == 'dellan':#УДАЛИТЬ
                idtemp['langs'].pop(message)
                res,tempOUT,tempKEY = 'mainmenu','Удалила =)',Mkeyboard
            elif idtemp['action'] == 'chlang':#ИЗМЕНИТЬ
                res,tempOUT,tempKEY = 'chlang0'+message,'На что меняем?',Mkeyboard
            elif idtemp['action'] == 'chwords0':#ПРОВЕРКА
                res,tempOUT,tempKEY,idtemp['chch'] = 'chwords1','Замечательный выбор!',chtkey2,message
            idtemp['action'] = res
        #ПОПОЛНИТЬ СЛОВАРЬ| ПРОВЕРЬ МЕНЯ --> ВЫХОД В ГЛАВНОЕ МЕНЮ
        elif message in (icmind,'Стоп!') and idtemp['action'] in ('adwords','chwords','chwords0','chwords1','PLAYN','edwords0','dellan','chlang'):
            if idtemp['action'] in ('adwords','chwords','edwords0'):#ВЫХОД В ГЛАВНОЕ МЕНЮ
                res,tempOUT,tempKEY = 'mainmenu','Окей, я готова двигаться дальше!=)',Mkeyboard
            elif idtemp['action'] in ('dellan','chlang'):#ВЫХОД В МЕНЮ РЕДАКТИРОВАНИЯ
                res,tempOUT,tempKEY = 'edwords0','Ок, вернулись=)',editk
            elif idtemp['action'] == 'chwords0':#ПРОВЕРЬ МЕНЯ --> ВЫХОД В МЕНЮ ВЫБОРА ТИПА ПРОВЕРКИ
                res,tempOUT,tempKEY = 'chwords','Ладно, шаг назад.',chtkey
            elif idtemp['action'] == 'chwords1':#ПРОВЕРЬ МЕНЯ --> ВЫХОД В МЕНЮ ВЫБОРА ЯЗЫКА
                res,tempOUT,tempKEY = 'chwords0','Серьезно?=(',buildkey(0,idtemp['langs'])
            elif idtemp['action'] == 'PLAYN':#ПРОВЕРЬ МЕНЯ -->ВЫХОД ИЗ ИГРЫ
                res,tempOUT,tempKEY = 'chwords1','Ладно.',chtkey2
            idtemp['action'] = res
        elif message == edwords:#РЕДАКТИРОВАТЬ
            idtemp['action'] = 'edwords0'
            tempOUT,tempKEY = 'Что меняем, %s?'%idtemp['uname'],editk
        elif message == chname and idtemp['action'] == 'edwords0':#РЕДАКТИРОВАТЬ --> ПОМЕНЯЙ ИМЯ
            idtemp['action'] = 'introO'
            tempOUT,tempKEY = 'Как теперь мне тебя называть?=)',Mkeyboard
        elif message == addlan and idtemp['action'] == 'edwords0':#РЕДАКТИРОВАТЬ --> ДОБАВИТЬ ЯЗЫК
            idtemp['action'] = 'introI'
            tempOUT = ('Давай добавим, %s! '%idtemp['uname'] +
                    'Напиши пожалуйста каждый язык через пробел, например: Английский Испанский Японский')
            tempKEY = Mkeyboard
        #РЕДАКТИРОВАТЬ --> УДАЛИТЬ ЯЗЫК|ОПЕЧАТКА В НАЗВАНИИ ЯЗЫКА
        elif message in (dellan,chlang) and idtemp['action'] == 'edwords0':
            idtemp['action'] = 'dellan' if message == dellan else 'chlang'
            tempOUT = 'Какой язык удаляем?' if message == dellan else 'Какой язык изменяем, %s?'%idtemp['uname']
            tempKEY = buildkey(1,idtemp['langs'])
        elif message == delwor and idtemp['action'] == 'edwords0':#РЕДАКТИРОВАТЬ --> УДАЛИТЬ СЛОВО
            idtemp['action'] = 'delwor'
            tempOUT,tempKEY = 'Хорошо, %s, что мне удалить? Напиши по примеру: Похмелье-Hang over'%idtemp['uname'] , Mkeyboard
        elif message == chwords:#ПРОВЕРЬ МЕНЯ
            idtemp['action'] = 'chwords'
            tempOUT,tempKEY = 'Ок, %s. Как реализуем проверку? Есть два варианта:\n1) Я пишу тебе слово, а ты мне перевод.(любовь-love)\n2) Я пишу перевод, а ты мне слово.(love-любовь).'%idtemp['uname'] , chtkey
        elif message in (love,evol) and idtemp['action'] == 'chwords':#ПРОВЕРЬ МЕНЯ --> ВЫБОР ЯЗЫКА
            idtemp['chkt'] = 0 if message==love else 1
            tempOUT,tempKEY,idtemp['action'] = 'Какой язык?',buildkey(0,idtemp['langs']),'chwords0'
        #ПРОВЕРЬ МЕНЯ --> ВЫБОР КОЛ-ВА слов
        elif (message in ('Все слова','Последние n') or message.isdigit()) and idtemp['action'] == 'chwords1':
            if message == 'Все слова': idtemp = formdict(uid,idtemp)
            elif message == 'Последние n':
                x = idtemp['langs'][min(idtemp['langs'])] if idtemp['chch'] == '!!!ВСЕ!!!' else idtemp['langs'][idtemp['chch']]
                tempOUT = 'Отличный выбор, %s!\nСколько слов? ответь цифрой 1 до %d'%(idtemp['uname'],len(x))
                tempKEY = stopk
            elif message.isdigit(): idtemp = formdict(uid,idtemp,int(message))
        elif message == reminme:#ОБНОВЛЕНИЕ 1. НАПОМНИТЬ МНЕ
            tempOUT,idtemp['action'] = 'О чем тебе напомнить, %s?'%idtemp['uname'],'remme0'

        elif message == 'show1': #ПЕРЕПИСАТЬ!!!ВЫВОД ВСЕХ ДАННЫХ В СООБЩЕНИИ
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
                    print('%s:\t%d.%d %d:%d'%(key,t[key][1],t[key][0],t[key][2],t[key][3]))
                print()
            except: print('Oops...')
        elif message == 'restart1': #ПЕРЕЗАГРУЗКА
            idtemp['action'] = 'mainmenu'
            for text in ('Чинюсь...','Исправление пространства времени...','Найдена доступная ячейка, подгружаюсь...',
            'ASDmiqwjfndasiuNASUYHDLWdoasmdofmaoedwSSSASDWЙЦвыфываЯЛДФЫ'):
                newmes(uid,text)
            tempOUT,tempKEY = '!!!OK!!!',Mkeyboard

        else:
            #ЗНАКОМСТВО|РЕДАКТИРОВАТЬ --> ПРОСИМ ВВЕСТИ ПОЛЬЗОВАТЕЛЯ ИЗУЧАЕМЫЕ ЯЗЫКИ|СОХРАНЯЕМ ИМЯ
            if idtemp['action'] in ('intro0','introO'):
                idtemp['uname'] =  message
                if idtemp['action'] == 'intro0':
                    idtemp['action'] = 'intro1'
                    tempOUT = ('Очень приятно, %s, Какие языки мы будем изучать?'%idtemp['uname'] +
                        'Напиши пожалуйста каждый язык через пробел, например: Английский Испанский Японский')
                else:
                    idtemp['action'] = 'mainmenu'
                    tempOUT = 'Хорошо, %s'%idtemp['uname']
            #ЗНАКОМСТВО|РЕДАКТИРОВАТЬ --> СОХРАНЯЕМ ЯЗЫКИ КОТОРЫЕ ИЗУЧАЕТ ПОЛЬЗОВАТЕЛЬ
            elif idtemp['action'] in ('intro1','introI'):
                for lang in message.split(' '):idtemp['langs'][lang] = []
                tempOUT = 'Замечательный выбор, а теперь смотри что я умею!' if idtemp['action']=='intro1' else 'Добавила =)'
                tempKEY,idtemp['action'] = Mkeyboard,'mainmenu'
            elif idtemp['action'] in idtemp['langs'].keys(): #ПОПОЛНЕНИЕ СЛОВ
                if message == 'Стоп!':#ПОПОЛНЕНИЕ СЛОВ --> ПОЛЬЗОВАТЕЛЬ ЗАКОНЧИЛ ПОПОЛНЯТЬ СЛОВА
                    idtemp['action'] = 'adwords'
                    tempOUT,tempKEY = 'Добавим для другого языка, или всё?',buildkey(1,idtemp['langs'])
                else:#ПОПОЛНЕНИЕ СЛОВ --> ДОБАВЛЯЕМ СЛОВА В СПИСОК
                    idtemp['langs'][idtemp['action']].append([message.split('-')[0].lower(), message.split('-')[1].lower()])
                    tempOUT,tempKEY = 'Ага, записала...',stopk
            elif idtemp['action'][:7] == 'chlang0':#РЕДАКТИРОВАТЬ --> ИСПРАВЛЯЕМ НАЗВАНИЕ ЯЗЫКА
                idtemp['langs'][message] = idtemp['langs'].pop(idtemp['action'][7:])
                tempOUT,tempKEY,idtemp['action'] = 'Готово!=)',Mkeyboard,'mainmenu'
            elif idtemp['action'] == 'delwor':#РЕДАКТИРОВАТЬ --> УДАЛИТЬ СЛОВО
                for language in idtemp['langs']:
                    try:
                        idtemp['langs'][language].remove(message.lower().split('-'))
                        tempOUT = 'Удалила!=)';break
                    except:tempOUT = 'Упс=( Не могу найти слова. Напиши точно так же как в твоем словаре, пожалуйста!'
                tempKEY,idtemp['action']=Mkeyboard,'mainmenu'
            #ПРОВЕРЬ МЕНЯ --> ПОЛЬЗОВАТЕЛЬ ВВОДИТ СЛОВО
            elif idtemp['action'] == 'PLAYN':
                #ПРАВИЛЬНО ОТВЕТИЛ
                if message.lower() in idtemp['dict'][0] and message != idtemp['dict'][0][idtemp['chkt']]:
                    tempOUT = 'Правильно!'
                    cur = ((idtemp['stlen']-idtemp['%'])/idtemp['stlen'])*100
                    tempOUT += '\nТочность: %.2f'%cur
                    if len(idtemp['dict'])>1:#СЛОВА ЕЩЁ ЕСТЬ
                        idtemp['dict'].remove(idtemp['dict'][0])
                        tempOUT += '\nНовое слово: %s (%s)'%(idtemp['dict'][0][idtemp['chkt']],idtemp['dict'][0][2])
                        tempKEY = stopk
                    else:#ПОСЛЕДНЕЕ СЛОВО
                        idtemp['action']='mainmenu'
                        cur = ((idtemp['stlen']-idtemp['%'])/idtemp['stlen'])*100
                        tempOUT,tempKEY = 'Поздравляю %s, мы закончили!=)\nТвой результат: %.2f'%(idtemp['uname'],cur),Mkeyboard
                else:#НЕПРАВИЛЬНО ОТВЕТИЛ
                    idtemp['%'] +=1
                    cur = ((idtemp['stlen']-idtemp['%'])/idtemp['stlen'])*100
                    tempOUT,tempKEY = 'Ошибка! Точность: %.2f'%cur,stopk
                    tempOUT += '\nПостарайся ещё, слово: %s (%s)'%(idtemp['dict'][0][idtemp['chkt']],idtemp['dict'][0][2])
            elif idtemp['action'] == 'remme0':#ОБНОВЛЕНИЕ. НАПОМНИ МНЕ
                idtemp['action'],idtemp['remi'] = 'remme1',message
                tempOUT = """Отлично, теперь укажи дату в формате: %d.%d.%d.%d  где:
                %d - Месяц
                %d - Число
                %d - Час
                %d - Минута
                Не используй нули и пробелы а то я запутаюсь =("""%(now.month,now.day,now.hour,now.minute,
                now.month,now.day,now.hour,now.minute)
            elif idtemp['action'] == 'remme1':#НАПОМИНАНИЕ --> ЗАПОМНИТЬ
                idtemp['action'] = 'mainmenu'
                dt = message.split('.')
                ptr = path + 'reminder.pkl'
                if os.path.isfile(ptr):tmpr = pload('reminder')
                else: tmpr = {idtemp['remi']:[uid,dt[0],dt[1],dt[2],dt[3]]}
                tmpr[idtemp['remi']] = [uid,int(dt[0]),int(dt[1]),int(dt[2]),int(dt[3])]
                pdump('reminder',tmpr)
                tempOUT,tempKEY ='Хорошо, %s. Я напомню'%idtemp['uname'], Mkeyboard
        #WRITING A NEW MESSAGE
        if tempOUT:
            if tempKEY: newmes(uid,tempOUT,tempKEY)
            else: newmes(uid,tempOUT)
        #WRITEFIRST
        ptw = path + 'writefirst.pkl'
        if os.path.isfile(ptw):wtfst = pload('writefirst')
        wtfst[uid] = [now.month,now.day, now.hour,now.minute]
        pdump('writefirst',wtfst)
        pdump(uid,idtemp)
    except: newmes(uid,'Oops...(Try restart1)')

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
                                'message':message,'keyboard':keyboard[0].get_keyboard()})
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
print('SYSTEM STARTED')
while True:#ПОЛУЧАЕМ НОВЫЕ СООБЩЕНИЯ В ЦИКЛЕ
    try:
        for event in longpoll.listen():
            if event.to_me:
                if event.type == VkEventType.MESSAGE_NEW: formanswer(event.user_id,event.text)
    except: print('SYSTEM FUCKED UP')