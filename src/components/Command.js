/* eslint-disable array-callback-return */
import { useParams, Link } from 'react-router-dom';
import { React, useState, useEffect, useRef } from 'react';
import '../App.css';
function Command() {
  const { command } = useParams();
  const [result, setResult] = useState([]);
  const [error, setError] = useState();
  useEffect(() => {
    const requestData = { command: command };

    fetch('/execute_command', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    })
      .then((response) => response.json())
      .then((data) => {
        //const myList = JSON.parse(data.result);
        console.log(data.result);
        setResult(data.result);
        setError(data.error);
      });
  }, [command]);
  return (
    <div style={{ color: 'wheat', fontSize: '25px' }}>
      This is your sql command: {command}
      {error}
      <br />
      <table className="walmart">
        {result.map((item) => (
          <tr style={{ color: 'wheat' }}>
            {item.map((i) => (
              <td style={{ color: 'wheat' }}>{i}</td>
            ))}
          </tr>
        ))}
      </table>
    </div>
  );
}
export default Command;
