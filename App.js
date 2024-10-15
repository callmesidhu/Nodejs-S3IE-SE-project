const express = require('express');
const path = require('path');
const { fetchData } = require('./actions/fetchData'); 

const app = express();
const PORT = process.env.PORT || 3000;


app.use(express.static(path.join(__dirname, 'public')));


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});


fetchData(app);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
