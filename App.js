const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const { fetchData } = require('./actions/fetchData'); 
const { handleFormSubmission } = require('./actions/submitData');

const app = express();
const PORT = process.env.PORT || 3000;



app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json()); 
app.use(bodyParser.json());



app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});


app.post('/submit', async (req, res) => {
        const formData = req.body;
        console.log('Form data received:', formData);  // Log incoming form data
        try {
            await appendToSheet(formData);
            res.send('Form data successfully submitted to Google Sheets.');
        } catch (err) {
            console.error('Error submitting data:', err);  // Log the actual error
            res.status(500).send('Error submitting data.');
        }
    });


fetchData(app);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
