import numpy as np
import cv2
import tkinter as tk
import tkinter.filedialog, tkinter.messagebox
import os

#複数のsampleを入れれるようにする
# recimage = cv2.imread("/Users/yuma/opencv/yumaFace.JPG")
# recimage2 = cv2.imread("/Users/yuma/opencv/uchidaFace.png")


class Dictionary:
    def __init__(self):

        self.face_detector = cv2.FaceDetectorYN_create("/Users/yuma/opencv/yunet_n_640_640.onnx", "", (320, 320))
        # FaceRecognizerSF の生成
        self.face_recognizer = cv2.FaceRecognizerSF_create("/Users/yuma/opencv/face_recognition_sface_2021dec.onnx", "")

        self.root = tk.Tk()
        self.root.withdraw()
        # 表示するファイルの拡張子を限定する
        self.file_Type = [("","*.JPG"),("","*.jpeg"),("","*.jpg"),("","*.PNG"),("","*.png"),("","*.HEIC")]
        # 表示する初期ディレクトリーを指定する
        self.userDirectry = os.path.expanduser("~")
        tkinter.messagebox.showinfo('','処理ファイルを選択')
        self.file = tkinter.filedialog.askopenfilenames(filetypes = self.file_Type,initialdir = self.userDirectry)
        self.list = list(self.file)
        # tkinter.messagebox.showinfo('○×プログラム',self.list)


    def recSave(self, image):
        recimage = cv2.imread(image)
        # 画像サイズの取得
        height, width, _ = recimage.shape
        self.face_detector.setInputSize((width, height))

        # 顔を検出する
        _, faces = self.face_detector.detect(recimage)
        # 顔を切り抜き特徴を抽出する
        aligned_face = self.face_recognizer.alignCrop(recimage, faces)
        # 特徴量の抽出
        face_feature = self.face_recognizer.feature(aligned_face)
        # outputするファイル名を取得するファイル名から取ってくるように変更する
        np.save("/Users/yuma/opencv/recproApplication/features/yuma2.npy", face_feature)
    


if __name__ == "__main__":
    save_data = Dictionary()
    save_data.recSave("/Users/yuma/opencv/yumaFace2.png")
