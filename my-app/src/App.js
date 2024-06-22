import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await axios.get('https://api.github.com/repos/photo2story/buddy/contents/comparison_AAPL_VOO.png');
        const fileData = response.data;
        setImageUrl(fileData.download_url);
      } catch (error) {
        console.error('Error fetching the image:', error);
      }
      setLoading(false);
    };

    fetchImage();
  }, []);

  return (
    <div className="App">
      <h1>React와 Flask 연동</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        imageUrl && <img src={imageUrl} alt="AAPL vs VOO" style={{ width: '100%' }} />
      )}
    </div>
  );
}

export default App;
