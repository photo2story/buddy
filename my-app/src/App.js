import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [stockName, setStockName] = useState('');
  const [imageUrl, setImageUrl] = useState('');

  const handleInputChange = (event) => {
    setStockName(event.target.value.toUpperCase());
  };

  const handleSearch = async () => {
    try {
      const response = await axios.get(`/image/comparison_${stockName}_VOO.png`);
      setImageUrl(response.config.url);
    } catch (error) {
      console.error('Error fetching image:', error);
      alert('이미지를 찾을 수 없습니다. 다시 시도해 주세요.');
    }
  };

  return (
    <div className="App">
      <h1>React와 Flask 연동</h1>
      <input 
        type="text" 
        id="stockName" 
        value={stockName}
        onChange={handleInputChange}
        placeholder="Enter stock name"
      />
      <button id="searchReviewButton" onClick={handleSearch}>Search</button>
      {imageUrl && (
        <div>
          <h3>{stockName} vs VOO</h3>
          <img 
            src={imageUrl} 
            alt={`${stockName} vs VOO`} 
            style={{ width: '100%' }} 
          />
        </div>
      )}
    </div>
  );
}

export default App;
