import os

#Import des variables d'environnement de la brique dockerisée

#Gestion des files Kafka
KAFKA_URL = str(os.environ["KAFKA_URL"])
KAFKA_PORT = str(os.environ["KAFKA_PORT"])
TOPIC_TO_CONSUME = str(os.environ["TOPIC_TO_CONSUME"])
TOPIC_TO_FILE = str(os.environ["TOPIC_TO_FILE"])

#Paramètres de fonctionnement de la brique
DEBUG_LEVEL = str(os.environ["DEBUG_LEVEL"])
PICTURES_NUMBER_TO_DOWNLOAD = str(os.environ["PICTURES_NUMBER_TO_DOWNLOAD"])
TOLERANCE=str(os.environ["TOLERANCE"])