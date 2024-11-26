# from unittest.mock import patch

# @patch("audio_utils.transcribe_audio")  # Patch direct
# def test_process_audio_with_complex_result(mock_transcribe):
#     # Configurer le retour comme un objet complexe
  
#     # Appel de la fonction testée
#     result = mock_transcribe("dummy_path.wav")

#     # Vérifications
#     mock_transcribe.assert_called_once_with("dummy_path.wav")
#     assert result == "Processed: mocked transcription"

#     # Vérifier l'utilisation des attributs
#     assert mock_transcribe.return_value.confidence == 0.95
import pytest
from unittest.mock import patch

# Fonction principale
def main_function(value):
    result = sub_function1(value)
    sub_function2(result)
    return result * 2

# Sous-fonctions
def sub_function1(value):
    return value + 1

def sub_function2(value):
    print(f"Processed: {value}")

# Test
@patch("test_mock.sub_function1", wraps=sub_function1)  # Mock partiel : garde le comportement réel
@patch("test_mock.sub_function2")  # Mock complet
def test_main_function(mock_sub_function2, mock_sub_function1):
    result = main_function(5)

    # Vérifications
    mock_sub_function1.assert_called_once_with(5)  # Vérifie l’appel
    mock_sub_function2.assert_called_once_with(6)  # Vérifie l’appel
    assert result == 12  # Résultat final correct



@patch("test_mock.sub_function1", side_effect=sub_function1)  # Spy sur sub_function1
@patch("test_mock.sub_function2")  # Mock de sub_function2
def test_main_function2(mock_sub_function2, mock_sub_function1):
    result = main_function(5)

    # Vérifier que sub_function1 est appelée correctement
    mock_sub_function1.assert_called_once_with(5)

    # Vérifier que sub_function2 est appelée avec le bon résultat
    mock_sub_function2.assert_called_once_with(6)

    # Vérifier le résultat final
    assert result == 12


if __name__=="__main__":
    pytest.main()