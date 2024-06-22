// index.js

const express = require('express');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

// 정적 파일 제공 설정
app.use(express.static(path.join(__dirname, 'static')));

// 라우트 설정
app.get('/', (req, res) => {
  res.send('Hello, Node.js!');
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
