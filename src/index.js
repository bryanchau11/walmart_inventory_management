import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Command from './components/Command';
import Header from './components/Header';
const routing = (
  <Router>
    <div>
      <Header />
      <Routes>
        <Route exact path="/index" element={<App />} />
        <Route exact path="/command/:command" element={<Command />} />
      </Routes>
    </div>
  </Router>
);
ReactDOM.render(routing, document.getElementById('root'));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
