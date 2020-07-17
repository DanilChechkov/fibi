from vk_api.keyboard import VkKeyboard, VkKeyboardColor

addW, shwL = 'Пополнить словарь', 'Мой словарь'
chwL = 'Проверь слова, Фиби!=)'
remL,relL = 'Напомни', 'Мои напоминания'
edyL = 'Редактировать'
#Mainkeyboard
MKey = VkKeyboard(one_time=False)
MKey.add_button(addW,color=VkKeyboardColor.POSITIVE)
MKey.add_button(shwL,color=VkKeyboardColor.POSITIVE)
MKey.add_line()
MKey.add_button(chwL,color=VkKeyboardColor.POSITIVE)
MKey.add_line()
MKey.add_button(remL,color=VkKeyboardColor.POSITIVE)
MKey.add_button(relL,color=VkKeyboardColor.POSITIVE)
MKey.add_line()
MKey.add_button(edyL,color=VkKeyboardColor.NEGATIVE)
#Backkeyboard
gatB = 'Вернуться назад'
SKey = VkKeyboard(one_time=False)
SKey.add_button(gatB,color=VkKeyboardColor.NEGATIVE)
#Editkeyboard
chaN, edyD = 'Моё имя', 'Название словаря'
addL, delL = 'Добавить язык','Удалить язык'
delW = 'Удалить слово'
EKey = VkKeyboard(one_time=False)
EKey.add_button(chaN,color=VkKeyboardColor.POSITIVE)
EKey.add_button(edyD,color=VkKeyboardColor.POSITIVE)
EKey.add_line()
EKey.add_button(addL,color=VkKeyboardColor.POSITIVE)
EKey.add_button(delL,color=VkKeyboardColor.NEGATIVE)
EKey.add_line()
EKey.add_button(addW,color=VkKeyboardColor.POSITIVE)
EKey.add_button(delW,color=VkKeyboardColor.NEGATIVE)
EKey.add_line()
EKey.add_button(gatB,color=VkKeyboardColor.NEGATIVE)
#Checking type keyboard
lovL,evoL = 'Любовь-Love','Love-Любовь'
CTKey = VkKeyboard(one_time=False)
CTKey.add_button(lovL,color=VkKeyboardColor.POSITIVE)
CTKey.add_button(evoL,color=VkKeyboardColor.POSITIVE)
CTKey.add_line()
CTKey.add_button(gatB,color=VkKeyboardColor.NEGATIVE)

lsnL,ranL = 'Последние n','Случайные n'
allL = 'Все слова'
CT2Key = VkKeyboard(one_time=False)
CT2Key.add_button(lsnL,color=VkKeyboardColor.POSITIVE)
CT2Key.add_button(ranL,color=VkKeyboardColor.POSITIVE)
CT2Key.add_line()
CT2Key.add_button(allL,color=VkKeyboardColor.POSITIVE)
CT2Key.add_line()
CT2Key.add_button(gatB,color=VkKeyboardColor.NEGATIVE)
yeL,noL = 'Да','Нет'
YNKey = VkKeyboard(one_time=False)
YNKey.add_button(yeL,color=VkKeyboardColor.POSITIVE)
YNKey.add_button(noL,color=VkKeyboardColor.NEGATIVE)
todL,tomL = 'Сегодня','Завтра'
REKey = VkKeyboard(one_time=False)
REKey.add_button(todL,color=VkKeyboardColor.POSITIVE)
REKey.add_button(tomL,color=VkKeyboardColor.POSITIVE)
REKey.add_line()
REKey.add_button(gatB,color=VkKeyboardColor.NEGATIVE)

def buildkey(type0,langs):
    keyboard = VkKeyboard(one_time=False)
    for x in enumerate(langs):
        if x[0]%2==0 and x[0]>1: keyboard.add_line()
        keyboard.add_button(x[1],color=VkKeyboardColor.POSITIVE)
    if not type0:
        keyboard.add_line()
        keyboard.add_button('Проверь по всем',color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(gatB,color=VkKeyboardColor.NEGATIVE)
    return keyboard