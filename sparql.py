from SPARQLWrapper import SPARQLWrapper, JSON
import copy

#La langue influe sur la labellisation des objets
ENDPOINT = "http://fr.dbpedia.org/sparql"
sparql = SPARQLWrapper(ENDPOINT)


def filterPunctuation(text) :
    output = copy.copy(text)
    punctuations = ["\n", "!","\"","#","$","%","&","'","(","*","+",","," ","-",".","/",":",";","<","=",">","?","@","[","\\","]","^","_","`","{","|","}","~", ")"]
    for p in punctuations :
        output = output.replace(p, ' ')
    return output


def isLocation(location):
    location = filterPunctuation(location)
    if '_' not in location:
        location = '_'.join(word.capitalize() for word in location.split())

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
    
    try:
        ret = int(results['results']['bindings'][0]['isloc']['value'])
    except:
        import sys
        print('Warning: could not retrieve result. Returning False as precaution')
        print(sys.exc_info()[1])
        ret = 0

    return ret > 0

def scanaphore(anaphore) :
    output = []
    
    if len(anaphore['env'].split("'")) == 1 :
        for word in anaphore['env'] :
            if isLocation(word) :
                output.append([anaphore['anaphore'], word])
        if len(output) > 1 :
            print("Multiple possible references for ")
            print(anaphore)
            print(output)
        elif not output :
            return output
        
    return output[0]