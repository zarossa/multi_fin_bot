def convert(amount, user_currency: int, amount_currency: int) -> float:
    exchange_rates = {
        1: 1,
        2: 76,
        3: 440,
    }
    rate = exchange_rates.get(user_currency) / exchange_rates.get(amount_currency)
    return float(amount) * rate
