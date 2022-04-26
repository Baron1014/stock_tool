import requests
import json
import numpy as np
import time
from datetime import datetime, timedelta

def MA(stock_name, start_date, target_date, N):
    # adjust start date 
    require_start_date = datetime.strptime(str(start_date), "%Y%m%d")
    if N == 5: require_start_date -= timedelta(days=10)
    elif N == 10: require_start_date -= timedelta(days=20)
    elif N == 20: require_start_date -= timedelta(days=40)
    elif N == 60: require_start_date -= timedelta(days=80)
    elif N == 120: require_start_date -= timedelta(days=150)
    elif N == 240: require_start_date -= timedelta(days=300)
    else:raise Exception("N must is only [5, 10, 20, 60, 120, 240]")
    require_start_date = require_start_date.strftime('%Y%m%d')

    api_url = "http://140.116.86.242:8081/stock/api/v1/api_get_stock_info_from_date_json/{}/{}/{}".format(stock_name, require_start_date, target_date)
    r = requests.get(api_url)
    history_info = json.loads(r.text)['data']
    history_data = [[datetime.fromtimestamp(int(data['date'])).date() ,data["close"]] for data in history_info]
    history_array = np.array(history_data)
    print(history_array)
    start_datetime = datetime.strptime(str(start_date), "%Y%m%d").date()
    print(start_datetime)
    # caculate MA
    need_index = np.argwhere(history_array[:, 0]>=start_datetime)
    ma_array = history_array[need_index].reshape(-1, 2)
    ma_array[:, 1] = 0
    print(ma_array)
 

if __name__ == "__main__":
    MA(2330, 20200420, 20200425, N=5)
