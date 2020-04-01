from SPARQLWrapper import SPARQLWrapper, JSON


#La langue influe sur la labellisation des objets
ENDPOINT = "http://fr.dbpedia.org/sparql"
sparql = SPARQLWrapper(ENDPOINT)


def isLocation(location):
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