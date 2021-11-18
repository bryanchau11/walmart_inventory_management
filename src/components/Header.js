import { useState, useRef } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Nav, Navbar, Container, Button, Form, FormControl, Alert } from 'react-bootstrap';
function Header() {
  const args = JSON.parse(document.getElementById('data').text);
  const [show, setShow] = useState(false);
  const textInput = useRef(null);
  const navigate = useNavigate();
  const onButtonClick = (event) => {
    event.preventDefault();
    if (textInput.current.value === '') {
      setShow(true);
    } else {
      navigate(`/command/${textInput.current.value}`);
      textInput.current.value = '';
    }
  };
  if (show) {
    return (
      <Alert variant="danger" onClose={() => setShow(false)} dismissible>
        <Alert.Heading>Oh snap! Your input is null !</Alert.Heading>
        Please enter something...
      </Alert>
    );
  }
  return (
    <div style={{ color: 'wheat' }}>
      <h1>Type your SQL command to execute</h1>
      <Form className="d-flex" onSubmit={onButtonClick}>
        <FormControl
          ref={textInput}
          type="text"
          placeholder="Type your SQL Command"
          className="me-2"
          aria-label="Search"
        />
        <Button onClick={onButtonClick} variant="outline-success">
          EXECUTE
        </Button>
      </Form>
    </div>
  );
}

export default Header;
