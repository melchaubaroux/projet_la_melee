"use client"

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import Logo from '@/app/public/logo.jpg'
import clsx from 'clsx';
import { useAuth } from '@/contexts/AuthenticationContext';


interface NavbarProps {
    className?: string;
}

const Navbar = ({className, ...props}:NavbarProps) => {

    const { token, logout } = useAuth();

    const customClassName = clsx(
        "w-screen shadow-md flex flex-row justify-between px-10 py-5 items-center",
        className
    )
    return (
        <nav className={customClassName}>
            <Link href="/">
                <Image src={Logo} alt="Logo de la Mêlée" className='h-12 w-12 rounded-full ' />
            </Link>
            <ul className="flex flex-row gap-5 items-center h-full text-white">
                {token ?
                    <>
                        <li>
                            <Link href="/logged/whisper">
                                Whisper
                            </Link>
                        </li>
                        <li>
                            <Link href="/logged/tchat">
                                Tchat
                            </Link>
                        </li>
                        <li>
                            <Link href="/logged/database">
                                Database
                            </Link>
                        </li>
                        <li onClick={logout}>
                           Déconnexion
                        </li>
                    </>
                :
                    <li>
                        <Link href="/login">
                            Login
                        </Link>
                    </li>
                }
                
                
            </ul>
        </nav>
    )
}

export default Navbar;