from data.exchange_client import BybitClient
from data.market_data import MarketData
from strategy.bos_strategy_wrapper import BosStrategyRunner


class MarketScanner:

    def __init__(self):

        self.client = BybitClient()
        self.market_data = MarketData(self.client)
        self.strategy = BosStrategyRunner()

    def get_top_pairs(self):

        print("Получаем список тикеров...")

        pairs = self.client.get_top_symbols(limit=20)

        print(f"Найдено {len(pairs)} топ пар")

        return pairs

    def scan_market(self):

        pairs = self.get_top_pairs()

        print("Начинаем сканирование рынка...\n")

        for symbol in pairs:

            try:

                print(f"Сканируем {symbol}")

                df = self.market_data.get_dataframe(symbol)

                signal = self.strategy.run(symbol, df)

                if signal:

                    print("СИГНАЛ:")
                    print(signal)

                else:
                    print("Сигнала нет")

                print("------\n")

            except Exception as e:

                print(f"Ошибка при анализе {symbol}: {e}")


if __name__ == "__main__":

    scanner = MarketScanner()

    scanner.scan_market()