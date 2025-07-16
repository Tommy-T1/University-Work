<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $servername = "myserver";
    $username = "rppt";
    $password = "123";
    $dbname = "web_db";

    $conn = new mysqli($servername, $username, $password, $dbname);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $email = $_POST['email'];
    $newPassword = password_hash($_POST['new_password'], PASSWORD_DEFAULT);

    $sql = "UPDATE users SET password = '$newPassword' WHERE email = '$email'";

    if ($conn->query($sql) === TRUE) {
        echo "Password reset successfully!";
        
        // Send email (You need to set up a mail server for this to work)
        $to = $email;
        $subject = "Password Reset";
        $message = "Your password for the email $email has been reset successfully.";
        $headers = "From: bookingwebsite.com";

        mail($to, $subject, $message, $headers);
    } else {
        echo "Error updating password: " . $conn->error;
    }

    $conn->close();
}
?>
