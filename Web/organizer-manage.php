<?php
/
try {
    $pdo = new PDO("mysql:host=localhost;dbname=web_db", "root", "123");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $pdo->prepare("SELECT participant_id, participant_name, participant_email FROM participants");
    $stmt->execute();
    $participants = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Close the database connection
    $pdo = null;
} catch (PDOException $e) {
    echo "Error: " . $e->getMessage();
}

echo '<h2>Manage Participants</h2>';
echo '<table>';
echo '<tr><th>Participant ID</th><th>Name</th><th>Email</th></tr>';
foreach ($participants as $participant) {
    echo '<tr>';
    echo '<td>' . $participant['participant_id'] . '</td>';
    echo '<td>' . $participant['participant_name'] . '</td>';
    echo '<td>' . $participant['participant_email'] . '</td>';
    echo '</tr>';
}
echo '</table>';
?>
