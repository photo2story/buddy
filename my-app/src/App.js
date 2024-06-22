import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [stockName, setStockName] = useState('');
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadReviews();
  }, []);

  const loadReviews = async () => {
    setLoading(true);
    try {
      // 여기에 Heroku 서버의 이미지 목록을 가져오는 API 호출을 추가합니다.
      const response = await axios.get('/api/images');  // 수정된 부분
      const files = response.data;
      const filteredReviews = files.filter(file => file.startsWith('comparison_') && file.endsWith('.png'))
        .map(file => {
          const stockName = file.replace('comparison_', '').replace('_VOO.png', '').toUpperCase();
          return {
            stockName,
            imageUrl: `/image/${file}`  // 수정된 부분
          };
        });
      setReviews(filteredReviews);
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
    setLoading(false);
  };

  const handleInputChange = (event) => {
    setStockName(event.target.value.toUpperCase());
  };

  const handleSearch = () => {
    const review = reviews.find(review => review.stockName.includes(stockName));
    if (review) {
      document.getElementById(`review-${review.stockName}`).scrollIntoView({ behavior: 'smooth' });
    } else {
      alert('Review is being prepared. Please try again later.');
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
      {loading ? <p>Loading...</p> : (
        <div id="reviewList">
          {reviews.map((review, index) => (
            <div key={index} id={`review-${review.stockName}`} className="review">
              <h3>{review.stockName} vs VOO</h3>
              <img 
                id={`image-${review.stockName}`} 
                src={review.imageUrl} 
                alt={`${review.stockName} vs VOO`} 
                style={{ width: '100%' }} 
                onClick={() => window.open(review.imageUrl, '_blank')}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
