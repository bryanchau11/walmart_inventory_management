import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';

function App() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"
  const args = JSON.parse(document.getElementById('data').text);

  // TODO: Implement your main page as a React component.
  return (
    <div>
      {args.list.map((i) => (
        <div>{i[0]}</div>
      ))}
    </div>
  );
}

export default App;
