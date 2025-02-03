import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk, ImageOps  # 画像データ用
import glob
import os
import time
import guihome

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()

        self.FACE_DETECTOR = cv2.FaceDetectorYN_create("/Users/yuma/opencv/yunet_n_640_640.onnx", "", (320, 320))
        self.FACE_RECOGNIZER = cv2.FaceRecognizerSF_create("/Users/yuma/opencv/face_recognition_sface_2021dec.onnx", "")
        self.COSINE_THRESHOLD = 0.363
        self.NORML2_THRESHOLD = 1.128

        self.master.title("real time")       # ウィンドウタイトル
        self.master.geometry("1440x847+0+0")     # ウィンドウサイズ(幅x高さ)

        # 特徴を読み込む
        self.dictionary = []
        self.files = glob.glob(os.path.join("/Users/yuma/opencv/recproApplication/features", "*.npy"))
        for file in self.files:
            feature = np.load(file)
            user_id = os.path.splitext(os.path.basename(file))[0] # face001.npy -> face001
            self.dictionary.append((user_id, feature))

        # Canvasの作成
        self.canvas = tk.Canvas(self.master, width=1080, height=600)
        # Canvasを配置
        self.canvas.place(x=720, y=320, anchor="center")

        back_button = tk.Button(self.master, text="戻る", command=self.back_home, font=("Helvetica", 50))
        back_button.place(x=120,y=740, anchor="center")

        photo_button = tk.Button(self.master, text="写真を撮る", command=self.take_picture, font=("Helvetica", 50))
        photo_button.place(x=1240, y=740, anchor="center")

        # カメラをオープンする
        self.capture = cv2.VideoCapture(0)

        self.disp_image()

    def disp_image(self):
        # '''画像をCanvasに表示する'''

        # フレーム画像の取得
        ret, frame = self.capture.read()

        # 画像サイズを設定する
        self.FACE_DETECTOR.setInputSize((frame.shape[1], frame.shape[0]))
        frame = cv2.flip(frame, 1)
        # 顔検出
        _, faces = self.FACE_DETECTOR.detect(frame)
        faces = faces if faces is not None else []

        _idx=0
        for face in faces:
            aligned_face=self.FACE_RECOGNIZER.alignCrop(frame, face)
            _idx+=1
            feature=self.FACE_RECOGNIZER.feature(aligned_face)
            # 辞書とマッチングする
            result, user = self.match(self.FACE_RECOGNIZER, feature, self.dictionary)
            (x, y, w, h, *_) = map(int, face)                   # ③ 検出値はfloat
            if (result == False):
                frame = self.mosaic_area(frame, x, y, w, h)
        self.picture = frame[54:666, 96:1184]
    
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
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        # 画像の描画
        self.canvas.delete("all")
        self.canvas.create_image(
                canvas_width / 2,       # 画像表示位置(Canvasの中心)
                canvas_height / 2,
                image=self.photo_image  # 表示画像データ
                )

        # disp_image()を10msec後に実行する
        self.after(10, self.disp_image)

    def match(self, recognizer, feature1, dic):
        for element in dic:
            userid, feature2 = element
            # FaceRecognizerSF でマッチする
            score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
            if score > self.COSINE_THRESHOLD:
                return True, (userid, score)
        return False, ('unknown', 0.0)

    def mosaic(self, src, ratio=0.05):
        small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

    def mosaic_area(self, src, x, y, width, height, ratio=0.05):
        dst = src.copy()
        dst[y:y + height, x:x + width] = self.mosaic(dst[y:y + height, x:x + width], ratio)
        return dst

    def back_home(self):
        self.master.destroy()
        self.capture.release()
        guihome.Homewindow()

    def take_picture(self):
        current_time = time.localtime()
        formatted_datetime = time.strftime("%Y-%m-%d %H-%M-%S", current_time)
        picture_file_name = formatted_datetime + ".png"
        picture_path = os.path.join("/Users/yuma/opencv/recproApplication/completeImage", picture_file_name)
        cv2.imwrite(picture_path, self.picture)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()