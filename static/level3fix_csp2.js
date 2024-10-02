console.log("level3fix_csp2.js loaded");

var currentTab = null;  // Track the current tab

// Function to sanitize the input (basic HTML escaping)
function sanitizeInput(input) {
  var div = document.createElement('div');
  div.appendChild(document.createTextNode(input));
  return div.innerHTML;  // Return the sanitized content
}

function chooseTab(num) {
  console.log("Choosing tab:", num);
  if (num === currentTab) return;  // Prevent reloading the same tab
  currentTab = num;  // Set the current tab

  // Sanitize the input and load content for the selected tab
  var sanitizedNum = sanitizeInput(num);
  var html = "Image " + parseInt(sanitizedNum) + "<br>";
  html += "<img src='/static/level3/cloud" + sanitizedNum + ".jpg' />";
  $('#tabContent').html(html);  // Inject sanitized content with jQuery

  // Update the URL hash only if it has changed
  if (window.location.hash !== '#' + sanitizedNum) {
    window.location.hash = sanitizedNum;
  }

  // Update active tab style
  $('.tab').each(function() {
    if (this.id === "tab" + sanitizedNum) {
      $(this).addClass('active');
    } else {
      $(this).removeClass('active');
    }
  });

  // Post message to parent frame (mimicking game-frame.js behavior)
  if (window.top !== window.self) {
    top.postMessage(window.location.toString(), "*");
  }
}

// Load the appropriate tab based on the hash when the page loads
window.onload = function() {
  console.log("Page loaded");
  var hashValue = unescape(window.location.hash.substr(1)) || "1";
  chooseTab(hashValue);

  // Add event listeners to tabs using jQuery
  $('#tab1').click(function() {
    chooseTab('1');
  });
  $('#tab2').click(function() {
    chooseTab('2');
  });
  $('#tab3').click(function() {
    chooseTab('3');
  });
};

// Add event listener to detect changes in the URL hash and update content
window.addEventListener("hashchange", function() {
  var hashValue = unescape(window.location.hash.substr(1));
  chooseTab(hashValue);
}, false);

// Mimic parent page communication (iframes, etc.)
window.addEventListener("message", function(event) {
  if (event.source === parent) {
    var hashValue = unescape(window.location.hash.substr(1));
    chooseTab(hashValue);
  }
}, false);
