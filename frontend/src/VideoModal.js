import React, { useState, useEffect } from 'react';

import { Modal, Row, Col, Container, InputGroup, Form } from 'react-bootstrap';

import config from './config.json';

const VideoModal = ({ show, onHide, video }) => {
  const [segments, setSegments] = useState([]);

  function getSegments() {
    if (video) {
      fetch(config['BACKEND_URL'] + '/getSegments/' + video._id)
        .then((data) => data.json())
        .then((res) => setSegments(res));
    } else {
      setSegments([]);
    }
  }

  useEffect(() => getSegments(), []);
  if (segments.length > 0) {
    console.log(segments[0])
  }

  function timeElement(segment) {
    function getTime(seconds) {
      const hours = Math.floor(seconds / 3600);
      seconds = seconds - hours * 3600;
      const minutes = Math.floor(seconds / 60);
      seconds = seconds - minutes * 60;
      seconds = Math.floor(seconds);

      let ret = seconds.toLocaleString('en-US', {minimumIntegerDigits: 2});
      ret = minutes.toLocaleString('en-US', {minimumIntegerDigits: 2}) + ':' + ret;

      if (hours > 0) {
        ret = hours.toLocaleString('en-US', {minimumIntegerDigits: 2}) + ':' + ret;
      }

      return ret;
    }


    const timeString = getTime(segment.start) + ' - ' + getTime(segment.end);

    return (
      <p style={{color: 'blue'}}>{timeString}</p>
    );
  }

  function skipVideo(seconds) {
    document.getElementById('videoElement').currentTime = seconds;
  }

  return (
    <Modal
      show={show}
      onHide={() => {setSegments([]); onHide()}} centered fullscreen
      onShow={getSegments}
    >
      <Modal.Header closeButton>
        <Modal.Title>{video?.title}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Container>
          <Row>
            {video && (
              <Col lg={9}>
                <video id="videoElement" width="100%" height="auto" controls src={config['ASSET_PREFIX'] + '/' + video.path}></video>
              </Col>
            )}
            <Col lg={3}>
              <p>Video Segments</p>
            <InputGroup className="mb-3">
              <Form.Control
                aria-label="Text to search for"
              />
            </InputGroup>
              <div>
                {segments.map((segment) => {
                  return (
                    <div key={segment.id} style={{cursor: 'pointer'}} onClick={() => skipVideo(segment.start)}>
                      {timeElement(segment)}
                      <p style={{fontSize: '12px'}}>{segment.text}</p>
                      <hr />
                    </div>
                  );
                })}
            </div>
            </Col>
          </Row>
        </Container>
      </Modal.Body>
    </Modal>
  );
};

export default VideoModal;
