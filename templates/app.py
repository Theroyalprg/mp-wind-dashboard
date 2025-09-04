from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Simple wind data for MP districts
MP_DISTRICTS = {
    'Ratlam': {'avg_wind_speed': 6.2, 'potential': 'High', 'grid_distance': 12},
    'Mandasaur': {'avg_wind_speed': 5.8, 'potential': 'Medium-High', 'grid_distance': 8},
    'Dewas': {'avg_wind_speed': 5.5, 'potential': 'Medium', 'grid_distance': 15},
    'Ujjain': {'avg_wind_speed': 5.2, 'potential': 'Medium', 'grid_distance': 6},
    'Indore': {'avg_wind_speed': 4.8, 'potential': 'Medium-Low', 'grid_distance': 3},
    'Bhopal': {'avg_wind_speed': 4.5, 'potential': 'Low-Medium', 'grid_distance': 5}
}

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>MP Wind Energy Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-blue-50">
    <div class="container mx-auto p-8">
        <h1 class="text-4xl font-bold text-center text-blue-800 mb-8">
            Madhya Pradesh Wind Energy Dashboard
        </h1>
        <div class="bg-white rounded-lg p-6 shadow-lg">
            <h2 class="text-2xl font-bold mb-4">Select District for Analysis:</h2>
            <div class="grid grid-cols-2 gap-4">
                <div class="p-4 border rounded hover:bg-blue-100 cursor-pointer" onclick="analyze('Ratlam')">
                    <h3 class="font-bold">Ratlam</h3>
                    <p>Wind Speed: 6.2 m/s</p>
                    <p>Potential: High</p>
                </div>
                <div class="p-4 border rounded hover:bg-blue-100 cursor-pointer" onclick="analyze('Mandasaur')">
                    <h3 class="font-bold">Mandasaur</h3>
                    <p>Wind Speed: 5.8 m/s</p>
                    <p>Potential: Medium-High</p>
                </div>
                <div class="p-4 border rounded hover:bg-blue-100 cursor-pointer" onclick="analyze('Dewas')">
                    <h3 class="font-bold">Dewas</h3>
                    <p>Wind Speed: 5.5 m/s</p>
                    <p>Potential: Medium</p>
                </div>
                <div class="p-4 border rounded hover:bg-blue-100 cursor-pointer" onclick="analyze('Ujjain')">
                    <h3 class="font-bold">Ujjain</h3>
                    <p>Wind Speed: 5.2 m/s</p>
                    <p>Potential: Medium</p>
                </div>
            </div>
            <div id="results" class="mt-8 hidden">
                <h2 class="text-2xl font-bold mb-4">Analysis Results:</h2>
                <div class="bg-green-100 p-6 rounded-lg">
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <h3 class="font-bold">Wind Assessment</h3>
                            <p id="windSpeed">Wind Speed: --</p>
                            <p id="potential">Potential: --</p>
                            <p id="capacity">Capacity Factor: --</p>
                        </div>
                        <div>
                            <h3 class="font-bold">Financial Analysis</h3>
                            <p id="cost">Project Cost: --</p>
                            <p id="roi">ROI: --</p>
                            <p id="payback">Payback: --</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-8 bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-xl font-bold mb-4">Data Sources</h2>
            <p>✅ NIWE (National Institute of Wind Energy)</p>
            <p>✅ MPREDA (MP Renewable Energy Development Agency)</p>
            <p>✅ IMD (India Meteorological Department)</p>
        </div>
    </div>
    
    <script>
        function analyze(district) {
            const data = {
                'Ratlam': {windSpeed: '6.2 m/s', potential: 'High', capacity: '28%', cost: '₹25L', roi: '18%', payback: '7 years'},
                'Mandasaur': {windSpeed: '5.8 m/s', potential: 'Medium-High', capacity: '25%', cost: '₹22L', roi: '15%', payback: '8 years'},
                'Dewas': {windSpeed: '5.5 m/s', potential: 'Medium', capacity: '23%', cost: '₹27L', roi: '12%', payback: '9 years'},
                'Ujjain': {windSpeed: '5.2 m/s', potential: 'Medium', capacity: '21%', cost: '₹20L', roi: '14%', payback: '8.5 years'}
            };
            
            if(data[district]) {
                document.getElementById('windSpeed').textContent = 'Wind Speed: ' + data[district].windSpeed;
                document.getElementById('potential').textContent = 'Potential: ' + data[district].potential;
                document.getElementById('capacity').textContent = 'Capacity Factor: ' + data[district].capacity;
                document.getElementById('cost').textContent = 'Project Cost: ' + data[district].cost;
                document.getElementById('roi').textContent = 'ROI: ' + data[district].roi;
                document.getElementById('payback').textContent = 'Payback Period: ' + data[district].payback;
                document.getElementById('results').classList.remove('hidden');
            }
        }
    </script>
</body>
</html>
    '''

@app.route('/api/districts')
def get_districts():
    return jsonify(MP_DISTRICTS)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
