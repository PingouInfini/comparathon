import base64
import logging
import os
from json import dumps

from kafka import KafkaProducer

import variables

kafka_port = variables.KAFKA_PORT
kafka_url = variables.KAFKA_URL

topic_to_fill_pictures = variables.TOPIC_TO_FILL_PICTURES
topic_to_fill_urls = variables.TOPIC_TO_FILL_URLS
topic_to_fill_hit = variables.TOPIC_TO_FILL_HIT
# assemblage de l'adresse de Kafka
kafka_endpoint = kafka_url + ":" + kafka_port

crazy_producer = KafkaProducer(bootstrap_servers=[kafka_endpoint], value_serializer=lambda x: dumps(x).encode('utf-8'))


def send_filtered_pictures(filtered_dir, bio_id):
    for file in os.listdir(filtered_dir):
        fname, fext = os.path.splitext(file)
        file_type_point = "image/" + str(fext).replace(".", "")
        try:
            image = picture_evolution(filtered_dir + "/" + file)
            picture = {
                'name': fname,
                'extension': file_type_point,
                'image': image
            }

            crazy_producer.send(topic_to_fill_pictures, value=(picture, bio_id))
            logging.info("Envoi de l'image < " + fname + " > dans la file Kafka : " + topic_to_fill_pictures)

        except Exception as e:
            logging.error(e)


def send_rawdata(bio_id, msg, hit):
    msg['urlsResults']['hit'] = hit
    try:
        crazy_producer.send(topic_to_fill_hit, value=(bio_id, msg))
        logging.info("Envoi des résultats dans la file kafka : " + topic_to_fill_hit)

    except Exception as e:
        logging.error(e)


def send_source_urls(urls_list, bio_id):
    with open(urls_list, "r") as urls_txtfile:
        urls = []
        for url in urls_txtfile:
            urls.append(url.rstrip("\n"))
        try:
            crazy_producer.send(topic_to_fill_urls, value=(urls, bio_id))
            logging.info("Envoi de l'url <" + str(urls) + " > dans la file : " + topic_to_fill_urls)
        except Exception as e:
            logging.error(e)


def picture_evolution(picture_path):
    with open(picture_path, "rb") as image:
        f = image.read()
    b = bytearray(f)
    bytified_picture = base64.b64encode(b).decode('UTF-8')
    return bytified_picture
