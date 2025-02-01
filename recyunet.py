import numpy as np
import cv2
import glob
import os



class RealTimeRec:
    def __init__(self):
        # FaceDetectorYNの生成
        self.FACE_DETECTOR = cv2.FaceDetectorYN_create("/Users/yuma/opencv/yunet_n_640_640.onnx", "", (320, 320))
        self.FACE_RECOGNIZER = cv2.FaceRecognizerSF_create("/Users/yuma/opencv/face_recognition_sface_2021dec.onnx", "")
        self.COSINE_THRESHOLD = 0.363
        self.NORML2_THRESHOLD = 1.128

    def rec_real_time(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,1280) # set Width
        self.cap.set(4, 720) # set Height
        

        # 特徴を読み込む
        self.dictionary = []
        self.files = glob.glob(os.path.join("/Users/yuma/opencv/recproApplication/features", "*.npy"))
        for file in self.files:
            feature = np.load(file)
            user_id = os.path.splitext(os.path.basename(file))[0] # face001.npy -> face001
            self.dictionary.append((user_id, feature))

        while True:
            ret, img = self.cap.read()
            # 画像サイズを設定する
            self.FACE_DETECTOR.setInputSize((img.shape[1], img.shape[0]))
            img = cv2.flip(img, 1)
            # 顔検出
            _, faces = self.FACE_DETECTOR.detect(img)
            faces = faces if faces is not None else []

            _idx=0
            _l=list()
            for face in faces:
                aligned_face=self.FACE_RECOGNIZER.alignCrop(img, face)
                _idx+=1
                feature=self.FACE_RECOGNIZER.feature(aligned_face)
                # 辞書とマッチングする
                result, user = self.match(self.FACE_RECOGNIZER, feature, self.dictionary)
                (x, y, w, h, *_) = map(int, face)                   # ③ 検出値はfloat
                if (result == False):
                    img = self.mosaic_area(img, x, y, w, h)

            # 検出した顔のバウンディングボックスとランドマークを描画する
            for face in faces:
                # バウンディングボックス
                box = list(map(int, face[:4]))
                color = (0, 0, 255)
                thickness = 2
                cv2.rectangle(img, box, color, thickness, cv2.LINE_AA)

                id, score = user if result else ("unknown", 0.0)
                text = "{0} ({1:.2f})".format(id, score)
                position = (box[0], box[1] - 10)
                font = cv2.FONT_HERSHEY_SIMPLEX
                scale = 0.6
                cv2.putText(img, text, position, font, scale, color, thickness, cv2.LINE_AA)                    
            cv2.imshow('video',img[30:690, 40:1240])
            cv2.moveWindow('video', 150, 100)

            k = cv2.waitKey(30) & 0xff
            if k == 27: # press 'ESC' to quit
                break

        self.cap.release()
        cv2.destroyAllWindows()
    

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
    
if __name__ == "__main__":
    test = RealTimeRec()
    test.rec_real_time()