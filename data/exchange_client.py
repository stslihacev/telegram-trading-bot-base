# data/exchange_client.py
import ccxt
import os
from dotenv import load_dotenv

load_dotenv()

class BybitClient:
    def __init__(self, testnet=True):
        api_key = os.getenv("BYBIT_API_KEY")
        api_secret = os.getenv("BYBIT_SECRET")
        self.exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future'
            }
        })
        if testnet:
            self.exchange.set_sandbox_mode(True)

    def fetch_ohlcv(self, symbol, timeframe, limit=200):
        """
        Возвращает OHLCV для пары.
        """
        try:
            return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        except Exception as e:
            print(f"Error fetching OHLCV for {symbol}: {e}")
            return []

    def fetch_tickers(self):
        """
        Возвращает все тикеры (для сканера).
        """
        try:
            return self.exchange.fetch_tickers()
        except Exception as e:
            print(f"Error fetching tickers: {e}")
            return {}