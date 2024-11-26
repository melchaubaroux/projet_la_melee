import os
import pytest
from unittest.mock import patch, MagicMock

from transcription_fonction_ressource import clean_audio, split_audio_by_silence, transcription




# Test de la fonction clean_audio
@patch("pydub.AudioSegment")  # Mocking de la méthode AudioSegment.from_file
def test_clean_audio( mock):
    input_file = "input_audio.mp3"
    output_file = "output_audio.mp3"

    # Création d'un mock pour l'audio
    mock_audio = MagicMock()

    mock_audio.from_file(input_file).return_value = mock_audio  # Simule la recuperation du fichier
    mock_audio.low_pass_filter(3000).return_value = mock_audio  # Simule le filtre passe-bas
    mock_audio.high_pass_filter(100).return_value = mock_audio  # Simule le filtre passe-haut
    mock_audio.export(output_file, format="mp3").return_value=mock_audio
    

    # Vérifier que la fonction `from_file` a été appelée avec le bon fichier
    mock_audio.from_file.assert_called_once_with(input_file)
    
    # Vérifier que les filtres audio ont été appliqués
    mock_audio.low_pass_filter.assert_called_once_with(3000)  # Vérifier le filtre passe-bas
    mock_audio.high_pass_filter.assert_called_once_with(100)  # Vérifier le filtre passe-haut
    
    # Vérifier que l'export du fichier a bien été appelé
    mock_audio.export.assert_called_once_with(output_file, format="mp3")


# Test de la fonction clean_audio inutile 
@patch("transcription_fonction_ressource.clean_audio")  # Mocking de la méthode AudioSegment.from_file
def test_clean_audio(mock_clean_audio):
    input_file = "input_audio.mp3"
    output_file = "output_audio.mp3"
    mock_clean_audio(input_file, output_file)
    mock_clean_audio.assert_called_once_with(input_file, output_file)
    



# Test de la fonction split_audio_by_silence
@patch("pydub.AudioSegment.from_file")  # Mock de AudioSegment.from_file
@patch("os.makedirs")  # Mock de os.makedirs
@patch("pydub.silence.split_on_silence")  # Mock de split_on_silence
def test_split_audio_by_silence(mock_split_on_silence, mock_makedirs, mock_from_file):

    input_file = "input_audio.mp3"
    directory_name= input_file[:-4]
    

    # Mock de l'audio source
    mock_audio = MagicMock()
    mock_from_file(input_file).return_value = mock_audio
    
    # Mock des segments après le découpage
    mock_segment1 = MagicMock()
    mock_segment2 = MagicMock()
    mock_directory= MagicMock()

    mock_split_on_silence(
        mock_audio,
        min_silence_len=1000,
        silence_thresh=-50).return_value = [mock_segment1, mock_segment2]
    
    mock_makedirs(input_file[:-4], exist_ok=True).return_value =mock_directory

    for i, segment in enumerate(mock_split_on_silence, start=1):

        output_file = f"chunk_{i}.mp3"
        segment.export(directory_name+"/"+output_file, format="mp3")

        # Vérifie que le segment a été exporté
        segment.export.assert_called_once_with(f"{input_file[:-4]}/chunk_{i}.mp3", format="mp3")

    
    # Vérifications d'appel
    mock_from_file.assert_called_once_with(input_file)  # Vérifie le chargement du fichier
    mock_split_on_silence.assert_called_once_with(
        mock_audio,
        min_silence_len=1000,
        silence_thresh=-50
    )
    mock_makedirs.assert_called_once_with(input_file[:-4], exist_ok=True)  # Vérifie la création du répertoire

    


       
# Test de la fonction transcription 1 
@patch("whisper.pad_or_trim")  # Mocking de la méthode pad_or_trim
@patch("whisper.log_mel_spectrogram")  # Mocking de la méthode log_mel_spectrogram
@patch("whisper.DecodingOptions")  # Mocking de l'objet DecodingOptions
@patch("whisper.decode")  # Mocking de la méthode decode
def test_transcription1(mock_decode, mock_decoding_options, mock_log_mel_spectrogram, mock_pad_or_trim):
    # Création d'un mock pour l'audio
    mock_file_audio = MagicMock()
    mock_audio = MagicMock()
    mock_model = MagicMock()
    mock_mel= MagicMock() 
    mock_options= MagicMock() 
    mock_result= MagicMock(text="Test de transcription")

    # Définir les valeurs retournées par les mocks
    mock_pad_or_trim(mock_file_audio).return_value = mock_audio
    # mock_log_mel_spectrogram(mock_audio,n_mels=80).to(mock_model.device).return_value =mock_mel# Mock du spectrogramme
    mock_log_mel_spectrogram(mock_audio,n_mels=80).to(mock_model.device).return_value = mock_mel# Mock du spectrogramme
    mock_decoding_options(language="fr").return_value = mock_options # Mock des options de décodage
    mock_decode(mock_model, mock_mel, mock_options).return_value = mock_result

        # Vérifier que pad_or_trim a été appelé sur l'audio
    mock_pad_or_trim.assert_called_once_with(mock_file_audio)
    
    # Vérifier que log_mel_spectrogram a été appelé avec les bonnes options
    mock_log_mel_spectrogram.assert_called_once_with(mock_audio,n_mels=80)
    
    # Vérifier que whisper.decode a été appelé avec les bons arguments
    mock_decode.assert_called_once_with(
        mock_model, 
        mock_mel, 
        mock_options
    )

    # Vérifier que le texte retourné est celui attendu
    assert mock_decode(mock_model, mock_mel, mock_options).return_value.text == "Test de transcription"
    

# Test de la fonction transcription 2
@patch("whisper.pad_or_trim")  # Mocking de la méthode pad_or_trim
@patch("whisper.log_mel_spectrogram")  # Mocking de la méthode log_mel_spectrogram
@patch("whisper.DecodingOptions")  # Mocking de l'objet DecodingOptions
@patch("whisper.decode")  # Mocking de la méthode decode
def test_transcription2(mock_decode, mock_decoding_options, mock_log_mel_spectrogram, mock_pad_or_trim):

    mock_file_audio = MagicMock()
    mock_model = MagicMock()


    audio=mock_pad_or_trim(mock_file_audio)
    mel= mock_log_mel_spectrogram(audio,n_mels=80).to(mock_model.device)# Mock du spectrogramme
    options=mock_decoding_options(language="fr") # Mock des options de décodage
    result = mock_decode(mock_model, mel, options)

    # Vérifier que pad_or_trim a été appelé sur l'audio
    mock_pad_or_trim.assert_called_once_with(mock_file_audio)
    
    # Vérifier que log_mel_spectrogram a été appelé avec les bonnes options
    mock_log_mel_spectrogram.assert_called_once_with(audio,n_mels=80)
    
    # Vérifier que whisper.decode a été appelé avec les bons arguments
    mock_decode.assert_called_once_with(
        mock_model, 
        mel,
        options
    )

    assert result !=None

    
    




if __name__ == "__main__":
    pytest.main()
