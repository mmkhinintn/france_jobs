# Projet France Jobs

## Description
Ce projet permet de récupérer, traiter et enregistrer des offres d'emploi en CDI depuis l'API de France Travail. Il inclut également des tests unitaires pour garantir le bon fonctionnement des méthodes utilisées.

## Structure du projet
```
/project_root
│
├── api/                        # Contient les classes liées à l'interaction avec l'API
│   ├── __init__.py             # Fichier d'initialisation du module API
│   └── api_france_job.py    # Classe pour interagir avec l'API France Emploi
│
├── tests/                      # Dossier pour les tests unitaires
│   ├── __init__.py             # Fichier d'initialisation des tests
│   └── test_france_job.py   # Tests unitaires pour les fonctionnalités API
│
├── logs/                       # Dossier pour les logs générés pendant l'exécution
│   └── file.log                 # Fichier de log pour les erreurs et autres informations
│
├── .github/                    # Dossier de configuration GitHub Actions
│   └── workflows/              # Contient la configuration de CI/CD pour GitHub Actions
│       └── ci.yml              # Fichier de configuration pour l'exécution des tests sur GitHub Actions
│
├── requirements.txt            # Liste des dépendances Python nécessaires pour le projet
├── .env                        # Fichier contenant les variables d'environnement (par exemple, CLIENT_ID, CLIENT_SECRET)
├── README.md                   # Documentation du projet
└── main.py                     # Point d'entrée du projet (facultatif selon le besoin)

```

## Installation
1. Cloner le dépôt :
   ```bash
   git clone https://github.com/mmkhinintn/france_jobs.git
   cd france_jobs
   ```
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation
### 1. Récupération des offres d'emploi
Le fichier `api_france_emploi.py` contient une classe `FranceEmploi` qui permet d'authentifier l'utilisateur, récupérer les offres d'emploi et les enregistrer sous format CSV.

Exemple d'utilisation :
```python
from api.api_france_job import FranceEmploi

france_emploi = FranceEmploi()
offers = france_emploi.fetch_offers()  # Récupérer les offres pour Paris
france_emploi.process_and_save(offers)
```

### 2. Lancer les tests
Le projet inclut des tests unitaires avec `pytest`. Pour les exécuter :
```bash
pytest tests/
```

## Configuration des Variables d'Environnement
Avant d'exécuter le script, assurez-vous d'avoir un fichier `.env` à la racine du projet contenant :
```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

## Sortie des Données
Les données récupérées sont sauvegardées sous format CSV :
- `offres_emploi.csv` : Liste des offres d'emploi.
- `entreprises.csv` : Informations sur les entreprises proposant les offres.
- `competences.csv` : Liste des compétences requises pour les offres.

## Logs
Les logs des exécutions sont enregistrés dans le dossier `logs/` avec un fichier horodaté.


