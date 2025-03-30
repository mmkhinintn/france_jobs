import pytest
from unittest.mock import patch, MagicMock
from api.api_france_job import FranceEmploi

# Pytest fixture pour initialiser l'objet FranceEmploi
@pytest.fixture
def france_emploi():
    return FranceEmploi()

# Test de l'authentification
@patch('requests.post')
def test_authenticate(mock_post, france_emploi):
    """Test de la méthode authenticate()"""

    # Simuler une réponse d'authentification avec un token valide
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "fake_token"}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Exécuter la méthode
    france_emploi.authenticate()

    # Vérifier que l'authentification a bien été appelée
    mock_post.assert_called_once()
    assert france_emploi.token == "fake_token"

# Test de fetch_offers()
@patch('requests.get')
@patch('requests.post')
def test_fetch_offers(mock_post, mock_get, france_emploi):
    """Test de la méthode fetch_offers()"""

    # Simuler l'authentification
    mock_post_response = MagicMock()
    mock_post_response.json.return_value = {"access_token": "fake_token"}
    mock_post_response.status_code = 200
    mock_post.return_value = mock_post_response

    # Simuler la récupération des offres
    mock_get_response = MagicMock()
    mock_get_response.json.return_value = {
        "resultats": [{"id": "123", "intitule": "Développeur", "description": "Développement web"}]
    }
    mock_get_response.status_code = 200
    mock_get.return_value = mock_get_response

    # Exécuter la méthode
    offers = france_emploi.fetch_offers("08")

    # Vérifications
    mock_post.assert_called_once()
    mock_get.assert_called_once()
    assert isinstance(offers, list)
    assert offers[0]['id'] == "123"

# Test de process_and_save()
@patch('pandas.DataFrame.to_csv')
def test_process_and_save(mock_to_csv, france_emploi):
    """Test de la méthode process_and_save()"""

    # Données fictives
    offers = [
        {
            "id": "123",
            "intitule": "Développeur",
            "description": "Développement web",
            "entreprise": {"nom": "TechCorp"},
            "competences": [{"code": "PYTHON", "libelle": "Python"}]
        }
    ]

    # Exécuter la méthode
    france_emploi.process_and_save(offers)

    # Vérifications (trois fichiers CSV doivent être générés)
    assert mock_to_csv.call_count == 3
