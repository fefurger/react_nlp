## API REST

Pour lancer l'API Rest, depuis le dossier exécutez:

    pip install -r requirements.txt
    
    Linux : export FLASK_APP=rest.py & flask run
    Windows : set FLASK_APP=rest.py & flask run

Se rendre sur localhost:5000 pour accéder à l'iterface Swagger de l'API
Les routes sont également accessibles via simple curl si vous voulez tester depuis le terminal

## Requirements :
* Python 2.7 (independent from Anaconda)
* Unitex

## Hint :
If you don't want to run LD_LIBRARY_PATH=.. before running python
Run once the following command in terminal

    export LD_LIBRARY_PATH=path/to/libunitex.so
    export LD_LIBRARY_PATH=~/../../usr/local/libunitex.so #this could work on Linux

## Get Libraries :
    sudo apt-get install python-dev
    sudo apt-get install python-setuptools
    sudo apt-get install python-yaml

## Locate Unitex :
    UNITEX_INC=/path/to/unitex/Src/C++ python setup.py install

## Build Configuration File :
    cd examples
    LD_LIBRARY_PATH=.. python build-config-file.py -l French -d path/to/Unitex/French/ -o unitex.yaml ../config/unitex-template.yaml


## Examples :
To apply run application, run the script run.sh

* Linux :

    bash run.sh

* Windows :

## Routes Utilisables :
### Texts
|VERB|CURL|RESPONSE|
|----|----|----|
| POST | curl -X POST "http://localhost:5000/texts/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@textToAdd.txt;type=text/plain" | textToAdd.txt has been added
| GET | curl -X GET "http://localhost:5000/texts/" -H "accept: application/json" | [<br>  "texte1.txt",<br>  "texte2.txt"<br>  ] |
| PUT | curl -X PUT "http://localhost:5000/texts/textToUpdate.txt" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@newText.txt;type=text/plain" | "text updated" |
| DELETE | curl -X DELETE "http://localhost:5000/texts/textToDelete.txt" -H "accept: application/json" | "text deleted" |
### graphs
|VERB|PATH|RESPONSE|
|----|----|----|
| POST | curl -X POST "http://localhost:5000/graphs/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@graphToAdd.grf;type=text/plain" | "'graphToAdd.grf' has been added" |
| GET | curl -X GET "http://localhost:5000/graphs/" -H "accept: application/json" | [<br>  "graph1.grf",<br>...,<br>"graphN.grf"<br>  ] |
| PUT | curl -X PUT "http://localhost:5000/graphs/graphToUpdate.txt" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@newGraph.txt;type=text/plain" | "graph updated" |
| DELETE | curl -X DELETE "http://localhost:5000/graphs/graphToDelete.txt" -H "accept: application/json" | "graph deleted" |
### nlp
|VERB|PATH|RESPONSE|
|----|----|----|
| GET | curl -X GET "http://localhost:5000/nlp/graph.fst2&text.txt" -H "accept: application/json" | [<br>anaphore1 ,<br>... ,<br>anaphoreN<br>] |

## Scénarios
* Ajouter un texte et un graphe pour appliquer le deuxième sur le premier :

    POST texts/{text}
    POST graphs/{graph}
    GET nlp/{graph}&{text}

* Charger la liste des textes pour en mettre à jour un :

    GET texts/
    PUT texts/{text}

* Supprimer un graphe :

    DELETE graphs/{graph}