import React, {useState, useEffect} from 'react';

import { Spinner } from 'react-bootstrap';

const LoadingBanner = () => {
  const [missingSubtitles, setMissingSubtitles] = useState([]);

  function getSubtitleStatus() {
    fetch('/getSubtitleStatus')
      .then(data => data.json())
      .then(res => setMissingSubtitles(res));
  }

  const [intervalId, setIntervalId] = useState(null);

  useEffect(() => {
    getSubtitleStatus();
    const id = setInterval(getSubtitleStatus, 2000);
    return () => clearInterval(id);
  }, []);

  let subtitleString = '';

  if (missingSubtitles.length == 1) {
    subtitleString = `"${missingSubtitles[0].title}".`;
  } else if (missingSubtitles.length > 1) {
    subtitleString = 'multiple videos.';
  }

  return (
    <div style={{background: 'tomato', width: '100%', borderRadius: '5px'}}>
      {missingSubtitles.length > 0 ?
        <div style={{position: 'relative', padding: '5px', marginBottom: '10px', height: '50px'}}>
          <Spinner animation='border' style={{
            position: 'absolute',
            top: '20%',
            left: '20px'
          }}/>
          <span style={{
            position: 'absolute',
            top: '50%',
            left: '70px',
            transform: 'translateY(-50%)'}}
          >
            Loading subtitles for {subtitleString}
          </span>
        </div>: null
      }
    </div>
  );
};

export default LoadingBanner;
