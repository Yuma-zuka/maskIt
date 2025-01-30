import tkinter as tk
import tkinter.filedialog, tkinter.messagebox
import os
import save_dictionary
import guihome
import imagerecpro
from work_enum import Work

class Dictionary:
    def __init__(self, work):
        self.work = work
        # 表示するファイルの拡張子を限定する
        self.image_extension = [("","*.JPG"),("","*.jpeg"),("","*.jpg"),("","*.PNG"),("","*.png"),("","*.HEIC")]

        self.root = tk.Tk()
        self.root.withdraw()

        # ----------------------- #
        # 機能ごとに拡張子の限定
        # 実行対象ファイルの選択
        # 実行クラスのインスタンス生成
        # 実行
        #  ---------------------- #
        match self.work:
            case Work.REGISTER:
                self.file_Type = self.image_extension
                self.ask_file()
                save_file = save_dictionary.Register()
                save_file.recSave(self.file)
            case Work.IMAGE:
                self.file_Type = self.image_extension
                self.ask_file()
                rec_file = imagerecpro.ImageRecPro()
                rec_file.rec_image(self.file)

    def ask_file (self):
        # 表示する初期ディレクトリーを指定する
        self.userDirectry = os.path.expanduser("~")
        self.file = tkinter.filedialog.askopenfilename(filetypes = self.file_Type,initialdir = self.userDirectry)
        if (self.file == ""):
            guihome.Homewindow()

if __name__ == "__main__":
    # save_data = Dictionary(Work.REGISTER)
    # save_data = Dictionary(Work.IMAGE)
    save_data = Dictionary(Work.MANAGE)