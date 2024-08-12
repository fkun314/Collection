# import some common libraries
import numpy as np
import matplotlib.pyplot as plt
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from tqdm import tqdm
import pandas as pd

import time

# 処理前の時刻
t1 = time.time() 

# Detectron2のコンフィグを読み込みます
cfg = get_cfg()

# モデル固有のコンフィグをマージします
cfg.merge_from_file("./configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")

# thresholdを設定します。この閾値より予測の確度が高いもののみ出力されます。
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5

# 今回利用するモデルのトレーニング済みファイルを読み込みます。
cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"
# cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"

# defaultだとcfgのDEVICE=cudaになっているので、cudaない場合はcpuに変更
# cfg.MODEL.DEVICE = "cpu"

# このclasses_listのindexと物体のカテゴリーIDが対応する
classes_list= MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes


# predictorを構築し、予測を実行します
predictor = DefaultPredictor(cfg)


    # ファイル名
input_name = 'sample'
input_video = input_name+'.mp4' # オリジナル動画

# メイン関数の実行
# 動画とそのフレームワーク情報を取得
video = cv2.VideoCapture(input_video)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)
frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(video.get(cv2.CAP_PROP_FPS))

# フレーム1枚ずつ処理する
for i in tqdm(range(frames)):
    ret, frame = video.read()
    # create_index(frame,i)
    outputs = predictor(frame)
    result = []
    [result.extend((
        i,
        outputs["instances"][x].pred_classes.item(),
        outputs["instances"][x].scores.item(),
        outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][0],
        outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][1],
        outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][2],
        outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][3]) 
    for x in range(len(outputs["instances"])))]
    df = pd.DataFrame(result, columns = ['frame-number','class-id','score','x-min','y-min','x-max','y-max'])
    # print(df)
    df.to_csv(str(input_name)+".csv", mode='a', header=False, index=False)
        
# 後処理
video.release()
print("frames -> " + str(frames))
print("fps -> " + str(fps))

# 処理後の時刻
t2 = time.time()

# 経過時間を表示
elapsed_time = t2-t1
print(f"経過時間-> {elapsed_time}")

