import glob
import os
import cv2

class Mp4():
    def __init__(self, dataPath):
        self.dataPath = dataPath

    # フォーマットを設定フィアルから取得する

    def create(self, startTime, endTime, fileName):

        print("start:{}".format(startTime))
        print("end:{}".format(endTime))

        s = startTime.timestamp()
        e = endTime.timestamp()

        formatFile = "{}/format.txt".format(self.dataPath)
        (width, height, fps) = self._getFormat(formatFile)
        print("width={} heighth={} fps={}".format(width,height,fps))

        list = []
        for t in self._getTimestampList(self.dataPath):
            if(startTime.timestamp() < t and t < endTime.timestamp()):
                list.append(t)            

        # 動画生成
        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        video = cv2.VideoWriter(fileName, fourcc, fps, (width, height))
        for t in list:
            file = '{}/{}.jpg'.format(self.dataPath, t)
            print(file)
            img = cv2.imread(file)
            video.write(img)
        video.release()

    def _getFormat(self, filaName):
        with open(filaName, mode='r') as f:
            w,h,f = f.read().split(',')
            width = int(w)
            height = int(h)
            fps = int(float(f))
        return (width, height, fps)

    # タイムスタンプ一覧取得
    def _getTimestampList(self, path):
        list = []
        for path in glob.glob("{}/*.jpg".format(path)):
            fileName = os.path.split(path)[1] # ファイル名取得
            t = fileName.replace('.jpg', '') # 拡張子削除
            list.append(float(t))
        list.sort()
        return list
