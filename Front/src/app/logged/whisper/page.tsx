'use client'

import React, { useState } from 'react';
import Input from '@/components/Input';
import { send } from 'process';
import { sendError } from 'next/dist/server/api-utils';

const Whisper = () => {

    
    
    // const send_video = async (e: React.FormEvent<HTMLFormElement> ) => {
        
    //     e.preventDefault();
    
    //     const formData = new FormData(e.currentTarget);
    //     const video = formData.get('video') as File | null;
    //     const mail_adresse = formData.get('email');
    
    //     console.log(video);
    //     console.log(mail_adresse);
        


    //     await fetch("http://localhost:8000/docs#/default/speech_to_text_transcription_post", {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({
    //             sender:"mel.chaubaroux@gmail.com" ,
    //             recipient: mail_adresse,
    //             video: video
                
    //         })
    //     }).catch(error => alert(error) )

    //     alert("information envoyé, le resultat sera envoyer dans votre boite mail.") ; 
    
    // };

    const send_video = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        
        const formData = new FormData(e.currentTarget);
        const video = formData.get('video') as File | null;
        const mail_adresse = formData.get('email');

        const [responseDiv, setResponseDiv] = useState(null);
      
        try {
          const response = await fetch("http://localhost:8000/docs#/default/speech_to_text_transcription_post", {
            method: 'POST',
            body: new FormData(), // Utilisez FormData pour les fichiers
            ...Object.fromEntries(formData),
          });

          console.log("premier print ", response.status, response.statusText)

          
        //   const responseDiv = document.createElement('div');
        //   responseDiv.className = 'response-div';
        //   responseDiv.textContent = JSON.stringify(response, null, 2);
        //   // Ajoute la div au formulaire
        //   const form = e.currentTarget;
        //   form.appendChild(responseDiv);


      
          if (!response.ok) {
            // throw new Error(`HTTP error! status: ${response.status}`);
            alert (`Erreur lors de l'envoi : ${response.status}`);
            console.log("deuxieme print ", response.status, response.statusText);
            console.warn(response.status, response.statusText);

            // throw new Error(`HTTP error! status: ${response.status, response.statusText}`);

            const responseDiv = document.createElement('div');
            responseDiv.className = 'response-div';
            responseDiv.textContent = JSON.stringify(response, null, 2);

            // Ajoute la div au formulaire
            const form = e.currentTarget;
            form.appendChild(responseDiv);


            

          }
      
        //   const data = await response.json();
        //   alert("Information envoyé, résultat sera envoyé dans votre boîte mail.");
        //   console.log(data); // Pour voir les données renvoyées par l'API
        } catch (error) {alert (`Erreur lors de l'envoi : ${error}`)}
               
        //   console.error('Erreur:', error);

    };
        
      
    
    return (
      
        <div className='flex justify-center items-center min-h-screen'>
            <div className='max-w-md mx-auto p-6 bg-white shadow-md rounded-lg'>
                <p className=' font-bold mb-2'>le texte de la video est envoyé a l'adresse mail</p>
                <form onSubmit={send_video} className='space-y-4'>
                    <div className='space-y-2'>
                        <label htmlFor='video' className='block text-sm font-medium text-gray-700'>Vidéo</label>
                        <input type="file" id='video' accept="video/*" className='w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-600' />
                    </div>
                    <div className='space-y-2'>
                        <label htmlFor='email' className='block text-sm font-medium text-gray-700'>Adresse email</label>
                        <input type="email" id='email' placeholder='exemple@domaine.com' className='w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-600' />
                    </div>
    
                    <button type='submit' className='w-full px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600'>Envoyer</button>
                </form>
            </div>
      </div>
      
    )
}

export default Whisper;