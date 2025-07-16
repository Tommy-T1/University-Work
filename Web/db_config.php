<?php
$servername = "myserver";
$username = "root";
$password = "123";
$dbname = "web_db";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
