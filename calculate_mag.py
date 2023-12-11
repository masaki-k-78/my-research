import math
import pandas as pd
import csv
import numpy as np
import datetime
from collections import deque


List = [] #脚部動作データ格納用
Time = [] #時間データ格納用
str = ""
data = pd.read_csv(f"results/{str}_SD.csv", header=None).values.tolist()
for x in range(len(data)):
    List.append(data[x][1])
    Time.append(data[x][0])


def calc_mbase(d): #10分間のテスト中の5分から8分までの3分間の脚部動作時間をmbaseとして計算
    mb = 0
    for i in range(15000, 24000):
        mb = mb + d[i]
    return mb

def movingLeg(l): #脚部動作を0,1に変換
    for x in  range(len(l)):
        if l[x] > 60: #閾値は仮に60
            l[x] = 1
        else:
            l[x] = 0
    return l

def init_dq(l):
    deq = deque([0]*9000, maxlen=9000)
    for x in range(15000, 24000):
        deq.append(l[x])
    return deq

List = movingLeg(List) #脚部動作の有無
mbase = calc_mbase(List) #基準の脚部動作時間
rbase = 9000 - mbase #基準の増加余地

mt = []
dq = init_dq(List)
FIRST_BREAK_TIME = 117000
SECOND_BREAK_TIME = 243000

for z in range(30000, 363000): #mtを計算
    if z >= FIRST_BREAK_TIME and z < FIRST_BREAK_TIME+30000: #休憩中はmtを0とする
        mt.append(0)
    elif z >= SECOND_BREAK_TIME and z < SECOND_BREAK_TIME+30000: #休憩中はmtを0とする
        mt.append(0)
    elif z == FIRST_BREAK_TIME+30000 or SECOND_BREAK_TIME+30000: #休憩が終了したらdqを初期化
        dq = init_dq(List)
    else:
        dq.append(List[z])
        mt.append(sum(dq))

dm = []

for z in range(len(mt)): #最初の10分が除かれたデータだからずれている
    if z >= FIRST_BREAK_TIME-30000 and z < FIRST_BREAK_TIME:
        dm.append(0)
    elif z >= SECOND_BREAK_TIME-30000 and z < SECOND_BREAK_TIME:
        dm.append(0)
    else:
        dm.append(mt[z] - mbase)

f = open(f"results/{str}_MAG.csv", 'w', encoding='utf-8', newline='')
writer = csv.writer(f)

pt = []
for z in range(len(dm)):
    pt = [[Time[z+30000], dm[z]/rbase]]
    writer.writerows(pt)

f.close()



