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

import UploadButton from './UploadButton.js';
import VideoTile from './VideoTile.js';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons';

import config from './config.json';

function uploadFile(e) {
  let file = e.target.files[0];
  let formData = new FormData();
  formData.append('video', file);

  fetch(config['BACKEND_URL'] + '/uploadVideo', {method: 'POST', body: formData})
    .then((data) => data.json()).then(res => console.log(res)).catch((e) => console.log(e));
}

function App() {
  const [videos, setVideos] = useState([]);

  function getVideos() {
    fetch(config['BACKEND_URL'] + '/getVideos')
      .then((data) => data.json())
      .then((res) => setVideos(res));
  }

  useEffect(() => getVideos(), []);

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
            <UploadButton getVideos={() => getVideos()} />
            <Form.Control
              aria-label="Text to search for"
            />
            <Button variant="outline-primary" id="searchButton">
              <FontAwesomeIcon size="lg" icon={faMagnifyingGlass}/>
            </Button>
          </InputGroup>
        </Col>
      </Row>
      <Row>
        {videos.map((video) => {
          return (
            <Col key={video._id} align='left' xs={4} md={3} lg={2} style={{
              marginBottom: '20px'
            }}>
              <VideoTile video={video} />
            </Col>
          );
        })}
      </Row>
    </Container>
  );
}

export default App;
