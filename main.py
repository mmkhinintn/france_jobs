import logging
import os
from datetime import datetime
from api.api_france_job import FranceEmploi


# Configurer les logs
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = datetime.now().strftime("%Y_%m_%d-%H_%M-%S-france_emploi.log")
log_file_full_name = os.path.join(log_dir, log_file)

logging.basicConfig(
    filename=log_file_full_name,
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

# Créer un gestionnaire de flux (console) et définir le niveau à DEBUG
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Créer un formatteur pour la console
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Ajouter le formatteur au gestionnaire de flux
ch.setFormatter(formatter)

# Ajouter le gestionnaire de flux au logger
logger = logging.getLogger(__name__)
logger.addHandler(ch)

# 🔹 Exécution du script
if __name__ == "__main__":
    try:
        logger.info("Début du processus.")
        france_emploi = FranceEmploi()
        offres = france_emploi.fetch_offers()
        france_emploi.process_and_save(offres)
        logger.info("Processus terminé avec succès.")
    except Exception as e:
        logger.error(f"Une erreur est survenue : {e}")
