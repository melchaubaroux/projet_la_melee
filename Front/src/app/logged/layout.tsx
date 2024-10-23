"use client"

import { useAuth } from '@/contexts/AuthenticationContext';
import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation'
import Navbar from '@/components/Navbar';

const LoggedLayout = (props: any) => {

    const { token } = useAuth();
    const router = useRouter()

    useEffect(() => {
        if (!token) {
            router.push('/login');
        }
    }
    , [token]);
    
    return (
        <>
            <Navbar className="h-[10vh]"/>
            {props.children}
        </>
    )
}

export default LoggedLayout;

