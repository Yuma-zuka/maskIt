import numpy as np
import cv2
import glob
import os


class ImageRecPro:
    def __init__(self):
        # FaceDetectorYNの生成
        self.FACE_DETECTOR = cv2.FaceDetectorYN_create("/Users/yuma/opencv/yunet_n_640_640.onnx", "", (320, 320))
        # FaceRecognizerの生成
        self.FACE_RECOGNIZER = cv2.FaceRecognizerSF_create("/Users/yuma/opencv/face_recognition_sface_2021dec.onnx", "")

        self.COSINE_THRESHOLD = 0.363
        self.NORML2_THRESHOLD = 1.128
    
    def rec_image(self):
        self.imagePath = "/Users/yuma/opencv/sample.JPG"
        self.imageName = "processed" + str(os.path.split(self.imagePath)[1])
        self.savePath = os.path.join('/Users/yuma/opencv/recproApplication/completeImage', self.imageName)
        self.dictionary = []
        self.files = glob.glob(os.path.join("/Users/yuma/opencv/recproApplication/features", "*.npy"))
        for file in self.files:
            feature = np.load(file)
            user_id = os.path.splitext(os.path.basename(file))[0] # face001.npy -> face001
            self.dictionary.append((user_id, feature))

        # 画像の読み込み
        self.image = cv2.imread(self.imagePath)

        # 画像サイズを設定する
        self.FACE_DETECTOR.setInputSize((self.image.shape[1], self.image.shape[0]))

        # 顔検出
        _, self.faces = self.FACE_DETECTOR.detect(self.image)
        self.faces = self.faces if self.faces is not None else []

        _idx=0
        # 検出した顔のバウンディングボックスとランドマークを描画する
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

        # 画像の表示
        print(self.savePath)
        cv2.imwrite(f"{self.savePath}", self.image)
        cv2.imshow("/Users/yuma/opencv/sample.JPG", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def match(self, recognizer, feature1, dic):
        for element in dic:
            userid, feature2 = element
            # FaceRecognizerSF でマッチする
            score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
            if score > self.COSINE_THRESHOLD:
                return True, (userid, score)
        return False, ('unknown', 0.0)
    
    def mosaic(self, src, ratio=0.1):
        small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

    def mosaic_area(self, src, x, y, width, height, ratio=0.1):
        dst = src.copy()
        dst[y:y + height, x:x + width] = self.mosaic(dst[y:y + height, x:x + width], ratio)
        return dst

if __name__ == "__main__":
    test = ImageRecPro()
    test.rec_image()