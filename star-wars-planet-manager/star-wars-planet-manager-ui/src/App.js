import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [planets, setPlanets] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/planet')
      .then(response => {
        setPlanets(response.data.planets);
      })
      .catch(error => {
        console.error('Error fetching planets:', error);
      });
  }, []);

  return (
    <div>
      <h1>Star Wars Planet Manager</h1>
      <ul>
        {planets.map(planet => (
          <li key={planet.id}>
            <strong>Name:</strong> {planet.name}<br />
            <strong>Diameter:</strong> {planet.diameter}<br />
            <strong>Population:</strong> {planet.population}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
