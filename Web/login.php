<?php
require_once('db_config.php');

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    $query = "SELECT * FROM users WHERE username = '$username'";
    $result = $conn->query($query);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if (password_verify($password, $row["password"])) {
            // Password is correct, redirect based on user role
            switch ($row["role"]) {
                case 'admin':
                    header("Location: admin.php");
                    break;
                case 'organizer':
                    header("Location: organizer.php");
                    break;
                case 'participant':
                    header("Location: participant.php");
                    break;
                default:
                    header("Location: default.php");
            }
        } else {
            echo "Invalid password.";
        }
    } else {
        echo "User not found.";
    }
}

$conn->close();
?>
