"""
IoT Environmental Control Web Server
Provides web-based control for RGB LEDs and real-time sensor monitoring
"""
import machine
import socket
from machine import Pin
from dht import DHT11, InvalidPulseCount
from time import sleep
from secrets import secrets
from do_connect import do_connect

# Hardware configuration constants
RED_LED_PIN = 13               # Red LED GPIO pin
GREEN_LED_PIN = 14             # Green LED GPIO pin  
BLUE_LED_PIN = 15              # Blue LED GPIO pin
DHT_SENSOR_PIN = 16            # DHT11 sensor data pin
WEB_SERVER_PORT = 80           # HTTP server port
MAX_CONNECTIONS = 1            # Maximum concurrent connections
REQUEST_BUFFER_SIZE = 1024     # HTTP request buffer size

# Sensor reading constants
SENSOR_RETRY_COUNT = 3         # Retry attempts for failed sensor readings
SENSOR_ERROR_VALUE = "Error"   # Display value for sensor errors

print("Initializing IoT Environmental Control System...")

# Initialize RGB LEDs
print("Setting up RGB LED pins...")
red_led = machine.Pin(RED_LED_PIN, machine.Pin.OUT)
green_led = machine.Pin(GREEN_LED_PIN, machine.Pin.OUT)
blue_led = machine.Pin(BLUE_LED_PIN, machine.Pin.OUT)

# Initialize DHT11 sensor
print(f"Initializing DHT11 sensor on pin {DHT_SENSOR_PIN}")
sensor_pin = Pin(DHT_SENSOR_PIN, Pin.IN)
dht_sensor = DHT11(sensor_pin)

def read_sensor_data():
    """
    Read temperature and humidity from DHT11 sensor with retry logic
    
    Returns:
        tuple: (temperature, humidity) or (None, None) if failed
    """
    for attempt in range(SENSOR_RETRY_COUNT):
        try:
            dht_sensor.measure()
            temperature = dht_sensor.temperature
            humidity = dht_sensor.humidity
            
            # Validate sensor readings
            if temperature is not None and humidity is not None:
                print(f"Sensor reading: {temperature}°C, {humidity}%")
                return temperature, humidity
            else:
                print(f"Invalid sensor reading on attempt {attempt + 1}")
                
        except (OSError, InvalidPulseCount) as e:
            print(f"Sensor read attempt {attempt + 1} failed: {e}")
            
        except Exception as e:
            print(f"Unexpected sensor error on attempt {attempt + 1}: {e}")
            
        # Small delay before retry
        if attempt < SENSOR_RETRY_COUNT - 1:
            sleep(0.1)
    
    print("All sensor read attempts failed")
    return None, None

def control_led(color):
    """
    Control RGB LED based on color selection
    
    Args:
        color: LED color ('red', 'green', 'blue', 'off')
    """
    # Turn off all LEDs first
    red_led.off()
    green_led.off()
    blue_led.off()
    
    # Turn on requested LED
    if color == 'red':
        red_led.on()
        print("LED: Red ON")
    elif color == 'green':
        green_led.on()
        print("LED: Green ON")
    elif color == 'blue':
        blue_led.on()
        print("LED: Blue ON")
    elif color == 'off':
        print("LED: All OFF")
    else:
        print(f"Unknown LED color: {color}")

def create_beautiful_webpage(temperature, humidity):
    """
    Generate a modern, responsive webpage with beautiful CSS styling
    
    Args:
        temperature: Current temperature reading
        humidity: Current humidity reading
        
    Returns:
        str: Complete HTML page with embedded CSS
    """
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IoT Environmental Control</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        
        .container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            width: 100%;
            text-align: center;
        }}
        
        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 2.2em;
            font-weight: 300;
        }}
        
        .subtitle {{
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }}
        
        .sensor-data {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .sensor-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .sensor-card.temperature {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}
        
        .sensor-card.humidity {{
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }}
        
        .sensor-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .sensor-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .control-section {{
            margin-bottom: 30px;
        }}
        
        .section-title {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.3em;
            font-weight: 500;
        }}
        
        .button-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .control-btn {{
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 1em;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: white;
        }}
        
        .btn-red {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        }}
        
        .btn-green {{
            background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        }}
        
        .btn-blue {{
            background: linear-gradient(135deg, #4dabf7 0%, #339af0 100%);
        }}
        
        .btn-off {{
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
            grid-column: 1 / -1;
        }}
        
        .control-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }}
        
        .control-btn:active {{
            transform: translateY(-1px);
        }}
        
        .footer {{
            margin-top: 30px;
            color: #888;
            font-size: 0.9em;
        }}
        
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #51cf66;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        @media (max-width: 480px) {{
            .container {{
                padding: 25px;
            }}
            
            .sensor-data {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 Smart Home</h1>
        <p class="subtitle">Environmental Control System</p>
        
        <div class="sensor-data">
            <div class="sensor-card temperature">
                <div class="sensor-value">{temperature}°</div>
                <div class="sensor-label">Temperature</div>
            </div>
            <div class="sensor-card humidity">
                <div class="sensor-value">{humidity}%</div>
                <div class="sensor-label">Humidity</div>
            </div>
        </div>
        
        <div class="control-section">
            <h3 class="section-title">💡 RGB LED Control</h3>
            <div class="button-grid">
                <form action="./red" method="get">
                    <button type="submit" class="control-btn btn-red">🔴 Red</button>
                </form>
                <form action="./green" method="get">
                    <button type="submit" class="control-btn btn-green">🟢 Green</button>
                </form>
                <form action="./blue" method="get">
                    <button type="submit" class="control-btn btn-blue">🔵 Blue</button>
                </form>
                <form action="./off" method="get">
                    <button type="submit" class="control-btn btn-off">⚫ Turn Off</button>
                </form>
            </div>
        </div>
        
        <div class="footer">
            <span class="status-indicator"></span>
            System Status: Online
        </div>
    </div>
</body>
</html>"""
    return html

def handle_web_request(connection):
    """
    Handle incoming HTTP requests and serve web pages
    
    Args:
        connection: Socket connection object
    """
    while True:
        client = None
        try:
            # Accept client connection
            client = connection.accept()[0]
            print("New client connected")
            
            # Receive HTTP request
            request_data = client.recv(REQUEST_BUFFER_SIZE)
            request_str = str(request_data)
            
            # Parse request path
            try:
                request_path = request_str.split()[1]
                print(f"Request: {request_path}")
            except (IndexError, ValueError):
                request_path = "/"
                print("Invalid request format, defaulting to root")
            
            # Process LED control commands
            if request_path == '/off' or request_path == '/off?':
                control_led('off')
            elif request_path == '/red' or request_path == '/red?':
                control_led('red')
            elif request_path == '/green' or request_path == '/green?':
                control_led('green')  
            elif request_path == '/blue' or request_path == '/blue?':
                control_led('blue')
            elif request_path == '/' or request_path == '/index.html':
                # Root path - just display the main page (no LED change)
                print("Serving main page")
            elif request_path == '/favicon.ico':
                # Ignore favicon requests
                print("Favicon request ignored")
            else:
                print(f"Unknown request path: {request_path}")
            
            # Read sensor data
            temperature, humidity = read_sensor_data()
            
            # Format sensor values for display
            if temperature is None or humidity is None:
                temp_display = SENSOR_ERROR_VALUE
                hum_display = SENSOR_ERROR_VALUE
                print("Using error values for sensor display")
            else:
                temp_display = f"{temperature:.1f}"
                hum_display = f"{humidity:.1f}"
            
            # Generate and send webpage
            html_content = create_beautiful_webpage(temp_display, hum_display)
            
            # Send HTTP response headers
            response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n"
            client.send(response_headers.encode('utf-8'))
            client.send(html_content.encode('utf-8'))
            
            print("Response sent successfully")
            
        except OSError as e:
            print(f"Network error handling request: {e}")
            
        except Exception as e:
            print(f"Unexpected error handling request: {e}")
            
        finally:
            # Always close client connection
            if client:
                try:
                    client.close()
                    print("Client connection closed")
                except:
                    pass

def create_web_server(ip_address):
    """
    Create and configure web server socket
    
    Args:
        ip_address: IP address to bind server to
        
    Returns:
        socket: Configured server socket
    """
    try:
        server_address = (ip_address, WEB_SERVER_PORT)
        server_socket = socket.socket()
        server_socket.bind(server_address)
        server_socket.listen(MAX_CONNECTIONS)
        
        print(f"Web server created successfully")
        print(f"Server Address: http://{ip_address}:{WEB_SERVER_PORT}")
        print(f"Max connections: {MAX_CONNECTIONS}")
        
        return server_socket
        
    except OSError as e:
        print(f"Failed to create web server: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error creating web server: {e}")
        raise

# Main program execution
print("Starting main program...")

try:
    # Connect to WiFi
    print("Connecting to WiFi network...")
    ip_address = do_connect()
    
    if ip_address is not None:
        print(f"WiFi connected successfully. IP: {ip_address}")
        
        # Create web server
        print("Creating web server...")
        server_connection = create_web_server(ip_address)
        
        # Start serving requests
        print("🌐 Web server is running!")
        print(f"📱 Open your browser and go to: http://{ip_address}")
        print("🔴🟢🔵 Control your RGB LEDs and monitor sensors")
        print("Press Ctrl+C to stop the server")
        
        handle_web_request(server_connection)
        
    else:
        print("ERROR: Failed to obtain IP address")
        
except KeyboardInterrupt:
    print("\\nWeb server stopped by user")
    print("Shutting down system...")
    
    # Turn off all LEDs before exit
    try:
        control_led('off')
    except:
        pass
        
    machine.reset()
    
except Exception as e:
    print(f"Critical error: {e}")
    print("System will restart...")
    machine.reset()