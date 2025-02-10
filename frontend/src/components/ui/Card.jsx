import React from 'react';

export const Card = ({ children }) => {
  return <div className="card bg-white shadow-md rounded-lg p-4 mb-4">{children}</div>;
};

export const CardHeader = ({ children }) => {
  return <div className="card-header font-bold text-lg mb-2">{children}</div>;
};

export const CardTitle = ({ children }) => {
  return <h2 className="card-title text-xl font-semibold mb-2">{children}</h2>;
};

export const CardContent = ({ children }) => {
  return <div className="card-content">{children}</div>;
};