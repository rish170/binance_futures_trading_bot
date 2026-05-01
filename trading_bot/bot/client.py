from binance.client import Client
from binance.enums import FuturesType
from binance.exceptions import BinanceAPIException
from .config import API_KEY, API_SECRET, BASE_URL
from .logger import logger

class BinanceFuturesClient:
    def __init__(self):
        try:
            self.client = Client(API_KEY, API_SECRET, testnet=True)
            self.client.FUTURES_URL = BASE_URL
            logger.info(f"Initialized Client | target=Binance_Futures_Testnet url={BASE_URL}")
        except Exception as e:
            logger.error(f"Error initializing client | type={type(e).__name__} message={str(e)}")
            raise

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
        try:
            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }
            if order_type == "LIMIT":
                params["timeInForce"] = "GTC"
                params["price"] = price

            logger.info(f"API Request: Placing order | symbol={symbol} side={side} type={order_type} quantity={quantity} price={price}")
            
            response = self.client.futures_create_order(**params)
            return response
        except BinanceAPIException as e:
            logger.error(f"API Error | type=BinanceAPIException status_code={e.status_code} message={e.message}")
            raise
        except Exception as e:
            logger.error(f"Network/Unexpected Error | type={type(e).__name__} message={str(e)}")
            raise
