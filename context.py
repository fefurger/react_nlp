# from nltk import word_tokenize
from do_concord import isLocation
import copy

def read_text(textPath):
    print('TP', textPath)
    with open(textPath, 'r') as tmp:
        text = tmp.read()
        print(text)
        text = text.replace('\r', '')
        return text

def around(ana, bf, af):
    couples = []
    location = False
    # taggedBefore = bf[:- min(10, len(bf))]
    for b in bf[:- min(10, len(bf))] :
        if isLocation(b) :
            location = True
            # taggedBefore += ['<reference>{}</reference>'.format(b)]
            couples.append((b, ana))
        # taggedBefore += [b]
    
    # taggedAfter = []
    for a in af[:min(10, len(af))] :
        if isLocation(a) :
            location = True
            # taggedAfter += ['<reference>{}</reference>'.format(a)]
            couples.append((a, ana))
        # taggedAfter += [a]
    # taggedAfter += af[min(10, len(af)):]
        
    if location :
        ana = "<anaphore>"+ana+"</anaphore> "
        
    return bf + [ana] + af, couples
    


def get_context(anas, text): 
    test_tag = copy.copy(text)
    count = 0
    couples = []
    for ana in list(set(anas)):
        count += 1
        splited = test_tag.split(' '+ana+' ')
        split_len = len(splited)
        print(str(count) + '/' +str(len(list(set(anas)))))
        taggedText = ''
        for i in range(split_len-1):
            sB = splited[i][-min(200, len(splited[i])):].split(' ')
            sA = splited[i+1][:min(200, len(splited[i+1]))].split(' ')
            sepB = - min(10, len(sB))
            sepA = min(10, len(sA))
            pronom, tmpCouples = around(ana, sB[sepB:], (sA[:sepA]))
            couples += tmpCouples
            taggedText += splited[i]+' '.join(pronom)
            if i+2 == split_len :
                taggedText += splited[-1]
        
        if taggedText :
            test_tag = copy.copy(taggedText)
        
    return test_tag, couples