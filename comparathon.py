import json
import logging
import os
import shutil

import face_recognition
import time

from variables import TOLERANCE as tolerance
import custom_producers


# Méthode centrale qui lance les méthodes de comparaison des images et d'extraction des URL, puis celles d'envoi dans
# les files Kafka à chaque msg kafka reçu
def get_relative_images_and_url(path_to_person_image, path_to_person_dir, msg):

    idBio = msg['biographics'].get('idBio')

    filtered_dir = path_to_person_dir + "/filtered_pictures"
    source_dir = path_to_person_dir + "/potential_pics"
    json_path = path_to_person_dir + "/{}.json".format(idBio)
    urls_list = path_to_person_dir + "/source_urls_{}.txt".format(idBio)

    # Création des dossiers qui contiendront les images validées
    if not os.path.isdir(filtered_dir):
        os.mkdir(filtered_dir)
        logging.info("création du dossier des images filtrées")

    hit = fill_results_dir_with_valid_pictures(path_to_person_image, source_dir, filtered_dir)
    msg['urlsResults']['imageHit'] = hit
    del msg['urlsResults']['listUrlImage']
    if hit != 0:
        ## Scoring
        msg['urlsResults']['points'] = msg['urlsResults']['points']*12
    # extract_urls_from_json(json_path, filtered_dir, urls_list)

    # renvoie le nombre de hit(filtered_picture) pour cette url

    rawdata_url_name = custom_producers.send_rawdata(idBio, msg)  # TODO modif list url (que url qui a hit)
    time.sleep(5)  # TODO à corriger
    custom_producers.send_filtered_pictures(filtered_dir, idBio, rawdata_url_name)  # TODO ajouter l'url de l'image
    shutil.rmtree(filtered_dir)
    shutil.rmtree(source_dir)


# Parcours le dossier des images téléchargées et enregistre dans un dossier les images filtrées validées
def fill_results_dir_with_valid_pictures(path_to_person_image, source_dir, filtered_dir):
    hit = 0

    try:
        # Chemin de l'image de référence et préparation
        ref_image = face_recognition.load_image_file(path_to_person_image)
        logging.info("Image de référence :" + path_to_person_image)

        ref_encoding = face_recognition.face_encodings(ref_image)[0]

        known_faces = [
            ref_encoding
        ]

        index = 0

        # Comparaison de chaque image candidate du dossier à l'image de référence, enregistrement si elle est validée
        for picture in os.listdir(source_dir):
            index += 1

            try:
                # potentielle image qui va être comparée à l'image de référence
                image = face_recognition.load_image_file(os.path.join(source_dir, picture))
                logging.info("Image potentielle comparée  :   " + os.path.join(source_dir, picture))
                results = face_recognition.compare_faces(known_faces, face_recognition.face_encodings(image)[0],
                                                         float(tolerance))

                if results[0]:
                    shutil.copy2(os.path.join(source_dir, picture), filtered_dir)
                    logging.info("Candidat reconnu sur l'image. Sauvegarde de l'image dans " + filtered_dir)
                    hit += 1

            except Exception as e:
                logging.error(e)  # la plupart du temps pas de visage reconnu

    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    return hit


def extract_urls_from_json(json_path, filtered_dir, urls_list):
    try:
        with open(json_path) as json_file:
            metadatas = json.load(json_file)
            written_file = open(urls_list, "w")
            pictures_list = os.listdir(filtered_dir)
            for picture in pictures_list:
                for metadata in metadatas:
                    if (metadata['image_filename'] == picture):
                        written_file.write(metadata['image_source'] + '\n')
                        logging.info("Ecriture d'URL source d'image validée à cet emplacement :   " + urls_list)
            written_file.close()
    except Exception as e:
        logging.error(e)
