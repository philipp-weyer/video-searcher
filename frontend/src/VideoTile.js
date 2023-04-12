import {useState, useEffect} from 'react';

import { Card } from 'react-bootstrap';

function VideoTile(props) {
  return (
    <Card style={{
      paddingTop: '10px',
      cursor: 'pointer'
    }}>
      <Card.Img variant="top" src={props.video.img} style={{
        'height': '100px',
        'width': '100%',
        'objectFit': 'contain',
        'display': 'block'
      }}/>
      <Card.Body>
        <Card.Text>{props.video.title}</Card.Text>
      </Card.Body>
    </Card>
  );
}

export default VideoTile;
