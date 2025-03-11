from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Legal fee calculation rules based on Costa Rican law
# These values would be extracted from the law document
FEE_PERCENTAGES = {
    "up_to_250000": 0.20,  # 20% for amounts up to 250,000 colones
    "from_250000_to_10000000": 0.15,  # 15% for amounts from 250,000 to 10,000,000 colones
    "from_10000000_to_25000000": 0.10,  # 10% for amounts from 10,000,000 to 25,000,000 colones
    "from_25000000_to_75000000": 0.08,  # 8% for amounts from 25,000,000 to 75,000,000 colones
    "above_75000000": 0.05,  # 5% for amounts above 75,000,000 colones
}

# Minimum fees for different types of legal services
MINIMUM_FEES = {
    "consultation": 50000,  # Minimum fee for a consultation
    "written_consultation": 100000,  # Minimum fee for a written consultation
    "power_of_attorney": 75000,  # Minimum fee for a power of attorney
    "notarial_services": 60000,  # Minimum fee for notarial services
}

@app.route('/api/calculate-fee', methods=['POST'])
def calculate_fee():
    data = request.json
    service_type = data.get('service_type')
    amount = data.get('amount', 0)
    
    # For services with minimum fees
    if service_type in MINIMUM_FEES:
        return jsonify({
            'fee': MINIMUM_FEES[service_type],
            'service_type': service_type
        })
    
    # For percentage-based fees
    if service_type == 'percentage_based':
        fee = 0
        
        # Calculate fee based on tiered percentages
        if amount <= 250000:
            fee = amount * FEE_PERCENTAGES["up_to_250000"]
        elif amount <= 10000000:
            fee = 250000 * FEE_PERCENTAGES["up_to_250000"]
            fee += (amount - 250000) * FEE_PERCENTAGES["from_250000_to_10000000"]
        elif amount <= 25000000:
            fee = 250000 * FEE_PERCENTAGES["up_to_250000"]
            fee += (10000000 - 250000) * FEE_PERCENTAGES["from_250000_to_10000000"]
            fee += (amount - 10000000) * FEE_PERCENTAGES["from_10000000_to_25000000"]
        elif amount <= 75000000:
            fee = 250000 * FEE_PERCENTAGES["up_to_250000"]
            fee += (10000000 - 250000) * FEE_PERCENTAGES["from_250000_to_10000000"]
            fee += (25000000 - 10000000) * FEE_PERCENTAGES["from_10000000_to_25000000"]
            fee += (amount - 25000000) * FEE_PERCENTAGES["from_25000000_to_75000000"]
        else:
            fee = 250000 * FEE_PERCENTAGES["up_to_250000"]
            fee += (10000000 - 250000) * FEE_PERCENTAGES["from_250000_to_10000000"]
            fee += (25000000 - 10000000) * FEE_PERCENTAGES["from_10000000_to_25000000"]
            fee += (75000000 - 25000000) * FEE_PERCENTAGES["from_25000000_to_75000000"]
            fee += (amount - 75000000) * FEE_PERCENTAGES["above_75000000"]
        
        return jsonify({
            'fee': fee,
            'service_type': service_type,
            'amount': amount
        })
    
    return jsonify({
        'error': 'Invalid service type or parameters'
    }), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 