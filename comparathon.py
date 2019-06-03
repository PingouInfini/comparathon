import json
import logging
import os
import shutil

import face_recognition

import google.googleimages as googleimages
from variables import TOLERANCE as tolerance
import custom_producers


# Méthode centrale qui lance les méthodes de comparaison des images et d'extraction des URL, puis celles d'envoi dans les files Kafka
def get_relative_images_and_url(person_names, path_to_person_image, path_to_person_dir, pic_number, bio_id):
    filtered_dir = path_to_person_dir + "/filtered_pictures"
    potential_pic_dir = path_to_person_dir + "/potential_pics"
    json_path = path_to_person_dir + "/{}.json".format(person_names)
    urls_list = path_to_person_dir + "/source_urls_{}.txt".format(person_names)

    # Création des dossiers qui contiendront les images téléchargées, les images validées et le json des urls
    if os.path.isdir(filtered_dir) == False:
        os.mkdir(filtered_dir)
        logging.info("création du dossier des images filtrées")
    if os.path.isdir(potential_pic_dir) == False:
        os.mkdir(potential_pic_dir)
        logging.info("création du dossier des images à trier")

    # Récupération des images depuis Google avec les nom + prénom, enregistrement dans dossier
    my_args = {"keywords": person_names, "limit": pic_number,
               "extract_metadata": True,
               "output_directory": potential_pic_dir,
               "metadata_directory": path_to_person_dir,
               "type": "photo"
               }

    googleimages.get_images_from_arguments(my_args)

    # Filtre des images depuis le dossier rempli ci-dessus
    source_dir = potential_pic_dir + "/" + person_names
    fill_results_dir_with_valid_pictures(path_to_person_image, source_dir, filtered_dir)

    # Extraction des urls associées aux images validées
    extract_urls_from_json(json_path, filtered_dir, urls_list)

    # Envoi des images dans la file Kafka
    custom_producers.send_filtered_pictures(filtered_dir, bio_id)

    # Envoi des url sources des images sélectionnées dans la file Kafka
    custom_producers.send_source_urls(urls_list, bio_id)


# Parcours le dossier des images téléchargées et enregistre dans un dossier les images filtrées validées
def fill_results_dir_with_valid_pictures(path_to_person_image, source_dir, filtered_dir):
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

                if results[0] == True:
                    shutil.copy2(os.path.join(source_dir, picture), filtered_dir)
                    logging.info("Candidat reconnu sur l'image. Sauvegarde de l'image dans " + filtered_dir)

            except Exception as e:
                logging.error(e)

    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")


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
