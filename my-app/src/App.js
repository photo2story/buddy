import React, { useEffect, useState } from 'react';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/data') // 백엔드 API 엔드포인트
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>React와 Flask 연동</h1>
        {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>Loading...</p>}
      </header>
    </div>
  );
}

export default App;
