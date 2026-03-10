import ccxt


class BybitClient:

    def __init__(self):
        import ccxt
        self.exchange = ccxt.bybit({
            "enableRateLimit": True,
            "options": {"defaultType": "linear"}
        })
        self.exchange.load_markets()

    def fetch_ohlcv(self, symbol, timeframe="1h", limit=500):
        return self.exchange.fetch_ohlcv(symbol, timeframe, limit)

    def get_top_symbols(self, limit=20, min_volume=1000):
        tickers = self.exchange.fetch_tickers()
        symbols = [
            s for s, d in tickers.items()
            if "USDT" in s and "/" in s and float(d.get("quoteVolume",0)) >= min_volume
        ]
        symbols.sort(key=lambda s: float(tickers[s]["quoteVolume"]), reverse=True)
        return symbols[:limit]