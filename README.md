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

    Fuck you !
