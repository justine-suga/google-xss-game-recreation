from flask import Flask, render_template, request, make_response
import bleach
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>Assignment 2: XSS Game Recreation</title>
        </head>
        <body>
            <h2> Justine Mathurin </h2>
            <h1>XSS Game Recreation</h1>
            <p>Click below to navigate levels:</p>
            <a href="/level1">Go to Level 1</a><br>
            <a href="/level2">Go to Level 2</a><br>
            <a href="/level3">Go to Level 3</a><br>
            <a href="/level4">Go to Level 4</a><br>
            <a href="/level5/welcome">Go to Level 5</a><br>
            <a href="/level6#static/gadget.js">Go to Level 6</a><br>
            <h1>XSS Game Patch fixes</h1>
            <p>Click below to navigate patched levels:</p>
            <a href="/level1fix">Go to Level 1</a><br>
            <a href="/level2fix">Go to Level 2</a><br>
            <a href="/level3fix">Go to Level 3</a><br>
            <a href="/level4fix">Go to Level 4</a><br>
            <a href="/level5fix/welcome">Go to Level 5</a><br>
            <a href="/level6fix#static/gadget.js">Go to Level 6</a><br>
            <h1>XSS Game CSP 2.0</h1>
            <p>Click below to navigate patched levels with CSP 2.0 protection:</p>
            <a href="/level1fix_csp2">Go to Level 1</a><br>
            <a href="/level2fix_csp2">Go to Level 2</a><br>
            <a href="/level3fix_csp2">Go to Level 3</a><br>
            <a href="/level4fix_csp2">Go to Level 4</a><br>
            <a href="/level5fix_welcome_csp2">Go to Level 5</a><br>
            <a href="/level6fix_csp2#static/gadget.js">Go to Level 6</a><br>
            <h1>XSS Game CSP 3.0</h1>
            <p>Click below to navigate patched levels with CSP 3.0 protection:</p>
            <a href="/level1fix_csp3">Go to Level 1</a><br>
            <a href="/level2fix_csp3">Go to Level 2</a><br>
            <a href="/level3fix_csp3">Go to Level 3</a><br>
            <a href="/level4fix_csp3">Go to Level 4</a><br>
            <a href="/level5fix_welcome_csp3">Go to Level 5</a><br>
            <a href="/level6fix_csp3#static/gadget.js">Go to Level 6</a><br>
        </body>
    </html>
    '''

# Original levels

@app.route('/level1', methods=['GET', 'POST'])
def level1():
    # Disable XSS protection (normally enabled by browsers)
    headers = {'X-XSS-Protection': '0'}
    
    query = request.args.get('query')
    
    if not query:
        # Render the main form when no query is present
        return '''
        <html>
            <head>
                <script src="/static/game-frame.js"></script>
                <link rel="stylesheet" href="/static/game-frame-styles.css" />
            </head>
            <body id="level1">
                <img src="/static/logos/level1.png">
                <div>
                    <form action="/level1" method="GET">
                        <input id="query" name="query" value="Enter query here..." onfocus="this.value=''">
                        <input id="button" type="submit" value="Search">
                    </form>
                    <br>
                    <a href="/" style="display: inline-block; margin-top: 10px; text-decoration: none;">
                        <button>Back to Homepage</button>
                    </a>
                </div>
            </body>
        </html>
        ''', 200, headers
    else:
        # Reflect the query in the result and include the Back to Homepage button
        return f'''
        <html>
            <head>
                <script src="/static/game-frame.js"></script>
                <link rel="stylesheet" href="/static/game-frame-styles.css" />
            </head>
            <body id="level1">
                <img src="/static/logos/level1.png">
                <div>
                    <p>Sorry, no results were found for <b>{query}</b>.</p>
                    <p><a href="/level1">Try again</a></p>
                    <br>
                    <a href="/" style="display: inline-block; margin-top: 10px; text-decoration: none;">
                        <button>Back to Homepage</button>
                    </a>
                </div>
            </body>
        </html>
        ''', 200, headers

@app.route('/level2', methods=['GET', 'POST'])
def level2():
    return render_template('level2.html')

@app.route('/level3')
def level3():
    return render_template('level3.html')

@app.route('/level4', methods=['GET'])
def level4():
    timer_value = request.args.get('timer', '3')
    return render_template('level4.html', timer=timer_value)

@app.route('/level4/timer', methods=['GET'])
def timer():
    timer_value = request.args.get('timer', '3')
    return render_template('timer.html', timer=timer_value)

@app.route('/level5/welcome', methods=['GET'])
def level5_welcome():
    return render_template('level5_welcome.html')

@app.route('/level5/signup', methods=['GET'])
def level5_signup():
    next_page = request.args.get('next', 'confirm')
    return render_template('level5_signup.html', next=next_page)

@app.route('/level5/confirm', methods=['GET'])
def level5_confirm():
    next_page = request.args.get('next', 'welcome')
    return render_template('level5_confirm.html', next=next_page)

@app.route('/level6', methods=['GET', 'POST'])
def level6():
    return render_template('level6.html')


# Patched levels
@app.route('/level1fix', methods=['GET', 'POST'])
def level1fix():
    # Keep headers, but XSS protection is handled by escaping now
    headers = {'X-XSS-Protection': '1; mode=block'}
    
    query = request.args.get('query')
    
    if not query:
        # Render the form when no query is present
        return render_template('level1fix.html')
    else:
        # Reflect the query in the result but ensure it is properly escaped
        return render_template('level1fix.html', query=query), 200, headers


ALLOWED_TAGS = ['b', 'i', 'em', 'strong', 'u', 'a', 'p', 'br']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}

@app.route('/level2fix', methods=['GET', 'POST'])
def level2fix():
    return render_template('level2fix.html')

# Sanitization function
def sanitize_input(input_text):
    return bleach.clean(input_text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)

@app.route('/level3fix')
def level3fix():
    return render_template('level3fix.html')

@app.route('/level4fix', methods=['GET'])
def level4fix():
    timer_value = request.args.get('timer', '3')
    return render_template('level4fix.html', timer=timer_value)

@app.route('/level4fix/timer', methods=['GET'])
def timerfix():
    timer_value = request.args.get('timer', '3')
    
    # Validate if the timer_value is numeric, otherwise default to 3
    if not timer_value.isdigit():
        timer_value = '3'
    
    return render_template('timerfix.html', timer=timer_value)


@app.route('/level5fix/welcome', methods=['GET'])
def level5fix_welcome():
    return render_template('level5fix_welcome.html')

@app.route('/level5fix/signup', methods=['GET'])
def level5fix_signup():
    next_page = request.args.get('next', 'confirm')

    # Validate the 'next' parameter to prevent XSS and JavaScript injection
    if not next_page.startswith("/") and not next_page.startswith("http"):
        next_page = "/level5fix/confirm"
    
    # Prevent 'javascript:' or 'data:' URLs from being used
    if next_page.lower().startswith("javascript:") or next_page.lower().startswith("data:"):
        next_page = "/level5fix/confirm"

    return render_template('level5fix_signup.html', next=next_page)


@app.route('/level5fix/confirm', methods=['GET'])
def level5fix_confirm():
    next_page = request.args.get('next', '/')

    # Validate and sanitize the 'next' parameter
    if not next_page.startswith("/") and not next_page.startswith("http"):
        next_page = "/"
    
    if next_page.startswith("javascript:") or next_page.startswith("data:"):
        next_page = "/"

    return render_template('level5fix_confirm.html', next=next_page)


@app.route('/level6fix', methods=['GET', 'POST'])
def level6fix():
    return render_template('level6fix.html')


# CSP 2.0

@app.route('/level1fix_csp2', methods=['GET', 'POST'])
def level1fix_csp2():
    response = make_response(render_template('level1fix_csp2.html'))
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    )
    return response

@app.route('/level2fix_csp2', methods=['GET', 'POST'])
def level2fix_csp2():
    response = make_response(render_template('level2fix_csp2.html'))
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    )
    return response

@app.route('/level3fix_csp2')
def level3fix_csp2():
    response = make_response(render_template('level3fix_csp2.html'))
    response.headers['Content-Security-Policy'] = (
    "default-src 'self'; script-src 'self' https://ajax.googleapis.com; object-src 'none'; base-uri 'self'; form-action 'self';"
)
    return response


@app.route('/level4fix_csp2', methods=['GET', 'POST'])
def level4fix_csp2():
    response = make_response(render_template('level4fix_csp2.html'))
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    )
    return response


@app.route('/timerfix_csp2', methods=['GET'])
def timerfix_csp2():
    timer_value = request.args.get('timer', '3')
    response = make_response(render_template('timerfix_csp2.html', timer=timer_value))
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none';"
    )
    return response


@app.route('/level5fix_welcome_csp2', methods=['GET', 'POST'])
def level5fix_welcome_csp2():
    response = make_response(render_template('level5fix_welcome_csp2.html'))
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    )
    return response

@app.route('/level5fix_signup_csp2', methods=['GET', 'POST'])
def level5fix_signup_csp2():
    response = make_response(render_template('level5fix_signup_csp2.html'))
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    )
    return response


@app.route('/level5fix_confirm_csp2', methods=['GET', 'POST'])
def level5fix_confirm_csp2():
    response = make_response(render_template('level5fix_confirm_csp2.html'))
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    )
    return response


@app.route('/level6fix_csp2', methods=['GET', 'POST'])
def level6fix_csp2():
    response = make_response(render_template('level6fix_csp2.html'))
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    )
    return response

# CSP 3.0

import os
import base64

def generate_nonce():
    return base64.b64encode(os.urandom(16)).decode('utf-8')


@app.route('/level1fix_csp3', methods=['GET', 'POST'])
def level1fix_csp3():
    # Random nonce
    nonce = generate_nonce()

    # Render the HTML with the nonce
    response = make_response(render_template('level1fix_csp3.html', nonce=nonce))

    # CSP 3.0 header with nonce
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}'; "
        f"style-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    )

    return response

@app.route('/level2fix_csp3', methods=['GET', 'POST'])
def level2fix_csp3():
    nonce = generate_nonce()
    response = make_response(render_template('level2fix_csp3.html', nonce=nonce))
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; style-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    )

    return response

@app.route('/level3fix_csp3', methods=['GET', 'POST'])
def level3fix_csp3():
    nonce = generate_nonce()
    response = make_response(render_template('level3fix_csp3.html', nonce=nonce))
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; script-src 'self' 'nonce-{nonce}' https://ajax.googleapis.com; style-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self';"
    )
    return response

@app.route('/level4fix_csp3', methods=['GET'])
def level4fix_csp3():
    nonce = generate_nonce()
    response = make_response(render_template('level4fix_csp3.html', nonce=nonce))
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; object-src 'none';"
    )
    return response

@app.route('/timerfix_csp3', methods=['GET'])
def timerfix_csp3():
    timer_value = request.args.get('timer', '3')
    nonce = generate_nonce()
    response = make_response(render_template('timerfix_csp3.html', timer=timer_value, nonce=nonce))
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; object-src 'none';"
    )
    return response

@app.route('/level5fix_welcome_csp3', methods=['GET'])
def level5fix_welcome_csp3():
    nonce = generate_nonce()
    response = make_response(render_template('level5fix_welcome_csp3.html', nonce=nonce))
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; object-src 'none';"
    )
    return response

@app.route('/level5fix_signup_csp3', methods=['GET'])
def level5fix_signup_csp3():
    nonce = generate_nonce()
    response = make_response(render_template('level5fix_signup_csp3.html', nonce=nonce))
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; object-src 'none';"
    )
    return response

@app.route('/level5fix_confirm_csp3', methods=['GET'])
def level5fix_confirm_csp3():
    nonce = generate_nonce()
    response = make_response(render_template('level5fix_confirm_csp3.html', nonce=nonce))
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; object-src 'none';"
    )
    return response


@app.route('/level6fix_csp3', methods=['GET', 'POST'])
def level6fix_csp3():
    nonce = generate_nonce()
    response = make_response(render_template('level6fix_csp3.html', nonce=nonce))
    response.headers['Content-Security-Policy'] = (
        f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; object-src 'none';"
    )
    return response

if __name__ == '__main__':
    app.run(debug=True)
