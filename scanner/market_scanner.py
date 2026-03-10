import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.exchange_client import BybitClient
from strategy.bos_strategy_wrapper import BosStrategyRunner
from config.settings import TOP_PAIRS_LIMIT


class MarketScanner:

    def __init__(self):
        self.client = BybitClient()
        self.runner = BosStrategyRunner()

    def get_top_pairs(self):

        print("Получаем список тикеров...")

        tickers = self.client.fetch_tickers()

        volume_dict = {}

        for symbol, data in tickers.items():

            try:
                if "USDT" in symbol and data["quoteVolume"]:
                    volume_dict[symbol] = data["quoteVolume"]
            except:
                continue

        sorted_pairs = sorted(
            volume_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_pairs = [pair for pair, _ in sorted_pairs[:TOP_PAIRS_LIMIT]]

        print(f"Найдено {len(top_pairs)} топ пар")

        return top_pairs

    def scan_market(self):

        pairs = self.get_top_pairs()

        print("Начинаем сканирование рынка...\n")

        for symbol in pairs:

            print(f"Анализ {symbol}")

            try:

                signal = self.runner.run(symbol)

                if signal:

                    print(
                        f"СИГНАЛ: {symbol} {signal['side']} | "
                        f"Entry {signal['entry_price']:.2f} "
                        f"TP {signal['tp']:.2f} "
                        f"SL {signal['sl']:.2f}"
                    )

                else:
                    print("Сигнала нет")

            except Exception as e:

                print(f"Ошибка при анализе {symbol}: {e}")

            print("------")


if __name__ == "__main__":

    scanner = MarketScanner()

    scanner.scan_market()