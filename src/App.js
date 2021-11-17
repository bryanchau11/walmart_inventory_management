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
      <table className="walmart">
        {args.product.map((i) => (
          <tr>
            <td>{i[0]} </td>
            <td>{i[1]}</td>
            <td>{i[2]}</td>
            <td>{i[3]}</td>
            <td>{i[4]}</td>
          </tr>
        ))}
      </table>
      <h1>Product Type Table</h1>
      <table className="walmart">
        {args.productType.map((i) => (
          <tr>
            <td>{i[0]} </td>
            <td>{i[1]}</td>
            <td>{i[2]}</td>
          </tr>
        ))}
      </table>
      <h1>Brand Table</h1>
      <table className="walmart">
        {args.brand.map((i) => (
          <tr>
            <td>{i[0]} </td>
          </tr>
        ))}
      </table>
      <h1>Store Table</h1>
      <table className="walmart">
        {args.store.map((i) => (
          <tr>
            <td>{i[0]} </td>
            <td>{i[1]}</td>
            <td>{i[2]}</td>
            <td>{i[3]}</td>
          </tr>
        ))}
      </table>
    </div>
  );
}

export default App;
