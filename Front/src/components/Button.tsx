import clsx from 'clsx';
import React from 'react';

interface ButtonProps {
    className?: string;
    children: React.ReactNode;
    disabled?: boolean;
}

const Button = ({...props}:ButtonProps) => {

    const customClassName = clsx(
        "px-3 py-3 rounded-lg bg-blue-500 hover:bg-blue-700 transition-all text-white cursor-pointer",
        props?.disabled ? "opacity-50 cursor-not-allowed" : "",
        props.className
    )

    return (
        <button {...props} className={customClassName}>{props.children}</button>
    )
}

export default Button;