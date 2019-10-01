from kafka import KafkaProducer
import json
import logging
from time import sleep

from argparse import ArgumentParser

parser = ArgumentParser(description='Bouchon Comparathon')

parser.add_argument("-v", "--verbosity", action="store_true", help="show debug logs")

options = parser.parse_args()


def main():
    try:
        logging.basicConfig(level=logging.INFO)
        if options.verbosity:
            logging.getLogger().setLevel(logging.DEBUG)

        logging.info(" Démarrage du bouchon ")

        producer = KafkaProducer(bootstrap_servers='localhost:8092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        tab = [
            { 'biographics' : {
                'idBio': '123451',
                'nom': 'Damien',
                'prenom': 'Bonnal'
            },
                'urlsResults': {
                    'url': 'https://www.nouvelobs.com/politique/20170710.OBS1881/les-presidents-et-le-sport-chirac-l'
                        '-homme-qui-aimait-trop-le-sumo.html',
                    'listUrlImage': ['https://media.nouvelobs.com/ext/uri/ureferentiel.nouvelobs.com/file/16156259.jpg',
                                  'https://media.nouvelobs.com/referentiel/633x306/16149075.jpg',
                                  'https://i.rugbyrama.fr/2017/06/25/2115412-44265450-2560-1440.jpg?w=1750',
                                  'https://images.ladepeche.fr/api/v1/images/view/5c3755243e45462be86730ae/large/image.jpg'],
                    'frequence': 1,
                    'themeMotclefHit': ['sport.rugby'],
                    'imageHit': 0
                }
             }
        ]

        for i in range(len(tab)):
            producer.send('scrapyToCompara', value=tab[i])
            sleep(0.5)

    except Exception as e:
        logging.error("ERROR : ", e)
    finally:
        logging.info(" Fin du bouchon ")
        exit(0)


if __name__ == '__main__':
    main()
