import decimal


def convert(amount: decimal.Decimal,
            user_currency_rate: decimal.Decimal,
            amount_currency_rate: decimal.Decimal) -> decimal.Decimal:
    rate = user_currency_rate / amount_currency_rate
    return amount * rate
