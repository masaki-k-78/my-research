import fitbit
from ast import literal_eval
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#API関連の処理---------------------
CLIENT_ID = ""
CLIENT_SECRET = ""
TOKEN_FILE = "token.txt"
tokens = open(TOKEN_FILE).read()
token_dict = literal_eval(tokens)
access_token = token_dict['access_token']
refresh_token = token_dict['refresh_token']

def updateToken(token):
    f = open(TOKEN_FILE, 'w')
    f.write(str(token))
    f.close()
    return

client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, access_token=access_token, refresh_token=refresh_token, refresh_cb=updateToken)

#---------------------------------

#心拍数を取得する関数
def get_heart_rate(date, detail_level):
    #heart rateを1[s]単位で取得してpandas DataFrameに変換
    hr = client.intraday_time_series(resource='activities/heart', base_date=date, detail_level=detail_level)['activities-heart-intraday']['dataset']
    hr = pd.DataFrame.from_dict(hr)
    return hr

#日付を指定してget_heart_rate()を実行(detail_level='1sec'/'1min'/'15min')
TODAY = '2022-11-25'
dv = client.get_devices()
print(dv)
hr = get_heart_rate(date=TODAY, detail_level='1sec')
print(hr)

#csvファイルに書き出し
hr.to_csv("FBS01.csv", index=False)

#グラフ描画-------------------------
plt.rcParams['font.size'] = 14
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.yaxis.set_ticks_position('both')
ax1.xaxis.set_ticks_position('both')
ax1.set_xlabel('Time[h]')
ax1.set_ylabel('Heart Rate [bpm]')
ax1.xaxis.set_major_locator(mdates.MinuteLocator(byminute=range(0, 60, 10)))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.plot(pd.to_datetime(hr['time']), hr['value'], label=TODAY, lw=1)
ax1.legend()
fig.tight_layout()
plt.setp(ax1.get_xticklabels(), rotation=90, ha="right")
plt.show()
plt.close()
#-------------------------
