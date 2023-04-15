import React, { useState, useEffect } from 'react';

import { Modal, Button } from 'react-bootstrap';

const DeleteDialog = ({ show, onHide, onDelete }) => {
  return (
    <Modal
      show={show}
      onHide={onHide} centered
    >
      <Modal.Header closeButton>
        <Modal.Title>Delete Video</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p>Are you sure you want to delete this video and all of its segment information?</p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant='secondary' onClick={onHide}>Cancel</Button>
        <Button variant='primary' onClick={onDelete}>Delete</Button>
      </Modal.Footer>
    </Modal>
  );
};

export default DeleteDialog;
