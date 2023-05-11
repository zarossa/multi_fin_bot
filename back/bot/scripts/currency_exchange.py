import decimal


def convert(amount, user_currency: int, amount_currency: int) -> decimal.Decimal:
    exchange_rates = {
        1: 1,
        2: 76,
        3: 440,
        4: 34,
    }
    rate = exchange_rates.get(user_currency) / exchange_rates.get(amount_currency)
    return decimal.Decimal(float(amount) * rate)
