function escapeHTML(str) {
    // Basic HTML escape to prevent script injection
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }
  
  function Post(message) { 
    this.message = message;
    this.date = (new Date()).getTime();
  }
  
  function PostDB(defaultMessage) {
    this._defaultMessage = defaultMessage || "";
  
    this.setup = function() {
      var defaultPost = new Post(escapeHTML(defaultMessage));
      window.localStorage["postDB"] = JSON.stringify({
        "posts" : [defaultPost]
      });
    };
  
    this.save = function(message, callback) {
      var newPost = new Post(escapeHTML(message));  // Escape message before saving
      var allPosts = this.getPosts();
      allPosts.push(newPost);
      window.localStorage["postDB"] = JSON.stringify({
        "posts" : allPosts
      });
  
      callback();
      return false;
    };
  
    this.clear = function(callback) {
      this.setup();
      callback();
      return false;
    };
  
    this.getPosts = function() {
      return JSON.parse(window.localStorage["postDB"]).posts;
    };
  
    if(!window.localStorage["postDB"]) { 
      this.setup();
    }
  }
  
  var defaultMessage = "Welcome! This is your personal stream. You can post anything you want here, especially madness.";
  
  var DB = new PostDB(defaultMessage);
  
  function displayPosts() {
    var containerEl = document.getElementById("post-container");
    containerEl.innerHTML = "";
  
    var posts = DB.getPosts();
    for (var i=0; i<posts.length; i++) {
      var html = '<div class="message-container">';
      html += '<b>You </b>';
      html += '<span class="date">' + new Date(posts[i].date) + '</span>';
      html += "<blockquote>" + posts[i].message + "</blockquote>";  // Already escaped
      html += "</div>";
      containerEl.innerHTML += html; 
    }
  }
  
  window.onload = function() { 
    document.getElementById('clear-form').onsubmit = function() {
      DB.clear(function() { displayPosts() });
      return false;
    }
  
    document.getElementById('post-form').onsubmit = function() {
      var message = document.getElementById('post-content').value;
      DB.save(message, function() { displayPosts() } );
      document.getElementById('post-content').value = "";
      return false;
    }
  
    displayPosts();
  }
  