#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import time
import datetime as dt
from datetime import timedelta
from box import Box
import json
import datetime

import Mqtt
import Mp4
import S3

identityPoolId = 'ap-northeast-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
endPoint = "xxxxxxxxxxxx-ats.iot.ap-northeast-1.amazonaws.com"
clientId = "myClientId"
topic = "monitorCameraTopic"

# dataPath
dataPath = './data'
print("dataPath:{}".format(dataPath))

# root-CA
rootCA = './root-CA.crt'
print("rootCA={}".format(rootCA))

# Bucket
bucketName = "monitoring-camera-data"

def onSubscribe(message):

    command = Box(json.loads(str(message, 'utf-8')))
    startTime = datetime.datetime.strptime(command.startTime, "%Y/%m/%d %H:%M:%S")
    seconds = command.seconds
    endTime = startTime + timedelta(seconds=seconds) 
    fileName = "/tmp/output.mp4"

    mp4 = Mp4.Mp4(dataPath)
    mp4.create(startTime, endTime, fileName)
    print("{} created.".format(fileName))

    s3 = S3.S3(identityPoolId)
    key = "{}.mp4".format(startTime)
    s3.putObject(bucketName, key, fileName)

def main():


    mqtt = Mqtt.Mqtt(identityPoolId, endPoint, clientId, topic, rootCA ,onSubscribe)
    mqtt.connect()

    while(True):
        time.sleep(0.5)

main()