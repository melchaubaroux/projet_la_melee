'use client';

import React, { useRef } from 'react';
import Box from '@/components/Box';
import Button from '@/components/Button'

const Database = () => {

    const adresse_api = `http://127.0.0.1:8001/`
    // Références pour les éléments du DOM
    const connexionResultRef = useRef(null);
    const credentialsResultRef = useRef(null);
    const tablesResultRef = useRef(null);
    const dataResultRef = useRef(null);
    const consistencyResultRef = useRef(null);
    const resetResultRef = useRef(null);
    const uploadResultRef = useRef(null);
    const deletionDocument = useRef(null)
    // const usernameRef = useRef(null);
    // const passwordRef = useRef(null);
    const tableSelectRef = useRef(null);
    const tableSelectDataRef = useRef(null);
    const fileInputRef = useRef(null);
    const updateFileInputRef = useRef(null);
    const documentToDeleteRef = useRef(null);
    const searchQueryRef = useRef(null);
    const numResultsRef = useRef(null);
    const searchResultRef = useRef(null);

    function checkConnection() {
        fetch('http://127.0.0.1:8001/available_connection')
            .then(res => res.text())
            .then(text => {
                if (connexionResultRef.current) {
                    connexionResultRef.current.textContent = text;
                }
            });
    }

    // function verifyCredentials() {
    //     const username = usernameRef.current.value;
    //     const password = passwordRef.current.value;
    //     fetch(`http://127.0.0.1:8001/verification_of_authorisation?username=${username}&password=${password}`)
    //         .then(res => res.text())
    //         .then(text => {
    //             if (credentialsResultRef.current) {
    //                 credentialsResultRef.current.textContent = text;
    //             }
    //         });
    // }

    function listTables() {
        fetch('http://127.0.0.1:8001/list_of_table')
            .then(res => res.text())
            .then(text => {
                if (tablesResultRef.current) {
                    tablesResultRef.current.textContent = text;
                }
            });
    }

    // function getData() {
    //     const table = tableSelectDataRef.current.value;
    //     fetch(`http://127.0.0.1:8001/pull_all/${table}`)
    //         .then(res => res.json())
    //         .then(data => {
    //             if (dataResultRef.current) {
    //                 dataResultRef.current.textContent = JSON.stringify(data, null, 2);
    //             }
    //         });
    // }

    // function checkConsistency() {
    //     const table = tableSelectRef.current.value;
    //     fetch(`/api/check_consitancy?table=${table}`)
    //         .then(res => res.json())
    //         .then(data => {
    //             if (consistencyResultRef.current) {
    //                 consistencyResultRef.current.textContent = JSON.stringify(data, null, 2);
    //             }
    //         });
    // }

    // function resetDatabase() {
    //     fetch('http://127.0.0.1:8001/reset')
    //         .then(res => res.json())
    //         .then(data => {
    //             if (resetResultRef.current) {
    //                 resetResultRef.current.textContent = JSON.stringify(data, null, 2);
    //             }
    //         });
    // }

    function uploadFile() {
        const file = fileInputRef.current.files[0];
        const formData = new FormData();
        formData.append('file', file);

        fetch('http://127.0.0.1:8001/upload', { method: 'POST', body: formData })
            .then(res => res.text())
            .then(text => {
                if (uploadResultRef.current) {
                    uploadResultRef.current.textContent = text;
                }
            });
    }

    function deleteDocument() {
        const documentToDelete = documentToDeleteRef.current.value;
        fetch(`http://127.0.0.1:8001/document deletion?table=${documentToDelete}` , {method: 'POST' })
            .then(res => res.text())
            .then(text => {
                if (deletionDocument.current) {
                    deletionDocument.current.textContent = text;
                }
            });
    }

    // function updateDocument() {
    //     const file = updateFileInputRef.current.files[0];
    //     const formData = new FormData();
    //     formData.append('file', file);

    //     fetch('http://127.0.0.1:8001/maj', { method: 'POST', body: formData })
    //         .then(res => res.text())
    //         .then(text => {
    //             if (uploadResultRef.current) {
    //                 uploadResultRef.current.textContent = text;
    //             }
    //         });
    // }

    function performVectorSearch() {
        const query = searchQueryRef.current.value;
        const numResults = parseInt(numResultsRef.current.value);
        fetch(`http://127.0.0.1:8001/vectorial_search?query=${query}&number_of_document=${numResults}`,{method: 'POST' })
            .then(res => res.text())//.json()
            .then(data => {
                if (searchResultRef.current) {
                    searchResultRef.current.textContent = data;// JSON.stringify(data, null, 2);
                }
            });
    }

    return (
        <div className='flex flex-wrap gap-4 '>

            {/* <h1>Accès aux endpoints</h1> */}

            <Box title="Etat du service" >
                <button onClick={checkConnection} className='border rounded-lg bg-gray-300 hover:bg-gray-500'>Vérifier connexion</button>
                <pre ref={connexionResultRef}></pre>
            </Box>

            {/* <input type="text" ref={usernameRef} placeholder="Nom d'utilisateur" />
            <input type="password" ref={passwordRef} placeholder="Mot de passe" />
            <button onClick={verifyCredentials}>Vérifier authentification</button>
            <pre ref={credentialsResultRef}></pre> */}


            <Box title="table disponible">
               
                <button onClick={listTables} className='border rounded-lg bg-gray-300 hover:bg-gray-500'>Lister tables</button>
                <pre ref={tablesResultRef}></pre>
            </Box>

            {/* <Box title="voir le contenue d'un table ">
                <select ref={tableSelectDataRef}>
                    <option value="">Sélectionnez une table</option>
                    <option value="index">Index</option>
                </select>  
                <button onClick={getData} className='border rounded-lg bg-gray-300 hover:bg-gray-500'>Toutes les données</button>
                <pre ref={dataResultRef}></pre>
                

            </Box>  */}          
            
            {/* <Box title="table vide ? " >
                <button onClick={checkConsistency} className='border rounded-lg bg-gray-300 hover:bg-gray-500'>Vérifier consistance</button>
                <pre ref={consistencyResultRef}></pre>
            </Box> */}

            {/* <Box title="" >
                <button onClick={resetDatabase}>Resetter base de données</button>
                <pre ref={resetResultRef}></pre>
            </Box> */}

            <Box title="importer un fichier" >
                <input type="file" ref={fileInputRef} />
                <button onClick={uploadFile} className='border rounded-lg bg-gray-300 hover:bg-gray-500'>Uploader fichier</button>
                <pre ref={uploadResultRef}></pre>
            </Box>

            <Box title="supprimer un document" >
                <input type="text" ref={documentToDeleteRef} placeholder="Nom du document à supprimer" />
                <button onClick={deleteDocument} className='border rounded-lg bg-gray-300 hover:bg-gray-500'>Supprimer document</button>
                <pre ref={deletionDocument}></pre>
            </Box>

            {/* <Box title="" >
                <input type="file" ref={updateFileInputRef} accept=".txt" />
                <button onClick={updateDocument}>Mettre à jour document</button>
            </Box> */}

            <Box title="recherche vectoriel RAG" >
                <input type="text" ref={searchQueryRef} placeholder="Rechercher..." />
                <input type="number" ref={numResultsRef} min="1" max="100" defaultValue="5" />
                <button onClick={performVectorSearch} className='border rounded-lg bg-gray-300 hover:bg-gray-500'>Rechercher vecteur</button>
                <pre ref={searchResultRef}></pre>
            </Box>

            {/* 
            // test d'affichage 
            <Box></Box>
            <Box></Box>
            <Box></Box> */}     

        </div>
    );
};

export default Database;