import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
from typing import Optional, Dict, Tuple

class StockDataFetcher:
    """股票数据获取器"""
    
    @staticmethod
    def get_current_price(symbol: str) -> Optional[float]:
        """
        获取股票当前价格
        
        Args:
            symbol: 股票代码
            
        Returns:
            当前价格，如果获取失败返回 None
        """
        try:
            stock = yf.Ticker(symbol)
            # 获取最近的数据
            hist = stock.history(period='1d')
            if not hist.empty:
                return hist['Close'].iloc[-1]
            return None
        except Exception as e:
            print(f"获取股票 {symbol} 价格失败: {str(e)}")
            return None

    @staticmethod
    def get_price_change(symbol: str, days: int = 1) -> Optional[Tuple[float, float]]:
        """
        获取股票价格变动
        
        Args:
            symbol: 股票代码
            days: 天数
            
        Returns:
            (价格变动百分比, 当前价格)，如果获取失败返回 None
        """
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period=f'{days+1}d')
            if len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                previous_price = hist['Close'].iloc[-2]
                change_pct = (current_price - previous_price) / previous_price
                return change_pct, current_price
            return None
        except Exception as e:
            print(f"获取股票 {symbol} 价格变动失败: {str(e)}")
            return None

    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """
        验证股票代码是否有效
        
        Args:
            symbol: 股票代码
            
        Returns:
            是否有效
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            return 'regularMarketPrice' in info
        except:
            return False

    @staticmethod
    def get_stock_info(symbol: str) -> Optional[Dict]:
        """
        获取股票基本信息
        
        Args:
            symbol: 股票代码
            
        Returns:
            股票信息字典，如果获取失败返回 None
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            return {
                'name': info.get('longName', symbol),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'Unknown'),
                'current_price': info.get('regularMarketPrice'),
                'previous_close': info.get('regularMarketPreviousClose'),
                'market_cap': info.get('marketCap'),
                'volume': info.get('regularMarketVolume')
            }
        except Exception as e:
            print(f"获取股票 {symbol} 信息失败: {str(e)}")
            return None 