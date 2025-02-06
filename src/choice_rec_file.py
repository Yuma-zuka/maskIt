import tkinter.filedialog, tkinter.messagebox
import os
import save_dictionary
import guihome
import imagerecpro
from work_enum import Work

# 実行対象ファイルを選択して各機能を実行するクラス
class Choices:
    def __init__(self, work):
        # 実行する機能を変数に入れる
        self.work = work
        # 表示するファイルの拡張子を限定する
        self.image_extension = [("","*.JPG"),("","*.jpeg"),("","*.jpg"),("","*.PNG"),("","*.png"),("","*.HEIC")]

        # ----------------------- #
        # 機能ごとに拡張子の限定
        # 実行対象ファイルの選択
        # 実行クラスのインスタンス生成
        # 実行
        #  ---------------------- #
        match self.work:
            case Work.REGISTER:
                self.file_type = self.image_extension
                self.ask_file()
                save_file = save_dictionary.Register() # データ登録クラスのインスタンス作成
                save_file.rec_save(self.file)
            case Work.IMAGE:
                self.file_type = self.image_extension
                self.ask_file()
                rec_file = imagerecpro.ImageRecPro() # 写真の処理をするクラスのインスタンス作成
                rec_file.rec_image(self.file)

    def ask_file (self):
        # 表示する初期ディレクトリーを指定する
        self.user_directry = os.path.expanduser("~")
        # 実行対象ファイルを選ぶ
        self.file = tkinter.filedialog.askopenfilename(filetypes=self.file_type, initialdir=self.user_directry)
        if (self.file == ""): # もしファイルを選択しなかったらホームウィンドウに戻る
            guihome.HomeWindow()

if __name__ == "__main__":
    # save_data = Choices(Work.REGISTER)
    save_data = Choices(Work.IMAGE)