"use client"
import React, { createContext, useState, useContext, ReactNode, use, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface AuthContextType {
    login: (username: string, password: string) => void;
    logout: () => void;
    token?: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [token, setToken] = useState<string | undefined>(undefined);

    const router = useRouter();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            setToken(token);
        }
    }, []);

    const login = async (username: string, password: string) => {
        // TODO : Call the API for login
        localStorage.setItem('token', 'toto');
        setToken('toto');
        router.push('/logged/tchat');
        // await fetch('http://localhost:8000/api/login', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify({username, password})
        // }).then(res => res.json())
        // .then(data => {
        //     console.log("Authenticated ! ❤️");
        //     setToken(data.token);
        //     localStorage.setItem('token', data.token);
        // }).catch(err => {
        //     console.error(err);
        // })
    };

    const logout = () => {
        setToken(undefined);
        localStorage.removeItem('token');
    };

    return (
        <AuthContext.Provider value={{ login, logout, token }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};