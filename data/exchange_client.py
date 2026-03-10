import ccxt


class BybitClient:

    def __init__(self):

        # Публичное подключение без API
        self.exchange = ccxt.bybit({
            "enableRateLimit": True,
            "options": {
                "defaultType": "linear"
            }
        })

    def get_top_symbols(self, limit=20):

        try:

            tickers = self.exchange.fetch_tickers()

            symbols = []

            for symbol in tickers:

                if "/USDT" in symbol and ":" not in symbol:
                    volume = tickers[symbol]["quoteVolume"]

                    if volume:
                        symbols.append((symbol, volume))

            symbols.sort(key=lambda x: x[1], reverse=True)

            top_symbols = [s[0] for s in symbols[:limit]]

            return top_symbols

        except Exception as e:
            print("Error fetching tickers:", e)
            return []

    def fetch_ohlcv(self, symbol, timeframe="15m", limit=200):

        return self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)