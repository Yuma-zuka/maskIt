import numpy as np
import cv2
import tkinter as tk
import os
import glob
import guihome
import choice_rec_file
from work_enum import Work

class Register:
    def __init__(self):
        # FaceDetectorYNの生成 顔を検出する器械の定義
        self.FACE_DETECTOR = cv2.FaceDetectorYN_create("onnx_file/yunet_n_640_640.onnx", "", (320, 320))
        # FaceRecognizerの生成 顔を認識するためのサンプル
        self.FACE_RECOGNIZER = cv2.FaceRecognizerSF_create("onnx_file/face_recognition_sface_2021dec.onnx", "")
        # 表示するための画像を一時的に保存するパス
        self.TEMPORARY_SAVE_PATH = "features/temporary_save_image.png"
        # 特徴を抽出してできたデータファイルを保存するパス
        self.FEATURES_DIRECTRY_PATH = "features"
        # 顔認証の一致率の定義>>この値を超えると一致とみなす
        self.COSINE_THRESHOLD = 0.363

    # 画像のから顔を取得して特徴を抽出。そして、それを記録するメソッド
    def rec_save(self, image_path):
        try:
            self.rec_image = cv2.imread(image_path) # 画像を読み込む
            height, width, _ = self.rec_image.shape # 画像サイズの取得
            self.FACE_DETECTOR.setInputSize((width, height)) # 画像サイズの設定
            try:
                # 顔を検出する
                _, faces = self.FACE_DETECTOR.detect(self.rec_image)
                menbers = 0 # 何人目の処理かをカウントするために変数を作成
                # 顔の数だけ繰り返す
                for face in faces:
                    # 顔を切り抜き特徴を抽出する
                    aligned_face = self.FACE_RECOGNIZER.alignCrop(self.rec_image, face)
                    # 特徴量の抽出
                    face_feature = self.FACE_RECOGNIZER.feature(aligned_face)
                    # 画像に含まれている顔の数が複数あればファイル名に数字をつける
                    # outputするファイル名を取得するファイル名から取ってくる
                    menbers += 1
                    if len(faces) > 1:
                        save_file_name = str(os.path.splitext(os.path.basename(image_path))[0]) + f"{menbers:d}.npy"
                    elif len(faces) == 1:
                        save_file_name = str(os.path.splitext(os.path.basename(image_path))[0]) + ".npy"
                    # ファイル名から、保存するパスを作成
                    save_path = os.path.join(self.FEATURES_DIRECTRY_PATH, save_file_name)
                    # 特徴量を記述したファイルを保存
                    np.save(save_path, face_feature)

                    dictionary = [] # 登録済データを入れる変数
                    self.FEATURES_FILES = glob.glob(os.path.join(self.FEATURES_DIRECTRY_PATH, "*.npy")) # 登録済データファイルの取得
                    # データファイルの数だけ読み取って変数に挿入
                    for file in self.FEATURES_FILES:
                        feature = np.load(file)
                        user_id = os.path.splitext(os.path.basename(file))[0] # face001.npy -> face001
                        dictionary.append((user_id, feature))

                    # 辞書とマッチングする
                    result, user = self.match(self.FACE_RECOGNIZER, face_feature, dictionary)

                    # バウンディングボックスと登録したファイル名の表示
                    box = list(map(int, face[:4])) # 四角で囲む座標
                    color = (0, 0, 255) # 色の指定
                    thickness = 2 # 線の厚さ
                    cv2.rectangle(self.rec_image, box, color, thickness, cv2.LINE_AA) # 四角の書き込み
                    id = user if result else ("unknown") # idをTrueならuserに、それ以外なら"unknown"にする
                    position = (box[0], box[1] - 10) # idの表示する座標
                    font = cv2.FONT_HERSHEY_SIMPLEX # フォントの指定
                    scale = 0.6 # 文字サイズの倍率
                    cv2.putText(self.rec_image, id, position, font, scale, color, thickness, cv2.LINE_AA) # 文字の書き込み
                    if menbers == len(faces):
                        self.rec_image = self.resize_image(self.rec_image) # resize_imageメソッドの呼び出し
                        self.make_result_window(None) # make_result_windowメソッドの呼び出し
            except:
                self.make_result_window("顔を検出できませんでした") # make_result_windowメソッドの呼び出し
        except:
            self.make_result_window("画像の読み取りに失敗しました")# make_result_windowメソッドの呼び出し

    # 顔認証のメソッド
    def match(self, recognizer, feature1, dic):
        hold_userid = "" # 保持しているユーザーidの定義
        hold_score = 0 # 保持しているユーザースコアの定義
        matching = False # 認証できたか否かの定義
        # データの数だけ繰り返す
        for element in dic:
            userid, feature2 = element # 登録してある特徴データとユーザー名を取得
            # FaceRecognizerSF でマッチする
            score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE) # 2つのデータの近似率を計算 3つ目の引数は計算方法
            # 一定の一致率を超えたら
            if score > self.COSINE_THRESHOLD:
                matching = True # 認証できたと定義する
                # 以前のスコアより高かったら保持しているスコアとユーザーを上書き
                if hold_score < score:
                    hold_score = score
                    hold_userid = userid
        # ループの最後まで行ったら実行
        if matching: # 認証できたか、それはどのユーザーかを返す
            return matching, (hold_userid) 
        else:
            return matching, ('unknown')
        
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
    
    def make_result_window(self,error):
        # ウィンドウの作成
        self.root = tk.Tk()
        self.root.title("register")  # ウィンドウ名
        self.root.geometry("1440x847+0+0") # ウィンドウサイズ
        self.root.configure(bg="#f1f1f2") # ウィンドウの背景色
        self.root.resizable(False, False) # ウィンドウのサイズを変化できないように設定

        # 戻るボタンの画像を取得
        self.BACK_BUTTON_IMAGE = tk.PhotoImage(file="material/back.png")
        # 続けて登録するボタンの画像を取得
        self.RETRY_BUTTON_IMAGE = tk.PhotoImage(file="material/next.png")
        
        back_button = tk.Canvas(self.root, width=180, height=70) # ボタンのキャンバスを作成
        back_button.place(x=120, y=790, anchor="center") # "戻る"ボタンの配置
        back_button.create_image(0, 0, image=self.BACK_BUTTON_IMAGE, anchor="nw") # イメージの貼り付け
        back_label = tk.Label(back_button, text="戻る", bg="#bcbabe", fg="#000000", font=("Helvetica", 54)) # 戻るボタンのラベルの設定
        back_label.place(x=70, y=3) # "戻る"ボタンのラベルの配置
        back_button.bind("<Button-1>", self.back_home) # back_homeメソッドの呼び出し
        back_label.bind("<Button-1>", self.back_home) # back_homeメソッドの呼び出し
        retry_button = tk.Canvas(self.root, width=450, height=70) # ボタンのキャンバスを作成
        retry_button.place(x=1180, y=790, anchor="center") # "続けて登録する"ボタンの配置
        retry_button.create_image(0, 0, image=self.RETRY_BUTTON_IMAGE, anchor="nw") # イメージの貼り付け
        retry_label = tk.Label(retry_button, text="続けて編集する", bg="#bbdceb", fg="#536f72", font=("Helvetica", 54)) # 続けて登録するボタンのラベルの設定
        retry_label.place(x=70, y=3) # "続けて登録する"ボタンのラベルの配置
        retry_button.bind("<Button-1>", self.re_regist) # re_registメソッドの呼び出し
        retry_label.bind("<Button-1>", self.re_regist) # re_registメソッドの呼び出し

        # 結果表示
        if error == None: # 検出できた時に検出した顔を枠で取って、名前をつけて表示する
            cv2.imwrite(self.TEMPORARY_SAVE_PATH, self.rec_image) # 一時的に書き出す
            image_tk  = tk.PhotoImage(file=self.TEMPORARY_SAVE_PATH, master=self.root) # 書き出したファイルをtkinterで読み込む
            canvas = tk.Canvas(self.root, width=self.rec_image.shape[1], height=self.rec_image.shape[0]) # Canvas作成
            canvas.place(x=720, y=380, anchor='center') # Canvas配置
            canvas.create_image(0, 0, image=image_tk, anchor='nw') # ImageTk 画像配置
            os.remove(self.TEMPORARY_SAVE_PATH) # 一時的に書き出したファイルを削除 
        else: # errorがあった時 エラー文の表示
            error_message = tk.Label(self.root, text=error, font=("Helvetica", 60)) # エラーメッセージのラベル設定
            error_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # エラーメッセージの配置
        self.root.mainloop() # ボタンの実行を待機
    # ホーム画面に戻るメソッド
    def back_home(self, _):
        self.root.destroy()
        guihome.HomeWindow()
    # 再び登録を続けるメソッド
    def re_regist(self, _):
        self.root.destroy()
        choice_rec_file.Choices(Work.REGISTER)

if __name__ == "__main__":
    save_data = choice_rec_file.Choices(Work.REGISTER)