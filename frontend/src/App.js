import {
  Button,
  Container,
  Row,
  Col,
  InputGroup,
  DropdownButton,
  Dropdown,
  Form,
  FormControl,
  Modal,
  Table
} from 'react-bootstrap';
import React, {useState, useEffect} from 'react';
import './App.scss';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMagnifyingGlass, faUpload } from '@fortawesome/free-solid-svg-icons';

function App() {
  return (
    <Container className="App" style={{"paddingTop": "15px"}}>
      <Row style={{marginBottom: '20px'}}>
        <Col align="center">
          <p className="title">MongoDB Video Searcher</p>
          <img src="/mongodb_logo.png" height="45px"/>
        </Col>
      </Row>
      <Row>
        <Col align="center">
          <InputGroup className="mb-3">
            <Button variant="outline-secondary" id="searchButton">
              <FontAwesomeIcon size="lg" icon={faUpload} style={{marginRight:'10px'}}/>
              Upload
            </Button>
            <Form.Control
              aria-label="Text to search for"
            />
            <Button variant="outline-primary" id="searchButton">
              <FontAwesomeIcon size="lg" icon={faMagnifyingGlass}/>
            </Button>
          </InputGroup>
        </Col>
      </Row>
    </Container>
  );
}

export default App;
