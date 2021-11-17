import logo from './logo.svg';
import './App.css';
import { useState, useRef } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Nav, Navbar, Container, Button, Form, FormControl, Alert } from 'react-bootstrap';
function App() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"
  const args = JSON.parse(document.getElementById('data').text);

  return (
    <div>
      <h1>Product Table</h1>
      <ul>
        {args.product.map((i) => (
          <li>
            {i[0]} {'      '} | {'      '}
            {i[1]}
            {'      '} | {'      '}
            {i[2]}
            {'      '} | {'      '}
            {i[3]}
            {'      '} | {'      '}
            {i[4]}{' '}
          </li>
        ))}
      </ul>
      <h1>Product Type Table</h1>
      <ul>
        {args.productType.map((i) => (
          <li>
            {i[0]} | {i[1]} | {i[2]}
          </li>
        ))}
      </ul>
      <h1>Brand Table</h1>
      <ul>
        {args.brand.map((i) => (
          <li>{i[0]}</li>
        ))}
      </ul>
      <h1>Store Table</h1>
      <ul>
        {args.store.map((i) => (
          <li>
            {i[0]} | {i[1]} | {i[2]} | {i[3]}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
