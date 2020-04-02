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