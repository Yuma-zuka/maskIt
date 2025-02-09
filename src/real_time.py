import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk, ImageOps
import glob
import os
import time
import guihome
from processing_enum import Processing

# RealTimeRecの起動用のクラス
class BootRealTime():
    def __init__(self):
        pass
    def boot(self): # RealTimeRecの起動
        root = tk.Tk()
        app = RealTimeRec(master = root)
        app.mainloop()

# リアルタイムで顔認識、顔認証、処理を実行するクラス
class RealTimeRec(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master) # スーパークラスの継承
        self.pack() # frameの組み込み

        # FaceDetectorYNの生成 顔を検出する器械の定義
        self.FACE_DETECTOR = cv2.FaceDetectorYN_create("onnx_file/yunet_n_640_640.onnx", "", (320, 320))
        # FaceRecognizerの生成 顔を認識するためのサンプル
        self.FACE_RECOGNIZER = cv2.FaceRecognizerSF_create("onnx_file/face_recognition_sface_2021dec.onnx", "")
        # 顔認証の一致率の定義>>この値を超えると一致とみなす
        self.COSINE_THRESHOLD = 0.363
        # 処理済の画像を保存するディレクトリのパス
        self.COMPLETE_IMAGE_DIRECTRY_PATH = "completeImage"
        # 特徴を抽出してできたデータファイルを保存するディレクトリのパス
        self.FEATURES_DIRECTRY_PATH = "features"

        # フィルター用の画像を読み込み
        self.GLASSES_IMAGE = cv2.imread("cover/glasses.png")
        self.GRASS_CROWN_IMAGE = cv2.imread("cover/grass_crown.png")
        self.HEART_IMAGE = cv2.imread("cover/heart.png")
        self.ROUND_IMAGE = cv2.imread("cover/round.png")
        self.ALL_FILTER_COUNT = max([e.value for e in Processing]) # フィルターの種類の最大値を定数として定義する
        self.deco = Processing.MOSAIC # 初期フィルターをモザイクに設定

        self.master.title("real time") # ウィンドウタイトル
        self.master.geometry("1440x847+0+0") # ウィンドウサイズ(幅x高さ)
        self.master.resizable(False, False) # ウィンドウのサイズを変化できないように設定

        # 特徴を読み込む
        self.dictionary = [] # 登録済データを入れる変数
        self.files = glob.glob(os.path.join(self.FEATURES_DIRECTRY_PATH, "*.npy")) # 登録済データファイルの取得
        # データファイルの数だけ読み取って変数に挿入
        for file in self.files:
            feature = np.load(file)
            user_id = os.path.splitext(os.path.basename(file))[0] # face001.npy -> face001
            self.dictionary.append((user_id, feature))

                # 戻るボタンの画像を取得
        self.BACK_BUTTON_IMAGE = tk.PhotoImage(file="material/back.png")

        # ウィンドウの詳細
        self.canvas = tk.Canvas(self.master, width=1080, height=600)# Canvasの作成
        self.canvas.place(x=720, y=320, anchor="center") # Canvasを配置
        back_button = tk.Canvas(self.master, width=180, height=70) # ボタンのキャンバスを作成
        back_button.place(x=120, y=790, anchor="center") # "戻る"ボタンの配置
        back_button.create_image(0, 0, image=self.BACK_BUTTON_IMAGE, anchor="nw") # イメージの貼り付け
        back_label = tk.Label(back_button, text="戻る", bg="#bcbabe", fg="#000000", font=("Helvetica", 54)) # 戻るボタンのラベルの設定
        back_label.place(x=70, y=3) # "戻る"ボタンのラベルの配置
        back_button.bind("<Button-1>", self.back_home) # back_homeメソッドの呼び出し
        back_label.bind("<Button-1>", self.back_home) # back_homeメソッドの呼び出し
        filter_change_button = tk.Button(self.master, text="フィルター変更", bg="#bbdceb", fg="#000000", command=self.change_filter, font=("Helvetica", 50)) # フィルターを変更するボタンの設定 change_filterメソッドの呼び出し
        filter_change_button.place(x=450, y=700, anchor="center") # "フィルター変更"ボタンの配置
        self.filter_label = tk.Label(self.master, text="MOSAIC", font=("Helvetica", 50)) # フィルター名を表示するラベルの設定
        self.filter_label.place(x=450, y=790, anchor="center") # ラベルの配置
        self.bool_check = tk.BooleanVar() # チェックボックスのオンオフのためにbooleanの宣言
        self.bool_check.set(True) # 初期状態をTrueにする
        check_box = tk.Checkbutton(self.master, text="顔認証", variable=self.bool_check, bg="#bbdceb", fg="#000000", font=("Helvetica", 50)) # 顔認証のチェックボタンの設定 
        check_box.place(x=860, y=700, anchor="center") # 顔認証チェックボタンの配置
        photo_button = tk.Button(self.master, text="写真を撮る", bg="#f0cb45", fg="#ffffff", command=self.take_picture, font=("Helvetica", 50)) # 写真を撮るボタンの設定 take_pictureメソッドの呼び出し
        photo_button.place(x=1280, y=790, anchor="center") # フォトボタンの配置
        self.log_label = tk.Label(self.master, text="写真を保存しました", font=("Helvetica", 50)) # 保存を表示するラベルの設定
        self.log_label.place_forget() # 表示しないようにする

        # カメラをオープンする
        self.capture = cv2.VideoCapture(0)
        # 画面に表示する
        self.disp_image() # disp_imageメソッドの呼び出し

    # 画像を表示するメソッド
    def disp_image(self):
        # '''画像をCanvasに表示する'''

        # フレーム画像の取得
        ret, frame = self.capture.read()

        # 画像サイズを設定する
        self.FACE_DETECTOR.setInputSize((frame.shape[1], frame.shape[0]))
        frame = cv2.flip(frame, 1)
        # 顔検出
        _, faces = self.FACE_DETECTOR.detect(frame)
        faces = faces if faces is not None else [] # 検出できなかったらNoneを定義する

        for face in faces: # 検出した顔を一つずつ実行
            if self.bool_check.get(): # 顔認証がオンになっていたら
                # 顔の特徴を抽出
                aligned_face=self.FACE_RECOGNIZER.alignCrop(frame, face)
                feature=self.FACE_RECOGNIZER.feature(aligned_face)
                # 辞書とマッチングする
                result = self.match(self.FACE_RECOGNIZER, feature, self.dictionary)
            else:
                result = False
            
            (x, y, w, h, *_) = map(int, face) # ③ 検出値はfloat
            # 切り取るサイズの調整
            if x + w > 1280:
                w = 1280 - x
            if y + h > 720:
                h = 720 - y

            # フィルターをかける
            if (result != True):
                if self.deco == Processing.MOSAIC: # モザイク
                    frame = self.mosaic_area(frame, x, y, w, h)
                else: # 画像を上に被せる
                    match self.deco:
                        case Processing.GLASSES:
                            self.deco_image = self.GLASSES_IMAGE
                        case Processing.GRASS_CROWN:
                            self.deco_image = self.GRASS_CROWN_IMAGE
                        case Processing.HEART:
                            self.deco_image = self.HEART_IMAGE
                        case Processing.ROUND:
                            self.deco_image = self.ROUND_IMAGE
                    self.put_pro_image(frame, x, y, w, h)

        # 顔が見切れてると検出されないため、端を切り落とす
        self.picture = frame[54:666, 96:1184]

        # ウィンドウに表示するための準備
        # BGR→RGB変換
        cv_image = cv2.cvtColor(self.picture, cv2.COLOR_BGR2RGB)
        # NumPyのndarrayからPillowのImageへ変換
        pil_image = Image.fromarray(cv_image)
        # キャンバスのサイズを取得
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        # 画像のアスペクト比（縦横比）を崩さずに指定したサイズ（キャンバスのサイズ）全体に画像をリサイズする
        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height))
        # PIL.ImageからPhotoImageへ変換する
        self.photo_image = ImageTk.PhotoImage(image=pil_image, master=self.master)
        # 画像の描画
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width / 2, canvas_height / 2, image=self.photo_image)  # 表示画像データ
        
        try: # 保存した後に表示するラベルを一定時間過ぎたら非表示にする
            self.pop_count += 1
            if self.pop_count == 15:
                self.log_label.place_forget()
                self.pop_count = None
        except:
            pass

        # disp_image()を10msec後に実行する
        self.after(10, self.disp_image)


    # 顔認証のメソッド
    def match(self, recognizer, feature1, dic):
        # データの数だけ繰り返す
        for element in dic:
            _, feature2 = element # 登録してある特徴データとユーザー名を取得
            # FaceRecognizerSF でマッチする
            score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE) # 2つのデータの近似率を計算 3つ目の引数は計算方法
            if score > self.COSINE_THRESHOLD: # 一定の一致率を超えたら認証成功を返す
                return True
        return False # 超えなかったら認証失敗を返す
    

    # モザイクをかけるために範囲を指定して上書きするメソッド
    def mosaic_area(self, src, x, y, width, height):
        dst = src.copy()
        dst[y:y + height, x:x + width] = self.mosaic(dst[y:y + height, x:x + width]) # mosaicメソッドの呼び出し
        return dst # 顔の部分にモザイクをかけた画像を返す
    # モザイクをかけるメソッド
    def mosaic(self, src, ratio=0.1):
        small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST) # 小さくする 補間でノイズ除去
        return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST) # 元のサイズに戻して返す 補間でノイズ除去

    # ホーム画面に戻るメソッド
    def back_home(self):
        self.master.destroy()
        self.capture.release()
        guihome.HomeWindow()

    # 写真を撮って保存するメソッド
    def take_picture(self):
        try:
            current_time = time.localtime() # 現在の年月日時分秒を取得する
            formatted_datetime = time.strftime("%Y-%m-%d %H-%M-%S", current_time) # フォーマットに年月日時分秒を挿入する
            picture_file_name = formatted_datetime + ".png" # ファイル名の作成
            picture_path = os.path.join(self.COMPLETE_IMAGE_DIRECTRY_PATH, picture_file_name) # ファイル名からパスを作成する
            cv2.imwrite(picture_path, self.picture) # 画像を保存
            # 写真を撮ったと表示する
            self.log_label.place(x=1190, y=700, anchor="center")
            self.pop_count = 0
        except:
            pass
    
    # フィルターを変更するメソッド
    def change_filter(self):
        self.filter_count = self.deco.value + 1 # フィルターを次のフィルターに変えるために変数を更新
        if self.filter_count > self.ALL_FILTER_COUNT: # フィルターの上限を超えたら
            self.filter_count = 0 # 最初のフィルター番号に戻す
        self.deco = Processing(self.filter_count) # フィルターを変更する
        self.filter_label["text"] = self.deco.name # 変更に応じてフィルター名の表示を変更する

    # フィルター画像を透過して被せるメソッド
    def put_pro_image(self, frame, x, y, w, h): # 元画像と顔の位置と幅と高さの引き数
        try:
            deco_cover_image = cv2.resize(self.deco_image, (w,h)) # フィルター画像のサイズを顔に合わせる
            TRANSPARENCE = (255,255,255) # 透過させるための定数の定義
            frame[y:y+h, x:x+w] = np.where(deco_cover_image==TRANSPARENCE, frame[y:y+h, x:x+w], deco_cover_image) # フィルター画像を透過させて被せる
        except:
            pass


if __name__ == "__main__":
    main = BootRealTime()
    main.boot()