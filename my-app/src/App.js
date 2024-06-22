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
      // Heroku 서버에서 이미지를 가져오는 코드
      const imageUrl = 'https://my-buddy-app-355192a036b3.herokuapp.com/image/comparison_AAPL_VOO.png';
      setReviews([{ stockName: 'AAPL', imageUrl }]);
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
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
