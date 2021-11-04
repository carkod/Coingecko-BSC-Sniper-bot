# Coingecko-BSC-Sniper-bot
![TradingTigers](https://trading-tigers.com/assets/img/TradingTigers.png)  

Trading-Tigers presents the open source Coingecko Sniper bot, it buys any BSC token that has been newly listed on Coingecko and checks their TakeProfit/StopLoss percentage and sells it at your conditions.

## Please support us by buying TIGS token!
<a href="https://t.me/TradingTigersChat">
<img src="https://www.latestcarernews.com/wp-content/uploads/2019/08/Telegram.bk.png" width="300" >  
</a>

# Infos
You pay 1% fees on each transaction.

# Install
First of all, you need install Python3+  
Run on Android you need Install [Termux](https://termux.com)  
```termux
pkg install python git
```

Clone Repo:  
```shell
git clone https://github.com/Trading-Tiger/Coingecko-BSC-Sniper-bot
cd Coingecko-BSC-Sniper-bot
```
Install Requirements:  
```python
python -m pip install -r requirements.txt
```  

# Setup & Start
Edit Settings.json with your infos, Address, SecretKey.  
Options:
```json
"MaximumTokenTAX": 15, // Max Token Tax from listed Token.
"Currency": "BUSD", // BNB or BUSD.
"AmountPerBuy": 10, // Amount in BUSD(1) or BNB(0.01).
"TakeProfit": 100, // Percentage Take Profit from your Input Value.
"StopLost": 25 // Percentage StopLose from your Input Value.
```

Start Sniper:  
```python
python3 main.py
```