import requests
import json
import numpy as np
import time
from datetime import datetime, timedelta

def main(stock_name, start_date, target_date):
    # MA
    result, ma5_title = MA(stock_name, start_date, target_date, N=5)
    tmp, ma10_title = MA(stock_name, start_date, target_date, N=10)
    result = np.hstack((result, tmp[:, 1:2]))
    tmp, ma20_title = MA(stock_name, start_date, target_date, N=20)
    result = np.hstack((result, tmp[:, 1:2]))
    tmp, ma60_title = MA(stock_name, start_date, target_date, N=60)
    result = np.hstack((result, tmp[:, 1:2]))
    tmp, ma120_title = MA(stock_name, start_date, target_date, N=120)
    result = np.hstack((result, tmp[:, 1:2]))
    tmp, ma240_title = MA(stock_name, start_date, target_date, N=240)
    result = np.hstack((result, tmp[:, 1:2]))

    # KD
    tmp, [rsv, k9, d9] = KD(stock_name, start_date, target_date)
    result = np.hstack((result, tmp[:, 1:]))

    titles = ['date', ma5_title, ma10_title, ma20_title, ma60_title, ma120_title, ma240_title, rsv, k9, d9]
    json_list = []
    for i in range(result.shape[0]):
        # to timestamp
        result[i, 0] = time.mktime(result[i, 0].timetuple())
        json_list.append(dict(zip(titles, result[i])))
    
    # result = np.round(result[:, 1: ], 2)
    
    return json.dumps({"data": json_list, 'title': titles})

def MA(stock_name, start_date, target_date, N):
    # heaader
    ma_name = "MA{}".format(N)
    # adjust start date 
    require_start_date = datetime.strptime(str(start_date), "%Y%m%d")
    if N == 5: require_start_date -= timedelta(days=10)
    elif N == 10: require_start_date -= timedelta(days=20)
    elif N == 20: require_start_date -= timedelta(days=50)
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
    start_datetime = datetime.strptime(str(start_date), "%Y%m%d").date()
    # caculate MA
    need_index = np.argwhere(history_array[:, 0]>=start_datetime)
    ma_array = history_array[need_index].reshape(-1, 2)
    ma_array[:, 1] = 0

    for i in range(ma_array.shape[0]):
        ma_array[i, 1] = np.mean(history_array[i:i+N, 1])

    ma_array[:, 1] = np.round(ma_array[:, 1].astype(float), 2)

    return ma_array, ma_name

def KD(stock_name, start_date, target_date, init_KD=50):
    # heaader
    kd_name = ['RSV', 'K9', 'D9']
    # adjust start date 
    require_start_date = datetime.strptime(str(start_date), "%Y%m%d")
    require_start_date -= timedelta(days=10)
    require_start_date = require_start_date.strftime('%Y%m%d')
    api_url = "http://140.116.86.242:8081/stock/api/v1/api_get_stock_info_from_date_json/{}/{}/{}".format(stock_name, require_start_date, target_date)
    r = requests.get(api_url)
    history_info = json.loads(r.text)['data']
    history_data = [[datetime.fromtimestamp(int(data['date'])).date(), data["high"], data["low"], data["close"]] for data in history_info]
    history_array = np.array(history_data)
    start_datetime = datetime.strptime(str(start_date), "%Y%m%d").date()
    # caculate KD
    need_index = np.argwhere(history_array[:, 0]>=start_datetime)
    kd_array = history_array[need_index].reshape(-1, 4)
    kd_array[:, 1:] = 0
    # RSV
    for i in range(kd_array.shape[0]):
        highest = history_array[i+1:i+10, 1].max()
        lowest = history_array[i+1:i+10, 2].min()
        kd_array[i, 1] = (history_array[i+1, 3] - lowest) / (highest-lowest) * 100
        
    # KD
    for i in range(kd_array.shape[0], -1, -1):
        if i==kd_array.shape[0]:
            pre_K, pre_D = init_KD, init_KD
        else:
            pre_rsv = kd_array[i, 1]
            # K
            kd_array[i, 2] = 2/3*pre_K + 1/3*pre_rsv
            # D
            kd_array[i, 3] = 2/3*pre_D + 1/3*kd_array[i, 2]
            # update K, D
            pre_K = kd_array[i, 2]
            pre_D = kd_array[i, 3]

    kd_array[:, 1:] = np.round(kd_array[:, 1:].astype(float), 2)
    
    return kd_array, kd_name
 


if __name__ == "__main__":
    json_result = main(2330, 20220420, 20220429)
    print(json_result)

    # json_result = KD(2330, 20220421, 20220429)
