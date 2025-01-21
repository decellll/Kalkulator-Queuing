from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Tambahkan ini untuk menangani CORS

app = Flask(__name__)
CORS(app)  # Aktifkan CORS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])  # Izinkan kedua metode GET dan POST
def calculate():
    try:
        if request.method != 'POST':
            return jsonify({'error': 'Method not allowed'}), 405
            
        queue_type = request.form.get('queue_type')
        arrival_rate = float(request.form.get('arrival_rate'))
        service_rate = float(request.form.get('service_rate'))
        
        # Calculate traffic intensity
        rho = arrival_rate / service_rate
        
        if queue_type == 'M/M/1':
            # M/M/1 calculations
            if rho >= 1:
                return jsonify({'error': 'Sistem tidak stabil. Traffic intensity harus kurang dari 1'})
            
            L = rho / (1 - rho)  # Average number of customers in system
            Lq = (rho * rho) / (1 - rho)  # Average number in queue
            W = 1 / (service_rate - arrival_rate)  # Average time in system
            Wq = rho / (service_rate - arrival_rate)  # Average time in queue
            P0 = 1 - rho  # Probability of zero customers
            
        elif queue_type == 'M/M/S':
            servers = int(request.form.get('servers', 1))
            if rho >= servers:
                return jsonify({'error': 'Sistem tidak stabil. Traffic intensity harus kurang dari jumlah server'})
            
            # M/M/S calculations
            P0 = 1 - rho  # Simplified P0 calculation
            L = rho / (1 - rho)  # Simplified L calculation
            Lq = (rho * rho) / (1 - rho)  # Simplified Lq calculation
            W = 1 / (service_rate - arrival_rate)
            Wq = rho / (service_rate - arrival_rate)
            
        return jsonify({
            'traffic_intensity': round(rho, 3),
            'avg_customers': round(L, 3),
            'time_in_queue': round(W, 3),
            'customers_in_queue': round(Lq, 3),
            'p0': round(P0, 3),
            'pn': round((1 - P0), 3)  # Probability of n customers
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)