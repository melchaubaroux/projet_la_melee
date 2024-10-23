import clsx from 'clsx';
import React from 'react';

interface InputProps {
    type?: string;
    placeholder?: string;
    className?: string;
    onChange?: (e:any) => void;
    disabled?: boolean;
    value?: string | number;
}

const Input = ({type = "text", disabled = false, ...props} : InputProps) => {

    const customClassName = clsx(
        "flex-1 h-10 border border-gray-300 rounded-lg p-3 w-80",
        props.className
    )

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (props.onChange) {
            props.onChange(e.target.value);
        }
    }

    return (
        <input {...props} disabled={disabled} type={type} className={customClassName} onChange={e => handleChange(e)}  />
    )
}

export default Input;