# 股票监控告警系统 (TradeAlert) | Stock Price Alert System

一个轻量级的股票价格监控工具，帮助用户设置价格告警，无需手动盯盘。

A lightweight stock price monitoring tool that helps users set price alerts without manual monitoring.

## 功能特点 | Features

- 支持添加/删除股票监控 | Add/remove stock monitoring
- 设置价格上下限告警 | Set upper/lower price alerts
- 自动获取实时价格数据 | Automatic real-time price data fetching
- 邮件通知告警信息 | Email notification for alerts
- 本地数据存储 | Local data storage

## 安装 | Installation

1. 克隆仓库 | Clone the repository:
```bash
git clone https://github.com/Heyjoy/TradeAlert.git
cd TradeAlert
```

2. 安装依赖 | Install dependencies:
```bash
pip install -r requirements.txt
```

3. 配置环境变量 | Configure environment variables:
复制 `.env.example` 文件为 `.env`，并填写必要的配置信息：
Copy `.env.example` to `.env` and fill in the required configuration:
- 邮件服务器配置 | Email server configuration
- 其他可选配置 | Other optional settings

## 使用方法 | Usage

1. 启动监控服务 | Start monitoring service:
```bash
python main.py start
```

2. 添加股票监控 | Add stock monitoring:
```bash
python main.py add --symbol AAPL --upper 200 --lower 150
```

3. 查看当前监控列表 | List current monitors:
```bash
python main.py list
```

4. 删除股票监控 | Remove stock monitoring:
```bash
python main.py remove --symbol AAPL
```

## 开发计划 | Development Plan

- [x] MVP 版本（命令行界面）| MVP version (CLI)
- [ ] Web 界面 | Web interface
- [ ] 更多通知方式（如微信、钉钉等）| More notification methods (WeChat, DingTalk, etc.)
- [ ] 更多技术指标监控 | More technical indicators monitoring
- [ ] 历史数据分析和回测 | Historical data analysis and backtesting

## 技术栈 | Tech Stack

- Python 3.8+
- SQLite (数据库 | Database)
- yfinance (股票数据 | Stock data)
- SQLAlchemy (ORM)
- schedule (任务调度 | Task scheduling)

## 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！
Feel free to submit issues and pull requests!

## 许可证 | License

MIT License

## 作者 | Author

Heyjoy

## 免责声明 | Disclaimer

本项目仅供学习和研究使用，不构成投资建议。使用本软件进行投资决策的风险由用户自行承担。

This project is for learning and research purposes only and does not constitute investment advice. Users bear the risk of using this software for investment decisions.
