const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(bodyParser.json());

// Database connection
const connection = mysql.createConnection({
  host: 'your_database_host',
  user: 'your_database_user',
  password: 'your_database_password',
  database: 'your_database_name'
});

connection.connect();

// Endpoint to get available events
app.get('/available-events', (req, res) => {
  const query = 'SELECT * FROM available_events'; // Replace 'available_events' with your actual table name

  connection.query(query, (error, results) => {
    if (error) {
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json(results);
    }
  });
});

// Endpoint to book an event
app.post('/book-event', (req, res) => {
  const userEmail = req.query.user;
  const eventName = req.query.event;

  const query = 'INSERT INTO booked_events (user_email, event_name) VALUES (?, ?)';

  connection.query(query, [userEmail, eventName], (error, results) => {
    if (error) {
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json({ success: true, message: 'Event booked successfully.' });
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
