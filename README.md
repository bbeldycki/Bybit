This is still WORK IN PROGRESS.
-

This bot was created to do automatic buy/sell transactions on bybit.com based on certain
indicators.

How it works?

Before running the code, you have to log to your account on bybit.com, manually choose indicators
and set specific alerts based on their value changes. Then, you have to turn on e-mail notifications
for these alerts. Now the setup is done and you can run the code.

The code checks the e-mail inbox every 15 seconds for new alerts. When it identifies the alert e-mail,
it sends a buy or sell request via bybit API.

Planned functionality:
-  
1. Access indicator values directly from bybit.com or tradingview.com websites
and eliminate the need to use e-mail notification in order to shorten the code response time.
2. Prepare a launcher file with user-friendly GUI for easy setup and use of the bot.
3. Add ML-based data analysis component for trend analysis and automatic update of order data
(e.g. leverage, stop loss value).
4. Access archive data, analyse them and implement trend forecasting based on the results.
