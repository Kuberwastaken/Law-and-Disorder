import React, { useState } from 'react';
import axios from 'axios';

function Game() {
  const [mode, setMode] = useState('setup');
  const [situation, setSituation] = useState('');
  const [result, setResult] = useState(null);
  const [players, setPlayers] = useState([
    { id: 1, name: 'Player 1', score: 0, isEditing: false },
    { id: 2, name: 'Player 2', score: 0, isEditing: false }
  ]);
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0);
  const [newPlayerName, setNewPlayerName] = useState('');
  const [winningScore, setWinningScore] = useState(50);

  const resetState = () => {
    setSituation('');
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/analyze', { situation });
      setResult(response.data);
      
      const updatedPlayers = [...players];
      updatedPlayers[currentPlayerIndex].score += response.data.verdict === 'YES' ? 10 : 5;
      setPlayers(updatedPlayers);
      
      setCurrentPlayerIndex((prev) => (prev + 1) % players.length);
      setSituation(''); // Only reset situation after successful submission
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleSingleQuery = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/analyze', { situation });
      setResult(response.data);
      setSituation(''); // Only reset situation after successful submission
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const addPlayer = () => {
    if (newPlayerName && players.length < 4) {
      setPlayers([
        ...players, 
        { 
          id: players.length + 1, 
          name: newPlayerName, 
          score: 0, 
          isEditing: false 
        }
      ]);
      setNewPlayerName('');
    }
  };

  const toggleEditPlayer = (index) => {
    const updatedPlayers = [...players];
    updatedPlayers[index].isEditing = !updatedPlayers[index].isEditing;
    setPlayers(updatedPlayers);
  };

  const handlePlayerNameChange = (index, newName) => {
    const updatedPlayers = [...players];
    updatedPlayers[index].name = newName;
    updatedPlayers[index].isEditing = false;
    setPlayers(updatedPlayers);
  };

  const renderSetupScreen = () => (
    <div className="game-container">
      <div className="neon-title">⚖️ Law & Disorder</div>
      
      <div className="score-board">
        <div className="game-mode-selection">
          <button onClick={() => setMode('game')}>Multiplayer Game</button>
          <button onClick={() => setMode('single-query')}>Constitutional Check</button>
        </div>
      </div>

      {mode === 'game' && (
        <>
          <div className="players-config">
            {players.map((player, index) => (
              <div 
                key={player.id} 
                className={`player-score ${index === currentPlayerIndex ? 'current-player' : ''}`}
              >
                {player.isEditing ? (
                  <input
                    type="text"
                    value={player.name}
                    onChange={(e) => handlePlayerNameChange(index, e.target.value)}
                    onBlur={() => toggleEditPlayer(index)}
                    autoFocus
                  />
                ) : (
                  <span onClick={() => toggleEditPlayer(index)}>
                    {player.name}
                  </span>
                )}
              </div>
            ))}
            {players.length < 4 && (
              <div className="add-player-section">
                <input
                  type="text"
                  value={newPlayerName}
                  onChange={(e) => setNewPlayerName(e.target.value)}
                  placeholder="New Player Name"
                  className="add-player-input"
                />
                <button 
                  onClick={addPlayer} 
                  className="add-player-btn"
                >
                  Add Player
                </button>
              </div>
            )}
          </div>
          <div className="winning-score">
            <label>
              Winning Score:
              <input
                type="number"
                value={winningScore}
                onChange={(e) => setWinningScore(Number(e.target.value))}
                min="10"
                max="500"
              />
            </label>
          </div>
        </>
      )}
    </div>
  );

  const renderMultiplayerGame = () => (
    <div className="game-container">
      <div className="neon-title">⚖️ Law & Disorder</div>
      
      <div className="score-board">
        {players.map((player, index) => (
          <div 
            key={player.id} 
            className={`player-score ${index === currentPlayerIndex ? 'current-player' : ''}`}
          >
            {player.isEditing ? (
              <input
                type="text"
                value={player.name}
                onChange={(e) => handlePlayerNameChange(index, e.target.value)}
                onBlur={() => toggleEditPlayer(index)}
                autoFocus
              />
            ) : (
              <span onClick={() => toggleEditPlayer(index)}>
                {player.name}: {player.score}
              </span>
            )}
          </div>
        ))}
      </div>
      
      <form onSubmit={handleSubmit} className="situation-form">
        <h2 className="current-player-turn">
          {players[currentPlayerIndex].name}'s Turn
        </h2>
        <textarea
          value={situation}
          onChange={(e) => setSituation(e.target.value)}
          placeholder="Enter an absurd legal situation that challenges the boundaries of the Indian Constitution..."
          required
        />
        <button type="submit" className="submit-btn">
          Challenge the Law
        </button>
      </form>

      {result && (
        <div className="result-card">
          <div className={`verdict ${result.verdict.toLowerCase()}`}>
            Verdict: {result.verdict}
          </div>
          <div className="legal-details">
            <div className="legal-reasoning">
              <h4>Constitutional Basis:</h4>
              {result.articles.map((article, i) => (
                <div key={i} className="article">
                  <strong>Article {article.article_no}:</strong> {article.text}
                </div>
              ))}
            </div>
            <div className="analysis">
              <h4>Judicial Reasoning:</h4>
              <p>{result.reasoning}</p>
            </div>
          </div>
          <button onClick={() => {
            resetState();
            setMode('setup');
          }} className="submit-btn">
            Back to Setup
          </button>
        </div>
      )}
    </div>
  );

  const renderSingleQueryMode = () => (
    <div className="game-container">
      <div className="neon-title">⚖️ Law & Disorder</div>
      
      <form onSubmit={handleSingleQuery} className="situation-form">
        <textarea
          value={situation}
          onChange={(e) => setSituation(e.target.value)}
          placeholder="Enter a legal scenario to check its constitutional validity..."
          required
        />
        <button type="submit" className="submit-btn">
          Check Legality
        </button>
      </form>

      {result && (
        <div className="result-card">
          <div className={`verdict ${result.verdict.toLowerCase()}`}>
            Verdict: {result.verdict}
          </div>
          <div className="legal-details">
            <div className="legal-reasoning">
              <h4>Constitutional Basis:</h4>
              {result.articles.map((article, i) => (
                <div key={i} className="article">
                  <strong>Article {article.article_no}:</strong> {article.text}
                </div>
              ))}
            </div>
            <div className="analysis">
              <h4>Judicial Reasoning:</h4>
              <p>{result.reasoning}</p>
            </div>
          </div>
          <button 
            onClick={() => resetState()} 
            className="submit-btn"
            style={{marginTop: '1rem'}}
          >
            Analyze Another Scenario
          </button>
        </div>
      )}

      <button 
        onClick={() => {
          resetState();
          setMode('setup');
        }} 
        className="submit-btn"
        style={{marginTop: '1rem'}}
      >
        Back to Setup
      </button>
    </div>
  );

  return (
    <>
      {mode === 'setup' && renderSetupScreen()}
      {mode === 'game' && renderMultiplayerGame()}
      {mode === 'single-query' && renderSingleQueryMode()}
    </>
  );
}

export default Game;