#!/usr/bin/env python3
# coding: UTF-8
import cv2
import numpy as np
import datetime
import time
import sys

useMonitor = False

# dataPath
dataPath = './data'
formatFile = "{}/format.txt".format(dataPath)
print("formatFile:{}".format(formatFile))


cap = cv2.VideoCapture(0)
 
## 使用する解像度を指定する

# 1フレーム 約380K 1秒で 約1.9M 1分で約114M 1時間で約6.8G 1日で約164G
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 5)

time.sleep(2)
            
# フレームを表示する
def show(frame, width, height, magnification):
    if(useMonitor==True):
        frame = cv2.resize(frame , (int(width * magnification), int(height * magnification)))
        cv2.imshow('frame', frame)
        cv2.waitKey(1) 

# 日時を付加
def setDateTime(dt, frame, width, height):
    # フォント
    font = cv2.FONT_HERSHEY_SIMPLEX;
    thickness = 2
    fontSize = height * 0.002

    dateStr = "{0:%Y-%m-%d %H:%M:%S}".format(dt)
    (w,h) = cv2.getTextSize(dateStr, font, fontSize, thickness)[0]

    cv2.putText(frame, dateStr, (int((width-w)/2),int(height-h-2)), font, fontSize,(255,255,255), thickness, lineType=cv2.LINE_8)
    return frame


def main():
    
    # 実際に利用できている解像度を取得する
    ret, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    height, width, channels = frame.shape[:3]
    print("width:{},height:{},fps:{}".format(width, height, fps))
    # フォーマットを設定フィアルに記録する
    with open(formatFile, mode='w') as f:
        f.write("{},{},{}".format(width,height,fps))

    
    # モニターの表示倍率
    magnification = 0.5
    
    while True:
        # フレーム取得
        ret, frame = cap.read() 
        # 日時取得
        dt = datetime.datetime.now()
        timestamp = dt.timestamp()
        # 日時表示
        frame = setDateTime(dt, frame, width, height)
        # ファイル名
        filename = "{}/{}.jpg".format(dataPath, timestamp)
        date = dt_utc_aware = datetime.datetime.fromtimestamp(timestamp)

        cv2.imwrite(filename, frame)
        # モニター
        show(frame, width, height, magnification)
 
    cap.release() 
    cv2.destroyAllWindows() 
 
main()

