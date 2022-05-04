## 股票技術指標撰寫
傳入參數`(股票代號, 日期區間(始), 日期區間(始))`可以獲得以下相關指標
1. 移動平均線： MA5、MA10、MA20、MA60、MA120、MA240
2. KD：RSV、K9、D9
3. MACD：EMA12、EMA26、DIF9、MACD
4. RSI：RSI5、RSI10
5. 乖離率：BIAS10、BIAS20
6. 威廉指標：CDP、AH、NH、NL、AL

### Installation
```cmd
pip3 install -r requirement.txt
```

### How to run?
```cmd
python3 tools.py -stock "STOCK NAME" -start "START_DATE" -end "END_DATE"
```

- Example:
若欲查找台積電(2330)從2022/04/21至2022/04/29的技術指標：
```cmd
python3 tools.py -stock 2330 -start 20220421 -end 20220429
```