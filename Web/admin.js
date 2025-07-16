function loadAdminContent(contentFile) {
    // Load admin content dynamically
    var xhr = new XMLHttpRequest();
    xhr.open('GET', contentFile, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('admin-content').innerHTML = xhr.responseText;
        }
    };
    xhr.send();
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
