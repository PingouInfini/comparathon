import json
import os
import face_recognition
import google.googleimages as googleimages
from variables import TOLERANCE as tolerance
import shutil


def get_relative_images_and_url(person_names, path_to_person_image, path_to_person_dir, pic_number):
    potential_pic_dir = path_to_person_dir + "potential_pics/"
    json_dir = path_to_person_dir + "json_dir/"
    filtered_dir = path_to_person_dir + "filtered_pictures/"

    # Création des dossiers qui contiendront les images téléchargées, les images validées et le json des urls
    os.mkdir(potential_pic_dir)
    os.mkdir(filtered_dir)
    os.mkdir(json_dir)

    # Récupération des images depuis Google avec les nom + prénom, enregistrement dans dossier
    my_args = {"keywords": person_names, "limit": pic_number,
               "extract_metadata": True,
               "output_directory": potential_pic_dir,
               "metadata_directory": path_to_person_dir,
               "type": "photo"
               }

    googleimages.get_images_from_arguments(my_args)

    # Filtre des images depuis le dossier rempli ci-dessus
    source_dir = potential_pic_dir + person_names
    fill_results_dir_with_valid_pictures(path_to_person_image, path_to_person_dir, source_dir, person_names)

    # Extraction des urls associées aux images validées
    json_path = json_dir + "{}.json".format(person_names)
    extract_urls_from_json(json_path, person_names)


# Parcours le dossier des images téléchargées et enregistre dans un dossier les images filtrées validées
def fill_results_dir_with_valid_pictures(path_to_person_image, path_to_person_dir, source_dir, filtered_dir):
    try:
        # Chemin de l'image de référence et préparation
        ref_image = face_recognition.load_image_file(path_to_person_image)

        ref_encoding = face_recognition.face_encodings(ref_image)[0]

        known_faces = [
            ref_encoding
        ]

        index = 0

        # Comparaison de chaque image candidate du dossier à l'image de référence, enregistrement si elle est validée
        for picture in os.listdir(source_dir):
            index += 1
            try:

                image = face_recognition.load_image_file(os.path.join(source_dir, picture))
                results = face_recognition.compare_faces(known_faces, face_recognition.face_encodings(image)[0],
                                                         tolerance)

                if results[0] == True:
                    shutil.copy2(os.path.join(source_dir, picture), filtered_dir)

            except:
                pass

    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        quit()


def extract_urls_from_json(json_path, candidate):
    filtered_dir = "filtered_pictures/{}".format(candidate)
    list_txt = "Associated_Urls_to{}.txt".format(candidate)
    try:
        with open(json_path) as json_file:
            metadatas = json.load(json_file)
            written_file = open(list_txt, "w")
            pictures_list = os.listdir(filtered_dir)
            for picture in pictures_list:
                for metadata in metadatas:
                    if (metadata['image_filename'] == picture):
                        written_file.write(metadata['image_source'] + '\n')
            written_file.close()
    except:
        quit()
