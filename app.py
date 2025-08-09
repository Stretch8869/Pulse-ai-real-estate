from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    return render_template('analyze.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    address = request.form['address']
    price = float(request.form['price'])
    bedrooms = int(request.form['bedrooms'])
    bathrooms = int(request.form['bathrooms'])
    sqft = float(request.form['sqft'])

    # More detailed, rule-based profitability analysis
    # Step 1: Estimate rental income (incorporating sqft)
    estimated_monthly_rent = (bedrooms * 500) + (max(0, bathrooms - 1) * 100) + (sqft * 0.1)
    annual_rent = estimated_monthly_rent * 12

    # Step 2: Estimate annual expenses
    property_taxes = price * 0.0125
    insurance = price * 0.005
    maintenance = price * 0.01
    vacancy = annual_rent * 0.05
    total_expenses = property_taxes + insurance + maintenance + vacancy

    # Step 3: Calculate Net Operating Income (NOI)
    noi = annual_rent - total_expenses

    # Step 4: Calculate Capitalization Rate (Cap Rate)
    cap_rate = (noi / price) * 100

    # Step 5: Determine profitability
    if cap_rate >= 5:
        profitability = "Potentially Profitable"
    else:
        profitability = "Less Likely to be Profitable"

    result_data = {
        "address": address,
        "profitability": profitability,
        "cap_rate": f"{cap_rate:.2f}%",
        "noi": f"${noi:,.2f}",
        "estimated_annual_rent": f"${annual_rent:,.2f}",
    }

    return render_template('result.html', result=result_data)

if __name__ == '__main__':
    app.run(debug=True)
