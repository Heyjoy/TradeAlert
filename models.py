from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# 创建数据库引擎
engine = create_engine('sqlite:///tradealert.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class StockMonitor(Base):
    """股票监控配置"""
    __tablename__ = 'stock_monitors'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True, nullable=False)  # 股票代码
    upper_price = Column(Float, nullable=True)  # 上限价格
    lower_price = Column(Float, nullable=True)  # 下限价格
    is_active = Column(Boolean, default=True)  # 是否激活
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<StockMonitor(symbol='{self.symbol}', upper={self.upper_price}, lower={self.lower_price})>"

class AlertRecord(Base):
    """告警记录"""
    __tablename__ = 'alert_records'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)  # 股票代码
    price = Column(Float, nullable=False)  # 触发价格
    alert_type = Column(String(20), nullable=False)  # 告警类型（upper/lower）
    message = Column(String(200), nullable=False)  # 告警消息
    is_notified = Column(Boolean, default=False)  # 是否已通知
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<AlertRecord(symbol='{self.symbol}', price={self.price}, type='{self.alert_type}')>"

def init_db():
    """初始化数据库"""
    Base.metadata.create_all(engine)

def get_session():
    """获取数据库会话"""
    return Session() 