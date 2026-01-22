"""
Stock data services using yfinance.
"""

import yfinance as yf
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional
import logging

from .models import Stock, StockPriceHistory
from .config import TRACKED_STOCKS, STOCK_SYMBOLS

logger = logging.getLogger(__name__)


class StockService:
    """
    Service for fetching and managing stock data.
    """
    
    @staticmethod
    def initialize_stocks() -> List[Stock]:
        """
        Initialize stocks from config.
        Creates Stock records if they don't exist.
        """
        stocks = []
        for symbol, name, sector in TRACKED_STOCKS:
            stock, created = Stock.objects.get_or_create(
                symbol=symbol,
                defaults={'name': name, 'sector': sector}
            )
            if not created:
                stock.name = name
                stock.sector = sector
                stock.save()
            stocks.append(stock)
        return stocks
    
    @staticmethod
    def fetch_current_prices() -> Dict[str, dict]:
        """
        Fetch current prices for all tracked stocks.
        Returns dict with symbol as key and price data as value.
        """
        try:
            tickers = yf.Tickers(' '.join(STOCK_SYMBOLS))
            results = {}
            
            for symbol in STOCK_SYMBOLS:
                try:
                    ticker = tickers.tickers[symbol]
                    info = ticker.info
                    
                    results[symbol] = {
                        'current_price': Decimal(str(info.get('currentPrice', 0) or info.get('regularMarketPrice', 0) or 0)),
                        'previous_close': Decimal(str(info.get('previousClose', 0) or 0)),
                        'day_high': Decimal(str(info.get('dayHigh', 0) or 0)),
                        'day_low': Decimal(str(info.get('dayLow', 0) or 0)),
                        'volume': info.get('volume', 0) or 0,
                        'market_cap': info.get('marketCap', 0) or 0,
                    }
                except Exception as e:
                    logger.error(f"Error fetching {symbol}: {e}")
                    results[symbol] = None
            
            return results
        except Exception as e:
            logger.error(f"Error fetching stock data: {e}")
            return {}
    
    @staticmethod
    def update_stock_prices() -> int:
        """
        Update all stock prices in database.
        Returns count of successfully updated stocks.
        """
        prices = StockService.fetch_current_prices()
        updated = 0
        
        for symbol, data in prices.items():
            if data is None:
                continue
            
            try:
                stock = Stock.objects.get(symbol=symbol)
                stock.current_price = data['current_price']
                stock.previous_close = data['previous_close']
                stock.day_high = data['day_high']
                stock.day_low = data['day_low']
                stock.volume = data['volume']
                stock.market_cap = data['market_cap']
                stock.save()
                updated += 1
            except Stock.DoesNotExist:
                logger.warning(f"Stock {symbol} not found in database")
            except Exception as e:
                logger.error(f"Error updating {symbol}: {e}")
        
        return updated
    
    @staticmethod
    def fetch_price_history(symbol: str, period: str = '1mo') -> List[dict]:
        """
        Fetch historical price data for a stock.
        
        Args:
            symbol: Stock symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
        
        Returns:
            List of price history dictionaries
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            history = []
            for timestamp, row in hist.iterrows():
                history.append({
                    'timestamp': timestamp.isoformat(),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume']),
                })
            
            return history
        except Exception as e:
            logger.error(f"Error fetching history for {symbol}: {e}")
            return []
    
    @staticmethod
    def get_stock_quote(symbol: str) -> Optional[dict]:
        """
        Get real-time quote for a single stock.
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            current_price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
            previous_close = info.get('previousClose', 0) or 0
            
            return {
                'symbol': symbol,
                'name': info.get('shortName', ''),
                'current_price': float(current_price),
                'previous_close': float(previous_close),
                'day_high': float(info.get('dayHigh', 0) or 0),
                'day_low': float(info.get('dayLow', 0) or 0),
                'volume': info.get('volume', 0) or 0,
                'market_cap': info.get('marketCap', 0) or 0,
                'change': float(current_price - previous_close) if previous_close else 0,
                'change_percent': float(((current_price - previous_close) / previous_close) * 100) if previous_close else 0,
            }
        except Exception as e:
            logger.error(f"Error getting quote for {symbol}: {e}")
            return None
