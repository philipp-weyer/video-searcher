import React, { useState } from 'react';
import { Button, Modal, Form, InputGroup } from 'react-bootstrap';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUpload } from '@fortawesome/free-solid-svg-icons';

import config from './config.json';

const UploadButton = (props) => {
  const [showPopup, setShowPopup] = useState(false);
  const [title, setTitle] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('video', selectedFile);

    try {
      await fetch(config['BACKEND_URL'] + '/uploadVideo', {
        method: 'POST',
        body: formData,
      }).then(data => data.json()).then(res => console.log(res.message));
      // Handle success
      setShowPopup(false);
      props.getVideos();
    } catch (error) {
      // Handle error
      console.error('Error uploading the file:', error);
    }
  };

  return (
    <>
      <Button variant="outline-secondary" onClick={() => setShowPopup(true)}>
        <FontAwesomeIcon size="lg" icon={faUpload} style={{marginRight:'10px'}}/>
        Upload
      </Button>
      <Modal show={showPopup} onHide={() => setShowPopup(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Upload Video</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <p>Title</p>
            <Form.Group controlId="videoTitle">
              <Form.Control
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </Form.Group>
            <p style={{marginTop: '10px'}}>Select Video</p>
            <InputGroup>
              <Form.Control
                type="file"
                id="fileInput"
                accept=".mp4"
                onChange={handleFileChange}
                style={{display: 'block'}}
              />
            </InputGroup>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowPopup(false)}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleUpload} disabled={title == '' || selectedFile == null}>
            Upload
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default UploadButton;
