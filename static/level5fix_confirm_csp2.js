var safeNext = "{{ next | e }}";
if (!safeNext.startsWith("/") && !safeNext.startsWith("http")) {
    safeNext = "/";
}
if (safeNext.startsWith("javascript:")) {
    safeNext = "/";
}
setTimeout(function() { window.location = safeNext; }, 5000);
