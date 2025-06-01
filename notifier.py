import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class EmailNotifier:
    """邮件通知器"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.notification_email = os.getenv('NOTIFICATION_EMAIL')
        
        if not all([self.smtp_server, self.smtp_port, self.smtp_username, 
                   self.smtp_password, self.notification_email]):
            raise ValueError("邮件配置不完整，请检查 .env 文件")

    def send_alert(self, symbol: str, price: float, alert_type: str, 
                  message: str) -> bool:
        """
        发送告警邮件
        
        Args:
            symbol: 股票代码
            price: 当前价格
            alert_type: 告警类型（upper/lower）
            message: 告警消息
            
        Returns:
            是否发送成功
        """
        try:
            # 创建邮件内容
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = self.notification_email
            msg['Subject'] = f"股票告警: {symbol} {alert_type.upper()}"

            # 构建邮件正文
            body = f"""
            股票告警通知
            
            股票代码: {symbol}
            当前价格: {price:.2f}
            告警类型: {alert_type}
            告警时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            详细信息:
            {message}
            
            此邮件由 TradeAlert 系统自动发送
            """
            
            msg.attach(MIMEText(body, 'plain'))

            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"发送告警邮件失败: {str(e)}")
            return False

    def send_test_email(self) -> bool:
        """
        发送测试邮件
        
        Returns:
            是否发送成功
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = self.notification_email
            msg['Subject'] = "TradeAlert 系统测试邮件"

            body = """
            这是一封测试邮件，用于验证 TradeAlert 系统的邮件通知功能是否正常。
            
            如果您收到这封邮件，说明邮件通知配置正确。
            
            此邮件由 TradeAlert 系统自动发送
            """
            
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"发送测试邮件失败: {str(e)}")
            return False 