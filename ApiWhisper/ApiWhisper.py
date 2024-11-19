from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi import FastAPI, UploadFile, File
import uvicorn
import whisper
import os 
# import ssl 

from transcription_fonction_ressource import *

from send_email import send_email

model = whisper.load_model("tiny") 

app = FastAPI()

# app.add_middleware(HTTPSRedirectMiddleware)

# Configuration SSL
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transcription")
def speech_to_text( file:UploadFile=File(...),sender="mel.chaubaroux@gmail.com", recipients="mel.chaubaroux@gmail.com"):

    texte = ""

    name_file=file.filename


    # on rajoute le nom de la video dans le sujet du mail 
    subject ="transcription audio de "+name_file[:-4]

    # Créez un nouveau fichier sur le disque avec le même nom
    with open(name_file, "wb+") as buffer :
        buffer.write(  file.file.read())

    # Split the audio based on silence
    print("découpage de l'audio en fonction des silences")
    split_audio_by_silence(
        name_file,
        silence_threshold=-66, # db = dbfs+96
        min_silence_duration=1000
    )
    print("demarrage de la transcription")

    list_of_segments = os.listdir(name_file[:-4])                
    number_of_segment = len(list_of_segments)

    
    for indice,segment in enumerate(list_of_segments):

        # chargement du segment courant 
        audio =whisper.load_audio(name_file[:-4]+"/"+segment)

        len_of_current_segment = len(audio)

        print("transcription de segment n°"+str(indice))

        number_of_chunk=len_of_current_segment//60000


    
        for chunk in range(0,len_of_current_segment,step:=60000):

            portion=whisper.pad_or_trim(audio[chunk:chunk+step])

            transcripted_segment=transcription(portion,model)
            
            texte+=transcripted_segment+"\n"

            print("chunk "+str(chunk//60000+1)+"/"+str(number_of_chunk))

            

        print(f"segment {indice+1}/{number_of_segment} transcript")

    os.remove(file.filename)
    send_email(subject, texte, sender, recipients)


    return texte
         

if __name__=="__main__" : 
    uvicorn.run(app,host='0.0.0.0', port=8000)#,ssl_keyfile='key.pem',ssl_certfile='cert.pem'
