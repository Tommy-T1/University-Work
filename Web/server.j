const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/reset-password', (req, res) => {
    // Back-end logic to handle password reset
    const email = req.body.email;
    const newPassword = req.body.newPassword;

    // Simulate database update (replace this with actual database queries)
    console.log(`Resetting password for ${email} to ${newPassword}`);

    // Respond with a success message
    res.json({ success: true, message: 'Password reset successful.' });
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
