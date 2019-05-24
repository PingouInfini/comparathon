# Comparathon

## Prerequis
Installation des libs nécessaires

    sudo apt-get -y install cmake
    pip install -r requirements.txt
    
## Usage


    comparathon.py "<candidate>" "<path_to_94A_photo.jpg>"

## Résultats

A l'issue : 
- téléchargement des images google dans **mesimages\\\<candidate>**
- fichier des urls associées dans **mesjson\\\<candidate>.json**
- stockage des images filtrées dans **filteredpictures\\\<candidate>**
- enregistrement des urls filtrées à la racine dans **Associated_Urls_to\<candidate\>.txt**


## Install DLIB for python3 (Big pain in the axx)

[https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf]

1. install linux packages from github.com/ageitgey/Dockerfile (ubuntu > 16.04)

       Warning!! libatlas-dev may be change to libatlas-base-dev (if asked)

2. Clone the code from github:

       git clone https://github.com/davisking/dlib.git
       
3. Build the main dlib library (optional if you just want to use Python):

       cd dlib
       mkdir build; cd build; cmake ..; cmake --build .
       
4. Build and install the Python extensions:

       cd ..
       sudo python3.6 setup.py install
       
***Si problème : créer à l'emplacement indiqué le dossier + fichier nécessaire 
puis relancer la commande***
       
5. At this point, you should be able to run python3 and type import dlib successfully.