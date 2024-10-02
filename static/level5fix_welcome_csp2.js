document.getElementById('signup-link').addEventListener('click', function(event) {
    var href = event.target.getAttribute('href');
    if (href.toLowerCase().startsWith('javascript:') || href.toLowerCase().startsWith('data:')) {
        event.preventDefault();
        alert('Nice try. Blocked potentially dangerous URL.');
    }
});
