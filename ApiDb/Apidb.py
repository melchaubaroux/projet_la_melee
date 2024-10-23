from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi import FastAPI, UploadFile, File

from prometheus_client import Gauge
import psutil



import uvicorn

from config_local import * 
from fonctions import * 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  creation de la table d'index si celle ci n'est pas déja existante : 

if table_existance("index")=='false':

    conn,cur=connection_db()
  
    cur.execute('CREATE EXTENSION IF NOT EXISTS vector ; ')

    cur.execute(f"""
                CREATE TABLE index (
                    id SERIAL PRIMARY KEY,
                    embedding VECTOR(384),
                    value VARCHAR 
                    );
                """)
    
    conn.commit()
    
    save_and_stop_connection(conn,cur)



########################################### endpoints #############################################


# check connection
@app.get("/available_connection", response_class=HTMLResponse)#JSONResponse
def test_connection():
    
    conn,cur=connection_db()

    return "True" if conn else "False"

@app.get("/monitoring")
def monitoring () : 
# Création des métriques
    cpu_usage = Gauge('system_cpu_usage', 'Utilisation CPU du système')
    memory_usage = Gauge('system_memory_usage', 'Utilisation Mémoire du système')

    def collect_metrics():
        """Collecte des métriques et les met à jour."""
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent

        # Mise à jour des métriques
        cpu_usage.set(cpu)
        memory_usage.set(memory)

        # print(cpu,memory)

        return f"cpu utilisé a {cpu} %, memoire utiliser a {memory}% "

    return collect_metrics()


   

# check login connection 
@app.get("/verification_of_authorisation", response_class=HTMLResponse)
def test_credentials (username,password) : 
    conn,cur=connection_db()
    return verification_of_authorisation(cur,'identifieur_client',username,password)

# check existence of a table 
@app.get("/exist/{table}", response_class=HTMLResponse)
def request_table(table):
    return table_existance(table)


# list of table for user  :
@app.get("/list_of_table", response_class=HTMLResponse) 
def list_of_table() : 
    return listing_table()

#pull all  data of a table 
@app.get("/pull_all/{table}", response_class=JSONResponse)
def request_table(table):
    conn,cur=connection_db()
    return get_table(table)


#verifie si une table contient des informations 
@app.get("/check_consitancy",response_class=JSONResponse)
def is_not_empty (table): 
    return check_consistancy (table)

#reset de la database 
@app.get("/reset",response_class=JSONResponse)
def reset_database(database="postgres"):

    conn,cur=connection_db()

    cur.execute("""
            SELECT tablename 
            FROM pg_catalog.pg_tables 
            WHERE schemaname != 'pg_catalog' AND 
                schemaname != 'information_schema';
                """)
    
    table_list=cur.fetchall()

    for table in table_list : 
        drop_table (table[0],cur)

    cur.execute(f"""
            CREATE TABLE index (
                id SERIAL PRIMARY KEY,
                embedding VECTOR(384),
                value VARCHAR 
                );
            """)

    save_and_stop_connection(conn,cur)


#integration des fichiers 
@app.post("/upload")
def upload(file:UploadFile=File(...)):
    return document_vectorisation(file)

@app.post("/document deletion")
def document_deletion(table) :

    # suppression de la  references dans la table de references 
    conn,cur=connection_db()
    cur.execute(f"""DELETE FROM index WHERE value = '{table}'; """)
    save_and_stop_connection(conn,cur) 

    # suppression de la table lié a la reference precedement supprimé
    conn,cur=connection_db()
    conn.autocommit =True 
    cur.execute(f"""DROP TABLE {table}; """)
    
    save_and_stop_connection(conn,cur) 
    

#mis a jour de fichiers 
@app.post("/maj")
def maj (file:UploadFile=File(...)):
    yield 0 


#recherche vectoriel des documents perninents
@app.post("/vectorial_search")
def vectorial_research (query:str,number_of_document:int=1) :

    vectorised_query=query_vectorisation(query) 
    relevent_document=find_revelent_documents(vectorised_query,limit=number_of_document)
    data=extract_document_informations(relevent_document,vectorised_query)
   
    return data 


if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1" , port=8001)

