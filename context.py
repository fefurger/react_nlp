from nltk import word_tokenize

def read_text(text):
    with open(text, 'r') as tmp:
        text = tmp.read().replace('\n', '')
        return text

def around(ana, bf, af):
    words = []
    before = bf.split(' ')
    after = af.split(' ')
    location = False
    if len(before)>10:
        for i in range(10):
            words.append(before[i])
    else:
        for b in before:
            words.append(b)
    if len(after)>10:
        for i in range(10):
            words.append(after[i])
    else:
        for a in after:
            words.append(a)
    taggedText = " <anaphore>"+ana+"</anaphore> "+af
    return words, taggedText


def get_context(anas, text):
    context_words = []
    previous = []
    test_tag = ''
    for ana in anas:
        taggedText = ''
        if ana not in previous:
            splited = text.split(ana)
            taggedText = splited[0]
            for i in range(len(splited)-1):
                words, tagged = around(ana, splited[i], splited[i+1])
                context_words.append({
                    "anaphore": ana,
                    "env": words
                })
                taggedText += tagged
            if ana not in previous:
                previous.append(ana)
        test_tag += taggedText
    return context_words, test_tag