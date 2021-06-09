import nicehash
import time


# Just enter your keys instead of *****
host = 'https://api2.nicehash.com'
organisation_id = '*****'
key = '*****'
secret = '******'

private_api = nicehash.private_api(host, organisation_id, key, secret)
public_api = nicehash.public_api(host)


def available_currency(currency):
    return float(private_api.get_accounts_for_currency(currency).get('available'))


def my_orders(market='BTCUSDT', status='all'):
    return private_api.get_my_exchange_orders2(market, status)


def current_btcusdt_price():
    return float(public_api.get_current_price().get('BTCUSDT'))


def make_new_sell_order(multiply, btcusdt=current_btcusdt_price()):
    price = multiply*btcusdt
    quantity = available_currency('BTC')
    print(
        f'Creating SELL order\nPrice: {price} USDT\nQuantity: {quantity} BTC')
    private_api.post_order('BTCUSDT', 'SELL', 'LIMIT', price, quantity)
    print('Thank you! Your order have been created!')
    print(
        f'You have created SELL order with price {price} USDT and SELLING {quantity} BTC')
    print('Waiting for order to complete!')


def make_new_buy_order(multiply, btcusdt=current_btcusdt_price()):
    price = multiply*btcusdt
    quantity = available_currency('USDT')/price
    print(f'Creating BUY order\nPrice: {price} USDT\nQuantity: {quantity} BTC')
    private_api.post_order('BTCUSDT', 'BUY', 'LIMIT', price, quantity)
    print('Thank you! Your order have been created!')
    print(
        f'You have created BUY order with price {price} USDT and BUYING {quantity} BTC')
    print('Waiting for order to complete!')


def run_bot():
    while True:

        if not list(my_orders('BTCUSDT', 'open')):
            if available_currency('BTC') >= 0.0001:
                if (current_btcusdt_price()) > minimal_BTC_sell_price:
                    make_new_sell_order(1.005)
                    time.sleep(2)
                elif current_btcusdt_price() <= minimal_BTC_sell_price:
                    make_new_sell_order(1, minimal_BTC_sell_price)
                    time.sleep(2)
            elif available_currency('BTC') < 0.0001:
                if current_btcusdt_price() > maximum_BTC_buy_price:
                    make_new_buy_order(0.995)
                    time.sleep(2)
                elif current_btcusdt_price() <= maximum_BTC_buy_price:
                    make_new_buy_order(1, maximum_BTC_buy_price)
                    time.sleep(2)
        else:
            time.sleep(1)


if __name__ == "__main__":
    minimal_BTC_sell_price = float(
        input('Please enter minimal BTC sell price(in USDT): '))
    maximum_BTC_buy_price = float(
        input('Please enter maximum BTC buy price(in USDT): '))
    print(
        f'BTC  MINIMAL SELLING PRICE IS SET TO : {minimal_BTC_sell_price} USDT')
    print(
        f'BTC  MAXIMAL BUYING PRICE IS SET TO : {maximum_BTC_buy_price} USDT')
    run_bot()
