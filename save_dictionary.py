import numpy as np
import cv2
import tkinter as tk
import os
import guihome #type: ignore
import choice_rec_file # type: ignore

class Register:
    def __init__(self):
        self.face_detector = cv2.FaceDetectorYN_create("/Users/yuma/opencv/yunet_n_640_640.onnx", "", (320, 320))
        # FaceRecognizerSF の生成
        self.face_recognizer = cv2.FaceRecognizerSF_create("/Users/yuma/opencv/face_recognition_sface_2021dec.onnx", "")

    def recSave(self, image_path):
        recimage = cv2.imread(image_path)
        # 画像サイズの取得
        height, width, _ = recimage.shape
        self.face_detector.setInputSize((width, height))

        # 顔を検出する
        _, faces = self.face_detector.detect(recimage)
        menbers = 0
        for face in faces:
            # 顔を切り抜き特徴を抽出する
            aligned_face = self.face_recognizer.alignCrop(recimage, face)
            # 特徴量の抽出
            face_feature = self.face_recognizer.feature(aligned_face)
            # 画像に含まれている顔の数が複数あればファイル名に数字をつける
            # outputするファイル名を取得するファイル名から取ってくる
            if len(faces) > 1:
                menbers += 1
                save_file_name = str(os.path.splitext(os.path.basename(image_path))[0]) + f"{menbers:d}.npy"
            elif len(faces) == 1:
                save_file_name = str(os.path.splitext(os.path.basename(image_path))[0]) + ".npy"
            save_path = os.path.join("/Users/yuma/opencv/recproApplication/features", save_file_name)
            np.save(save_path, face_feature)
            self.make_result_window()

    def make_result_window(self):
        # ウィンドウの作成
        self.root = tk.Tk()
        self.root.title("register")
        self.root.geometry("1000x800+200+50")
        back_button = tk.Button(self.root, text="戻る", command=self.back_home, font=("Helvetica", 30))
        back_button.place(x=20,y=730)
        retry = tk.Button(self.root, text="続けて登録する", command=self.register, font=("Helvetica", 30))
        retry.place(x=730,y=730)
        self.root.mainloop()
    
    def back_home(self):
        self.root.destroy()
        guihome.Homewindow()
    def register(self):
        self.root.destroy()
        choice_rec_file.Dictionary()

if __name__ == "__main__":
    save_data = Register()
    save_data.recSave()
