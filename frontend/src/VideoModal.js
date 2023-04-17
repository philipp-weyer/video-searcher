import React, { useState, useEffect } from 'react';

import {
  Button,
  Modal,
  Row,
  Col,
  Container,
  InputGroup,
  Form
} from 'react-bootstrap';

import DeleteDialog from './DeleteDialog.js';

const VideoModal = ({ show, onHide, video }) => {
  const [segments, setSegments] = useState([]);

  function getSegments(input='') {
    if (video) {
      let urlComponent = video._id;
      if (input !== '') {
        urlComponent += `?text=${encodeURIComponent(input)}`;
      }
      fetch('/getSegments/' + urlComponent)
        .then((data) => data.json())
        .then((res) => setSegments(res));
    } else {
      setSegments([]);
    }
  }

  useEffect(() => getSegments(), []);

  const [hoverSegment, setHoverSegment] = useState(null);

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

  function textElement(segment) {
    let fontSize = segment.id == hoverSegment ? '14px' : '12px';

    if (segment.highlights === undefined || segment.highlights.length == 0) {
      return (<p style={{fontSize: fontSize}}>{segment.text}</p>);
    }

    let texts = segment.highlights[0].texts;

    return (
      <p style={{fontSize: fontSize}}>
        {texts.map((doc, index) => {
          if (doc.type == 'text') {
            return <span key={index}>{doc.value}</span>
          } else {
            return <b key={index}>{doc.value}</b>
          }
        })}
      </p>
    );
  }

  function skipVideo(seconds) {
    document.getElementById('videoElement').currentTime = seconds;
  }

  const [deleteSelected, setDeleteSelected] = useState(false);

  function deleteVideo(video) {
    fetch('/deleteVideo/' + video._id)
      .then((data) => data.json())
      .then(onHide);
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
        <Container fluid>
          <Row>
            {video && (
              <Col lg={9}>
                <video id="videoElement" width="100%" height="auto" controls src={'/' + video.path}></video>
                <Button
                  variant='danger'
                  onClick={() => setDeleteSelected(true)}
                >
                  Delete Video
                </Button>
              </Col>
            )}
            <Col lg={3}>
              <p>Video Segments</p>
              <InputGroup className="mb-3">
                <Form.Control
                  aria-label="Text to search for"
                  onChange={(e) => getSegments(e.target.value)}
                />
              </InputGroup>
              <div style={{maxHeight: '70vh', overflowY: 'auto'}}>
                {segments.map((segment) => {
                  return (
                    <div key={segment.id}>
                      <div
                        style={{
                          cursor: 'pointer'
                        }}
                        onClick={() => skipVideo(segment.start)}
                        onMouseEnter={() => setHoverSegment(segment.id)}
                        onMouseLeave={() => setHoverSegment(null)}
                      >
                        {timeElement(segment)}
                        {textElement(segment)}
                      </div>
                      <hr />
                    </div>
                  );
                })}
              </div>
            </Col>
          </Row>
        </Container>
        <DeleteDialog
          show={deleteSelected}
          onHide={() => setDeleteSelected(false)}
          onDelete={() => {setDeleteSelected(false); deleteVideo(video)}} />
      </Modal.Body>
    </Modal>
  );
};

export default VideoModal;
