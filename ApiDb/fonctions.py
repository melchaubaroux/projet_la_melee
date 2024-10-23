from os import remove

import psycopg2
from pgvector.psycopg2 import register_vector
from psycopg2.extensions import AsIs

from sentence_transformers import SentenceTransformer

import config_local as config

model = SentenceTransformer('all-MiniLM-L6-v2')


#fonction generique qui permet de verifier si une fonction appelé abouti sans probleme 
# et sinon renvoi la fonction et le probleme renconctré
def check_execution(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
           return "ERROR with",func.__name__, str(e)
    
    return wrapper


# Gestion des tables 
################################################

@check_execution
def connection_db(database=config.database):
    try : 
        conn = psycopg2.connect(
            host=config.host,
            # database=config.database,
            user=config.user,
            password=config.password,
            port = 5432
            # options=config.options
        )
        print(f"success to connect with db at :{config.host}") 
        return conn,conn.cursor()

    except Exception as e  : 

        return f"fail to connect with db: \n {e}"

@check_execution
def save_and_stop_connection(conn,cur):
    conn.commit() 
    cur.close()
    conn.close()
    print("connection closed to db ")

@check_execution
def drop_table (table,cursor):

    print(f"dropping {table}: ",end="")
    try : 

        cursor.execute(f"DROP TABLE {table} ;")

        print("no more table at this name")
        
    except Exception as e  : 

        print("fail to drop: ",e)

@check_execution
def table_existance (table) :

    conn,cur=connection_db(table)
    cur.execute(f" SELECT column_name FROM information_schema.columns WHERE table_name = '{table}';")
    table = cur.fetchone()

    if len(table)>0 : 
        return "true"
    else : 
        return "false"
            
@check_execution
def check_consistancy (table):

    conn,cur=connection_db(table)
    
    try : 
        if table_existance(table)=="true":

            cur.execute(f"SELECT * FROM {table};")
            result=cur.fetchone()

            if len(result)>0 : 
                return "true"#,type(result),result
            else : 
                "false",result
        
        else : 
            return "no table at this name "
    except Exception as e  : 
        return e

# @check_execution
def create_table (table_name,colonne_name,colonne_type):

    print("create table process beginning : ")

    conn,cur=connection_db()

    drop_table(table_name,cur)
    conn.commit()
    
    try : 
        col_name_type=(",").join([f"{d[0]} {d[1]} "  for d in zip(colonne_name,colonne_type)])

        query=f"CREATE TABLE {table_name} ({col_name_type});"

        # Execute a command: this creates a new table
        cur.execute(query)
        conn.commit()
        print(f"{table_name} créé avec succées" )
        

    except Exception as e : 

        print(e)

    save_and_stop_connection(conn,cur)

@check_execution
def get_table (table):

    conn,cur=connection_db()
    cur.execute(f"SELECT * FROM {table};")
    return cur.fetchall()

# @check_execution
def insert_many(table_name,col_name,data):

    conn,cur=connection_db()
 
    try : 
        for indice,value in enumerate(data):
            print(indice,value)

            try :
                
                cur.execute(f"INSERT INTO {table_name} ({(',').join(col_name)}) VALUES (%s,%s)",value)
                conn.commit()
                
            
            except Exception as e  : 
                print(e)
                print("fail:\n",indice) 

                conn.rollback()

            else : 

                print("insert_many achived without problem")
                conn.commit()
        
        save_and_stop_connection(conn,cur)
          

    except Exception as e : 
        print("insertion failed rollback activated" )
        print(e)

# recuperation automatique des noms et types de colonne
@check_execution
def get_colonne (ref): 

    col_type=["int" if type(r)==int else "varchar" for r in ref.values()]
    col_name=list(ref.keys())

    return col_type,col_name

@check_execution
def verification_of_authorisation (cursor,table,username,password):
    cursor.execute(f"SELECT * FROM {table} WHERE username like '{username}' and  password like '{password}' ")
    data=cursor.fetchone()
    return  'loged' if data != None else 'login error'

@check_execution
def listing_table(database:str="postgres"):

    try:
        conn,cur=connection_db(database)
        

        cur.execute("""
                    SELECT tablename 
                    FROM pg_catalog.pg_tables 
                    WHERE schemaname != 'pg_catalog' AND 
                        schemaname != 'information_schema';
                """)

        tables="Bases de données disponibles:\n"+"\n".join(x[0] for x in cur.fetchall())
        
        cur.close()
        conn.close()

        return tables
        
    except Exception as e :
        return f"Erreur lors de la connexion à la base de données: {e}"


# Section vectoriel
# @check_execution
def query_vectorisation (query:str):

    # Charger un modèle pré-entraîné
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # encode la requete 
    query_embedding = model.encode(query)
    #la renvoie sous forme de liste pour pouvoir l'utilisé dans postgrs sql
    return query_embedding.tolist()



@check_execution
def extension_file_suppression (document_name) : 

    # inversion du nom 
    document_name = document_name[::-1]
    #suppression de l'extension 
    document_name = document_name[document_name.find(".")+1:]
    # retour a la normal 
    document_name = document_name[::-1]

    return document_name

@check_execution
def read_external_data(file) : return file.file.read()

@check_execution
def write_external_data_in_buffer (file,document_name) : 

    with open(document_name, "wb+") as buffer :
                buffer.write(file.file.read())

@check_execution
def read_buffer(document_name):
    with open(document_name) as file :
        return file.read()


@check_execution
def document_vectorisation (file):
    # ajouter dans la table d'index le nom du document et sa vectorisation global 
    #creer un nouvelle table du nom du document  puis y inserer le contenu du document vectorisé avec la version en texte 
    # gere txt , pdf 

        #connection
        conn,cur=connection_db()
        register_vector(conn)

        #recuperation des données
        document_name=extension_file_suppression(file.filename)
        write_external_data_in_buffer (file,document_name)
        document=read_buffer(document_name)

        # vectorisation global 
        embeddings = model.encode(document)

        # integration dans la base d'index du fichier vectorisé mais non decoupé :
        cur.execute(f"INSERT INTO index (embedding,value) VALUES  (%s,%s)",(embeddings,document_name))

        # vectorisation par partie de document 
        splited_document = document.split('. ')

        # creation table 
        cur.execute(f"CREATE TABLE {document_name} (id SERIAL PRIMARY KEY,embedding VECTOR(384),value VARCHAR);")

        for chunk in splited_document : 
            vectorised_chunk = model.encode(chunk)
            cur.execute(f"INSERT INTO {document_name} (embedding,value) VALUES (%s,%s)",(vectorised_chunk,chunk))

        save_and_stop_connection(conn,cur)

        remove(document_name)

        return "document vectorisé et enregistré "
    
   

@check_execution
def find_matching (vectorised_query,table,limit=10):

    vq=vectorised_query
    conn,cur=connection_db()

    data= []

    # distance de manhattan 
    L1= " (embedding <-> '%s') "
    # distance euclidienne
    L2= " (embedding <+> '%s') "

    # inutilisé  formule de liaison , les documents les plus pertinent ont la valeur la plus elevé 
    L=f"( 1 / ( 0.5 * ({L1} + {L2}) ) )"

    # comparaisons d'orientation avec le cosinus  une valeur entre -1 et 1  avec 1 la colinearité
    cosine= "(embedding <=> '%s')"

    # comparaisons d'orientation avec le arcosinus une valeur entre -180 et 180  avec 0 la colinearité 
    inner_product = "abs( embedding <#> '%s') "
    
    params= [AsIs(vq) for x in range(4)]

    cur.execute(f"""
            SELECT value,{L1}
            FROM {table}
            WHERE {cosine} >= 0.5 AND {inner_product} <= 45 
            ORDER BY {L1} ASC LIMIT {limit} ;
            """,params)

    result=cur.fetchall()

    data+=result

    save_and_stop_connection(conn,cur)

    return data 

@check_execution
def find_revelent_documents(vectorised_query,limit=1) : return find_matching(vectorised_query,"index",limit)

@check_execution
def extract_document_informations(documents_identifier:list,vectorised_query):

    data=[]
    for identifier in documents_identifier:
        data+=[identifier[0],find_matching(vectorised_query,identifier[0])]

    return data 



