import React, { useState, useEffect } from 'react';
import { BrowserRouter, Link, Switch, Route } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/api/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <BrowserRouter>
            <div>
              <Link className="App-link" to="/">Home</Link>
              &nbsp;|&nbsp;
              <Link className="App-link" to="/about">About</Link>
            </div>
            <Switch>
              <Route exact path="/">
                  <img src={logo} className="App-logo" alt="logo" />
                  <p>
                    Edit <code>src/App.js</code> and save to reload.
                  </p>
                  <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Learn React
                  </a>
                  <p>The time, {currentTime} is really a big number!.</p>
              </Route>
              <Route path="/about">
                  <p>This page is about me!</p>
              </Route>
            </Switch>
          </BrowserRouter>
      </header>
    </div>
  );
}

export default App;
