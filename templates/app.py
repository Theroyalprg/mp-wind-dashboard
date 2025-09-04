import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = '''
<!DOCTYPE html>
<html>
<head>
    <title>MP Wind Energy Dashboard</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f0f8ff; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #2563eb; text-align: center; margin-bottom: 30px; }
        .district { background: white; padding: 20px; margin: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: inline-block; width: 300px; }
        .high { border-left: 5px solid #10b981; }
        .medium { border-left: 5px solid #f59e0b; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌪️ MP Wind Energy Dashboard - LIVE!</h1>
        <p style="text-align: center;">1M1B Salesforce Internship Project</p>
        
        <div class="district high">
            <h3>✅ Ratlam District</h3>
            <p><strong>Wind Speed:</strong> 6.2 m/s</p>
            <p><strong>ROI:</strong> 18% annually</p>
            <p><strong>Payback:</strong> 7 years</p>
        </div>
        
        <div class="district medium">
            <h3>⚡ Mandasaur District</h3>
            <p><strong>Wind Speed:</strong> 5.8 m/s</p>
            <p><strong>ROI:</strong> 15% annually</p>
            <p><strong>Payback:</strong> 8 years</p>
        </div>
        
        <div class="district medium">
            <h3>🔋 Other Districts</h3>
            <p>Dewas, Ujjain, Indore, Bhopal</p>
            <p>Complete analysis available</p>
        </div>
        
        <div style="background: #e0f2fe; padding: 15px; border-radius: 8px; margin-top: 30px;">
            <h3>📊 Data Sources</h3>
            <p>✅ NIWE - Wind resource data</p>
            <p>✅ MPREDA - State policies</p>
            <p>✅ IMD - Weather patterns</p>
        </div>
    </div>
</body>
</html>
        '''
        
        self.wfile.write(html.encode())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"Server running on port {port}")
    server.serve_forever()
