# Import libraries
from flask import Flask, jsonify  
import requests                   
import time                       
import logging                    
import os                         

# Create Flask app instance
app = Flask(__name__)             

# Setup logging to a file
if not os.path.exists('logs'):    
    os.makedirs('logs')           
logging.basicConfig(              
    filename='logs/latency.log',  
    level=logging.INFO,           
    format='%(asctime)s - %(message)s'  
)

# Mock telecom API (fallback if external fails)
@app.route('/mock-call', methods=['GET'])  
def mock_call():
    time.sleep(0.2)               # Simulate a 200ms network delay
    return {"status": "call_routed", "destination": "Madrid"}  

# Main endpoint to simulate a call with an API
@app.route('/call', methods=['GET'])  
def simulate_call():
    start_time = time.time()         
    try:
        response = requests.get("https://restcountries.com/v3.1/name/spain", timeout=5)
        response.raise_for_status()   
    except requests.RequestException as e:  
        response = mock_call()        
        logging.warning(f"External API failed: {e}, using mock")  

    latency = (time.time() - start_time) * 1000  
    logging.info(f"API call latency: {latency:.2f} ms")  
    return jsonify({                  # Return JSON response
        "message": "Call processed",
        "latency_ms": latency,
        "api_data": response.json() if isinstance(response, requests.Response) else response
    })                                

# Stats endpoint to summarize latency
@app.route('/stats', methods=['GET'])  
def get_stats():
    with open('logs/latency.log', 'r') as f:  
        lines = f.readlines()         
    # Extract latencies from last 10 logs (filter for safety)
    latencies = [float(line.split('latency: ')[1].split(' ms')[0]) 
                 for line in lines[-10:] if 'latency' in line]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0  
    return jsonify({                 
        "avg_latency_ms": avg_latency,
        "recent_calls": len(latencies)
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  