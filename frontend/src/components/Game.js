import React, { useState } from 'react';
import axios from 'axios';
import './Game.css';

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
  const [editingName, setEditingName] = useState('');
  const [waitingForGuess, setWaitingForGuess] = useState(false);
  const [submittedSituation, setSubmittedSituation] = useState('');

  const resetState = () => {
    setSituation('');
    setResult(null);
    setWaitingForGuess(false);
    setSubmittedSituation('');
  };

  const getOppositePlayerIndex = () => {
    const totalPlayers = players.length;
    return (currentPlayerIndex + Math.floor(totalPlayers/2)) % totalPlayers;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmittedSituation(situation);
    setWaitingForGuess(true);
  };

  const handleGuess = async (guess) => {
    try {
      const response = await axios.post('http://localhost:5000/analyze', { situation: submittedSituation });
      setResult(response.data);
      
      const updatedPlayers = [...players];
      const oppositePlayerIndex = getOppositePlayerIndex();
      
      // Calculate if guess was correct
      const isLegal = response.data.verdict === 'YES';
      const guessedCorrectly = (guess === 'legal' && isLegal) || (guess === 'illegal' && !isLegal);
      
      // Update scores
      if (guessedCorrectly) {
        updatedPlayers[oppositePlayerIndex].score += 5; // Correct guess
      } else {
        updatedPlayers[oppositePlayerIndex].score = Math.max(0, updatedPlayers[oppositePlayerIndex].score - 1); // Wrong guess, minimum 0
      }
      
      setPlayers(updatedPlayers);
      setWaitingForGuess(false);
      setSituation('');
    } catch (error) {
      console.error('Error:', error);
      setWaitingForGuess(false);
    }
  };

  const handleSingleQuery = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/analyze', { situation });
      setResult(response.data);
      setSituation('');
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
    setEditingName(players[index].name);
  };

  const handlePlayerNameChange = (index, newName) => {
    const updatedPlayers = [...players];
    updatedPlayers[index].name = newName;
    updatedPlayers[index].isEditing = false;
    setPlayers(updatedPlayers);
  };

  const handleNameKeyPress = (e, index) => {
    if (e.key === 'Enter') {
      handlePlayerNameChange(index, editingName);
    }
  };

  const nextTurn = () => {
    setCurrentPlayerIndex((prev) => (prev + 1) % players.length);
    resetState();
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
                    value={editingName}
                    onChange={(e) => setEditingName(e.target.value)}
                    onBlur={() => handlePlayerNameChange(index, editingName)}
                    onKeyPress={(e) => handleNameKeyPress(e, index)}
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
            className={`player-score ${index === currentPlayerIndex ? 'current-player' : ''} ${index === getOppositePlayerIndex() ? 'opposite-player' : ''}`}
          >
            {player.isEditing ? (
              <input
                type="text"
                value={editingName}
                onChange={(e) => setEditingName(e.target.value)}
                onBlur={() => handlePlayerNameChange(index, editingName)}
                onKeyPress={(e) => handleNameKeyPress(e, index)}
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
      
      {!waitingForGuess ? (
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
          <div className="button-group">
            <button type="submit" className="submit-btn">
              Submit Situation
            </button>
          </div>
        </form>
      ) : (
        <div className="guess-section">
          <h2 className="current-player-turn">
            {players[getOppositePlayerIndex()].name}'s Turn to Guess
          </h2>
          <div className="situation-display">
            <p>{submittedSituation}</p>
          </div>
          <div className="button-group">
            <button 
              onClick={() => handleGuess('legal')} 
              className="submit-btn legal-btn"
            >
              Legal
            </button>
            <button 
              onClick={() => handleGuess('illegal')} 
              className="submit-btn illegal-btn"
            >
              Not Legal
            </button>
          </div>
        </div>
      )}

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
          <div className="button-group">
            <button onClick={nextTurn} className="submit-btn">
              Next Turn
            </button>
            <button 
              onClick={() => {
                resetState();
                setMode('setup');
              }} 
              className="submit-btn"
            >
              Back to Setup
            </button>
          </div>
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
          <div className="button-group">
            <button 
              onClick={() => resetState()} 
              className="submit-btn"
            >
              Analyze Another Scenario
            </button>
            <button 
              onClick={() => {
                resetState();
                setMode('setup');
              }} 
              className="submit-btn"
            >
              Back to Setup
            </button>
          </div>
        </div>
      )}
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