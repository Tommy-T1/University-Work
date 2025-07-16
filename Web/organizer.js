// organizer.js

function loadOrganizerContent(contentFile) {
    // Load organizer content dynamically
    var xhr = new XMLHttpRequest();
    xhr.open('GET', contentFile, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('organizer-content').innerHTML = xhr.responseText;
        }
    };
    xhr.send();

    // Load organizer events if the contentFile is 'organizer-events.php'
    if (contentFile === 'organizer-events.php') {
        fetchOrganizerEvents();
    }
}

function fetchOrganizerEvents() {
    // Fetch organizer's events from the server
    fetch('/get-organizer-events.php')
        .then(response => response.json())
        .then(data => displayOrganizerEvents(data))
        .catch(error => console.error('Error:', error));
}

function displayOrganizerEvents(events) {
    const organizerContent = document.getElementById('organizer-content');

    if (events.length > 0) {
        const eventList = document.createElement('ul');

        events.forEach(event => {
            const listItem = document.createElement('li');
            listItem.textContent = event.event_name;
            eventList.appendChild(listItem);
        });

        organizerContent.appendChild(eventList);
    } else {
        organizerContent.innerHTML = '<p>No events found.</p>';
    }
}

function logout() {
    // Perform logout on the server side
    var logoutXHR = new XMLHttpRequest();
    logoutXHR.open('GET', 'logout.php', true);
    logoutXHR.onreadystatechange = function() {
        if (logoutXHR.readyState == 4 && logoutXHR.status == 200) {
            // Redirect to the login page
            window.location.href = 'login.html';
        }
    };
    logoutXHR.send();
}
