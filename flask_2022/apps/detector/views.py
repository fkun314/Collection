# 大量のライブラリをインポート
from regex import P
from requests import session
from apps.app import db
from apps.crud.models import User
import uuid
from pathlib import Path
import math
import itertools
import random
import cv2
import numpy as np
from PIL import Image
import copy
import sys
from datetime import datetime
import threading
from tqdm import tqdm
import pandas as pd
import time
import uuid
from scipy import stats
import matplotlib.pyplot as plt
from PIL import Image
from time import sleep
# UploadImageFormをimportする
from apps.detector.forms import DeleteForm, UploadImageForm, UploadMovieForm
from apps.detector.models import UserImage, UserVideo, DetectedLists, DetectedImages, IndexVideos, RelationshipTables
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
    make_response,
    jsonify,
)
import matplotlib.pyplot as plt
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import sqlite3
import ctypes

# 比較するときのソート
def list_sort_find_max(result):
    # resultのthetaが最大のものを取得
    max, max_uuid = sorted(
        result, key=lambda x: x[2])[-1][2], sorted(result, key=lambda x: x[2])[-1][3]

    # max_uuidが一致するまでresultの順番を入れ替える
    for i in range(len(result)):
        p = result.pop(0)
        if p[3] != max_uuid:
            result.append(p)
        else:
            result.insert(0, p)
            break

    return (result)


# 2つのリストのオブジェクト名を比較し、一致しているかを判定する
def check_2_list(a, b):
    for i in range(len(b)):
        b.append(b[i])

    # bのオブジェクト名の中にaのオブジェクト名が順番通りに含まれているか確認
    for i in range(len(a)):
        if a[0][0] == b[i][0]:
            itti = 0
            return_b = []
            for j in range(len(a)):
                if a[j][0] in b[i+j][0]:
                    itti += 1
                    return_b.append(b[i+j])
                    if itti == len(a):
                        return True, a, return_b

        else:
            continue
    
    return False, a, b

def img_plot(im_path,video_path, frame_number, plt_list, base_list):
# Figureとaxの準備 ... matplotlibの定型的な処理
    fig = plt.figure(figsize=(8, 6))
    fig.patch.set_facecolor('white') #<--これはなくてもよさそう。図全体の背景色を設定するが、imageで塗られる形になるため。
    ax = fig.add_subplot(1, 1, 1)

    # 背景に画面イメージを出す
    im = Image.open(im_path)

    # imのサイズを取得
    im_width, im_height = im.size

    x = []
    y = []
    x_base = []
    y_base = []

    for i in plt_list:
        x.append(i[1])
        y.append(i[2])
    x.append(plt_list[0][1])
    y.append(plt_list[0][2])

    for i in base_list:
        x_base.append(i[1])
        y_base.append(i[2])
    x_base.append(base_list[0][1])
    y_base.append(base_list[0][2])

    # タッチ座標をプロットする
    ax.scatter(x, y, c='red', s=20)
    ax.scatter(x_base, y_base, c='blue', s=20)

    for i in range(len(x)-1):
        ax.plot([x[i], x[i+1]], [y[i], y[i+1]], c='red', linewidth=3)
        ax.plot([x_base[i], x_base[i+1]], [y_base[i], y_base[i+1]], c='#5AB8DD', linewidth=3)

    ax.imshow(im)

    which = 0

    # プロット画像を保存する
    try:
        plt.savefig('apps/images/location/'+im_path.replace('apps/images/predicted/', '').replace('.png', '')+"_"+video_path.replace('.mp4', '')+'_'+str(frame_number)+'.png')
        which = 0
    except:
        plt.savefig('apps/images/location/'+im_path.replace('apps/images/temp/', '').replace('.png', '')+"_"+video_path.replace('.mp4', '')+'_'+str(frame_number)+'.png')
        which = 1


    if which == 0:
        return str(im_path.replace('apps/images/predicted/', '').replace('.png', '')+"_"+video_path.replace('.mp4', '')+'_'+str(frame_number)+'.png')
    else:
        return str(im_path.replace('apps/images/temp/', '').replace('.png', '')+"_"+video_path.replace('.mp4', '')+'_'+str(frame_number)+'.png')

# 処理前の時刻
t1 = time.time()

# Detectron2のコンフィグを読み込みます
cfg = get_cfg()

# モデル固有のコンフィグをマージします
cfg.merge_from_file("apps/detector/configs/COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")

# thresholdを設定します。この閾値より予測の確度が高いもののみ出力されます。
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7

# 今回利用するモデルのトレーニング済みファイルを読み込みます。
cfg.MODEL.WEIGHTS = "detectron2://COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x/137849600/model_final_f10217.pkl"

# defaultだとcfgのDEVICE=cudaになっているので、cudaない場合はcpuに変更
# cfg.MODEL.DEVICE = "cpu"

# このclasses_listのindexと物体のカテゴリーIDが対応する
classes_list= MetadataCatalog.get(cfg.DATASETS.TRAIN[0]).thing_classes

# predictorを構築し、予測を実行します
predictor = DefaultPredictor(cfg)

# template_folderを指定する(staticは指定しない)
dt = Blueprint("detector", __name__, template_folder="templates")

# Threadで動画解析を行う
name_quere = []
class MyThread(threading.Thread):
    def __init__(self, target, name):
        super(MyThread, self).__init__(target=target, name=name)
        self.stop_event = threading.Event()
        self.progress = 0

    def stop(self):
        self.stop_event.set()

    def run(self):
        global name_quere
        # 処理時間を計測する
        start = time.time()
        # 検出数をカウントする
        count = 0
        try:
            dbname = 'local.sqlite'
            conn = sqlite3.connect(dbname)
            cur = conn.cursor()
            cur.execute("update user_videos set is_detected = 3 where video_path = ?",[str(threading.currentThread().getName())])
            conn.commit()
            cur.close()
            conn.close()

            input_video = 'apps/movies/'+str(threading.currentThread().getName())
            
            while(True):
                time.sleep(3)
                conn = sqlite3.connect(dbname)
                cur = conn.cursor()
                cur.execute("update user_videos set is_detected = 3 where video_path = ?",[str(threading.currentThread().getName())])
                conn.commit()
                cur.close()
                conn.close()
                
                self.progress = -1
                if name_quere[0] == str(threading.currentThread().getName()):
                    break

            if name_quere[0] == str(threading.currentThread().getName()):
                conn = sqlite3.connect(dbname)
                cur = conn.cursor()
                cur.execute("update user_videos set is_detected = 1 where video_path = ?",[str(threading.currentThread().getName())])
                conn.commit()
                cur.close()
                conn.close()

                user_id = 0
                conn = sqlite3.connect(dbname)
                cur2 = conn.cursor()
                cur2.execute("select user_id from user_videos where video_path = ?",[str(threading.currentThread().getName())])
                conn.commit()
                for row in cur2:
                    user_id = row[0]
                cur2.close()
                conn.close()

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
                    conn = sqlite3.connect(dbname)
                    cur = conn.cursor()
                    self.progress = round(i/frames*100,2)
                    ret, frame = video.read()
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
                    count += len(outputs["instances"])
                    cur.execute("INSERT INTO index_videos (user_id, id, fps_number, detected_count) VALUES (?,?,?,?)", [user_id,threading.currentThread().getName(), i, len(outputs["instances"])])
                    df = pd.DataFrame(result, columns = ['frame-number','class-id','score','x-min','y-min','x-max','y-max'])
                    for t in result:
                        # 相対値
                        relative_x_min = round(float(t[3])/ width ,4)
                        relative_y_min = round(float(t[4])/ height ,4)
                        relative_x_max = round(float(t[5])/ width ,4)
                        relative_y_max = round(float(t[6])/ height ,4)

                        center_x = round((relative_x_min + relative_x_max)/2,4)
                        center_y = round((relative_y_min + relative_y_max)/2,4)

                        cur.execute("INSERT INTO detected_lists (user_id, id, fps_number, detected_name, detected_score, detected_x_min, detected_y_min, detected_x_max, detected_y_max, center_x, center_y) VALUES (?,?,?,?,?,?,?,?,?,?,?)", [user_id,threading.currentThread().getName(), i, classes_list[t[1]], round(t[2],4), relative_x_min, relative_y_min, relative_x_max, relative_y_max, center_x, center_y])

                    conn.commit()
                    cur.close()
                    conn.close()

                self.progress = 100

                conn = sqlite3.connect(dbname)
                cur = conn.cursor()
                cur.execute("update user_videos set is_detected = 2 where video_path = ?",[str(threading.currentThread().getName())])
                conn.commit()
                cur.close()
                conn.close()

                conn = sqlite3.connect(dbname)
                cur = conn.cursor()

                name_quere.pop(0)


        finally:
            #処理時間を表示
            print('処理時間：{0:.3f}秒'.format(time.time() - start))
            # 検出数を表示
            print('検出数：{}個'.format(count))

    # 例外を発生させて強制終了
    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    def raise_exception(self):
        thread_id = self.get_id()
        resu = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if resu > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Failure in raising exception')   


jobs = {}

@dt.route('/start/<id>/')
def root(id):
    t = MyThread(target=MyThread, name=id)
    t.start()
    jobs[id] = t
    return make_response(f'{id}の処理を受け付けました\n'), 202

@dt.route('/status/<id>/')
def status(id):
    if id in jobs:
        return make_response(f'{id}は実行中です\n'), 200
    else:
        return make_response(f'{id}は実行していません\n'), 200

predict_info = []
predict_progress = []
# dtアプリケーションを使ってエンドポイントを作成する
@dt.route("/")
@login_required
def index():
    return render_template("detector/index.html")

@dt.route("/list")
@login_required
def listview():
    predict_info = []

    # # UserとUserVideoをjoinして動画一覧を取得する
    user_movie = (
        db.session.query(User, UserVideo)
        .join(UserVideo)
        .filter(User.id == UserVideo.user_id)
        .filter(User.id == current_user.id)
        # deskで逆順
        .order_by(UserVideo.id.desc())
        .all()
    )

    # 完了したのを削除する
    # https://yuta0306.github.io/py-dict-iter-err
    if jobs:
        try:
            for i in list(jobs):
                if jobs[i].progress == 100:
                    jobs[i].stop()
                    del jobs[i]
        finally:
            print("remove")

    time.sleep(0.2)
    # 削除したものを除外して進捗表示
    if jobs:
        for i in jobs:
            info = (db.session.query(UserVideo).filter(UserVideo.video_path == i).first())
            predict_info.append([info.video_title,jobs[i].progress])
    else:
        predict_info = []

    delete_form = DeleteForm()

    return render_template(
        "detector/list.html",
        user_videos=user_movie,
        delete_form=delete_form,
        predict_info=predict_info,
    )

# 動画再生用のエンドポイント
@dt.route("/video/<path:filename>")
def image_movie(filename):
    return send_from_directory(current_app.config['UPLOAD_MOVIE_FOLDER'], filename)

# 画像表示用のエンドポイント
@dt.route("/img/<path:filename>")
def image(filename):
    return send_from_directory(current_app.config['UPLOAD_IMG_FOLDER'], filename)

# 解析済み画像表示用のエンドポイント
@dt.route("/img-predicted/<path:filename>")
def image_predicted(filename):
    return send_from_directory(current_app.config['UPLOAD_IMG_PREDICTED_FOLDER'], filename)

# 解析済み画像表示用のエンドポイント（位置関係）
@dt.route("/img-angle/<path:filename>")
def image_angle(filename):
    return send_from_directory(current_app.config['UPLOAD_IMG_ANGLE_FOLDER'], filename)

# 動画解析済み表示用のエンドポイント
@dt.route("/movie-predicted/<path:filename>")
def movie_predicted(filename):
    return send_from_directory(current_app.config['UPLOAD_MOVIE_PREDICTED_FOLDER'], filename)

# ローディング画面（未実装）
@dt.route("/loading/<path:filename>", methods=["GET", "POST"])
def loading(filename):
    return render_template("detector/loading.html",filename=filename)

# 動画の詳細データを表示する
@login_required
@dt.route("/detail/<path:filename>", methods=["GET", "POST"])
def detail(filename):
    # 動画の詳細データを取得する
    video_path = 'apps/movies/'+filename
    cap = cv2.VideoCapture(video_path)
    # 動画の縦と横のサイズを取得する
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # 動画のフレームレートを取得する
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 動画の総フレーム数を取得する
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # 動画の総時間を取得する
    duration = frame_count / fps
    # durationの分と秒に変換する
    minutes, seconds = divmod(int(duration), 60)
    time = "{:02d}:{:02d}".format(minutes, seconds)

    # 動画の詳細データをまとめる
    video_detail = {
        "width": int(width),
        "height": int(height),
        "fps": round(fps,2),
        "frame_count": int(frame_count),
        "duration": time,
    }

    return render_template("detector/video_result.html",filename=filename,video_detail=video_detail)


# 動画解析の結果を返すAPIを作成
@dt.route("/api/predict/<path:filename>/<fps>", methods=["GET", "POST"])
def api_result(filename, fps):
    video_search = []
    predict_results = db.session.query(IndexVideos).filter(IndexVideos.fps_number == fps).filter(IndexVideos.id == filename).all()
    for predict_video_result in predict_results:
        predict_details = db.session.query(DetectedLists).filter(DetectedLists.id == predict_video_result.id).filter(DetectedLists.fps_number == fps).all()
        for predict_detail in predict_details:
            # 位置関係の計算のためのリスト
            fps_number = predict_detail.fps_number
            video_search.append([predict_detail.id, predict_detail.fps_number, predict_detail.detected_name, round((predict_detail.detected_score)*100,2) ,predict_detail.detected_x_min, predict_detail.detected_y_min, predict_detail.detected_x_max, predict_detail.detected_y_max])

    return jsonify(video_search)

# 動画再生用のエンドポイント
@dt.route("/play/<path:filename>/<time>/<title>/<fps>/<val>")
def playMovie(filename, fps, title, time, val):
    return render_template("detector/play.html",filename=filename,fps=fps,title=title,time=time,val=val,starttime=time)

# 結果表示用のエンドポイント
@dt.route("/result_detail/<id>/<path:filename>/<fps>")
def result_detail(id, filename, fps):
    starttime = fps
    total_frame = db.session.query(UserVideo).filter(UserVideo.video_path == filename).first()

    s = float(starttime) // float(total_frame.fps_info)
    ms = int(starttime) - int(s) * int(total_frame.fps_info)
    ms = float(ms)/int(total_frame.fps_info)
    s = s + ms
    s = round(s, 3)

    # データベースから検索
    predict_results_img = DetectedImages.query.filter_by(id=id).all()

    image_search = []
    object_img_name_list = []
    video_search = []
    video_search_pre = []

    # 物体の位置関係保存用
    img_point_list = []
    result = []

    # 画像の縦と横のサイズを取得
    img_path = 'apps/images/predicted/'+id
    im = Image.open(img_path)
    h, w = im.size

    # 動画の縦と横のサイズを取得
    video_path = 'apps/movies/'+filename
    cap = cv2.VideoCapture(video_path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # 画像の検索結果を取得
    object_img_count = len(predict_results_img)
    for predict_img_result in predict_results_img:
        image_search.append([predict_img_result.detected_name, predict_img_result.detected_score, predict_img_result.detected_x_min, predict_img_result.detected_y_min, predict_img_result.detected_x_max, predict_img_result.detected_y_max])
        # UIDを追加
        uid = uuid.uuid4()
        img_point_list.append([predict_img_result.detected_name, (predict_img_result.detected_x_min + predict_img_result.detected_x_max) / 2 * h, (predict_img_result.detected_y_min + predict_img_result.detected_y_max) / 2 * w,uid])
        object_img_name_list.append(predict_img_result.detected_name)

    image_search = sorted(image_search, key=lambda x: (x[0],x[2],x[4]))

    user_id = current_user.id

    # 動画の検索結果を取得
    predict_results = db.session.query(IndexVideos).filter(IndexVideos.user_id == user_id).filter(IndexVideos.fps_number == fps).filter(IndexVideos.id == filename).all()
    for predict_video_result in predict_results:
        predict_details = db.session.query(DetectedLists).filter(DetectedLists.id == predict_video_result.id).filter(DetectedLists.fps_number == fps).all()
        # 中心座標のリスト
        video_point_result = []
        fps_number = 0
        # 要素数が一致する
        for predict_detail in predict_details:
            # 位置関係の計算のためのリスト
            fps_number = predict_detail.fps_number
            video_search.append([predict_detail.id, predict_detail.fps_number, predict_detail.detected_name, predict_detail.detected_score ,predict_detail.detected_x_min, predict_detail.detected_y_min, predict_detail.detected_x_max, predict_detail.detected_y_max])
            # UIDを追加
            uid = uuid.uuid4()
            video_point_result.append([predict_detail.detected_name, (predict_detail.detected_x_min + predict_detail.detected_x_max) / 2 * h, (predict_detail.detected_y_min + predict_detail.detected_y_max) / 2 * w, uid])

    plot_img_path = 'apps/images/predicted/'+id

    score = 0

    search_results_count = len(video_search)
    for i in range(0,search_results_count,object_img_count):
        video_search_pre.append(video_search[i:i+object_img_count])    
    for j in range(len(video_search_pre)):
        object_video_name_list = []
        object_video_detail_list = []
        for i in range(len(video_search_pre[j])):
            object_video_name_list.append(video_search_pre[j][i][2])
            object_video_detail_list.append(video_search_pre[j][i][0:])
        object_video_detail_list = sorted(object_video_detail_list, key=lambda x:(x[2],x[4],x[6]))
        object_video_name_list = sorted(object_video_name_list, key=lambda x:x[0])

        match_count = 0
        for i in range(len(image_search)):
            if(str(image_search[i][0]) == str(object_video_name_list[i])):
                match_count += 1

        # オブジェクト名の一致数が画像と動画で一致したとき
        if(match_count == len(image_search)):
            tmp = []
            # ピクセルのズレが平均0.1以内のとき
            for i in range(len(image_search)):
                if((round(abs(image_search[i][2] - object_video_detail_list[i][4]),4)+round(abs(image_search[i][3] - object_video_detail_list[i][5]),4)+round(abs(image_search[i][4] - object_video_detail_list[i][6]),4)+round(abs(image_search[i][5] - object_video_detail_list[i][7]),4)) / 4 <= 0.1):
                    tmp.append([object_video_detail_list[i][0],object_video_detail_list[i][1],object_video_detail_list[i][2],object_video_detail_list[i][3],object_video_detail_list[i][4],object_video_detail_list[i][5],object_video_detail_list[i][6],object_video_detail_list[i][7],round((1-(abs(image_search[i][2] - object_video_detail_list[i][4])+abs(image_search[i][3] - object_video_detail_list[i][5])+abs(image_search[i][4] - object_video_detail_list[i][6])+abs(image_search[i][5] - object_video_detail_list[i][7])))*100,5),round(abs(image_search[i][2] - object_video_detail_list[i][4]),6),round(abs(image_search[i][3] - object_video_detail_list[i][5]),6),round(abs(image_search[i][4] - object_video_detail_list[i][6]),6),round(abs(image_search[i][5] - object_video_detail_list[i][7]),6)])
                    score += round((1-(abs(image_search[i][2] - object_video_detail_list[i][4])+abs(image_search[i][3] - object_video_detail_list[i][5])+abs(image_search[i][4] - object_video_detail_list[i][6])+abs(image_search[i][5] - object_video_detail_list[i][7])))*100,5)
            if(len(tmp) == object_img_count):
                result.append(tmp)

    final_results = []

    score /= object_img_count
    score = round(score,2)

    for k in result:
        for i in k:
            video_title = db.session.query(UserVideo).filter(UserVideo.video_path == filename).first()
            final_results.append([video_title.video_title,i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[0],i[8],i[9],i[10],i[11],i[12]])

    # 詳細ページの動画のフレームをimgに保存する
    detail_page_frame = final_results[0]
    best_match_filename = str(uuid.uuid4())+'.png'
    detail_page_frame.append(best_match_filename)

    cap = cv2.VideoCapture("apps/movies/"+detail_page_frame[8])
    cap.set(cv2.CAP_PROP_POS_FRAMES, detail_page_frame[1])
    ret, frame = cap.read()
    height, width, channels = frame.shape
    plot_list = []
    for i in video_search:
        plot_list.append(i[2:8])
    for i in plot_list:
        random_rgb = random_rgb_vibrant()
        cv2.rectangle(frame, (int(i[2]*width), int(i[3]*height)), (int(i[4]*width), int(i[5]*height)), random_rgb, 5)
        cv2.putText(frame, str(i[0]+" "+str(round(float(str(i[1])),3))), (int(i[2]*width), int((i[3]*height)+(height*0.015))), cv2.FONT_HERSHEY_PLAIN, 2.5, random_rgb, 5, cv2.LINE_AA)

    cv2.imwrite("apps/movies/predicted/"+str(best_match_filename), frame)

    # final_resultsの[1]を100倍にして％表示にする
    for i in final_results:
        i[3] = round(i[3]*100,2)

    return render_template("detector/result_detail.html",filename=filename,starttime=s,plot_img_path=plot_img_path,img_path=id,match_info=final_results,detail_page_frame=detail_page_frame[14],id=id,score=score)

# 図形を描画する
def draw_route(im_path, video_path, frame_number, min_perm_t, min_perm_q):
    # 画像読み込み
    img = cv2.imread(im_path)
    x_perm_t = [x[i] for i in min_perm_t]
    y_perm_t = [y[i] for i in min_perm_t]
    x_perm_t.append(x[min_perm_t[0]])
    y_perm_t.append(y[min_perm_t[0]])

    x_perm_q = [x[i] for i in min_perm_q]
    y_perm_q = [y[i] for i in min_perm_q]
    x_perm_q.append(x[min_perm_q[0]])
    y_perm_q.append(y[min_perm_q[0]])

    plt.imshow(img)
    plt.plot(x_perm_t, y_perm_q, 'ro-')

    # plt.show()
        # プロット画像を保存する
    try:
        plt.savefig('apps/images/location/'+im_path.replace('apps/images/predicted/', '').replace('.png', '')+"_"+video_path.replace('.mp4', '')+'_'+str(frame_number)+'.png')
        which = 0
    except:
        plt.savefig('apps/images/location/'+im_path.replace('apps/images/temp/', '').replace('.png', '')+"_"+video_path.replace('.mp4', '')+'_'+str(frame_number)+'.png')
        which = 1

    if which == 0:
        return str(im_path.replace('apps/images/predicted/', '').replace('.png', '')+"_"+video_path.replace('.mp4', '')+'_'+str(frame_number)+'.png')
    else:
        return str(im_path.replace('apps/images/temp/', '').replace('.png', '')+"_"+video_path.replace('.mp4', '')+'_'+str(frame_number)+'.png')

# 一致度を計算
def calc_match(tmp):
    def distance_four(x1, y1, x2, y2):
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def distance_two(p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def angle(p1, p2):
        return np.arctan2(p2[1] - p1[1], p2[0] - p1[0])

    # 直線で最短の経路を検索する
    def search_route(x, y):
        n = len(x)
        min_distance = float("inf")
        min_perm = None
        for perm in itertools.permutations(range(n)):
            d = 0
            for i in range(n-1):
                d += distance_four(x[perm[i]], y[perm[i]], x[perm[i+1]], y[perm[i+1]])
            d += distance_four(x[perm[n-1]], y[perm[n-1]], x[perm[0]], y[perm[0]])
            if d < min_distance:
                min_distance = d
                min_perm = perm
        return min_perm

    # 距離と角度を計算する
    def calc_distance_and_angle(min_perm):
        x_perm = [x[i] for i in min_perm]
        y_perm = [y[i] for i in min_perm]
        x_perm.append(x[min_perm[0]])
        y_perm.append(y[min_perm[0]])

        # 順番に並べ替えられた点のペアを作成する
        pairss = [(x[i], y[i]) for i in min_perm] + [(x[0], y[0])]

        # 全てのペア間の距離と内角を計算する
        distances = [distance_two(pairss[i], pairss[i+1]) for i in range(len(pairss) - 1)]
        angles = [angle(pairss[i], pairss[i+1]) for i in range(len(pairss) - 1)]

        # angleを度数法に変換
        angles = [np.rad2deg(angle) for angle in angles]

        return distances, angles

    # aをx座標かつy座標でソートする
    # 始点が左上になるようにする
    tmp = sorted(tmp, key=lambda x: (x[1], x[2]))

    # 6つの座標
    x = []
    y = []
    answer_list = []

    for item in tmp:
        x.append(item[1])
        y.append(item[2])

    # 最短経路を求める
    min_perm = search_route(x, y)

    # 距離と内角を計算
    distance, angle = calc_distance_and_angle(min_perm)

    # min_permを元に、aを並び替える
    tmp = [tmp[i] for i in min_perm]

    # distanceとangleを組み合わせる
    for i in range(len(tmp)):
        answer_list.append([tmp[i][0] ,tmp[i][1],tmp[i][2],distance[i], angle[i]])

    return answer_list

# 傾きを計算
def katamuki(val1):
    deg_list = []
    val1 += val1[:3]
    for i in range(len(val1)-3):
        x0, y0 = val1[i][1], val1[i][2]
        x1, y1 = val1[i+1][1], val1[i+1][2]
        x2, y2 = val1[i+2][1], val1[i+2][2]

        vec1 = [x1-x0, y1-y0]
        vec2 = [x2-x0, y2-y0]

        vec1_norm = np.linalg.norm(vec1)
        vec2_norm = np.linalg.norm(vec2)

        cos = np.dot(vec1, vec2) / (vec1_norm * vec2_norm)
        rad = np.arccos(cos)
        deg = np.rad2deg(rad)
        deg_list.append(deg)
    
    # deg_listの平均
    deg_ave = sum(deg_list) / len(deg_list)

    return deg_ave

# tmpとtmp_x_plus1とin_aで、tmpを基準にした2直線のなす角度を求める
def angle_between(tmp, tmp_x_plus1, in_a):
    v1 = [tmp_x_plus1[1] - tmp[1], tmp_x_plus1[2] - tmp[2]]
    v2 = [in_a[1]-tmp[1], in_a[2]-tmp[2]]
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    len1 = math.sqrt(v1[0]**2 + v1[1]**2)
    len2 = math.sqrt(v2[0]**2 + v2[1]**2)
    angle = math.acos(dot/(len1*len2))
    angle = math.degrees(angle)
    
    # 0~180度の間の出力ではなく、-180~180度の間の出力にする
    if in_a[2] > tmp[2]:
        angle = 360-angle

    # UUIDとangleを返す
    return angle,in_a[3]

# 内角を求める
def calc_angle(v1, v2):
    v1_unit = v1 / np.linalg.norm(v1)
    v2_unit = v2 / np.linalg.norm(v2)
    angle = np.arccos(np.clip(np.dot(v1_unit, v2_unit), -1.0, 1.0))
    angle = math.degrees(angle)
    return angle

# 図形の描画に必要な計算を行う
def calc_dist_and_ang(a):
    in_a = a
    # aにUUIDを追加
    a_uuid = []

    for i in range(len(in_a)):
        a_uuid.append([in_a[i][0], in_a[i][1], in_a[i][2], in_a[i][3]])

    # aをx座標でソート
    in_a.sort(key=lambda x: [x[1],x[2]], reverse=True)

    result = []
    if(len(a_uuid) > 2):
        # すでに通った点を記録する
        passed_list = []
        for j in range(len(in_a)):
            tmp = in_a.pop(0)
            tmp_x_plus = copy.deepcopy(tmp)
            tmp_x_plus[1] = tmp_x_plus[1] + 1
            
            # tmp基準で計測しているため、tmpは通ったとみなす
            passed_list.append(tmp)
            
            # tmpからの角度を計算し、角度とUUIDを記録する
            angle_uuid = []
            for i in range(len(in_a)):
                angle,in_a_uuid = angle_between(tmp, tmp_x_plus, in_a[i])
                angle_uuid.append([angle, in_a_uuid])

            # 角度が小さい順にソートする
            angle_uuid.sort(key=lambda x: [x[0]], reverse=False)

            # angle_uuidの[1]の順番になるようにin_aをソートする
            for k in range(len(angle_uuid)):
                for l in range(len(in_a)):
                    if(angle_uuid[k][1] == in_a[l][3]):
                        tmp = in_a.pop(l)
                        in_a.insert(k, tmp)
                        break

        # 内角を計算するには、passed_listの最初にpassed_listの最後を追加、最後にpassed_listの最初を追加する必要がある
        passed_list.insert(0,passed_list[-1])
        passed_list.append(passed_list[1])

        # #6点の内角を計算するには、8点の座標が必要
        for i in range(1, len(passed_list)-1):
            v1 = np.array([passed_list[i-1][1]-passed_list[i][1], passed_list[i-1][2]-passed_list[i][2]])
            v2 = np.array([passed_list[i+1][1]-passed_list[i][1], passed_list[i+1][2]-passed_list[i][2]])
            # 内角を計算する
            angle = calc_angle(v1, v2)
            # 次の点までの距離を計算する
            dist = math.sqrt((passed_list[i+1][1]-passed_list[i][1])**2 + (passed_list[i+1][2]-passed_list[i][2])**2)
            result.append([passed_list[i][0],dist,angle,passed_list[i][3]])

    elif len(in_a) == 2:
        # 2点の場合
        x0, y0 = in_a[0][1], in_a[0][2]
        x1, y1 = in_a[1][1], in_a[1][2]
        n1 = np.array([x0, y0])
        n2 = np.array([x1, y1])
        nagasa = np.linalg.norm(n1-n2)
        result.append([in_a[0][0], nagasa, 0, in_a[0][3]])
        result.append([in_a[1][0], nagasa, 0, in_a[1][3]])

    elif len(in_a) == 1:
        # 1点の場合
        result.append([in_a[0][0], 0, 0, in_a[0][3]])

    return result, a_uuid

# 位置関係の検索結果
@dt.route("/playAngle/<id>/<path:filename>/<fps>")
def playMovieAngle(id, filename, fps):
    # データベースから検索
    predict_results_img = DetectedImages.query.filter_by(id=id).all()

    image_search = []
    object_img_name_list = []
    object_px_list = []
    video_search = []
    video_search_pre = []
    ruizi = []

    # 物体の位置関係保存用
    img_point_list = []
    result = []

    # 画像の縦と横のサイズを取得
    img_path = 'apps/images/predicted/'+id
    im = Image.open(img_path)
    w, h = im.size

    # 動画の縦と横のサイズを取得
    video_path = 'apps/movies/'+filename
    cap = cv2.VideoCapture(video_path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # 画像の検索結果を取得
    object_img_count = len(predict_results_img)
    for predict_img_result in predict_results_img:
        image_search.append([predict_img_result.detected_name, predict_img_result.detected_score, predict_img_result.detected_x_min, predict_img_result.detected_y_min, predict_img_result.detected_x_max, predict_img_result.detected_y_max])
        # UIDを追加
        uid = uuid.uuid4()
        img_point_list.append([predict_img_result.detected_name, (predict_img_result.detected_x_min + predict_img_result.detected_x_max) / 2 , (predict_img_result.detected_y_min + predict_img_result.detected_y_max) / 2,uid])
        object_img_name_list.append(predict_img_result.detected_name)

    image_search = sorted(image_search, key=lambda x: (x[0],x[2],x[4]))

    # ユーザーidの取得
    user_id = current_user.id

    # スコアの取得
    score = 0

    # 動画の検索結果を取得
    predict_results = db.session.query(IndexVideos).filter(IndexVideos.user_id == user_id).filter(IndexVideos.fps_number == fps).filter(IndexVideos.id == filename).all()
    for predict_video_result in predict_results:
        img_point_list_backup = copy.deepcopy(img_point_list)

        predict_details = db.session.query(DetectedLists).filter(DetectedLists.id == predict_video_result.id).filter(DetectedLists.fps_number == fps).all()
        # 中心座標のリスト
        video_point_result = []
        fps_number = 0
        # 要素数が一致する
        for predict_detail in predict_details:
            # 位置関係の計算のためのリスト
            fps_number = predict_detail.fps_number
            video_search.append([predict_detail.id, predict_detail.fps_number, predict_detail.detected_name, predict_detail.detected_score ,predict_detail.detected_x_min, predict_detail.detected_y_min, predict_detail.detected_x_max, predict_detail.detected_y_max])
            # UIDを追加
            uid = uuid.uuid4()
            video_point_result.append([predict_detail.detected_name, (predict_detail.detected_x_min + predict_detail.detected_x_max) / 2 , (predict_detail.detected_y_min + predict_detail.detected_y_max) / 2 , uid])
        
        # 中心座標から位置関係の計算
        predict_video_result_id = predict_video_result.id

        a = img_point_list_backup
        b = copy.deepcopy(video_point_result)

        a_a = copy.deepcopy(a)
        b_b = copy.deepcopy(b)

        result_a,a_uuid = calc_dist_and_ang(a)
        result_b,b_uuid = calc_dist_and_ang(b)

        aa = []
        for i in result_a:
            for j in a_a:
                if i[3] == j[3]:
                    aa.append(j)
        bb = []
        for i in result_b:
            for j in b_b:
                if i[3] == j[3]:
                    bb.append(j)

        # result_aの角度とresult_bの角度の差を求める
        angle_diff = []
        for i in range(len(result_a)):
            angle_diff.append([result_a[i][2] - result_b[i][2]])

        # aaとbbのバックアップ
        aa_backup = copy.deepcopy(aa)
        bb_backup = copy.deepcopy(bb)

        # aaのリストに画像のサイズを割って動画のサイズを掛ける
        for i in aa:
            i[1] = (i[1] ) * int(w)
            i[2] = (i[2] ) * int(h)
        # bbのリストに画像のサイズを割って動画のサイズを掛ける
        for i in bb:
            i[1] = (i[1] ) * int(w)
            i[2] = (i[2] ) * int(h)

        # 画像にプロット
        plot_img_path = img_plot(img_path, predict_video_result.id, fps_number,aa, bb)

        break

    starttime = fps
    total_frame = db.session.query(UserVideo).filter(UserVideo.video_path == filename).first()

    s = float(starttime) // float(total_frame.fps_info)
    ms = int(starttime) - int(s) * int(total_frame.fps_info)
    ms = float(ms)/int(total_frame.fps_info)
    s = s + ms
    s = round(s, 3)

    search_results_count = len(video_search)
    for i in range(0,search_results_count,object_img_count):
        video_search_pre.append(video_search[i:i+object_img_count])
    for j in range(len(video_search_pre)):
        object_video_name_list = []
        object_video_detail_list = []
        for i in range(len(video_search_pre[j])):
            object_video_name_list.append(video_search_pre[j][i][2])
            object_video_detail_list.append(video_search_pre[j][i][0:])
        object_video_detail_list = sorted(object_video_detail_list, key=lambda x:(x[2],x[4],x[6]))
        object_video_name_list = sorted(object_video_name_list, key=lambda x:x[0])

        match_count = 0
        for i in range(len(image_search)):
            if(str(image_search[i][0]) == str(object_video_name_list[i])):
                match_count += 1
            tmp = []
            tmp.append([object_video_detail_list[i][0],object_video_detail_list[i][1],object_video_detail_list[i][2],object_video_detail_list[i][3],object_video_detail_list[i][4],object_video_detail_list[i][5],object_video_detail_list[i][6],object_video_detail_list[i][7],round((1-(abs(image_search[i][2] - object_video_detail_list[i][4])+abs(image_search[i][3] - object_video_detail_list[i][5])+abs(image_search[i][4] - object_video_detail_list[i][6])+abs(image_search[i][5] - object_video_detail_list[i][7])))*100,5),round(abs(image_search[i][2] - object_video_detail_list[i][4]),6),round(abs(image_search[i][3] - object_video_detail_list[i][5]),6),round(abs(image_search[i][4] - object_video_detail_list[i][6]),6),round(abs(image_search[i][5] - object_video_detail_list[i][7]),6)])

            score += round((1-(abs(image_search[i][2] - object_video_detail_list[i][4])+abs(image_search[i][3] - object_video_detail_list[i][5])+abs(image_search[i][4] - object_video_detail_list[i][6])+abs(image_search[i][5] - object_video_detail_list[i][7])))*100,5)
            result.append(tmp)

            #類似シーンのみ検出した場合は映ってるもの全部をリストに入れる
            ruizi.append([object_video_detail_list[i][0],object_video_detail_list[i][1],object_video_detail_list[i][2],object_video_detail_list[i][3],object_video_detail_list[i][4],object_video_detail_list[i][5],object_video_detail_list[i][6],object_video_detail_list[i][7],round((1-(abs(image_search[i][2] - object_video_detail_list[i][4])+abs(image_search[i][3] - object_video_detail_list[i][5])+abs(image_search[i][4] - object_video_detail_list[i][6])+abs(image_search[i][5] - object_video_detail_list[i][7])))*100,5),round(abs(image_search[i][2] - object_video_detail_list[i][4]),6),round(abs(image_search[i][3] - object_video_detail_list[i][5]),6),round(abs(image_search[i][4] - object_video_detail_list[i][6]),6),round(abs(image_search[i][5] - object_video_detail_list[i][7]),6)])
    
    final_results = []

    if len(result) == 0:
        result.append(ruizi)

    for k in result:
        for i in k:
            video_title = db.session.query(UserVideo).filter(UserVideo.video_path == filename).first()
            final_results.append([video_title.video_title,i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[0],i[8],i[9],i[10],i[11],i[12]])
    
    # スコアの平均を計算
    score = round(score / len(result),2)

    # 詳細ページの動画のフレームをimgに保存する
    detail_page_frame = final_results[0]
    best_match_filename = str(uuid.uuid4())+'.png'
    detail_page_frame.append(best_match_filename)

    cap = cv2.VideoCapture("apps/movies/"+detail_page_frame[8])
    cap.set(cv2.CAP_PROP_POS_FRAMES, detail_page_frame[1])
    ret, frame = cap.read()
    plot_list = []
    for i in video_search:
        plot_list.append(i[2:8])

    for i in plot_list:
        random_rgb = random_rgb_vibrant()
        cv2.rectangle(frame, (int(i[2]*width), int(i[3]*height)), (int(i[4]*width), int(i[5]*height)), random_rgb, 5)
        cv2.putText(frame, str(i[0]+" "+str(round(float(str(i[1])),3))), (int(i[2]*width), int((i[3]*height)+(height*0.015))), cv2.FONT_HERSHEY_PLAIN, 2.5, random_rgb, 5, cv2.LINE_AA)

    cv2.imwrite("apps/images/temp/"+str(best_match_filename), frame)

    time.sleep(0.1)
    img_path = "apps/images/temp/"+str(best_match_filename)
    
    image_distance_angle_list_video = copy.deepcopy(aa_backup)
    video_distance_angle_list_video = copy.deepcopy(bb_backup)
    # image_distance_angle_listの[1]にwidth,[2]にheightをかける
    for i in image_distance_angle_list_video:
        i[1] = i[1] * width
        i[2] = i[2] * height
    for i in video_distance_angle_list_video:
        i[1] = i[1] * width
        i[2] = i[2] * height

    plot_video_path = img_plot(img_path, predict_video_result_id, fps_number,image_distance_angle_list_video, video_distance_angle_list_video)

    # final_resultsの[1]を100倍にして％表示にする
    for i in final_results:
        i[3] = round(i[3]*100,2)

    return render_template("detector/playAngle.html",filename=filename,starttime=s,plot_img_path=plot_img_path,img_path=id,match_info=final_results,detail_page_frame=detail_page_frame[14],plot_video_path=plot_video_path,score=score)

def random_rgb_vibrant():
    min_luminance = 50
    max_luminance = 205
    return (
        random.randint(min_luminance, max_luminance),
        random.randint(min_luminance, max_luminance),
        random.randint(min_luminance, max_luminance)
    )

# 画像のアップロード処理（位置関係）
@dt.route("/upload_img/", methods=["GET", "POST"])
# ログイン必須とする
@login_required
def upload_image():
    # UploadImageFormを利用してバリデーションをする
    form = UploadImageForm()
    if form.validate_on_submit():
        # アップロードされた画像ファイルを取得する
        file = form.image.data

        # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        # 画像を保存する
        image_path = Path(current_app.config["UPLOAD_IMG_FOLDER"], image_uuid_file_name)
        file.save(image_path)

        # DBに保存する
        user_image = UserImage(user_id=current_user.id, image_path=image_uuid_file_name)
        db.session.add(user_image)
        db.session.commit()

        # user_idを取得する
        user_id = current_user.id

        return redirect(url_for("detector.predict_img", msg=image_uuid_file_name, id=user_id, search_type='wide'))
    return render_template("detector/upload_img.html", form=form)

# 画像のアップロード処理（位置情報）
@dt.route("/upload_fast_img/", methods=["GET", "POST"])
# ログイン必須とする
@login_required
def upload_fast_image():
    # UploadImageFormを利用してバリデーションをする
    form = UploadImageForm()
    if form.validate_on_submit():
        # アップロードされた画像ファイルを取得する
        file = form.image.data

        # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        # 画像を保存する
        image_path = Path(current_app.config["UPLOAD_IMG_FOLDER"], image_uuid_file_name)
        file.save(image_path)

        # DBに保存する
        user_image = UserImage(user_id=current_user.id, image_path=image_uuid_file_name)
        db.session.add(user_image)
        db.session.commit()

        # user_idを取得する
        user_id = current_user.id

        return redirect(url_for("detector.predict_img", msg=image_uuid_file_name, id=user_id, search_type="fast"))
    return render_template("detector/upload_fast_img.html", form=form)

# 動画アップロード
@dt.route("/upload_movie/", methods=["GET", "POST"])
# ログイン必須とする
@login_required
def upload_movie():
    # UploadImageFormを利用してバリデーションをする
    form = UploadMovieForm()
    if form.validate_on_submit():
        # アップロードされた画像ファイルを取得する
        file = form.movie.data

        # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        # 動画を保存する
        video_path = Path(current_app.config["UPLOAD_MOVIE_FOLDER"], image_uuid_file_name)
        file.save(video_path)

        time.sleep(0.5)

        cap = cv2.VideoCapture(str(video_path))
        totalframecount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = int(cap.get(cv2.CAP_PROP_FPS))

        # DBに保存する
        user_image = UserVideo(user_id=current_user.id, total_frame=totalframecount,fps_info=video_fps,video_title=file.filename, video_path=image_uuid_file_name)
        db.session.add(user_image)
        db.session.commit()

        return redirect(url_for("detector.predict", msg=image_uuid_file_name))
    return render_template("detector/upload_movie.html", form=form)

# 動画をアップロードし、Detectron2のThreadを起動する
@dt.route("/upload_movie/detec/<string:msg>")
def predict(msg):
    global name_quere
    # detectron2を適応させる
    t = MyThread(target=MyThread, name=msg)
    t.start()
    jobs[msg] = t
    name_quere.append(msg)
    return redirect(url_for("detector.listview"))

# 検索結果を表示する
@dt.route("/search_result/<string:id>/<string:search_type>", methods=["GET", "POST"])
def search_result(id, search_type):
    t1 = time.time() # 時間計測開始
    search_count = 0

    # トランザクション回数をカウントする
    transaction_count = 0
    # トランザクション時間をカウントする
    transaction_time = 0


    if search_type == "wide":
        # データベースから検索
        t3 = time.time()
        predict_results_img = DetectedImages.query.filter_by(id=id).all()
        transaction_count += 1
        transaction_time += time.time() - t3
        image_search = []
        object_img_name_list = []
        video_search = []
        video_search_pre = []

        # 物体の位置関係保存用
        img_point_list = []
        result = []

        # 画像の縦と横のサイズを取得
        img_path = 'apps/images/predicted/'+id
        im = Image.open(img_path)
        h, w = im.size

        # 画像の検索結果を取得
        object_img_count = len(predict_results_img)
        for predict_img_result in predict_results_img:
            image_search.append([predict_img_result.detected_name, predict_img_result.detected_score, predict_img_result.detected_x_min, predict_img_result.detected_y_min, predict_img_result.detected_x_max, predict_img_result.detected_y_max])
            # UIDを追加
            uid = uuid.uuid4()
            img_point_list.append([predict_img_result.detected_name, (predict_img_result.detected_x_min + predict_img_result.detected_x_max) / 2 * h, (predict_img_result.detected_y_min + predict_img_result.detected_y_max) / 2 * w, uid])
            object_img_name_list.append(predict_img_result.detected_name)

        # 検出数がある場合
        if object_img_count > 0:
            image_search = sorted(image_search, key=lambda x: (x[0],x[2],x[4]))

            # ユーザーidの取得
            user_id = current_user.id

            # 図形の傾きをリスト
            angle_list = []

            # 画像雨の傾きリストをHTMLに送るためのやつ
            angle_rate = []


            t3 = time.time()
            # 動画の検索結果を取得
            predict_results = db.session.query(IndexVideos).filter(IndexVideos.user_id == user_id).all()
            transaction_count += 1
            transaction_time += time.time() - t3
            for predict_video_result in predict_results:
                search_count += 1
                img_point_list_backup = copy.deepcopy(img_point_list)
                # 検出数が一致するなら
                if(int(predict_video_result.detected_count) == int(object_img_count)):
                    t = time.time()
                    predict_details = db.session.query(DetectedLists).filter(DetectedLists.id == predict_video_result.id, DetectedLists.fps_number == predict_video_result.fps_number).all()
                    transaction_count += 1
                    transaction_time += time.time() - t
                    # 中心座標のリスト
                    video_point_result = []
                    fps_number = 0
                    # 要素数が一致する
                    for predict_detail in predict_details:
                        # 位置関係の計算のためのリスト
                        fps_number = predict_detail.fps_number
                        video_search.append([predict_detail.id, predict_detail.fps_number, predict_detail.detected_name, predict_detail.detected_score ,predict_detail.detected_x_min, predict_detail.detected_y_min, predict_detail.detected_x_max, predict_detail.detected_y_max])
                        # UIDを追加
                        uid = uuid.uuid4()
                        video_point_result.append([predict_detail.detected_name, (predict_detail.detected_x_min + predict_detail.detected_x_max) / 2 * h, (predict_detail.detected_y_min + predict_detail.detected_y_max) / 2 * w, uid])

                    # 中心座標から位置関係の計算
                    a = img_point_list_backup
                    b = copy.deepcopy(video_point_result)

                    a_a = copy.deepcopy(a)
                    b_b = copy.deepcopy(b)

                    result_a,a_uuid = calc_dist_and_ang(a)
                    result_b,b_uuid = calc_dist_and_ang(b)

                    aa = []
                    for i in result_a:
                        for j in a_a:
                            if i[3] == j[3]:
                                aa.append(j)
                    bb = []
                    for i in result_b:
                        for j in b_b:
                            if i[3] == j[3]:
                                bb.append(j)

                    if len(aa) == len(bb) and len(result_a) == len(result_b) and len(a_a) == len(b_b):
                        # result_aとresult_bの物体名が一致しているか確認
                        # 順番まで確認する
                        st, result_a, result_b = check_2_list(result_a, result_b)
                        if st == False:
                            continue

                        a_deg = []
                        b_deg = []

                        for i in result_a:
                            for j in a_uuid:
                                if i[3] == j[3]:
                                    a_deg.append([i[0], j[1], j[2], j[3]])

                        for i in result_b:
                            for j in b_uuid:
                                if i[3] == j[3]:
                                    b_deg.append([i[0], j[1], j[2], j[3]])

                        def_deg_list = []


                        # a_degとb_degのなす角を計算
                        for i in range(len(a_deg)-1):
                            vec1 = [a_deg[i+1][1]-a_deg[i][1], a_deg[i+1][2] - a_deg[i][2]]
                            vec2 = [b_deg[i+1][1]-b_deg[i][1], b_deg[i+1][2] - b_deg[i][2]]
                            absvec1 = np.linalg.norm(vec1)
                            absvec2 = np.linalg.norm(vec2)
                            inner = np.inner(vec1, vec2)
                            cross = np.cross(vec1, vec2)

                            # オブジェクトが複数のとき
                            if len(a_deg) >= 2:
                                cos_theta = inner/(absvec1*absvec2)
                                cos_theta = round(cos_theta, 10)
                                theta = math.degrees(math.acos(cos_theta))
                                theta = round(theta, 2)

                                def_deg_list.append(theta)
                            else:
                                def_deg_list.append(0)

                        angle_list.append([fps_number,np.mean([i for i in def_deg_list])])

                        gosa = []
                        hennohi_a = []
                        hennohi_b = []

                        # オブジェクトが複数のとき
                        if len(a_deg) >= 2:
                            for i in range(len(result_a)):
                                gosa.append([result_a[i][0], result_a[i][1] / result_b[i]
                                            [1], result_a[i][2] - result_b[i][2]])

                            for i in range(1,len(result_a)):
                                hennohi_a.append(abs((result_a[i][1] / result_a[0]
                                            [1])))
                            for i in range(1,len(result_a)):
                                hennohi_b.append(abs((result_b[i][1] / result_b[0]
                                            [1])))
                        else:
                            gosa.append([result_a[i][0], 0, 0])
                            hennohi_a.append(0)
                            hennohi_b.append(0)

                        # 図形の傾き
                        if np.mean([i for i in def_deg_list]) < 30:
                            if len(aa) == len(bb):
                                # id, fps, 図形の傾き、長さの平均、長さの分散、角度の平均、角度の分散
                                angle_rate.append([predict_video_result.id, fps_number, round(np.mean([i for i in def_deg_list]),4), round(np.mean([i[1] for i in gosa]),4),round(np.var([i[1] for i in gosa]),4),  round(abs(np.mean([i[2] for i in gosa])),4), round(np.var([i[2] for i in gosa]),4)])

            search_results_count = len(video_search)
            t = 0

            for i in range(0,search_results_count,object_img_count):
                video_search_pre.append(video_search[i:i+object_img_count])

            for j in range(len(video_search_pre)):
                object_video_name_list = []
                object_video_detail_list = []
                for i in range(len(video_search_pre[j])):
                    object_video_name_list.append(video_search_pre[j][i][2])
                    object_video_detail_list.append(video_search_pre[j][i][0:])

                object_video_detail_list = sorted(object_video_detail_list, key=lambda x:(x[2],x[4],x[6]))
                object_video_name_list = sorted(object_video_name_list, key=lambda x:x[0])
                match_count = 0
                for i in range(len(image_search)):
                    if(str(image_search[i][0]) == str(object_video_name_list[i])):
                        match_count += 1

                if(match_count == len(image_search)):
                    tmp = []
                    # ピクセルのズレが0.1以内のとき
                    for i in range(len(image_search)):
                        if((round(abs(image_search[i][2] - object_video_detail_list[i][4]),4)+round(abs(image_search[i][3] - object_video_detail_list[i][5]),4)+round(abs(image_search[i][4] - object_video_detail_list[i][6]),4)+round(abs(image_search[i][5] - object_video_detail_list[i][7]),4)) / 4 <= 0.1):
                            t += 1
                            tmp.append([object_video_detail_list[i][0],object_video_detail_list[i][1],round((1-(abs(image_search[i][2] - object_video_detail_list[i][4])+abs(image_search[i][3] - object_video_detail_list[i][5])+abs(image_search[i][4] - object_video_detail_list[i][6])+abs(image_search[i][5] - object_video_detail_list[i][7])))*100,5)])

                    if(len(tmp) == object_img_count):
                        tmp_sum = 0
                        for i in range(len(tmp)):
                            tmp_sum += tmp[i][2]
                        tmp_ave = round(tmp_sum / len(tmp),2)

                        result.append([tmp[0][0],tmp[0][1],tmp_ave])

            final_results = []

            for k in result:
                t4 = time.time()
                video_title = db.session.query(UserVideo).filter(UserVideo.video_path == k[0]).first()
                transaction_count += 1
                transaction_time += time.time() - t4
                final_results.append([video_title.video_title,k[1],k[2],k[0]])

            # final_results[2]をソートする
            final_results = sorted(final_results, key=lambda x: x[2], reverse=True)

            # angle_rateのvideo_idをvideo_titleに変換
            for k in angle_rate:
                t5 = time.time()
                video_title = db.session.query(UserVideo).filter(UserVideo.video_path == k[0]).first()
                transaction_count += 1
                transaction_time += time.time() - t5
                k.append(video_title.video_title)

            # ベストマッチの動画のフレームをimgに保存する
            if final_results:
                best_match = final_results[0]
                best_match_filename = str(uuid.uuid4())+'.png'
                best_match.append(best_match_filename)

                cap = cv2.VideoCapture("apps/movies/"+best_match[3])
                cap.set(cv2.CAP_PROP_POS_FRAMES, best_match[1])
                ret, frame = cap.read()
                cv2.imwrite("apps/images/predicted/"+str(best_match_filename), frame)
            else:
                best_match = "None"

        else:
            best_match = "None"
            final_results = []
            angle_rate = []

        t2 = time.time() # 時間計測終了
        search_time = round(t2-t1,3)

        return render_template("detector/search_result.html", id=id, best_match= best_match,image_search=image_search, video_search=final_results, slice_=object_img_count, angle_rate=angle_rate, slice_angle=len(angle_rate), search_time=search_time, search_count=search_count)

    else:
        # データベースから検索
        t6 = time.time()
        predict_results_img = DetectedImages.query.filter_by(id=id).all()
        transaction_count += 1
        transaction_time += time.time() - t6
        image_search = []
        object_img_name_list = []
        video_search = []
        video_search_pre = []
        result = []

        # 画像の検索結果を取得
        object_img_count = len(predict_results_img)
        for predict_img_result in predict_results_img:
            image_search.append([predict_img_result.detected_name, predict_img_result.detected_score, predict_img_result.detected_x_min, predict_img_result.detected_y_min, predict_img_result.detected_x_max, predict_img_result.detected_y_max])
            object_img_name_list.append(predict_img_result.detected_name)

        # 画像のオブジェクトがある場合
        if object_img_count > 0:
            image_search = sorted(image_search, key=lambda x: (x[0],x[2],x[4]))
            # ユーザーidの取得
            user_id = current_user.id

            # 動画の検索結果を取得
            t7 = time.time()
            predict_results = db.session.query(IndexVideos).filter(IndexVideos.user_id == user_id).all()
            transaction_count += 1
            transaction_time += time.time() - t7
            for predict_video_result in predict_results:
                search_count += 1
                # 検出数が一致するなら
                if(int(predict_video_result.detected_count) == int(object_img_count)):
                    t8 = time.time()
                    predict_details = db.session.query(DetectedLists).filter(DetectedLists.id == predict_video_result.id, DetectedLists.fps_number == predict_video_result.fps_number).all()
                    transaction_count += 1
                    transaction_time += time.time() - t8
                    # 要素数が一致する
                    for predict_detail in predict_details:
                        video_search.append([predict_detail.id, predict_detail.fps_number, predict_detail.detected_name, predict_detail.detected_score ,predict_detail.detected_x_min, predict_detail.detected_y_min, predict_detail.detected_x_max, predict_detail.detected_y_max])

            search_results_count = len(video_search)
            t = 0

            for i in range(0,search_results_count,object_img_count):
                video_search_pre.append(video_search[i:i+object_img_count])

            for j in range(len(video_search_pre)):
                object_video_name_list = []
                object_video_detail_list = []
                for i in range(len(video_search_pre[j])):
                    object_video_name_list.append(video_search_pre[j][i][2])
                    object_video_detail_list.append(video_search_pre[j][i][0:])
                object_video_detail_list = sorted(object_video_detail_list, key=lambda x:(x[2],x[4],x[6]))
                object_video_name_list = sorted(object_video_name_list, key=lambda x:x[0])

                match_count = 0
                for i in range(len(image_search)):
                    if(str(image_search[i][0]) == str(object_video_name_list[i])):
                        match_count += 1

                # オブジェクト名の一致数が画像と動画で一致したとき
                if(match_count == len(image_search)):
                    tmp = []

                    for i in range(len(image_search)):
                        if((round(abs(image_search[i][2] - object_video_detail_list[i][4]),4)+round(abs(image_search[i][3] - object_video_detail_list[i][5]),4)+round(abs(image_search[i][4] - object_video_detail_list[i][6]),4)+round(abs(image_search[i][5] - object_video_detail_list[i][7]),4)) / 4 <= 0.1):
                            t += 1
                            tmp.append([object_video_detail_list[i][0],object_video_detail_list[i][1],round((1-(abs(image_search[i][2] - object_video_detail_list[i][4])+abs(image_search[i][3] - object_video_detail_list[i][5])+abs(image_search[i][4] - object_video_detail_list[i][6])+abs(image_search[i][5] - object_video_detail_list[i][7])))*100,5)])

                    if(len(tmp) == object_img_count):
                        # 一致率の平均値を計算
                        tmp_sum = 0
                        for i in range(len(tmp)):
                            tmp_sum += tmp[i][2]
                        tmp_ave = round(tmp_sum / len(tmp),2)

                        result.append([tmp[0][0],tmp[0][1],tmp_ave])
            final_results = []

            for k in result:
                t9 = time.time()
                video_title = db.session.query(UserVideo).filter(UserVideo.video_path == k[0]).first()
                transaction_count += 1
                transaction_time += time.time() - t9
                final_results.append([video_title.video_title,k[1],k[2],k[0]])

            # final_results[2]をソートする
            final_results = sorted(final_results, key=lambda x: x[2], reverse=True)

            # ベストマッチの動画のフレームをimgに保存する
            if final_results:
                best_match = final_results[0]
                best_match_filename = str(uuid.uuid4())+'.png'
                best_match.append(best_match_filename)

                cap = cv2.VideoCapture("apps/movies/"+best_match[3])
                cap.set(cv2.CAP_PROP_POS_FRAMES, best_match[1])
                ret, frame = cap.read()
                cv2.imwrite("apps/images/predicted/"+str(best_match_filename), frame)
            else:
                best_match = "None"

        else:
            final_results = []
            best_match = "None"

        t2 = time.time() # 時間計測終了
        search_time = round(t2-t1,3)

        return render_template("detector/search_fast_result.html", id=id, best_match= best_match,image_search=image_search, video_search=final_results, slice_=object_img_count, search_time=search_time, search_count=search_count)

# 画像解析
@dt.route("/upload_img/detec/<string:msg>/<string:search_type>")
def predict_img(msg, search_type):
    mode = 0
    if "0" == msg[-1]:
        msg = msg[0:-1]
        mode = 1

    dbname = 'local.sqlite'
    # detectron2を適応させる
    input_img = 'apps/images/'+msg
    video = cv2.VideoCapture(input_img)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    msg = str(msg)
    user_id = current_user.id

    ret, frame = video.read()
    outputs = predictor(frame)
    result = []
    [result.extend((
        outputs["instances"][x].pred_classes.item(),
        outputs["instances"][x].scores.item(),
        outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][0],
        outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][1],
        outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][2],
        outputs["instances"][x].pred_boxes.tensor.cpu().numpy()[0][3]) 
    for x in range(len(outputs["instances"])))]
    df = pd.DataFrame(result, columns = ['class-id','score','x-min','y-min','x-max','y-max'])

    v = Visualizer(frame[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2.imwrite("apps/images/predicted/"+str(msg),out.get_image()[:, :, ::-1])

    # DBに保存
    dbname = "local.sqlite"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    for t in result:
        # 相対値
        relative_x_min = round(float(t[2])/ width ,4)
        relative_y_min = round(float(t[3])/ height ,4)
        relative_x_max = round(float(t[4])/ width ,4)
        relative_y_max = round(float(t[5])/ height ,4)
        center_x = round((float(t[2]) + float(t[4]))/2/width,4)
        center_y = round((float(t[3]) + float(t[5]))/2/height,4)
        if(mode == 0):
            cur.execute("INSERT INTO detected_images (user_id, id, detected_name, detected_score, detected_x_min, detected_y_min, detected_x_max, detected_y_max, center_x, center_y) VALUES (?,?,?,?,?,?,?,?,?,?)", [user_id, msg, classes_list[t[0]], round(float(t[1]),4), relative_x_min, relative_y_min, relative_x_max, relative_y_max, center_x, center_y])

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("detector.search_result", id=str(msg), search_type=search_type))

# 画像検索履歴
@dt.route("/img_history")
def img_history():
    im_history = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .filter(User.id == current_user.id)
        # deskで逆順
        .order_by(UserImage.id.desc())
        .all()
    )
    return render_template("detector/img_history.html", im_history=im_history)

# 画像を削除
@dt.route("/images/delete/<string:image_id>", methods=["POST"])
@login_required
def delete_movie(image_id):
    try:
        # user_imageテーブルからレコードを削除する
        video_path = db.session.query(UserVideo).filter(UserVideo.id == image_id).first()

        db.session.query(UserVideo).filter(UserVideo.id == image_id).delete()

        db.session.query(DetectedLists).filter(DetectedLists.id == video_path.video_path).delete()

        db.session.query(IndexVideos).filter(IndexVideos.id == video_path.video_path).delete()

        db.session.commit()
    except Exception as e:
        flash("画像削除処理でエラーが発生しました。")
        # エラーログ出力
        current_app.logger.error(e)
        db.session.rollback()
    return redirect(url_for("detector.index"))

@dt.route("/delete/img/all")
@login_required
def delete_all_img():
    db.session.query(UserImage).filter(UserImage.user_id == current_user.id).delete()
    db.session.commit()

    db.session.query(DetectedImages).filter(DetectedImages.user_id == current_user.id).delete()
    db.session.commit()

    im_history = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        # deskで逆順
        .order_by(UserImage.id.desc())
        .all()
    )

    return render_template("detector/img_history.html", im_history=im_history)