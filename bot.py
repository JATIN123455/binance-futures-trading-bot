from binance import Client
from binance.enums import *
import argparse
from logger import logger
from config import TESTNET_BASE_URL

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = TESTNET_BASE_URL
        logger.info("Initialized Binance Futures Testnet Client")

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logger.info(f"Market Order Response: {order}")
            return order
        except Exception as e:
            logger.error(f"Market Order Error: {e}")
            raise

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                quantity=quantity,
                price=price,
                timeInForce=TIME_IN_FORCE_GTC
            )
            logger.info(f"Limit Order Response: {order}")
            return order
        except Exception as e:
            logger.error(f"Limit Order Error: {e}")
            raise

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_STOP,
                quantity=quantity,
                stopPrice=stop_price,
                price=limit_price,
                timeInForce=TIME_IN_FORCE_GTC
            )
            logger.info(f"Stop-Limit Order Response: {order}")
            return order
        except Exception as e:
            logger.error(f"Stop-Limit Order Error: {e}")
            raise


def validate_side(side):
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    return side.upper()


def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")

    parser.add_argument("--api_key", required=True)
    parser.add_argument("--api_secret", required=True)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True, choices=["market", "limit", "stop-limit"])
    parser.add_argument("--quantity", type=float, required=True)
    parser.add_argument("--price", type=float)
    parser.add_argument("--stop_price", type=float)

    args = parser.parse_args()
    side = validate_side(args.side)

    bot = BasicBot(args.api_key, args.api_secret)

    if args.type == "market":
        result = bot.place_market_order(args.symbol, side, args.quantity)

    elif args.type == "limit":
        if not args.price:
            raise ValueError("Limit order requires --price")
        result = bot.place_limit_order(args.symbol, side, args.quantity, args.price)

    elif args.type == "stop-limit":
        if not args.price or not args.stop_price:
            raise ValueError("Stop-limit requires --price and --stop_price")
        result = bot.place_stop_limit_order(
            args.symbol, side, args.quantity, args.stop_price, args.price
        )

    print("\nOrder Placed Successfully:")
    print(result)


if __name__ == "__main__":
    main()
