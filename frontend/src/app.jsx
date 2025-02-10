import React from 'react';
import LegalGame from './components/LegalGame';
import './styles/globals.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-gray-900">
            Law & Disorder - Indian Constitution Game
          </h1>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <LegalGame />
        </div>
      </main>
    </div>
  );
}

export default App;