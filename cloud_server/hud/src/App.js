import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [currentTemp, setCurrentTemp] = useState(0);
  const [currentBrightness, setCurrentBrightness] = useState(0);
  const [motion_state, setMotionState] = useState(0);
  
  useEffect(() => {
    fetch('/temperature').then(res => res.json()).then(data => {
      setCurrentTemp(data.temp);
    });
  }, []);

  useEffect(() => {
    fetch('/brightness').then(res => res.json()).then(data => {
      setCurrentBrightness(data.brightness);
    });
  }, []);

  useEffect(() => {
    fetch('/motion_state').then(res => res.json()).then(data => {
      setMotionState(data.motion_state);
    });
  }, []);

  return (
    <div className="App">
      {<header className="App-header">
        <p>The current temperature is {currentTemp}.</p>
        <p>The current brightness is {currentBrightness}.</p>
        <p>The current motion state is {motion_state}.</p>
      </header>}
    </div>
  );
}

export default App;