from nltk import word_tokenize

def read_text(text):
    with open(text, 'r', encoding='utf-8') as tmp:
        text = tmp.read().replace('\n', '')
        return text

def around(bf, af):
    words = []
    before = word_tokenize(bf)
    after = word_tokenize(af)
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

    return words

def get_context(anas, text):
    context_words = []
    previous = []
    for ana in anas:
        if ana not in previous:
            tx = text
            splited = tx.split(ana)
            for i in range(len(splited)-1):
                words = around(splited[i], splited[i+1])
                context_words.append({
                    "anaphore": ana,
                    "env": words
                })
            if ana not in previous:
                previous.append(ana)
    return context_words



