import numpy as np
import cv2
import tkinter as tk
import os
import glob
import guihome #type: ignore
import choice_rec_file # type: ignore

class Register:
    def __init__(self):
        self.face_detector = cv2.FaceDetectorYN_create("/Users/yuma/opencv/yunet_n_640_640.onnx", "", (320, 320))
        # FaceRecognizerSF の生成
        self.face_recognizer = cv2.FaceRecognizerSF_create("/Users/yuma/opencv/face_recognition_sface_2021dec.onnx", "")

        self.FEATURES_FILE = glob.glob(os.path.join("/Users/yuma/opencv/recproApplication/features", "*.npy"))

        self.temporary_save_path = "/Users/yuma/opencv/recproApplication/features/temporary_save_image.png"

        self.COSINE_THRESHOLD = 0.363
        self.NORML2_THRESHOLD = 1.128

    def recSave(self, image_path):
        try:
            self.recimage = cv2.imread(image_path)
            # 画像サイズの取得
            height, width, _ = self.recimage.shape
            self.face_detector.setInputSize((width, height))
            try:
                # 顔を検出する
                _, faces = self.face_detector.detect(self.recimage)
                menbers = 0
                _idx=0
                for face in faces:
                    # 顔を切り抜き特徴を抽出する
                    aligned_face = self.face_recognizer.alignCrop(self.recimage, face)
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

                    # 登録した顔の特徴データを取得する
                    dictionary = []
                    for file in self.FEATURES_FILE:
                        feature = np.load(file)
                        user_id = os.path.splitext(os.path.basename(file))[0] # face001.npy -> face001
                        dictionary.append((user_id, feature))

                    aligned_face=self.face_recognizer.alignCrop(self.recimage, face)
                    _idx+=1
                    feature=self.face_recognizer.feature(aligned_face)
                    # 辞書とマッチングする
                    result, user = self.match(self.face_recognizer, feature, dictionary)

                    # バウンディングボックスと登録したファイル名の表示
                    box = list(map(int, face[:4]))
                    color = (0, 0, 255)
                    thickness = 2
                    cv2.rectangle(self.recimage, box, color, thickness, cv2.LINE_AA)
                    id, _ = user if result else ("unknown",(0.0))
                    position = (box[0], box[1] - 10)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    scale = 0.6
                    cv2.putText(self.recimage, id, position, font, scale, color, thickness, cv2.LINE_AA)
                    self.recimage = self.resize_image(self.recimage)

                    self.make_result_window(False)
            except:
                self.make_result_window("顔を検出できませんでした")
        except:
            self.make_result_window("画像の読み取りに失敗しました")


    def make_result_window(self,error):
        # ウィンドウの作成
        self.root = tk.Tk()
        self.root.title("register")
        self.root.geometry("1000x800+200+50")
        back_button = tk.Button(self.root, text="戻る", command=self.back_home, font=("Helvetica", 30))
        back_button.place(x=20,y=730)
        retry = tk.Button(self.root, text="続けて登録する", command=self.register, font=("Helvetica", 30))
        retry.place(x=730,y=730)
        if error == False:
            # 検出できた時に検出した顔を枠で取って、名前をつけて表示する
            cv2.imwrite(self.temporary_save_path, self.recimage)
            image_tk  = tk.PhotoImage(file=self.temporary_save_path, master=self.root)
            canvas = tk.Canvas(self.root, width=self.recimage.shape[1], height=self.recimage.shape[0]) # Canvas作成
            canvas.pack(anchor='center', expand=1)
            canvas.create_image(0, 0, image=image_tk, anchor='nw') # ImageTk 画像配置
            os.remove(self.temporary_save_path)
            print("success")
        else:
            self.set_error_message(error)
        self.root.mainloop()

    def set_error_message(self,error_type):
        error_message = tk.Label(self.root, text=error_type, font=("Helvetica", 60))
        error_message.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def match(self, recognizer, feature1, dic):
        for element in dic:
            userid, feature2 = element
            # FaceRecognizerSF でマッチする
            score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
            if score > self.COSINE_THRESHOLD:
                return True, (userid, score)
        return False, ('unknown', 0.0)
    
    def resize_image(self, subject_image):
        hei, wid, _ = subject_image.shape
        while wid > 800:
                subject_image = cv2.resize(subject_image, None, fx=0.9, fy=0.9)
                wid = subject_image.shape[1]
        while hei > 640:
                subject_image = cv2.resize(subject_image, None, fx=0.9, fy=0.9)
                hei = subject_image.shape[0]
        return subject_image

    def back_home(self):
        self.root.destroy()
        guihome.Homewindow()
    def register(self):
        self.root.destroy()
        choice_rec_file.Dictionary()

if __name__ == "__main__":
    save_data = choice_rec_file.Dictionary()
