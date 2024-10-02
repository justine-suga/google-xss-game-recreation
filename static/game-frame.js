// Post a message to the parent window to simulate game-frame.js behavior
window.onload = function() {
    if (window.top !== window.self) {
        top.postMessage(window.location.toString(), "*");
    }
};

// Utility to sanitize input to prevent XSS
function sanitizeInput(input) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(input));
    return div.innerHTML; // Escape user input before inserting it into the DOM
}

// Handle tab switching and content loading
function chooseTab(num) {
    var tabContent = document.getElementById('tabContent');
    var sanitizedNum = sanitizeInput(num);
    var html = "Image " + parseInt(sanitizedNum) + "<br>";
    html += "<img src='/static/level3/cloud" + sanitizedNum + ".jpg' />";
    tabContent.innerHTML = html; // Inject sanitized content

    // Update the URL hash to reflect the active tab
    if (window.location.hash !== '#' + sanitizedNum) {
        window.location.hash = sanitizedNum;
    }

    // Update the active tab styles
    var tabs = document.querySelectorAll('.tab');
    tabs.forEach(function(tab) {
        if (tab.id === "tab" + sanitizedNum) {
            tab.className = "tab active";
        } else {
            tab.className = "tab";
        }
    });
}

// Automatically load the correct tab based on the URL hash when the page loads
window.onload = function() {
    var hashValue = unescape(window.location.hash.substr(1)) || "1";
    chooseTab(hashValue);

    // Add event listeners to each tab for handling clicks
    document.getElementById('tab1').addEventListener('click', function() {
        chooseTab('1');
    });
    document.getElementById('tab2').addEventListener('click', function() {
        chooseTab('2');
    });
    document.getElementById('tab3').addEventListener('click', function() {
        chooseTab('3');
    });
};

// Listen for hash changes and update the tab content accordingly
window.addEventListener("hashchange", function() {
    var hashValue = unescape(window.location.hash.substr(1));
    chooseTab(hashValue);
}, false);

// Handle postMessage events (e.g., for communication between iframes)
window.addEventListener("message", function(event) {
    if (event.source === parent) {
        var hashValue = unescape(window.location.hash.substr(1));
        chooseTab(hashValue);
    }
}, false);
