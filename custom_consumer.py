
import json
import logging
import os
import threading
import requests
from ftplib import FTP
import re
import uuid

from kafka import KafkaConsumer

import comparathon
import variables

kafka_port = variables.KAFKA_PORT
kafka_url = variables.KAFKA_URL
topic_to_consume = variables.TOPIC_TO_CONSUME

# pic_number = variables.PICTURES_NUMBER_TO_DOWNLOAD

# assemblage de l'adresse de Kafka
kafka_endpoint = kafka_url + ":" + kafka_port


# Consommateur de la file Kafka from Scrapython

class vierundneunzig_Verbraucher(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')
        consumer.subscribe(topic_to_consume)
        logging.info("Consume datas from topic :" + str(topic_to_consume))
        logging.info("CONSUMER : waiting for data")
        home_path = os.getcwd()

        # Consommation du topic
        for msg in consumer:
            msg = msg.value
            logging.info("## Trying to eat first kafka data ##")

            idBio = msg['biographics'].get('idBio')
            extension = 'jpeg'
            listUrlImage = msg['urlsResults'].get('listUrlImage')
            img_name = idBio+"."+extension

            logging.info("## Consume data associated to bio_Id n° : " + str(idBio) + " ##")

            path_idBioDir = os.getcwd() + "/results/" + "{}".format(idBio)
            path_to_person_image = path_idBioDir + "/" + img_name

            if not (os.path.isdir(path_idBioDir)):
                logging.info("Création du dossier racine du candidat")
                os.makedirs(path_idBioDir)

                # ftp = FTP(os.environ['FTP_ADDR'])
                # ftp.login(os.environ['FTP_ID'], os.environ['FTP_PASSWORD'])
                # ftp.cwd(os.environ['FTP_PATH'])
                ftp = FTP("192.168.0.9")
                ftp.login("nimir", "@soleil1")
                ftp.cwd("dev/ftp")

                # if os.path.exists(path_to_person_image):
                #     logging.info("suppression de la photo pre-existante")
                #     os.remove(path_to_person_image)
                os.chdir(os.getcwd() + "/results/"+idBio)
                ftp.nlst()
                ftp.retrbinary('RETR '+img_name, open(img_name, 'wb').write)
            else:
                os.chdir(os.getcwd() + "/results/"+idBio)

            path_source_dir = path_idBioDir + "/potential_pics"
            if not (os.path.isdir(path_source_dir)):
                logging.info("Creating source directory")
                os.makedirs(path_source_dir)
            os.chdir(path_source_dir)

            logging.info("création de la photo du candidat:  " + str(path_to_person_image))

            for urlImage in listUrlImage:
                try:
                    extension = re.search("\.[0-9A-Za-z]+$", urlImage).group(0)
                    imageFileName = str(uuid.uuid4()) + extension
                    get_media_url(imageFileName, urlImage)
                except Exception as e:
                    logging.error(e)

            # Appel de la fonction qui télécharge des images depuis Google et les compare à la photo de la personne
            comparathon.get_relative_images_and_url (path_to_person_image, path_idBioDir, msg)
            os.chdir(home_path)
        consumer.close()
        logging.info("Fermeture du consumer")


def get_media_url(imageFileName, media):
    logging.debug("getting media url...")
    url = re.compile("^((http|https):\/\/|(www\.|ftp\.))")
    if not url.search(media):
        media = "http://" + media
    with open(str(imageFileName), 'wb') as handle:
        try:
            response = requests.get(media, stream=True)

            if not response.ok:
                logging.error(response)

            else:
                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
        except Exception as e:
            logging.error(e)


"""
Tests if the source directory doesn't contain a json or an image (except processedData directory)
"""
def isSourceDirectoryEmpty(ftp):
    filelist = []
    ftp.retrlines('LIST', filelist.append)
    return len(filelist) == 1

"""
Tests if the given directory exists 
"""
def directory_exists(directory, ftp):
    filelist = []
    ftp.retrlines('LIST', filelist.append)
    for f in filelist:
        if f.split()[-1] == directory and f.upper().startswith('D'):
            return True
    return False


"""
Create a given directory
"""
def crdir(dir, ftp):
    if len(dir.rsplit("/", 1)) == 2:
        ftp.cwd(dir.rsplit("/", 1)[0])
        dir = dir.rsplit("/", 1)[1]
    if directory_exists(dir, ftp) is False:  # (or negate, whatever you prefer for readability)
        ftp.mkd(dir)

