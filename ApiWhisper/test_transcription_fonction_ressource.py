import os
import pytest
from unittest.mock import patch, MagicMock
from transcription_fonction_ressource import clean_audio, split_audio_by_silence, transcription

# Test de la fonction clean_audio
@patch("pydub.AudioSegment.from_file")  # Mocking de la méthode AudioSegment.from_file
@patch("pydub.AudioSegment.export")  # Mocking de la méthode AudioSegment.export
def test_clean_audio(mock_export, mock_from_file):
    # Création d'un mock pour l'audio
    mock_audio = MagicMock()
    mock_from_file.return_value = mock_audio
    
    input_file = "input_audio.mp3"
    output_file = "output_audio.mp3"
    
    # Appel de la fonction clean_audio
    clean_audio(input_file, output_file)
    
    # Vérifier que la fonction `from_file` a été appelée avec le bon fichier
    mock_from_file.assert_called_once_with(input_file)
    
    # Vérifier que les filtres audio ont été appliqués
    mock_audio.__sub___.assert_called_once_with(10)  # Vérifier que le volume a été réduit de 10dB
    mock_audio.low_pass_filter.assert_called_once_with(3000)  # Vérifier le filtre passe-bas
    mock_audio.high_pass_filter.assert_called_once_with(100)  # Vérifier le filtre passe-haut
    
    # Vérifier que l'export du fichier a bien été appelé
    mock_export.assert_called_once_with(output_file, format="mp3")


# Test de la fonction split_audio_by_silence
@patch("pydub.AudioSegment.from_file")  # Mocking de la méthode AudioSegment.from_file
@patch("pydub.AudioSegment.export")  # Mocking de la méthode AudioSegment.export
@patch("os.makedirs")  # Mocking de la méthode os.makedirs
@patch("pydub.silence.split_on_silence")  # Mocking de la méthode split_on_silence
def test_split_audio_by_silence(mock_split_on_silence, mock_makedirs, mock_export, mock_from_file):
    # Création d'un mock pour l'audio
    mock_audio = MagicMock()
    mock_from_file.return_value = mock_audio
    
    # Mock des segments générés après split
    mock_segment = MagicMock()
    mock_segment.export = MagicMock()
    mock_split_on_silence.return_value = [mock_segment, mock_segment]  # Simule deux segments
    
    input_file = "input_audio.mp3"
    
    # Appel de la fonction split_audio_by_silence
    split_audio_by_silence(input_file)
    
    # Vérifier que la fonction `from_file` a été appelée avec le bon fichier
    mock_from_file.assert_called_once_with(input_file)
    
    # Vérifier que split_on_silence a été appelé avec les bons paramètres
    mock_split_on_silence.assert_called_once_with(mock_audio, min_silence_len=1000, silence_thresh=-50)
    
    # Vérifier que os.makedirs a été appelé pour créer un dossier
    mock_makedirs.assert_called_once_with(input_file[:-4], exist_ok=True)
    
    # Vérifier que chaque segment a été exporté
    assert mock_segment.export.call_count == 2  # Vérifie que deux segments ont été exportés


# Test de la fonction transcription
@patch("whisper.pad_or_trim")  # Mocking de la méthode pad_or_trim
@patch("whisper.log_mel_spectrogram")  # Mocking de la méthode log_mel_spectrogram
@patch("whisper.decode")  # Mocking de la méthode decode
def test_transcription(mock_decode, mock_log_mel_spectrogram, mock_pad_or_trim):
    # Création d'un mock pour l'audio
    mock_audio = MagicMock()
    mock_model = MagicMock()

    # Définir les valeurs retournées par les mocks
    mock_pad_or_trim.return_value = mock_audio
    mock_log_mel_spectrogram.return_value = MagicMock()  # Mock du spectrogramme
    mock_decode.return_value = MagicMock(text="Test de transcription")
    
    # Appel de la fonction transcription
    result = transcription(mock_audio, mock_model)
    
    # Vérifier que pad_or_trim a été appelé sur l'audio
    mock_pad_or_trim.assert_called_once_with(mock_audio)
    
    # Vérifier que log_mel_spectrogram a été appelé avec les bonnes options
    mock_log_mel_spectrogram.assert_called_once_with(mock_audio, n_mels=80)
    
    # Vérifier que whisper.decode a été appelé avec les bons arguments
    mock_decode.assert_called_once_with(mock_model, mock_log_mel_spectrogram.return_value, whisper.DecodingOptions(language="fr"))
    
    # Vérifier que le texte retourné est celui attendu
    assert result == "Test de transcription"


if __name__ == "__main__":
    pytest.main()
