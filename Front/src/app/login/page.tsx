"use client"
import Button from '@/components/Button';
import Input from '@/components/Input';
import React, { useMemo } from 'react';
import Image from 'next/image';
import Logo from '@/app/public/logo.jpg';
import { useAuth } from '@/contexts/AuthenticationContext';

const LoginPage = () => {

    const [username, setUsername] = React.useState<string>('');
    const [password, setPassword] = React.useState<string>('');
    const [loading, setLoading] = React.useState<boolean>(false);

    const { login } = useAuth();

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        try { 
            const response = await fetch('http://127.0.0.1:8001/verification_of_authorisation?username='+username+"&password="+password, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
              });

            const responseValue = await response.text();

            console.log(responseValue)

            if (responseValue == "loged")  {
                // Gérer le succès de l'authentification ici
                await login(username, password);
                console.log('Authentification réussie');

            }
            else {
                // gestion de l'erreur d'identification 
                throw new Error('Erreur d\'authentification');
            }

            } catch (error) {
                // Afficher une erreur à l'utilisateur
              console.error('Erreur:', error);
              
            } finally {
                setLoading(false);
            }
        
        };


    const canSubmit = useMemo(() => {
        return username.length > 0 && password.length > 0 && !loading
    }, [username, password, loading])

    return (
        <div className='h-full flex justify-center items-center'>
            <div className="rounded p-5 shadow-lg">
                <form onSubmit={handleSubmit}>
                    <div className="flex flex-col gap-5 items-center">
                        <Image className="rounded-full" src={Logo} width={100} height={100} alt={'Logo de la Mêlée'} />
                        <Input onChange={setUsername} disabled={loading} placeholder="Nom d'utilisateur" />
                        <Input onChange={setPassword} disabled={loading} type="password" placeholder="Mot de passe" />
                        <Button disabled={!canSubmit}>Se connecter</Button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default LoginPage;