from proj.celery import app
from .models import Currency
import requests


@app.task
def update_currency_rates():
    url = 'https://api.exchangerate.host/latest?base=USD'
    response = requests.get(url)
    data = response.json()
    rates = data.get('rates')

    currencies = Currency.objects.all()
    for currency in currencies:
        currency.rate = rates.get(currency.code)
        currency.save()
