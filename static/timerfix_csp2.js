function startTimer(seconds) {
    seconds = parseInt(seconds) || 3;
    setTimeout(function() { 
      window.alert("Time is up!");  // This alert should now work
      window.history.back();  // Go back to the previous page
    }, seconds * 1000);
  }
  
  // Move onload event to JavaScript
  window.addEventListener('DOMContentLoaded', function() {
    const loadingGif = document.querySelector('img[src="/static/loading.gif"]');
    const timerValue = loadingGif.getAttribute('data-timer');  // Fetch the timer value from the data attribute
    startTimer(timerValue);  // Start the timer when the page loads
  });
  