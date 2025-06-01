# 股票监控告警系统 (TradeAlert)

一个轻量级的股票价格监控工具，帮助用户设置价格告警，无需手动盯盘。

## 功能特点

- 支持添加/删除股票监控
- 设置价格上下限告警
- 自动获取实时价格数据
- 邮件通知告警信息
- 本地数据存储

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/Heyjoy/TradeAlert.git
cd TradeAlert
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
复制 `.env.example` 文件为 `.env`，并填写必要的配置信息：
- 邮件服务器配置
- 其他可选配置

## 使用方法

1. 启动监控服务：
```bash
python main.py start
```

2. 添加股票监控：
```bash
python main.py add --symbol AAPL --upper 200 --lower 150
```

3. 查看当前监控列表：
```bash
python main.py list
```

4. 删除股票监控：
```bash
python main.py remove --symbol AAPL
```

## 开发计划

- [x] MVP 版本（命令行界面）
- [ ] Web 界面
- [ ] 更多通知方式（如微信、钉钉等）
- [ ] 更多技术指标监控
- [ ] 历史数据分析和回测

## 许可证

MIT License
