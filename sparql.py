from SPARQLWrapper import SPARQLWrapper, JSON
import copy

#La langue influe sur la labellisation des objets
ENDPOINT = "http://fr.dbpedia.org/sparql"
sparql = SPARQLWrapper(ENDPOINT)

_COUNT = 0


# Returns the text without the punctuation
def filterPunctuation(text) :
    output = copy.copy(text)
    punctuations = ["\n", "!","\"","#","$","%","&","'","(","*","+",","," ","-",".","/",":",";","<","=",">","?","@","[","\\","]","^","_","`","{","|","}","~", ")"]
    for p in punctuations :
        output = output.replace(p, ' ')
    return output


# Returns a boolean, True if the location is in dbpedia
def isLocation(location):
    location = filterPunctuation(location)
    
    try :
        sparql.setQuery("""
            SELECT ?isloc
            WHERE {{
                BIND(EXISTS {{
                    dbpedia-fr:{} rdf:type dbpedia-owl:Location
                }} AS ?isloc) .
            }}
        """.format(location))
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except :
        return False
    
    try:
        ret = int(results['results']['bindings'][0]['isloc']['value'])
    except:
        import sys
        print('Warning: could not retrieve result. Returning False as precaution')
        print(sys.exc_info()[1])
        ret = 0
        
    return ret > 0


#Return : taggedText : "text<pronom>text", couples : [(location, pronoun)]
def around(pronoun, beforePronoun, afterPronoun):
    couples = []
    location = False
    
    # Verify if each word is a Location via SPARQL
    for bp in beforePronoun : 
        if len(bp)>2 and isLocation(bp) :
            location = True
            #If it's a location we have a new couple (location, pronoun)
            couples.append((bp, pronoun))
    
    for ap in afterPronoun :
        if len(ap)>2 and isLocation(ap) :
            location = True
            couples.append((ap, pronoun))
        
    if location : #pronoun must be TAGGED
        pronoun = "<pronom>"+pronoun+"</pronom> "
        
    return beforePronoun + [pronoun] + afterPronoun, couples


def counter() :
    global _COUNT
    _COUNT+=1
    return _COUNT


#Return taggedText : "text<pronoun>text", couples : [(location, pronoun)]
def searchLocation(pronouns, text): 
    print("Searching Locations ...")
    taggedText = copy.copy(text)
    couples = []
    
    pronouns = list(set(pronouns))
    for p in pronouns: #For each distinct pronoun p
        splitedText = taggedText.split(' '+p+' ') # Split the text
        split_len = len(splitedText)
        _COUNT = 0
        
        print('\t'+str(counter())+'/'+str(len(pronouns))+' pronouns - ('+p+')')
        
        tmpTaggedText = ''
        for i in range(split_len-1): # For each pronoun p found in text
            print('\t\t'+str(i+1)+'/'+str(split_len)+' candidates')
            
            #Get environement : 10 words in 200 caracteres before and after 
            beforPronoun = splitedText[i][-min(200, len(splitedText[i])):].split(' ')
            afterPronoun = splitedText[i+1][:min(200, len(splitedText[i+1]))].split(' ')
            sepB = - min(10, len(beforPronoun))
            sepA = min(10, len(afterPronoun))
            
            pronoun, tmpCouples = around(p, beforPronoun[sepB:], afterPronoun[:sepA])
            
            couples += tmpCouples
            tmpTaggedText += splitedText[i]+' '.join(pronoun) #Add the pronoun and the text before
            
            if i+2 == split_len :#If it's the last pronoun, add the texte after it
                tmpTaggedText += splitedText[-1] 
                
        print('')
        
        if tmpTaggedText : #update tagged text with new pronoun tagged
            taggedText = copy.copy(tmpTaggedText)
        
    return taggedText, couples