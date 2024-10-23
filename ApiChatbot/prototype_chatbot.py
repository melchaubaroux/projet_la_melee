import requests
import json

# from  wrapper import name_execution_time

# from fonctions import * 



# @name_execution_time
def request_database(query:str): 

    # Définissez l'URL de base de l'API du RAG
    url_rag_base="http://127.0.0.1:8001/vectorial_search?query="

    # Définissez l'URL complete de l'API du RAG
    url_rag_final = f"{url_rag_base}{query}"

    headers = {'Content-Type': 'application/json'}

    

    # Envoyez la requête POST à l'API du rag 
    response_rag  = requests.post(url_rag_final, headers=headers, data="")

    print(response_rag.content)

    return response_rag

   
def search_on_internet(query:str): 
    pass

# @name_execution_time
def analyse_request(query:str):
    
    pass


# @name_execution_time
def send_request(query:str):

    # Définissez l'URL de base de l'API d'Ollama
    url_llm_base = "http://127.0.0.1:11434"

    # Construisez l'URL complète pour la requête d'inférence
    url_llm_final = f"{url_llm_base}/api/generate"


    #questionner le RAG 
    # response_rag=request_database(query)

    # print(response_rag.content)


    headers = {'Content-Type': 'application/json'}
 
    prompt=f"""tu dois repondre le plus rapidement possible et sobrement ,  a partir uniquement des informations suivantes: {response_rag._content} , répond a la question suivante {query} en français seulement"""

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

    print(response)

    # Vérifiez si la requête a réussi
    if response.status_code == 200:
        # Affichez la réponse
        print("Response:", response.json()['response'])
    else:
        print(f"Failed to get a response. Status code: {response.status_code}")


prompt=f"""combien font deux plus deux, repond sobrement et le plus rapidement possible"""

# prompt=f"""comment fonctionnne le financement opco pour les formations qualiopi"""

send_request(prompt)

# request_database("finacment opco")
