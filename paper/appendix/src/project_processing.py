#from email.mime import image
import re
#from symbol import typelist
from ultralytics import YOLO
import cv2
from PIL import Image
import random
import os
import yt_dlp
import matplotlib.pyplot as plt
import numpy as np
import glob
import torch
import shutil
from pytube import YouTube

class project_processing:
    def get_random_frame(self, name, video_path, out_path, img_sum):
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        #print(frame_count)
        for count in range(img_sum):
            new_img_name = f"{name}_{str(count).zfill(4)}.jpg"
            new_img_path = out_path + new_img_name
            #出力フォルダが存在しない場合は作成する
            os.makedirs(out_path, exist_ok=True)
            random_frame_number = random.randint(0, frame_count - 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_number)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(new_img_path, frame)
                print(f"Saved random frame {random_frame_number} as {new_img_name}")
        print(f"saved at {out_path}")

    def cropping(self, train_type, input_path, output_path):
        #model = YOLO("yolov8n.pt")
        #yolov8n.ptで推論しようとすると、obj = result.pandas~の部分でエラーになるよ
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained = True)
        image_files = glob.glob(os.path.join(input_path, '*.jpg')) 
        # 出力フォルダが存在しない場合は作成する
        os.makedirs(output_path, exist_ok=True)
        #通し番号
        count = 0
        for image_file in image_files:
            # 画像の読み込み
            image = cv2.imread(image_file)
            # 物体検出の実行
            result = model(image)
            # 物体検出結果をPandasのDataFrame形式で取得する
            obj = result.pandas().xyxy[0]
            # 検出された電車のバウンディングボックスの中身を別のフォルダに保存する
            for j in range(len(obj)):
                # バウンディングボックスの情報を取得
                name = obj.name[j]
                score = obj.confidence[j]
                #画像に複数の電車が映っている場合はその画像の処理はスキップする
                if name.count("train") > 2:
                    continue
                if name == "train" and score >=0.90:
                    #保存先のパスを生成
                    filename = f"{train_type}_{str(count).zfill(3)}"
                    img_filename = filename + ".jpg"
                    save_path = os.path.join(output_path, img_filename)
                    cv2.imwrite(save_path, image)
                    print(f"saved {img_filename}")
                    count += 1 
        #保存した画像を消す（物体認識をする前の画像を消す）
        # ディレクトリ内のファイルを取得
        file_list = os.listdir(input_path)
        for file_name in file_list:
            file_path = os.path.join(input_path, file_name)
            # ファイルが存在し、拡張子が.jpgの場合にのみ削除
            if os.path.isfile(file_path) and file_name.endswith(".jpg"):
                os.remove(file_path)
                print(f"{file_name} を削除しました")
        #物体認識をする前の画像フォルダを削除する
        #os.rmdir(input_path)
        #print(f"{input_path} を削除しました")

