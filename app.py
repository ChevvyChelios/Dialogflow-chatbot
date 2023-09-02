
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    # print(source_currency)
    # print(amount)
    # print(target_currency)
    
    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount, 2)
    
    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    
    # print(final_amount)
    return jsonify(response)

def fetch_conversion_factor(source, target):
    url = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_4jkFmkiJpTapPgjLMa1ZM1oo6wlYssP4UQKFmrup&currencies={}&base_currency={}".format(target,source)
    resp = requests.get(url)
    resp = resp.json()
    cf = resp['data'][target]
    # print(resp)
    # print(cf)
    return cf

if __name__ == '__main__':
    app.run(debug=True)