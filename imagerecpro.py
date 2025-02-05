import numpy as np
import cv2
import glob
import os
import tkinter as tk
import guihome
import choice_rec_file
from work_enum import Work

# 写真を加工するクラス
class ImageRecPro:
    # クラスファイルが作成されたときに定義するもの
    def __init__(self):
        # FaceDetectorYNの生成 顔を検出する器械の定義
        self.FACE_DETECTOR = cv2.FaceDetectorYN_create("/Users/yuma/opencv/yunet_n_640_640.onnx", "", (320, 320))
        # FaceRecognizerの生成 顔を認識するためのサンプル
        self.FACE_RECOGNIZER = cv2.FaceRecognizerSF_create("/Users/yuma/opencv/face_recognition_sface_2021dec.onnx", "")
        # 表示するための画像を一時的に保存するパス
        self.temporary_save_path = "/Users/yuma/opencv/recproApplication/completeImage/temporary_save_image.png"
        # 顔認証の一致率の定義>>この値を超えると一致とみなす
        self.COSINE_THRESHOLD = 0.363

        self.dictionary = [] # 登録済データを入れる変数
        self.files = glob.glob(os.path.join("/Users/yuma/opencv/recproApplication/features", "*.npy")) # 登録済データファイルの取得
        # データファイルの数だけ読み取って変数に挿入
        for file in self.files:
            feature = np.load(file)
            user_id = os.path.splitext(os.path.basename(file))[0] # face001.npy -> face001
            self.dictionary.append((user_id, feature))

    # 写真を加工するメソッド
    def rec_image(self, rec_file):
        self.imagePath = rec_file # 加工する写真
        self.imageName = "processed" + str(os.path.splitext(os.path.basename(self.imagePath))[0]) + ".png" # 出力する時のファイル名
        self.savePath = os.path.join('/Users/yuma/opencv/recproApplication/completeImage', self.imageName) # 出力する時のパス

        try:
            # 画像の読み込み
            self.image = cv2.imread(self.imagePath)
            # 画像サイズを設定する
            self.FACE_DETECTOR.setInputSize((self.image.shape[1], self.image.shape[0]))
            # 顔検出
            _, self.faces = self.FACE_DETECTOR.detect(self.image)
            self.faces = self.faces if self.faces is not None else [] # 検出できなかったらNoneを定義する
            
            for face in self.faces: # 検出した顔を一つずつ実行
                # 顔の特徴を抽出
                aligned_face=self.FACE_RECOGNIZER.alignCrop(self.image, face)
                feature=self.FACE_RECOGNIZER.feature(aligned_face)
                # 辞書とマッチングする
                result = self.match(self.FACE_RECOGNIZER, feature, self.dictionary) # matchメソッドの呼び出し
                # 顔の座標と幅、高さを取得
                (x, y, w, h, *_) = map(int, face)
                # 認証できなかった人にモザイクをかける
                if result == False:
                    self.image = self.mosaic_area(self.image, x, y, w, h) # mosaic_areaメソッドの呼び出し
            
            # 画像の保存
            cv2.imwrite(self.savePath, self.image)
            # 保存する画像を表示するために表示サイズに加工する
            self.show_image = self.resize_image(self.image) # resize_imageメソッドの呼び出し
            # 画像を表示するために一時的に書き出す
            cv2.imwrite(self.temporary_save_path, self.show_image)
            # 画像の表示
            self.make_result_window(None) # make_result_windowメソッドの呼び出し
        except:
            self.make_result_window("画像の読み取りに失敗しました") # make_result_windowメソッドの呼び出し
    
    # 顔認証のメソッド
    def match(self, recognizer, feature1, dic):
        # データの数だけ繰り返す
        for element in dic:
            _, feature2 = element # 登録してある特徴データとユーザー名を取得
            # FaceRecognizerSF でマッチする
            score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE) # 2つのデータの近似率を計算 3つ目の引数は計算方法
            if score > self.COSINE_THRESHOLD: # 一定の一致率を超えたら認証成功とユーザー名と近似率を返す
                return True
        return False # 超えなかったら認証失敗とunknownと近似率0.0を返す
    
    # モザイクをかけるために範囲を指定して上書きするメソッド
    def mosaic_area(self, src, x, y, width, height):
        dst = src.copy()
        dst[y:y + height, x:x + width] = self.mosaic(dst[y:y + height, x:x + width]) # mosaicメソッドの呼び出し
        return dst # 顔の部分にモザイクをかけた画像を返す
    # モザイクをかけるメソッド
    def mosaic(self, src, ratio=0.1):
        small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST) # 小さくする 補間でノイズ除去
        return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST) # 元のサイズに戻して返す 補間でノイズ除去
    
    # 画像サイズをちょうど良くする
    def resize_image(self, subject_image):
        hei, wid, _ = subject_image.shape
        if wid > 1200:
            magnification = 1200 / wid
            subject_image = cv2.resize(subject_image, None, fx=magnification, fy=magnification, interpolation=cv2.INTER_NEAREST)
            hei, wid, _ = subject_image.shape
        if hei > 700:
            magnification = 700 / hei
            subject_image = cv2.resize(subject_image, None, fx=magnification, fy=magnification, interpolation=cv2.INTER_NEAREST)
        return subject_image # ちょうどよくした画像を返す
    
    # 結果を画面に表示するメソッド
    def make_result_window(self, error):
        # ウィンドウの作成
        self.root = tk.Tk()
        self.root.title("recognize image") # ウィンドウの名前
        self.root.geometry("1440x848+0+0") # ウィンドウサイズと位置
        self.root.resizable(False, False) # ウィンドウのサイズを変化できないように設定
        back_button = tk.Button(self.root, text="戻る", command=self.back_home, font=("Helvetica", 50)) # ホームに戻るボタンの設定 back_homeメソッドの呼び出し
        back_button.place(x=30,y=740) # "戻る"ボタンの配置
        retry = tk.Button(self.root, text="続けて編集する", command=self.re_rec_image, font=("Helvetica", 50)) # 続けて編集するボタンの設定 re_rec_imageメソッドの呼び出し
        retry.place(x=1020,y=740) # "続けて編集する"ボタンの配置
        # 結果表示
        if error == None: # errorがなかった時 画像表示
            image_tk  = tk.PhotoImage(file=self.temporary_save_path, master=self.root) # 表示する画像の取得
            canvas = tk.Canvas(self.root, width=self.show_image.shape[1], height=self.show_image.shape[0]) # Canvas作成
            canvas.place(x=720, y=380, anchor='center') # Canvas配置
            canvas.create_image(0, 0, image=image_tk, anchor='nw') # ImageTk 画像配置
            os.remove(self.temporary_save_path) # 一時的に保存していた画像の削除
        else: # errorがあった時 エラー文の表示
            error_message = tk.Label(self.root, text=error, font=("Helvetica", 60)) # エラーメッセージのラベル設定
            error_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # エラーメッセージの配置
        self.root.mainloop() # ボタンの実行を待機
    # ホーム画面に戻るメソッド
    def back_home(self):
        self.root.destroy()
        guihome.Homewindow()
    # 再び写真を処理するメソッド
    def re_rec_image(self):
        self.root.destroy()
        choice_rec_file.Dictionary(Work.IMAGE)

if __name__ == "__main__":
    test = choice_rec_file.Dictionary(Work.IMAGE)