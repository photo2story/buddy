import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    loadImage();
  }, []);

  const loadImage = async () => {
    try {
      const url = 'https://my-buddy-app-355192a036b3.herokuapp.com/image/comparison_AAPL_VOO.png';
      setImageUrl(url);
    } catch (error) {
      console.error('Error fetching image:', error);
    }
  };

  return (
    <div className="App">
      <h1>React와 Flask 연동</h1>
      {imageUrl && <img src={imageUrl} alt="Stock Comparison" style={{ width: '100%' }} />}
    </div>
  );
}

export default App;
