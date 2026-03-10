import ccxt


class BybitClient:
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        import ccxt
        self.exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'},
            'test': testnet
        })

    def fetch_ohlcv(self, symbol, timeframe="15m", limit=200):
        return self.exchange.fetch_ohlcv(symbol, timeframe, limit)

    def get_top_symbols(self, limit=20, min_volume=500000):
        """Возвращает топ-ликвидных USDT-фьючерсных пар по объёму за 24 часа"""
        symbols = []
        try:
            tickers = self.exchange.fetch_tickers()
        except Exception as e:
            print(f"Error fetching tickers: {e}")
            return symbols

        for symbol, data in tickers.items():
            if "USDT" in symbol and "PERP" in symbol:  # фильтруем perpetual
                try:
                    quote_volume = float(data.get("quoteVolume", 0))
                    if quote_volume >= min_volume:
                        symbols.append(symbol)
                except:
                    continue

        # сортируем по объёму по убыванию
        symbols = sorted(symbols, key=lambda s: float(tickers[s].get("quoteVolume", 0)), reverse=True)

        return symbols[:limit]