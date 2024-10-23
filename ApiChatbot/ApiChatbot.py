from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi import FastAPI, UploadFile, File

import requests
import json

import uvicorn

# from fonctions import * 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

########################################### endpoints #############################################

@app.post("/query")
def send_query(query:str):

    print(query)

    # Définissez l'URL de base de l'API d'Ollama
    url_llm_base = "http://127.0.0.1:11434"

    # Construisez l'URL complète pour la requête d'inférence
    url_llm_final = f"{url_llm_base}/api/generate"

    # Définissez l'URL de base de l'API du RAG
    url_rag_base="http://127.0.0.1:8001/vectorial_search?query="

    requete_utilisateur=query

    # Construisez l'URL complète pour la requête d'inférence
    url_rag_final = f"{url_rag_base}{requete_utilisateur}"

    headers = {'Content-Type': 'application/json'}

    # Envoyez la requête POST à l'API du rag 
    response_rag  = requests.post(url_rag_final, headers=headers, data="")

    # Vérifiez si la requête a réussi
    # 
    print(response_rag._content)
    prompt=f"""tu est un assistant administrif d'une association qui promeut le numérique et dispense des formations,  a partir uniqument des informations suivante {response_rag._content} , repond a la question suivante {requete_utilisateur} en français seulement"""

    # Préparez les données de la requête
    data = {
        "model": "llama3",
        "prompt":prompt,
        "stream": False,
    }

    # Convertissez les données en JSON
    json_data = json.dumps(data)

    # Envoyez la requête POST à l'API d'Ollama
    response = requests.post(url_llm_final, headers=headers, data=json_data)

    # Vérifiez si la requête a réussi
    if response.status_code == 200:
        # Affichez la réponse
        print("Response:", response.json()['response'])
        return response.json()['response']
    else:
        print(f"Failed to get a response. Status code: {response.status_code}")
        return f"Failed to get a response. Status code: {response.status_code}"

    





if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1" , port=8002)

