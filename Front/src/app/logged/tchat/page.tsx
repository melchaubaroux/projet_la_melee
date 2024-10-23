import TchatWidget from '@/components/TchatWidget';
import React, { useEffect, useState } from 'react';

// interface Thread {
//     id: number;
//     title: string;
//     messages: Message[];
// }

// interface Message {
//     id: number;
//     content: string;
//     threadId: number;
//     userId: number; // If present, the message is from a user, otherwise it's from the botw
// }

const Tchat = () => {

    // const [threads, setThreads] = useState<any[]>([]);

    // useEffect(() => {
    //     fetch('http://localhost:8000/api/threads')
    //         .then(res => res.json())
    //         .then(data => {
    //             setThreads(data);
    //         })
    // }, [])


    return (
        <div className="flex flex-row h-full">
            <div className="w-1/5 bg-gray-300">
            
            </div>
            <TchatWidget className="w-4/5" />
        </div>
    )
}

export default Tchat;