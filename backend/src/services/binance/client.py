class BinanceClient:
    def validate_symbol(self, symbol: str) -> bool:
        return symbol.isupper() and symbol.endswith("USDT") and 6 <= len(symbol) <= 12


binance_client = BinanceClient()
