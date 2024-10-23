"use client"
import clsx from 'clsx';
import React, { useState } from 'react';
import { FiPaperclip } from "react-icons/fi";
import { FaPaperPlane } from "react-icons/fa";
import Input from './Input';



interface TchatWidgetProps {
    className?: string;
}

interface Message {
    content: string;
    // threadId: number;
    userId: number; // If present, the message is from a user, otherwise it's from the botw
}


const TchatWidget = ({...props}:TchatWidgetProps) => {

    const [query, setQuery] = useState<string>('');
    const [messages, setMessages] = useState<Message[]>([
        {content: "Entrez un message pour discuter", userId: 0},
    ]);
    const [loading, setLoading] = useState<boolean>(false);

    const customClassName = clsx(
        "h-full",
        props.className
    )

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement> | null) => {
        
        if(e) e.preventDefault();
        
        setLoading(true);

        await fetch("http://localhost:8002/query?query="+query, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // body: JSON.stringify(query)
        }).then(res => res.json())
        .then(data => {
            setMessages([...messages,{content: query, userId: 1},  {content: data, userId: 0}]);
            console.log(data);
        }).catch(err => {
            setMessages([...messages,{content: query, userId: 1}, {content: "Oups, une erreur est survenue", userId: 0}]);
        })
        setQuery('');
        setLoading(false);
    }

    return (
        <div className={customClassName}>
            <div className="h-[80%]">
                <div className="h-full overflow-y-auto">
                    {messages.map((message, index) => (
                        <div key={index} className={clsx("p-3", message.userId ? "text-right" : "text-left")}>
                            <div className={clsx("bg-gray-300 rounded-lg p-3 inline-block", message.userId ? "bg-green-400" : "bg-orange-500")}>
                                {message.content}
                            </div>
                        </div>
                    ))}
                    {loading && <div className="text-center">En attente du serveur...</div>}
                </div>
            </div>
            <div className="h-[20%] border-t border-red-500 flex flex-row justify-center items-center p-5">
                <form className='flex flex-row gap-3 w-full' onSubmit={handleSubmit}>
                    <div className="bg-gray-200 flex flex-row justify-between items-center rounded-xl p-3 gap-10 w-full">
                        <div className="rounded-full p-3">
                            <FiPaperclip className='text-black text-3xl cursor-pointer' />
                        </div>
                        <Input value={query} disabled={loading} onChange={setQuery} />
                        <div className="rounded-full p-3 cursor-pointer bg-black" onClick={e => handleSubmit(null)}>
                            <FaPaperPlane className='text-white' />
                        </div>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default TchatWidget;