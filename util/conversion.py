"""Bitcoin, ethereum, stellar units handling. Conversions to and from fiat currencies."""
import util.logger

# number of decimals after decimal point in currencies
ETH_DECIMALS = 18
BTC_DECIMALS = 8
STELLAR_DECIMALS = 7
DECIMAL_POINT = '.'

LOGGER = util.logger.logging.getLogger('pkt.util.currency_conversions')


def divisible_to_indivisible(amount, decimals):
    """
    Convert amount of some currency from divisible units to indivisible.
    :param str or int amount: Amount of units to be converted
    :param int decimals: Number of decimals in convertible currency
    :return int: Amount of indivisible units
    """
    if not isinstance(amount, str) and not (isinstance(amount, int) and not isinstance(amount, bool)):
        raise TypeError('Only string and integer allowed for conversions')

    amount = str(amount)
    if DECIMAL_POINT in amount:
        integer_part, fractional_part = amount.split(DECIMAL_POINT)
        fractional_part = fractional_part[:decimals]
    else:
        integer_part, fractional_part = amount, '0' * decimals

    if integer_part != '0':
        amount = "{0}{1:<0{decimals}}".format(integer_part, fractional_part, decimals=decimals)
    else:
        striped = fractional_part.lstrip('0')
        leading_zeros_amount = len(fractional_part) - len(striped)
        trailing_zeros_amount = decimals - leading_zeros_amount - len(striped)
        amount = "{0}{1}".format(striped, '0' * trailing_zeros_amount)

    amount = amount or '0'
    return int(amount)


def indivisible_to_divisible(amount, decimals):
    """
    Convert amount of some currency from indivisible units to divisible
    :param str or int amount: Amount of units to be converted
    :param int decimals: Number of decimals in convertible currency
    :return str: Amount of divisible units
    """
    if not isinstance(amount, str) and not (isinstance(amount, int) and not isinstance(amount, bool)):
        raise TypeError('Only string and integer allowed for conversions')

    amount = str(amount)
    amount = "{}.{}".format(amount[:-decimals], amount[-decimals:]) if len(amount) > decimals else \
        "0.{amount:0>{decimals}}".format(amount=amount, decimals=decimals)
    integer_part, fractional_part = amount.split('.')
    striped = fractional_part.rstrip('0')
    amount = "{}.{}".format(integer_part, striped or '0')

    return amount


def stroops_to_units(amount):
    """
    Convert amount presented in stroops to units.
    :param str or int amount: Amount of stroops to be converted
    :return str: Amount of stellar units
    """
    return indivisible_to_divisible(amount, STELLAR_DECIMALS)


def units_to_stroops(amount):
    """
    Convert stellar units to stroops.
    :param str or int amount: Amount of units to be converted
    :return int: Amount of stroops
    """
    return divisible_to_indivisible(amount, STELLAR_DECIMALS)


def wei_to_eth(amount):
    """
    Convert wei to ethereum
    :param str or int amount: Amount of wei to be converted
    :return str: Amount of ethereum
    """
    return indivisible_to_divisible(amount, ETH_DECIMALS)


def eth_to_wei(amount):
    """
    Convert ethereum to wei
    :param str or int amount: Amount of ethereum to be converted
    :return int: Amount of wei
    """
    return divisible_to_indivisible(amount, ETH_DECIMALS)


def satoshi_to_btc(amount):
    """
    Convert satoshi to bitcoin
    :param str or int amount: Amount of bitcoin to be converted
    :return str: Amount of bitcoin
    """
    return indivisible_to_divisible(amount, BTC_DECIMALS)


def btc_to_satoshi(amount):
    """
    Convert bitcoin to satoshi
    :param amount: Amount of bitcoin to be converted
    :return int: Amount of satoshi
    """
    return divisible_to_indivisible(amount, BTC_DECIMALS)


def currency_to_euro_cents(amount, eur_price, decimals):
    """
    Convert amount of coins of some currency to euro cents.
    Price should be in EUR by one divisible unit of crypto currency.
    :param amount: amount of indivisible units of some currency
    :param eur_price: price in EUR by one divisible unit of some currency
    :param decimals: number of decimals in one divisible unit of some currency
    :return: amount of EUR cents
    """
    price_decimals = len(eur_price.split('.')[1])
    # price in fictitious units (portions of euro cents) by one indivisible unit of specified crypto currency
    fictitious_units_price = divisible_to_indivisible(eur_price, price_decimals)
    fictitious_units_amount = fictitious_units_price * amount
    # minus two because initial price was in EUR and we want euro cents
    euro_cents = indivisible_to_divisible(fictitious_units_amount, price_decimals + decimals - 2)
    LOGGER.warning("precision loss: %s converted to %s", euro_cents, round(float(euro_cents)))
    # integer part of result will be amount of euro cents
    return round(float(euro_cents))


def btc_to_euro_cents(amount, eur_price):
    """
    Convert amount of BTC satoshi to euro cents.
    Price should be in EUR by one BTC. Amount should be in satoshi.
    :param amount: Amount of satoshi
    :param eur_price: EUR price of one BTC
    :return: amount of EUR cents
    """
    return currency_to_euro_cents(amount, eur_price, BTC_DECIMALS)


def eth_to_euro_cents(amount, eur_price):
    """
    Convert amount of ETH wei to euro cents.
    Price should be in EUR by one ETH. Amount should be in wei.
    :param amount: Amount of wei
    :param eur_price: EUR price of one ETH
    :return: amount of EUR cents
    """
    return currency_to_euro_cents(amount, eur_price, ETH_DECIMALS)


def xlm_to_euro_cents(amount, eur_price):
    """
    Convert amount of XLM stroop to euro cents.
    Price should be in EUR by one XLM. Amount should be in stroop.
    :param amount: Amount of stroop
    :param eur_price: EUR price of one XLM
    :return: amount of EUR cents
    """
    return currency_to_euro_cents(amount, eur_price, STELLAR_DECIMALS)


def bul_to_euro_cents(amount, eur_price):
    """
    Convert amount of BUL stroop to euro cents.
    Price should be in EUR by one BUL. Amount should be in stroop.
    :param amount: Amount of stroop
    :param eur_price: EUR price of one XLM
    :return: amount of EUR cents
    """
    return currency_to_euro_cents(amount, eur_price, STELLAR_DECIMALS)


def euro_cents_to_xlm_stroops(euro_cents_amount, xlm_price):
    """
    Convert amount of euro cents to XLM stroops.
    Price should be in EUR by one XLM.
    :param euro_cents_amount: amount of EUR cents
    :param xlm_price: EUR price of one XLM
    :return: amount of XLM stroops
    """
    try:
        price_decimals = len(xlm_price.split('.')[1])
    except IndexError:
        price_decimals = 0
    fictitious_units_amount = divisible_to_indivisible(euro_cents_amount, STELLAR_DECIMALS + price_decimals)
    fictitious_units_price = divisible_to_indivisible(xlm_price, price_decimals + 2)
    stroops = fictitious_units_amount // fictitious_units_price
    LOGGER.warning("possible precision loss: %s / %s = %s", fictitious_units_amount, fictitious_units_price, stroops)
    return stroops


def euro_cents_to_bul_stroops(euro_cents_amount, bul_price):
    """
    Convert amount of euro cents to BUL stroops.
    Price should be in EUR by one XLM.
    :param euro_cents_amount: amount of EUR cents
    :param bul_price: EUR price of one BUL
    :return:
    """
    try:
        price_decimals = len(bul_price.split('.')[1])
    except IndexError:
        price_decimals = 0
    fictitious_units_amount = divisible_to_indivisible(euro_cents_amount, STELLAR_DECIMALS + price_decimals)
    fictitious_units_price = divisible_to_indivisible(bul_price, price_decimals + 2)
    stroops = fictitious_units_amount // fictitious_units_price
    LOGGER.warning("possible precision loss: %s / %s = %s", fictitious_units_amount, fictitious_units_price, stroops)
    return stroops
