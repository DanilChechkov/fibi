import random
from keysFi import SKey

def formdict(lvev,language,chkt,SDict,i=0):
    cdict = []
    for lang in SDict:
        if language in SDict.keys(): 
            lang = language
        FDict = SDict[lang][:]
        if chkt == 2:
            random.shuffle(FDict)
        for wpair in enumerate(FDict[::-1]):
            if i and i == wpair[0]:break
            elem = wpair[1][::1] if lvev == 1 else wpair[1][::-1]
            elem.append(lang)
            cdict.append(elem)
        if language in SDict.keys():break
    return cdict

def startgame(ud):
    random.shuffle(ud['cdict'])
    ud['stlen'] = len(ud['cdict'])
    ud['wansw'] = 0
    ud['wdict'] = []
    ud['act'] = ['playn',3]
    out = 'Хорошо, я начинаю: %s (%s). Всего слов: %d'%(ud['cdict'][0][0],ud['cdict'][0][2],ud['stlen'])
    key =  SKey
    return ud, out, key