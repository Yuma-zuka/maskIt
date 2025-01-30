import numpy as np
import cv2
import glob
import os
import tkinter as tk
import guihome #type: ignore
import choice_rec_file # type: ignore
from work_enum import Work # type: ignore


class ImageRecPro:
    def __init__(self):
        # FaceDetectorYNの生成
        self.FACE_DETECTOR = cv2.FaceDetectorYN_create("/Users/yuma/opencv/yunet_n_640_640.onnx", "", (320, 320))
        # FaceRecognizerの生成
        self.FACE_RECOGNIZER = cv2.FaceRecognizerSF_create("/Users/yuma/opencv/face_recognition_sface_2021dec.onnx", "")
        #表示するための画像を一時的に保存するパス
        self.temporary_save_path = "/Users/yuma/opencv/recproApplication/completeImage/temporary_save_image.png"

        self.COSINE_THRESHOLD = 0.363
    
    def rec_image(self, rec_file):
        self.imagePath = rec_file
        self.imageName = "processed" + str(os.path.splitext(os.path.basename(self.imagePath))[0]) + ".png"
        self.savePath = os.path.join('/Users/yuma/opencv/recproApplication/completeImage', self.imageName)
        self.dictionary = []
        self.files = glob.glob(os.path.join("/Users/yuma/opencv/recproApplication/features", "*.npy"))
        for file in self.files:
            feature = np.load(file)
            user_id = os.path.splitext(os.path.basename(file))[0] # face001.npy -> face001
            self.dictionary.append((user_id, feature))

        try:
            # 画像の読み込み
            self.image = cv2.imread(self.imagePath)

            # 画像サイズを設定する
            self.FACE_DETECTOR.setInputSize((self.image.shape[1], self.image.shape[0]))

            # 顔検出
            _, self.faces = self.FACE_DETECTOR.detect(self.image)
            self.faces = self.faces if self.faces is not None else []

            _idx=0
            for face in self.faces:
                #モザイク実行
                
                aligned_face=self.FACE_RECOGNIZER.alignCrop(self.image, face)
                _idx+=1
                feature=self.FACE_RECOGNIZER.feature(aligned_face)
                # 辞書とマッチングする
                result, user = self.match(self.FACE_RECOGNIZER, feature, self.dictionary)
                
                (x, y, w, h, *_) = map(int, face)
                if result == False:
                    self.image = self.mosaic_area(self.image, x, y, w, h)
                
            # 画像の保存
            print(self.savePath)
            cv2.imwrite(self.savePath, self.image)
            self.show_image = self.resize_image(self.image)
            cv2.imwrite(self.temporary_save_path, self.show_image)
            # 画像の表示
            self.make_result_window(False)
        except:
            self.make_result_window("画像の読み取りに失敗しました")

    def match(self, recognizer, feature1, dic):
        for element in dic:
            userid, feature2 = element
            # FaceRecognizerSF でマッチする
            score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
            if score > self.COSINE_THRESHOLD:
                return True, (userid, score)
        return False, ('unknown', 0.0)
    
    def make_result_window(self,error):
        # ウィンドウの作成
        self.root = tk.Tk()
        self.root.title("recognize image")
        self.root.geometry("1000x800+200+50")
        back_button = tk.Button(self.root, text="戻る", command=self.back_home, font=("Helvetica", 30))
        back_button.place(x=20,y=730)
        retry = tk.Button(self.root, text="続けて編集する", command=self.re_rec_image, font=("Helvetica", 30))
        retry.place(x=730,y=730)
        if error == False:
            # 検出できた時に検出した顔を枠で取って、名前をつけて表示する
            image_tk  = tk.PhotoImage(file=self.temporary_save_path, master=self.root)
            canvas = tk.Canvas(self.root, width=self.show_image.shape[1], height=self.show_image.shape[0]) # Canvas作成
            canvas.place(x=500, y=360, anchor='center')
            canvas.create_image(0, 0, image=image_tk, anchor='nw') # ImageTk 画像配置
            os.remove(self.temporary_save_path)
        else:
            self.set_error_message(error)
        self.root.mainloop()

    def set_error_message(self,error_type):
        error_message = tk.Label(self.root, text=error_type, font=("Helvetica", 60))
        error_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def resize_image(self, subject_image):
        hei, wid, _ = subject_image.shape
        if wid > 1000:
            magnification = 1000 / wid
            subject_image = cv2.resize(subject_image, None, fx=magnification, fy=magnification, interpolation=cv2.INTER_NEAREST)
            hei, wid, _ = subject_image.shape
        if hei > 720:
            magnification = 720 / hei
            subject_image = cv2.resize(subject_image, None, fx=magnification, fy=magnification, interpolation=cv2.INTER_NEAREST)
        return subject_image
    
    def mosaic(self, src, ratio=0.1):
        small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

    def mosaic_area(self, src, x, y, width, height, ratio=0.1):
        dst = src.copy()
        dst[y:y + height, x:x + width] = self.mosaic(dst[y:y + height, x:x + width], ratio)
        return dst
    
    def back_home(self):
        self.root.destroy()
        guihome.Homewindow()
    def re_rec_image(self):
        self.root.destroy()
        choice_rec_file.Dictionary(Work.IMAGE)

if __name__ == "__main__":
    test = choice_rec_file.Dictionary(Work.IMAGE)