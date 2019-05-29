from kafka import KafkaConsumer
import json
import variables
import logging
import comparathon
import base64
import os
import threading

kafka_port = variables.KAFKA_PORT
kafka_url = variables.KAFKA_URL
topic_to_consume = variables.TOPIC_TO_CONSUME

pic_number = variables.PICTURES_NUMBER_TO_DOWNLOAD

# assemblage de l'adresse de Kafka
kafka_endpoint = kafka_url + ":" + kafka_port


# Consommateur de la file Kafka from Housthon

class vierundneunzig_Verbraucher(threading.Thread):
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=kafka_endpoint,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 auto_offset_reset='latest')
        consumer.subscribe([topic_to_consume])
        logging.debug("Consume datas from topic :" + str(topic_to_consume))
        logging.info("CONSUMER : waiting for data")

        # Consommation du topic
        for msg in consumer:
            logging.info("## Trying to eat first kafka data ##")
            nom = msg.value[0]
            prenom = msg.value[1]
            bytified_picture = msg.value[2]
            picture_extension = msg.value[3]
            bio_id = msg.value[4]
            logging.info("## Consume data associated to bio_Id n° : " + str(bio_id) + " ##")

            # Assemblage pour recherche google
            person_names = nom + " " + prenom

            # Création du dossier personnalisé du candidat où sont stockées les images (ref & downloaded)
            os.mkdir(os.getcwd() + "pictures/" + "{}_{}".format(nom, prenom))
            path_to_person_dir = os.getcwd() + "pictures/" + "{}_{}".format(nom, prenom) + "/"
            path_to_person_image = path_to_person_dir + "{}_{}_image".format(nom, prenom) + ".{}".format(
                picture_extension)

            # Decodage de l'image bytifiée transmise dans la file Kafka et enregistrement dans le dossier perso
            with open(path_to_person_image) as picture_file:
                logging.DEBUG("## Trying of decode and save bytified picture ##")
                picture_file.write(base64.decodebytes(bytified_picture))

            # Appel de la fonction qui télécharge des images depuis Google et les compare à la photo de la personne
            comparathon.get_relative_images_and_url(person_names, path_to_person_image, path_to_person_dir, pic_number)

        consumer.close()
        logging.info("CONSUMER CLOSING")
