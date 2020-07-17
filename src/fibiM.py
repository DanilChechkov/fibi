#!/usr/bin/env python3

#VKAPI      (сохр данных)(для ответов)(напоминания)
import vk_api,os, pickle, random, datetime,time,threading,sys
from vk_api.longpoll import VkLongPoll,VkEventType
from vk_api.utils import get_random_id
import fibiGM as gm                                             #Моудль создания словаря для игры
import keysFi as k                                              #Модуль с клавиатурами
#Импортированно отдельными модулями чтобы не захломлять код

#Данный словарь позволяет создать навигацию в меню с помощью кнопки вернуться назад
ksNacts = { ('addwo',0):['Мы в главном меню =)',k.MKey],
            ('addwo',10):['Мы в меню редактирования =)',k.EKey],
            ('addwo',1):['Окей, добавим для другого языка или в главное меню?',1],
            ('addwo',11):['Окей, добавим для другого языка или вернемся в меню редактирования?',1],
            ('edydi',11):['Вернулись назад',1],
            ('playn',1):['Окей, выбирай снова, как мы тебя будем проверять?',k.CTKey],
            ('playn',2):['Ну ладно, выбирай снова какой язык',0],
            ('playn',3):['Ок. Выбери тип проверки',k.CT2Key],
            ('remmi',1):['Ок, давай по новой. О чем напомнить?',k.SKey],
            ('remmi',2):['Ок,на что меняем дату?',k.REKey]}

ksNacts[('edywo',0)]=ksNacts[('playn',0)]=ksNacts[('remmi',0)]= ksNacts[('addwo',0)]
ksNacts[('intro',10)]=ksNacts[('edydi',10)]=ksNacts[('edydi',15)]=ksNacts[('edydi',16)]=ksNacts[('edydi',17)] = ksNacts[('addwo',10)]
ksNacts[('playn',4)] = ksNacts[('playn',3)]
#Этот словарь упрощает формирование ответов и клавиатур из меню редактирования
edMenu = {  11: (['edywo',0],'Заменила =)', k.EKey),
            15: (['edywo',0],'Добавила!', k.EKey),
            16: (['edywo',0],'Удалила!=(',k.EKey),
            17: [['edydi',17],'Упс=( Не могу найти слова. Напиши точно так же как в твоем словаре, пожалуйста!',k.SKey]}

PATH1 = os.getcwd() +'/'
ptw = PATH1 + 'writefirst.pkl'      #Здесь хранятся записи о том когда пользователь писал в последний раз
ptr = PATH1 + 'reminder.pkl'        #Тут хранятся напоминания

fibcount = 0                        #Переменная для отсчета минут, использована в функции WriteFirst

token = open(PATH1 +'token').readline().rstrip()    #Здесь хранится токен
print('\nToken:\t',token) 

print('Connecting...')
#ПОДКЛЮЧАЕМСЯ К VK
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def introF(message,bhv,userd): # Разобрано в ReadMe
    print('INTRO function is working')
    if bhv == 0:
        userd['act'][1] = 1

        tempOUT = open(PATH1 + 'someos','r').readlines()[0][:-1]
        tempKEY = 0
    elif bhv in (1,10):
        if bhv == 1: userd['act'][1] = 2
        else:userd['act'] = ['edywo',0]
        userd['name'] = message
        f = open(PATH1 + 'someos','r').readlines()
        tempOUT = (f[1][:-1] + userd['name'] + f[2][:-1]) if bhv == 1 else 'Ок, %s'%userd['name']
        tempKEY=0 if bhv == 1 else k.EKey
    elif bhv == 2:
        userd['act'] = ['mainm',0]
        
        for lang in message.split():
            userd['dict'][lang] = []

        tempOUT = open(PATH1 + 'someos','r').readlines()[3][:-1]
        tempKEY = k.MKey

    return userd,tempOUT,tempKEY

def mainmF(message,bhv,userd):# Разобрано в ReadMe
    try:
        userd = zeros(userd)
        if message == k.shwL:#User asks to show his dict
            tempOUT = random.choice(open(PATH1 + 'takedict','r').readlines())
            tempOUT = tempOUT[:-1]
            tempOUT += '%s:\n'%userd['name']
            count = 0 
            for lang in userd['dict'].keys():
                    count += len(userd['dict'][lang])
                    tempOUT += '\n%s (слов - %d):\n'%(lang,len(userd['dict'][lang]))
                    for word in userd['dict'][lang]:
                        if len(tempOUT) >= 3800:
                            newmes(userd['id'],tempOUT)
                            tempOUT = ''
                        tempOUT += '%s-%s\n'%(word[0],word[1])
            tempOUT += '\nВсего слов - %d'%count
            tempKEY = k.MKey
        elif message == k.addW:#User asks to add words in dict
            userd['act'] = ['addwo',0]

            tempOUT = 'Окей, но всё по порядку, %s =) Какой язык?'%userd['name']
            tempKEY = k.buildkey(1, userd['dict'].keys())
        elif message == k.edyL:#User asks to open editing menu
            userd['act'] = ['edywo',0]

            tempOUT = random.choice(open(PATH1+'editenter','r').readlines())
            tempKEY = k.EKey
        elif message == k.chwL:#User asks to check words
            userd['act'] = ['playn',0]
            tempOUT = 'Ок, %s. Как реализуем проверку? Есть два варианта:\n1) Я пишу тебе слово, а ты мне перевод.(любовь-love)\n2) Я пишу перевод, а ты мне слово.(love-любовь).'%userd['name']
            tempKEY = k.CTKey
        elif message == k.remL:#User asks to remind something
            userd['act'] = ['remmi',0]
            tempOUT = random.choice(open(PATH1 + 'remmi','r').readlines())
            tempKEY = k.SKey
        elif message == k.relL:#User asks for reminders list
            tempOUT = 'Список активных напоминаний, %s:\n'%userd['name']
            out = ''

            tempKEY = k.MKey
            remis = pload('reminder')
            if remis:
                for element in remis:
                    if element[-2] == userd['id']:
                        out += '%s, нужно напомнить %d.%d в %d:%d\n'%(element[-1],element[1],element[0],element[2],element[3])
            if not out:
                tempOUT = random.choice(open(PATH1+'noremis','r').readlines())
            else:
                tempOUT += out
        else:
            tempOUT = 'Прости, я тебя не понимаю =('
            tempKEY = k.MKey
    except:
        print('Main function panic')
        tempOUT = 'Panic! (failed to start MF. Exception code: "fuck me. how did you do that?") System restarted'
        userd = zeros(userd)
        tempKEY = k.MKey
    return userd,tempOUT,tempKEY

def addwoF(message,bhv,userd):  # Разобрано в ReadMe
    try:
        if bhv in (0,10):#User is making a choice (Which lang to use adding words)
            userd['act'][1] = 1 if bhv == 0 else 11
            userd['act'].append(message)

            tempOUT = open(PATH1 + 'someos','r').readlines()[4][:-1]
            tempKEY = k.SKey
        elif bhv in (1,11):#User send a word pair to add in dict
            message = message.lower()
            for pair in message.split('\n'):
                words = pair.split('-')
                if len(words)!=2:
                    tempOUT = open(PATH1 + 'someos','r').readlines()[5][:-1]
                else:
                    tempOUT = random.choice(open(PATH1 + 'addwords','r').readlines())
                    if words[0][-1] == ' ': words[0] = words[0][:-1]
                    if words[1][0] == ' ': words[1] = words[1][1:]
                    userd['dict'][ userd['act'][2] ].append([words[0],words[1]])
            tempKEY = k.SKey
        else:
            tempOUT = 'Что-то где-то не так, попытайся еще но по другому'
            tempKEY = k.SKey
    except:
        print('Addwords function panic')
        tempOUT = 'No way! (failed to start AF) System restarted'
        userd = zeros(userd)
        tempKEY = k.MKey
    return userd,tempOUT,tempKEY

def edywoF(message,bhv,userd):  #Editing menu
    try:
        ans = { k.addW: (['addwo',10],'Окей, но всё по порядку, %s =) Какой язык?'%userd['name'],k.buildkey(1, userd['dict'].keys())),
                k.chaN: (['intro',10],'Как я могу к тебе обращаться теперь?', k.SKey ),
                k.edyD: (['edydi',10],'Выбирай',k.buildkey(1, userd['dict'].keys())),
                k.addL: (['edydi',15],'Какой язык добавляем? =)',k.SKey),
                k.delL: (['edydi',16],'Какой язык удалить?',k.buildkey(1, userd['dict'].keys())),
                k.delW: (['edydi',17],'Что удалить? Напиши точно как в словаре, например Любовь-Love',k.SKey)}
        if message in ans.keys():
            userd['act'],tempOUT,tempKEY = ans[message]
        else:
            userd['act'] = ['edywo',0]
            tempOUT = 'Я не совсем тебя понимаю'
            tempKEY = k.EKey
    except:
        userd['act'] = ['edywo',0]
        print('Edit function panic')
        tempOUT = '(failed to start EF) System restarted'
        tempKEY = k.EKey
    return userd,tempOUT,tempKEY

def edydiF(message,bhv,userd):  #Editing menu actions
    try:
            
        if bhv == 10: edMenu[10] = (['edydi',11, message],'На что меняем?',k.SKey)
        
        if bhv in edMenu.keys():
            tempOUT,tempKEY = edMenu[bhv][1:]
            if bhv == 10: userd['act'].append(message) #User made a choice which name of language to change
            elif bhv == 11: #User send what we should replace
                userd['dict'][message] = userd['dict'].pop( userd['act'][2] )
            elif bhv == 15: userd['dict'][message] = [] #User send what language we should add
            elif bhv == 16: userd['dict'].pop(message)  #User asks to delete dictionary
            elif bhv == 17:
                words = message.lower().split('-')
                for language in userd['dict']:
                    if words in userd['dict'][language]:
                        userd['dict'][language].remove(words)
                        tempKEY = k.EKey
                        tempOUT = 'Удалила!=)'
                        edMenu[bhv][0] = ['edywo',0]
                        break
            userd['act'] = edMenu[bhv][0]
        else:
            tempOUT = 'Я не совсем тебя понимаю'
            tempKEY = k.EKey
    except:
        userd['act'] = ['edywo',0]
        print('EditDICT function panic')
        tempOUT = '(failed to start EFD) System restarted'
        tempKEY = k.EKey
    return userd,tempOUT,tempKEY

def playnF(message,bhv,userd):  #Playing function
    try:
        if bhv == 0:
            if message in (k.lovL,k.evoL):
                userd['chkt'] = 1 if message == k.lovL else 2

                userd['act'] = ['playn',1]
                tempOUT = random.choice(open(PATH1+'chkt','r').readlines())
                tempKEY = k.buildkey(0, userd['dict'].keys())
            else:
                tempOUT = 'Ты что-то делаешь не так.'
                tempKEY = k.CTKey
        elif bhv == 1:
            if message in (userd['dict'].keys()) or message == 'Проверь по всем':
                userd['chlan'] = message

                userd['act'] = ['playn',2]
                tempOUT = 'Ок, записала =) Как будем проверять?'
                tempKEY = k.CT2Key
            else:
                tempOUT = 'Ты что-то делаешь не так, дорогуша'
                tempKEY = k.buildkey(0, userd['dict'].keys())
        elif bhv == 2:
            tempOUT = ''
            if message == k.allL:
                userd['chkt2'] = 3
                userd['act'] = ['playn',3]
                userd['cdict'] = gm.formdict(userd['chkt'],userd['chlan'],userd['chkt2'],userd['dict'])
            elif message == k.lsnL or message == k.ranL:
                userd['chkt2'] = 1 if message == k.lsnL else 2
                x = userd['dict'][min(userd['dict'])]
                tempOUT = 'Загадай число от 1 до %d'%(len(x))
                tempKEY = k.SKey
            elif message.isdigit():
                userd['act'] = ['playn',3]
                userd['cdict'] = gm.formdict(userd['chkt'],userd['chlan'],userd['chkt2'],userd['dict'],int(message))
            else:
                tempOUT = 'Ты что-то делаешь не так.'
                tempKEY = k.CT2Key
            
            if not tempOUT: userd,tempOUT,tempKEY = gm.startgame(userd)

        elif bhv == 3:
            if message.lower() == userd['cdict'][0][1]: tempOUT = 'Правильно! '
            else:
                userd['wdict'].append(userd['cdict'][0])
                tempOUT = 'Ошибка! '
                userd['wansw'] += 1
            userd['cdict'].remove(userd['cdict'][0])
            tempOUT += 'Точность: %.1f\n'%(((userd['stlen']-userd['wansw'])/userd['stlen'])*100)
            if userd['cdict']:
                tempOUT += 'Следующее слово: %s (%s)'%(userd['cdict'][0][0],userd['cdict'][0][2])
                tempKEY = k.SKey
            else:
                tempOUT += 'Поздравляю, мы закончили!'
                if userd['wansw']>0:
                    userd['act'] = ['playn',4]
                    tempOUT += '\nЖелаешь провести работу над ошибками(%d), %s?'%(len(userd['wdict']),userd['name'])
                    tempKEY = k.YNKey
                else:
                    userd = zeros(userd)
                    tempKEY = k.MKey
        elif bhv == 4:
            if message == k.noL:
                tempOUT = random.choice(open(PATH1 + 'endgame').readlines())
                tempOUT += '\nЗапомни и больше не ошибайся:\n'
                for w1,w2,lan in userd['wdict']:
                    tempOUT += '%s - %s (%s)\n'%(w1,w2,lan)
                userd = zeros(userd)
                tempKEY = k.MKey
            elif message == k.yeL:
                userd['cdict'] = userd['wdict'][:]
                userd,tempOUT,tempKEY = gm.startgame(userd)
        else:
            tempOUT = 'Что-то ты делаешь не так. Давай сначала'
            tempKEY = k.MKey
            userd = zeros(userd)
    except:
        userd = zeros(userd)
        print('Playing function panic')
        tempOUT = '(failed to start PF) System restarted'
        tempKEY = k.MKey
    return userd,tempOUT,tempKEY

def remmiF(message,bhv,userd):
    try:
        now = datetime.datetime.now()
        if bhv == 0:
            userd['act'] = ['remmi',1]
            userd['remi'] = [message]

            tempOUT = "Супер, записала, теперь укажи дату в формате %s, где день и месяц разделены пробелом.\nИли выбери на клавиатуре"%now.strftime('%d %m')
            tempKEY = k.REKey
        elif bhv == 1:
            userd['act'] = ['remmi',2]
            if message == k.todL:
                userd['remi'].append(now.month)
                userd['remi'].append(now.day)
            elif message.lower() == "завтра":
                tomorrow = now + datetime.timedelta(days=1)
                userd['remi'].append(tomorrow.month)
                userd['remi'].append(tomorrow.day)
            elif message[-1:].isdigit():
                dt = [int(x) for x in message.split()]
                userd['remi'].append(dt[1])
                userd['remi'].append(dt[0])
            tempOUT = "А теперь укажи время дня в формате %s, где час и минута разделены пробелом."%now.strftime('%H %M')
            tempKEY = k.SKey
        elif bhv == 2:
            userd['act'] = ['mainm',0]
            dt = [int(x) for x in message.split()]
            userd['remi'].append(dt[0])
            userd['remi'].append(dt[1])
            if os.path.isfile(ptr):tmpr = pload('reminder')
            else: tmpr = []
            z = userd['remi'][1:]
            z.append(userd['id'])
            z.append(userd['remi'][0])
            tmpr.append(z)
            tmpr.sort()
            print(tmpr)
            pdump('reminder',tmpr)
            tempOUT,tempKEY ='Хорошо, %s. Я напомню'%userd['name'], k.MKey
        else:
            tempOUT = 'Что-то ты делаешь не так. Давай сначала'
            tempKEY = k.MKey
            userd = zeros(userd)
    except:
        userd = zeros(userd)
        print('Reminders adding function panic')
        tempOUT = '(failed to start RF) System restarted'
        tempKEY = k.MKey
    return userd,tempOUT,tempKEY


def formanswer(uid,message):
    OUTM=OUTK=False
    now = datetime.datetime.now()
    if os.path.isfile(PATH1+str(uid)+'.pkl'):
        userd = pload(uid)
    else:
        userd = {   'id': uid,
                    'act': ['intro',0],
                    'dict': {},
                    'chkt': 0,
                    'chlan': 'NONE',
                    'chkt2':0,
                    'cdict':[],
                    'wdict':[],
                    'stlen':0,
                    'wansw':0,
                    'remi':'NONE'}
    #System restart
    if message == 'restart1':
        userd = zeros(userd)
        OUTM,OUTK = 'Система перезагружена',k.MKey
    elif message[0:7].lower() == 'спасибо' and userd['act'][0] not in ('playn','addwo') :
            OUTM = random.choice(open(PATH1+'welcome','r').readlines())
    #Backward navigation in menu
    elif message == k.gatB:
        OUTM,OUTK = ksNacts[tuple(userd['act'][:2])]
        if userd['act'][1] == 0:
            userd['act'] = ['mainm',0]
        elif userd['act'][1] in (10,15,16,17):
            userd['act'] = ['edywo',0]
        else:
            userd['act'] = userd['act'][:2]
            userd['act'][1] -= 1
        if OUTK in (0,1):
            OUTK = k.buildkey(OUTK,userd['dict'].keys())
    #Call function with dictionary. Instead of IF_ELSE blocks
    else:
        userd,OUTM,OUTK = calfunc[userd['act'][0]](message,userd['act'][1],userd) 
    pdump(uid,userd)
    print(userd)

    #Write first saving date
    if os.path.isfile(ptw):wtfst = pload('writefirst')
    else: wtfst = {}
    
    wtfst[uid] = [now.month,now.day, now.hour,now.minute]
    pdump('writefirst',wtfst)

    if OUTM:
        if OUTK: newmes(uid,OUTM,OUTK)
        else: newmes(uid,OUTM)


def newmes(uid,message,*keyboard): #ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЙ
    if keyboard:
        vk.method('messages.send',{'user_id' :uid,'random_id': get_random_id(),
                                'message':message,'keyboard':keyboard[0].get_keyboard()})
    else:vk.method('messages.send',{'user_id' :uid,'random_id': get_random_id(),'message':message})

def zeros(ud): #ОБНУЛЕНИЕ ПЕРЕМЕННЫХ
    ud['act'] = ['mainm',0]
    ud['chkt'] = 0
    ud['chkt2'] = 0
    ud['stlen'] = 0
    ud['wansw'] = 0
    ud['chlan'] = 'NONE'
    ud['cdict'] = []
    ud['wdict'] = []
    ud['wdict'] = []
    ud['remi'] = 'NONE'
    return ud
def pdump(fNAME,dLOC): #ФУНКЦИЯ СОХРАНЕНИЯ ДАННЫХ ПОЛЬЗОВАТЕЛЯ НА ДИСК
    with open(PATH1 + str(fNAME)+'.pkl','wb') as f: pickle.dump(dLOC,f)
def pload(fNAME): #ФУНКЦИЯ ЗАГРУЗКИ ДАННЫХ ПОЛЬЗОВАТЕЛЯ С ДИСКА 
    with open(PATH1 + str(fNAME)+'.pkl','rb') as f: return pickle.load(f)

    

def WriteFirst():#Function for reminders and writing first
    global fibcount
    fibcount +=1
    nowt = datetime.datetime.now()

    print(nowt.strftime('%d-%m-%Y\t%H:%M'))

    dtm = [nowt.month,nowt.day,nowt.hour,nowt.minute]
    if fibcount == 90:
        newmes(214708790,'All good!')
        fibcount = 0
    
    if os.path.isfile(ptw):
        wtfst = pload('writefirst')
        if wtfst:
            for uid in wtfst.keys():
                if (dtm[0]>wtfst[uid][0] or dtm[1]>wtfst[uid][1]) and (dtm[2] >= wtfst[uid][2] and dtm[3] > wtfst[uid][3]):
                    tTp = { 'chkt':2,
                            'chlan':'Проверь по всем',
                            'chkt2':2,
                            'act':['playn',2],
                            }

                    ud = pload(uid)
                    ud = zeros(ud)
                    for key in tTp.keys():
                        ud[key] = tTp[key]
                    
                    x = ud['dict'][min(ud['dict'])]
                    tempOUT = 'Загадай число от 1 до %d'%(len(x))
                    tempKEY = k.SKey
                    newmes(uid,tempOUT,tempKEY)
                    pdump(uid,ud)
        else:
            print('Wtfst db is empty')
    else:
        print('No wtfst db yet')
    
    if os.path.isfile(ptr):
        remDB = pload('reminder')
        if remDB:
            for reminder in remDB[:]:
                remdat = reminder[0:4]
                if dtm[0]==remdat[0] and dtm[1]==remdat[1]:
                    if (dtm[2]==remdat[2] and dtm[3]>=remdat[3]) or (dtm[2]>remdat[2]):
                        hey = random.choice(open(PATH1 +'hey','r').readlines())
                        rem = random.choice(open(PATH1 +'remitxt','r').readlines())
                        for text in (hey,reminder[-1],rem):
                            newmes(reminder[-2],text)
                        remDB.remove(reminder)
            pdump('reminder',remDB)
        else:
            print('Reminder db is empty')
    else:
        print('No reminder db yet')

    threading.Timer(60, WriteFirst).start()



calfunc = { 'intro':introF,
            'mainm':mainmF,
            'addwo':addwoF,
            'edywo':edywoF,
            'edydi':edydiF,
            'playn':playnF,
            'remmi':remmiF}

print('Second thread creating...')
WriteFirst()
print('Checking for update...')
uptxt = open(PATH1 + 'update','r').readlines()
if uptxt:
    ids = os.listdir(PATH1)
    pkls = filter(lambda x: x.endswith('.pkl'), ids) 
    for idd in ids:
        if idd[:2].isdigit():
            uidd = idd[:-4]
            newmes(uidd,uptxt,k.MKey)
    open(PATH1+'update','w').writelines('')
    print('Update information send')
else:
    print('No updates')

print('System is ready')
while True:#ПОЛУЧАЕМ НОВЫЕ СООБЩЕНИЯ В ЦИКЛЕ
    try:
        for event in longpoll.listen():
            if event.to_me:
                if event.type == VkEventType.MESSAGE_NEW: 
                    formanswer(event.user_id,event.text)
    except:
        print('System fucked up with no reason (maybe internet)')
        time.sleep(15)
        print('SYSTEM RESTARTED')