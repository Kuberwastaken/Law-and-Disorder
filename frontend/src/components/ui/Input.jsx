import React from 'react';

export const Input = ({ value, onChange, placeholder }) => {
  return (
    <input
      className="input border border-gray-300 rounded py-2 px-4 mb-4 w-full"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
    />
  );
};