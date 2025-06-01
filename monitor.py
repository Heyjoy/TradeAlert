import time
import schedule
from datetime import datetime
from typing import List, Optional
from models import StockMonitor, AlertRecord, get_session
from stock_data import StockDataFetcher
from notifier import EmailNotifier

class StockMonitorService:
    """股票监控服务"""
    
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.notifier = EmailNotifier()
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '300'))  # 默认5分钟
        self.price_change_threshold = float(os.getenv('PRICE_CHANGE_THRESHOLD', '0.02'))  # 默认2%

    def add_monitor(self, symbol: str, upper_price: Optional[float] = None, 
                   lower_price: Optional[float] = None) -> bool:
        """
        添加股票监控
        
        Args:
            symbol: 股票代码
            upper_price: 上限价格
            lower_price: 下限价格
            
        Returns:
            是否添加成功
        """
        # 验证股票代码
        if not self.data_fetcher.validate_symbol(symbol):
            print(f"无效的股票代码: {symbol}")
            return False

        session = get_session()
        try:
            # 检查是否已存在
            existing = session.query(StockMonitor).filter_by(symbol=symbol).first()
            if existing:
                existing.upper_price = upper_price
                existing.lower_price = lower_price
                existing.is_active = True
                existing.updated_at = datetime.now()
            else:
                monitor = StockMonitor(
                    symbol=symbol,
                    upper_price=upper_price,
                    lower_price=lower_price
                )
                session.add(monitor)
            
            session.commit()
            return True
        except Exception as e:
            print(f"添加股票监控失败: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    def remove_monitor(self, symbol: str) -> bool:
        """
        删除股票监控
        
        Args:
            symbol: 股票代码
            
        Returns:
            是否删除成功
        """
        session = get_session()
        try:
            monitor = session.query(StockMonitor).filter_by(symbol=symbol).first()
            if monitor:
                session.delete(monitor)
                session.commit()
                return True
            return False
        except Exception as e:
            print(f"删除股票监控失败: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    def list_monitors(self) -> List[dict]:
        """
        获取所有监控配置
        
        Returns:
            监控配置列表
        """
        session = get_session()
        try:
            monitors = session.query(StockMonitor).filter_by(is_active=True).all()
            return [{
                'symbol': m.symbol,
                'upper_price': m.upper_price,
                'lower_price': m.lower_price,
                'created_at': m.created_at,
                'updated_at': m.updated_at
            } for m in monitors]
        finally:
            session.close()

    def check_price(self, symbol: str) -> None:
        """
        检查单个股票价格
        
        Args:
            symbol: 股票代码
        """
        session = get_session()
        try:
            monitor = session.query(StockMonitor).filter_by(
                symbol=symbol, is_active=True).first()
            if not monitor:
                return

            current_price = self.data_fetcher.get_current_price(symbol)
            if current_price is None:
                return

            # 检查价格告警
            if monitor.upper_price and current_price >= monitor.upper_price:
                self._create_alert(session, symbol, current_price, 'upper',
                    f"价格 {current_price:.2f} 超过上限 {monitor.upper_price:.2f}")
            
            if monitor.lower_price and current_price <= monitor.lower_price:
                self._create_alert(session, symbol, current_price, 'lower',
                    f"价格 {current_price:.2f} 低于下限 {monitor.lower_price:.2f}")

            # 检查价格变动
            price_change = self.data_fetcher.get_price_change(symbol)
            if price_change:
                change_pct, _ = price_change
                if abs(change_pct) >= self.price_change_threshold:
                    self._create_alert(session, symbol, current_price, 'change',
                        f"价格变动 {change_pct:.2%} 超过阈值 {self.price_change_threshold:.2%}")

        except Exception as e:
            print(f"检查股票 {symbol} 价格失败: {str(e)}")
        finally:
            session.close()

    def _create_alert(self, session, symbol: str, price: float, 
                     alert_type: str, message: str) -> None:
        """
        创建告警记录并发送通知
        
        Args:
            session: 数据库会话
            symbol: 股票代码
            price: 当前价格
            alert_type: 告警类型
            message: 告警消息
        """
        try:
            # 创建告警记录
            alert = AlertRecord(
                symbol=symbol,
                price=price,
                alert_type=alert_type,
                message=message
            )
            session.add(alert)
            session.commit()

            # 发送通知
            if self.notifier.send_alert(symbol, price, alert_type, message):
                alert.is_notified = True
                session.commit()
        except Exception as e:
            print(f"创建告警记录失败: {str(e)}")
            session.rollback()

    def start_monitoring(self) -> None:
        """启动监控服务"""
        def check_all_prices():
            monitors = self.list_monitors()
            for monitor in monitors:
                self.check_price(monitor['symbol'])

        # 设置定时任务
        schedule.every(self.check_interval).seconds.do(check_all_prices)
        
        print(f"监控服务已启动，检查间隔: {self.check_interval} 秒")
        while True:
            schedule.run_pending()
            time.sleep(1) 