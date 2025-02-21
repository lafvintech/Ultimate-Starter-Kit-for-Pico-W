from machine import Pin
import network
import time
from secrets import *
from do_connect import *
import usocket as socket

# Initialize network connection
do_connect()

# Define relay pin configuration
RELAY_PIN = 15
relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(0)  # Set initial state to OFF (0)

# HTML template for web interface
# Contains CSS for switch styling and JavaScript for AJAX requests
HTML_TEMPLATE = """<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{{font-family:Arial; text-align: center; margin: 0px auto; padding-top:30px;}}
.switch{{position:relative;display:inline-block;width:120px;height:68px}}
.switch input{{display:none}}
.slider{{position:absolute;top:0;left:0;right:0;bottom:0;background-color:#ccc;border-radius:34px}}
.slider:before{{position:absolute;content:"";height:52px;width:52px;left:8px;bottom:8px;background-color:#fff;-webkit-transition:.4s;transition:.4s;border-radius:68px}}
input:checked+.slider{{background-color:#2196F3}}
input:checked+.slider:before{{-webkit-transform:translateX(52px);-ms-transform:translateX(52px);transform:translateX(52px)}}
</style>
<script>
function toggleCheckbox(element) {{
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/?relay=" + (element.checked ? "on" : "off"), true);
  xhr.send();
}}
</script>
</head>
<body>
<h1>Pico W IoT Relay Control</h1>
<label class="switch">
<input type="checkbox" onchange="toggleCheckbox(this)" {state}>
<span class="slider"></span>
</label>
</body>
</html>"""

def web_server():
    """
    Generate HTML response based on current relay state
    Returns: HTML content with current relay state
    """
    relay_state = 'checked' if relay.value() == 1 else ''
    return HTML_TEMPLATE.format(state=relay_state)

def handle_request(conn):
    """
    Handle incoming HTTP requests
    Args:
        conn: Socket connection object
    """
    # Receive and process HTTP request
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    
    # Process relay control commands
    if '/?relay=on' in request:
        print('RELAY ON')
        relay.value(1)
    elif '/?relay=off' in request:
        print('RELAY OFF')
        relay.value(0)

    # Send HTTP response
    response = web_server()
    conn.send(b'HTTP/1.1 200 OK\n')
    conn.send(b'Content-Type: text/html\n')
    conn.send(b'Connection: close\n\n')
    conn.sendall(response.encode('utf-8'))
    conn.close()

# Initialize socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))  # Bind to port 80
s.listen(5)       # Listen for up to 5 connections

print('Server started, waiting for connections...')

# Main loop to handle incoming connections
while True:
    try:
        # Accept new connection
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        handle_request(conn)
    except OSError as e:
        print('Connection closed: %s' % e)
