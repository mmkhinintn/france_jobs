import os
import requests
import pandas as pd
import logging
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configurer le logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class FranceEmploi:
    client_id: str = os.getenv("CLIENT_ID")
    client_secret: str = os.getenv("CLIENT_SECRET")
    base_url: str = "https://api.francetravail.fr/v1/offres"
    token: str = None

    def authenticate(self):
        """Récupère le token d'authentification OAuth2."""
        try:
            logger.info("Tentative d'authentification...")
            url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
                "scope": "api_offresdemploiv2 o2dsoffre",
            }
            response = requests.post(url, data=data)
            response.raise_for_status()
            self.token = response.json().get("access_token")
            logger.info("Authentification réussie.")
        except Exception as e:
            logger.error(f"Erreur lors de l'authentification : {e}")
            raise

    def fetch_offers(self, departement: str = "07") -> List[Dict]:
        """Récupère les offres d'emploi en CDI pour un département donné."""
        if not self.token:
            self.authenticate()

        try:
            logger.info(
                f"Récupération des offres pour le département {departement}..."
            )
            headers = {"Authorization": f"Bearer {self.token}"}
            params = {
                "typeContrat": "CDI",
                "departement": departement,
            }
            url = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search"
            response = requests.get(
                url,
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            offres = response.json().get("resultats", [])
            logger.info(f"{len(offres)} offres récupérées.")
            return offres
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des offres : {e}")
            raise

    def process_and_save(self, offers: List[Dict]):
        """Traite les offres et sauvegarde les données dans des fichiers CSV."""
        try:
            logger.info(
                "Traitement des données et sauvegarde dans des fichiers CSV..."
            )

            # Offres d'emploi
            df_offres = pd.DataFrame(
                [
                    {key: offre.get(key, "Non spécifié") for key in offre}
                    for offre in offers
                ]
            )
            df_offres.to_csv(
                "offres_emploi.csv",
                index=False,
                encoding="utf-8",
            )
            logger.info("Fichier 'offres_emploi.csv' créé.")

            # Entreprises (évite les doublons)
            df_entreprises = pd.DataFrame(
                [
                    {
                        key: offre.get("entreprise", {}).get(key, "Non précisé")
                        for key in offre.get("entreprise", {})
                    }
                    for offre in offers
                ]
            ).drop_duplicates()
            df_entreprises.to_csv(
                "entreprises.csv",
                index=False,
                encoding="utf-8",
            )
            logger.info("Fichier 'entreprises.csv' créé.")

            # Compétences (évite les doublons)
            competences = [
                {key: comp.get(key, "Non spécifié") for key in comp}
                for offre in offers
                for comp in offre.get("competences", [])
                if comp.get("code")
            ]
            df_competences = pd.DataFrame(competences)
            df_competences.to_csv(
                "competences.csv",
                index=False,
                encoding="utf-8",
            )
            logger.info("Fichier 'competences.csv' créé.")

            logger.info("Tous les fichiers CSV ont été créés avec succès.")

        except Exception as e:
            logger.error(
                f"Erreur lors du traitement et de l'enregistrement des fichiers : {e}"
            )
            raise
