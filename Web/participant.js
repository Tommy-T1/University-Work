function loadParticipantContent(contentFile) {
    // Load participant content dynamically
    var xhr = new XMLHttpRequest();
    xhr.open('GET', contentFile, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById('participant-content').innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}
