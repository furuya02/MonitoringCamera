#!/usr/bin/env python3
# coding: UTF-8

import os
import glob
import datetime
import time

# dataPath
dataPath = '/home/pi/MonitoringCamera/data'

# 1時間以上前のデータを削除する
hour = 1

# 指定時間より前のタイムスタンプを取得
dt = datetime.datetime.now()
dt = dt - datetime.timedelta(hours=hour)
timestamp = dt.timestamp()

for path in glob.glob("{}/*.jpg".format(dataPath)):
    fileName = os.path.split(path)[1] # ファイル名取得
    t = fileName.replace('.jpg', '') # 拡張子削除
    # 指定時間より前のデータを削除する
    if(float(t) < timestamp):
        print("delete {}".format(path))
        os.remove(path)
        