import numpy as np
import cv2
import os
from moviepy import *
class MovieRecPro:
    def __init__(self):
        # FaceDetectorYNの生成
        self.FACE_DETECTOR = cv2.FaceDetectorYN_create("/Users/yuma/opencv/yunet_n_640_640.onnx", "", (320, 320))
        
    def rec_Movie(self):
        self.video_path = "/Users/yuma/opencv/samplemovie.mp4"
        self.audio_path = '/Users/yuma/opencv/recproApplication/completevideo/audiosample.mp3'
        self.cap = cv2.VideoCapture(self.video_path)
        self.cap.set(3,640) # set Width
        self.cap.set(4,480) # set Height

        # 各種プロパティーを取得
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # フレームの幅
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # フレームの高さ
        self.fps = float(self.cap.get(cv2.CAP_PROP_FPS))  # FPS

        # VideoWriter を作成する。
        self.output_file = "/Users/yuma/opencv/recproApplication/completevideo/output_video.mp4"  # 保存する動画ファイル名
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 動画のコーデックを指定
        self.out = cv2.VideoWriter(self.output_file, self.fourcc, self.fps, (self.frame_width, self.frame_height), True)

        while True:
            ret, img = self.cap.read()

            if not ret:
                break

            # 画像サイズを設定する
            self.FACE_DETECTOR.setInputSize((img.shape[1], img.shape[0]))
            # 顔検出
            _, faces = self.FACE_DETECTOR.detect(img)
            faces = faces if faces is not None else []
            for face in faces:
                (x, y, w, h, *_) = map(int, face)                   # ③ 検出値はfloat
                # cv2.rectangle(img, (x, y), (x + w, y + h), GREEN, 2, cv2.LINE_AA)
                img = self.mosaic_area(img, x, y, w, h)

                    # 検出した顔のバウンディングボックスとランドマークを描画する
            # for face in faces:
                # バウンディングボックス
                # box = list(map(int, face[:4]))
                # color = (0, 0, 255)
                # thickness = 2
                # cv2.rectangle(img, box, color, thickness, cv2.LINE_AA)

            # 動画にフレームを書き込む
            self.out.write(img)
            # cv2.imshow('video',img)

            k = cv2.waitKey(1) & 0xff
            if k == 27 : # press 'ESC' to quit
                break

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

        self.picture_clip = VideoFileClip(self.output_file)
        self.audio_clip = AudioFileClip(self.video_path)
        self.audio_clip.write_audiofile(self.audio_path)
        self.rec_output_file = str(os.path.splitext(os.path.basename(self.video_path))[0]) + "_processed.mov"
        self.rec_output_file = os.path.join("/Users/yuma/opencv/recproApplication/completevideo", self.rec_output_file)
        self.picture_clip.write_videofile(self.rec_output_file, codec='libx264', audio=self.audio_path, audio_codec='aac', temp_audiofile=self.audio_path, remove_temp=True)
        os.remove(self.output_file)
        os.remove(self.audio_path)
    
    def mosaic(self, src, ratio=0.1):
            small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
            return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

    def mosaic_area(self, src, x, y, width, height, ratio=0.1):
        dst = src.copy()
        dst[y:y + height, x:x + width] = self.mosaic(dst[y:y + height, x:x + width], ratio)
        return dst
    
if __name__ == "__main__":
    test = MovieRecPro()