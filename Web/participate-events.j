const express = require('express');
const mysql = require('mysql');
const app = express();
const port = 3000;

// Database connection
const connection = mysql.createConnection({
  host: 'your_database_host',
  user: 'your_database_user',
  password: 'your_database_password',
  database: 'your_database_name'
});

connection.connect();

// Endpoint to get events from the database
app.get('/participate-events', (req, res) => {
  const query = 'SELECT * FROM events'; // Replace 'events' with your actual table name

  connection.query(query, (error, results) => {
    if (error) {
      res.status(500).json({ error: 'Internal Server Error' });
    } else {
      res.json(results);
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
