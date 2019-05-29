import custom_consumer
import logging
import variables

# Gestion du niveau de criticité des logs

debug_level = variables.DEBUG_LEVEL

if debug_level == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)
elif debug_level == "INFO":
    logging.basicConfig(level=logging.INFO)
elif debug_level == "WARNING":
    logging.basicConfig(level=logging.WARNING)
elif debug_level == "ERROR":
    logging.basicConfig(level=logging.ERROR)
elif debug_level == "CRITICAL":
    logging.basicConfig(level=logging.CRITICAL)

# Lancement de la brique comparathon

if __name__ == '__main__':
    thread = custom_consumer.vierundneunzig_Verbraucher()
    thread.start()
