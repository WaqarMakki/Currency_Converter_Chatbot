from flask import Flask,request,jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency'][0]['currency']
    amount = data['queryResult']['parameters']['unit-currency'][0]['amount']
    target_currency = data['queryResult']['parameters']['currency-name'][0]

    final_amount = fetch_conversion_factor(source_currency,target_currency, amount)
    # final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText': "{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)


def fetch_conversion_factor(source, target, amount):

    url = "https://api.apilayer.com/exchangerates_data/convert?to={}&from={}&amount={}".format(target, source, amount)
    payload = {}
    headers = {
        "apikey": "HyXC9KxnOwqUOOjfeWyc7OsQQxTI3Nkk"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['result']


if __name__ == "__main__":
    app.run(debug=True)
