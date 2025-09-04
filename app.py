import os
import socket

def create_response():
    return '''HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head><title>MP Wind Energy Dashboard</title></head>
<body>
<h1>🌪️ MP Wind Energy Dashboard - LIVE!</h1>
<p>1M1B Salesforce Internship Project</p>
<div>
<h3>✅ Ratlam: 6.2 m/s wind, 18% ROI</h3>
<h3>⚡ Mandasaur: 5.8 m/s wind, 15% ROI</h3>
<h3>🔋 Dewas: 5.5 m/s wind, 12% ROI</h3>
</div>
</body>
</html>'''

port = int(os.environ.get('PORT', 8000))
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', port))
server_socket.listen(5)

print(f"Server running on port {port}")

while True:
    client_socket, addr = server_socket.accept()
    client_socket.send(create_response().encode())
    client_socket.close()
