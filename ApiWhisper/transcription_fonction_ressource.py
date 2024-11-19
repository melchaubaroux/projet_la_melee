# module de fonction pour la transcription audio 

# module requis 
import whisper
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os



# clean l'audio 
def clean_audio(input_file, output_file):
    # Charge l'audio
    audio = AudioSegment.from_file(input_file)
    
    # Réduit le volume de 10 dB pour éviter d'endommager l'audio lors du traitement
    audio = audio - 10
    
    # Applique un filtre passe-bas pour supprimer les hauts fréquences indésirables
    low_pass_filter = audio.low_pass_filter(3000)  # ajustez la fréquence selon vos besoins
    
    # Applique un filtre passe-haut pour supprimer les basses fréquences indésirables
    high_pass_filter = low_pass_filter.high_pass_filter(100)  # ajustez la fréquence selon vos besoins
    
    # Exporte l'audio nettoyé
    high_pass_filter.export(output_file, format="mp3")


def split_audio_by_silence(input_file, silence_threshold=-50, min_silence_duration=1000):
    audio = AudioSegment.from_file(input_file)

    # Split the audio based on silence
    segments = split_on_silence(
        audio,
        min_silence_len=min_silence_duration,
        silence_thresh=silence_threshold
    )

    # creation du repertoire qui acceuillera les morceaux découper sur les silences

    os.makedirs(input_file[:-4],exist_ok=True)

    for i, segment in enumerate(segments, start=1):

        output_file = f"chunk_{i}.mp3"
        segment.export(input_file[:-4]+"/"+output_file, format="mp3")

        # Print the start and end time of each chunk
        chunk_start_time = (segment[i].frame_count() / segment.frame_rate) * 1000
        chunk_end_time = (segment[i+1].frame_count() / segment.frame_rate) * 1000
        print(f"Segment {i}: {chunk_start_time}ms to {chunk_end_time}ms")


def transcription (audio,model):
        
    
        audio = whisper.pad_or_trim(audio)

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio,n_mels=80).to(model.device)

        # decode the audio
        options = whisper.DecodingOptions(language="fr")
        result = whisper.decode(model, mel, options)

        return result.text


# def split_into_10_minute_segments(filename):
#     segments = []
#     audio = load_audio(filename)
#     for i in range(0, len(audio), 600000):  # 10 minutes en millisecondes
#         start = max(0, i - 600000)
#         end = min(len(audio), i + 600000)
#         segment_filename = f"{filename[:-4]}_{len(segments)}.wav"
#         save_segment(start, end, filename, segment_filename)
#         segments.append(segment_filename)
#     return segments


# def save_segment(start: int, end: int, original_file: str, new_file: str):
#     audio = load_audio(original_file)[start:end]
#     save_wav(audio, new_file)

if __name__ == "__main__": 
   
    
    print("lancement des test de "+os.path.basename(__file__))

