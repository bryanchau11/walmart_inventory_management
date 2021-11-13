/* eslint-disable array-callback-return */
import { useParams, Link } from 'react-router-dom';
import { React, useState, useEffect, useRef } from 'react';

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
    <div>
      This is your sql command: {command}
      {error}
      <br />
      <ul>
        {result.map((item) => (
          <li>
            {item.map((i) => (
              <div>{i} |</div>
            ))}
          </li>
        ))}
      </ul>
    </div>
  );
}
export default Command;
