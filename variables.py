import os

#Import des variables d'environnement de la brique dockerisée

#Gestion des files Kafka
# KAFKA_URL = str(os.environ["KAFKA_IP"])
# KAFKA_PORT = str(os.environ["KAFKA_PORT"])
# TOPIC_TO_CONSUME = str(os.environ["TOPIC_TO_CONSUME"])
# TOPIC_TO_FILL_PICTURES = str(os.environ["TOPIC_TO_FILL_PICTURES"])
# TOPIC_TO_FILL_URLS = str(os.environ["TOPIC_TO_FILL_URLS"])
# TOPIC_TO_FILL_HIT = str(os.environ["TOPIC_TO_FILL_HIT"])

KAFKA_URL = '192.168.0.10'
KAFKA_PORT = '8092'
TOPIC_TO_CONSUME = 'scrapyToCompara'
TOPIC_TO_FILL_PICTURES = 'ggimgToColissi'
TOPIC_TO_FILL_URLS = ''
TOPIC_TO_FILL_HIT = 'comparaToColissi'

#Paramètres de fonctionnement de la brique
# DEBUG_LEVEL = str(os.environ["DEBUG_LEVEL"])
# PICTURES_NUMBER_TO_DOWNLOAD = str(os.environ["PICTURES_NUMBER_TO_DOWNLOAD"])
# TOLERANCE= os.environ["TOLERANCE"]

DEBUG_LEVEL = "INFO"
PICTURES_NUMBER_TO_DOWNLOAD = ''
TOLERANCE= "0.6"