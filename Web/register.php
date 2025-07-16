<?php
require_once('db_config.php');

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST["email"];
    $username = $_POST["username"];
    $password = password_hash($_POST["password"], PASSWORD_BCRYPT);
    $role = $_POST["role"];

    $checkUserQuery = "SELECT * FROM users WHERE username = '$username' OR email = '$email'";
    $checkUserResult = $conn->query($checkUserQuery);

    if ($checkUserResult->num_rows > 0) {
        echo "User with this email or username already exists. Please choose another.";
    } else {
        $insertUserQuery = "INSERT INTO users (email, username, password, role) VALUES ('$email', '$username', '$password', '$role')";

        if ($conn->query($insertUserQuery) === TRUE) {
            echo "Registration successful! You can now login.";
        } else {
            echo "Error: " . $insertUserQuery . "<br>" . $conn->error;
        }
    }
}

$conn->close();
?>
