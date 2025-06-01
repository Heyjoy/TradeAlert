import argparse
import os
from dotenv import load_dotenv
from models import init_db
from monitor import StockMonitorService
from notifier import EmailNotifier

def setup():
    """初始化设置"""
    # 加载环境变量
    load_dotenv()
    
    # 初始化数据库
    init_db()
    
    # 测试邮件配置
    try:
        notifier = EmailNotifier()
        if notifier.send_test_email():
            print("邮件配置测试成功")
        else:
            print("警告: 邮件配置测试失败")
    except Exception as e:
        print(f"警告: 邮件配置错误 - {str(e)}")

def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description='股票监控告警系统')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 启动监控服务
    parser_start = subparsers.add_parser('start', help='启动监控服务')
    
    # 添加股票监控
    parser_add = subparsers.add_parser('add', help='添加股票监控')
    parser_add.add_argument('--symbol', required=True, help='股票代码')
    parser_add.add_argument('--upper', type=float, help='上限价格')
    parser_add.add_argument('--lower', type=float, help='下限价格')
    
    # 删除股票监控
    parser_remove = subparsers.add_parser('remove', help='删除股票监控')
    parser_remove.add_argument('--symbol', required=True, help='股票代码')
    
    # 列出所有监控
    parser_list = subparsers.add_parser('list', help='列出所有监控')

    args = parser.parse_args()
    service = StockMonitorService()

    if args.command == 'start':
        print("正在启动监控服务...")
        service.start_monitoring()
    elif args.command == 'add':
        if service.add_monitor(args.symbol, args.upper, args.lower):
            print(f"成功添加股票监控: {args.symbol}")
        else:
            print(f"添加股票监控失败: {args.symbol}")
    elif args.command == 'remove':
        if service.remove_monitor(args.symbol):
            print(f"成功删除股票监控: {args.symbol}")
        else:
            print(f"删除股票监控失败: {args.symbol}")
    elif args.command == 'list':
        monitors = service.list_monitors()
        if monitors:
            print("\n当前监控列表:")
            print("-" * 80)
            print(f"{'股票代码':<10} {'上限价格':<12} {'下限价格':<12} {'更新时间':<20}")
            print("-" * 80)
            for m in monitors:
                print(f"{m['symbol']:<10} "
                      f"{m['upper_price'] if m['upper_price'] else 'N/A':<12} "
                      f"{m['lower_price'] if m['lower_price'] else 'N/A':<12} "
                      f"{m['updated_at'].strftime('%Y-%m-%d %H:%M:%S'):<20}")
            print("-" * 80)
        else:
            print("当前没有监控的股票")
    else:
        parser.print_help()

if __name__ == '__main__':
    setup()
    main() 