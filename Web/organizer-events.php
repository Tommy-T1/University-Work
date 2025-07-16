<?php

try {
    $pdo = new PDO("mysql:host=localhost;dbname=web_db", "root", "123");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $pdo->prepare("SELECT event_id, event_name, event_date FROM events");
    $stmt->execute();
    $events = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Close the database connection
    $pdo = null;
} catch (PDOException $e) {
    echo "Error: " . $e->getMessage();
}

echo '<h2>View Events</h2>';
echo '<ul>';
foreach ($events as $event) {
    echo '<li>' . $event['event_name'] . ' - ' . $event['event_date'] . '</li>';
}
echo '</ul>';
?>
