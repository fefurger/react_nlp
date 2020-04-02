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
    taggedBefore = bf[:- max(10, len(bf))]
    for b in bf:#[- max(10, len(bf)):] :
        if b and not "<" in b :
            if isLocation(b) :
                location = True
                taggedBefore += ['<reference>{}</reference>'.format(b)]
                couples.append((b, ana))
            else :
                taggedBefore += [b]
    
    taggedAfter = []
    for a in af:#[:min(10, len(af))] :
        if a and not "<" in a :
            if isLocation(a) :
                location = True
                taggedAfter += ['<reference>{}</reference>'.format(a)]
                couples.append((a, ana))
            else :
                taggedAfter += [a]
    taggedAfter += af[min(10, len(af)):]
        
    if location :
        ana = "<anaphore>"+ana+"</anaphore> "
        
    return taggedBefore + [ana] + taggedAfter, couples


def get_context(anas, text): 
    test_tag = copy.copy(text)
    print('test_tag')
    print(test_tag)
    print('TexT')
    print(text)
    count = 0
    couples = []
    for ana in list(set(anas)):
        count += 1
        splited = test_tag.split(ana)
        split_len = len(splited)
        print(str(count) + '/' +str(len(anas)))
        taggedText = ''
        for i in range(split_len-1):
            sB = splited[i].split(' ')
            sA = splited[i+1].split(' ')
            sepB = - min(10, len(sB))
            sepA = min(10, len(sA))
            pronom, tmpCouples = around(ana, sB[sepB:], (sA[:sepA]))
            couples += tmpCouples
            taggedText += ' '.join(sB[:sepB] + pronom)
            if i+2 == split_len :
                taggedText += ' '.join(sA[sepA:])
            else :
                splited[i+1] = ' '.join(sA[sepA:])
        
        if taggedText :
            test_tag = copy.copy(taggedText)
    print('TT', taggedText)
        
    return test_tag, couples