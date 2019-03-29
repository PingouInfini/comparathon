# Comparathon

## Prerequis
Installation des libs nécessaires

    pip install -r requirements.txt
    
## Usage


    comparathon.py "<candidate>" "<path_to_94A_photo.jpg>"

## Résultats

A l'issue : 
- téléchargement des images google dans **mesimages\\\<candidate>**
- fichier des urls associées dans **mesjson\\\<candidate>.json**
- stockage des images filtrées dans **filteredpictures\\\<candidate>**
- enregistrement des urls filtrées à la racine dans **Associated_Urls_to\<candidate\>.txt**
