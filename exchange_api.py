import requests

API_URL = "https://api.exchangerate.host/latest"

def get_rates(base="GBP"):
    response = requests.get(API_URL, params={"base": base})
    data = response.json()
    return data["rates"]

def convert_gbp(amount, currency="USD"):
    rates = get_rates("GBP")
    rate = rates.get(currency, 1)
    return amount * rate