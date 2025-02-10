import React from 'react';

export const Button = ({ children, onClick }) => {
  return (
    <button className="btn bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700" onClick={onClick}>
      {children}
    </button>
  );
};