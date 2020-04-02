from do_concord import isLocation
import copy

_COUNT = 0

def read_text(textPath):
    with open(textPath, 'r') as tmp:
        text = tmp.read().replace('\r', '')
        return text


#Return : taggedText : "text<pronom>text", couples : [(location, pronoun)]
def around(pronoun, beforePronoun, afterPronoun):
    couples = []
    location = False
    
    for bp in beforePronoun : 
        if len(bp)>2 and isLocation(bp) :
            location = True
            couples.append((bp, pronoun))
    
    for ap in afterPronoun :
        if len(ap)>2 and isLocation(ap) :
            location = True
            couples.append((ap, pronoun))
        
    if location :
        pronoun = "<pronom>"+pronoun+"</pronom> "
        
    return beforePronoun + [pronoun] + afterPronoun, couples


def counter() :
    global _COUNT
    _COUNT+=1
    return _COUNT


#Return textTag : "texte<pronom>text", couples : [(location, pronoun)]
def get_context(anas, text): 
    test_tag = copy.copy(text)
    couples = []
    
    for ana in list(set(anas)):
        splited = test_tag.split(' '+ana+' ')
        split_len = len(splited)
        _COUNT = 0
        
        print(ana+' - '+str(counter())+'/'+str(len(list(set(anas)))))
        
        taggedText = ''
        for i in range(split_len-1):
            print('\t'+str(i)+'/'+str(split_len))
            sB = splited[i][-min(200, len(splited[i])):].split(' ')
            sA = splited[i+1][:min(200, len(splited[i+1]))].split(' ')
            sepB = - min(10, len(sB))
            sepA = min(10, len(sA))
            pronom, tmpCouples = around(ana, sB[sepB:], sA[:sepA])
            couples += tmpCouples
            taggedText += splited[i]+' '.join(pronom)
            if i+2 == split_len :
                taggedText += splited[-1]
        
        if taggedText :
            test_tag = copy.copy(taggedText)
        
    return test_tag, couples