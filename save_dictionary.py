import numpy as np
import cv2

#複数のsampleを入れれるようにする
# recimage = cv2.imread("/Users/yuma/opencv/yumaFace.JPG")
# recimage2 = cv2.imread("/Users/yuma/opencv/uchidaFace.png")


class Dictionary:
    def __init__(self):    
        self.face_detector = cv2.FaceDetectorYN_create("/Users/yuma/opencv/yunet_n_640_640.onnx", "", (320, 320))
        # FaceRecognizerSF の生成
        self.face_recognizer = cv2.FaceRecognizerSF_create("/Users/yuma/opencv/face_recognition_sface_2021dec.onnx", "")

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
