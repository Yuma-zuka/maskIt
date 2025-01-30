import numpy as np
import tkinter as tk
import tkinter.filedialog, tkinter.messagebox
import os
import guihome 
from work_enum import Work 

class ManageData:
    def __init__(self):
        self.DATA_DIRECTRY = os.path.expanduser("/Users/yuma/opencv/recproApplication/features")
        self.DATA_EXTENTION = [("","*.npy")]
        self.GOMIBAKO_IMAGE = "/Users/yuma/opencv/recproApplication/material/gomibako.png"
        self.YAJIRUSHI_IMAGE = "/Users/yuma/opencv/recproApplication/material/yajirushi.png"
        self.work = None
        self.root = tk.Tk()
        self.root.title("manage")
        self.root.geometry("1440x848+0+0")
        back_button = tk.Button(self.root, text="戻る", command=self.back_home, font=("Helvetica", 50))
        back_button.place(x=30,y=740)
        enter = tk.Button(self.root, text="実行", command=self.enter_changing, font=("Helvetica", 50))
        enter.place(x=1270,y=740)
        remove_button = tk.Button(self.root, text="ファイルを削除", command=self.remove_file, font=("Helvetica", 80))
        remove_button.place(x=80,y=50)
        rename_button = tk.Button(self.root, text="ファイル名変更", command=self.rename_file, font=("Helvetica", 80))
        rename_button.place(x=760,y=50)

        self.root.mainloop()


    def remove_file(self):
        self.remove_item()

        self.message_files = ""
        self.file = tkinter.filedialog.askopenfilenames(filetypes = self.DATA_EXTENTION,initialdir = self.DATA_DIRECTRY)
        if len(self.file) > 10:
            remainder = len(self.file) - 10
            self.file_count = 0
        for remove_file in self.file:
            self.message_files += os.path.split(remove_file)[1]
            if len(self.file) > 10:
                self.file_count += 1
                if self.file_count == 10:
                    self.message_files += f"    ...その他{remainder}件"
                    break
            self.message_files += "\n"

        if len(self.file) != 0:
            # 削除するファイルの表示
            self.message_box = tk.Message(self.root, justify="center", width=1300, text=self.message_files, font=("Helvetica", 30))
            self.message_box.place(x=720, y=340, anchor="center")
            # ファイルを選択したらゴミ箱を表示する
            self.gomibako_canvas = tk.Canvas(self.root, width=200, height=300) # Canvas作成
            gomibako_image_tk  = tk.PhotoImage(file=self.GOMIBAKO_IMAGE, master=self.root)
            self.gomibako_canvas.place(x=720, y=670, anchor='center')
            self.gomibako_canvas.create_image(0, 0, image=gomibako_image_tk, anchor='nw') # ImageTk 画像配置
            self.work = Work.REMOVE
            self.root.mainloop()


    def rename_file(self):
        self.remove_item()

        self.file = tkinter.filedialog.askopenfilename(filetypes = self.DATA_EXTENTION,initialdir = self.DATA_DIRECTRY)
        if self.file != "":
            file_name = os.path.split(self.file)[1]
            self.file_label = tk.Label(self.root, text=file_name, font=("Helvetica", 40))
            self.file_label.place(x=720, y=300, anchor="center")

            self.yajirushi_canvas = tk.Canvas(self.root, width=200, height=300) # Canvas作成
            yajirushi_image_tk  = tk.PhotoImage(file=self.YAJIRUSHI_IMAGE, master=self.root)
            self.yajirushi_canvas.place(x=720, y=480, anchor='center')
            self.yajirushi_canvas.create_image(0, 0, image=yajirushi_image_tk, anchor='nw') # ImageTk 画像配置

            self.entry = tk.Entry(self.root, justify="center", width=15, font=("Helvetica", 40))
            self.entry.place(x=720, y=670, anchor="center")

            self.extention_label = tk.Label(self.root, text=".npy", font=("Helvetica", 40))
            self.extention_label.place(x=940, y=670, anchor="center")
            self.work = Work.RENAME
            self.root.mainloop()

    def isOk(self, text):
        if not text.encode('utf-8').isalnum():
            print("error")
            return False
        print("succ")
        return True


    def enter_changing(self):
        match self.work:
            case Work.REMOVE:
                for file in self.file:
                    os.remove(file)
                    self.message_box.destroy()
                self.work = None
            case Work.RENAME:
                try:
                    self.error_label.destroy()
                except:
                    pass
                if self.isOk(self.entry.get()):
                    renamed_file_name = self.entry.get()
                    after_file_name = renamed_file_name + ".npy"
                    after_file_path = os.path.join(self.DATA_DIRECTRY, after_file_name)
                    os.rename(self.file, after_file_path)
                    self.file_label.destroy()
                    self.entry.configure(state="disabled")
                    self.work = None
                else:
                    self.error_label = tk.Label(self.root, fg="#ff0000", text="※半角英数字で入力", font=("Helvetica", 40))
                    self.error_label.place(x=720, y=750, anchor="center")

    def back_home(self):
        self.root.destroy()
        guihome.Homewindow()

    def remove_item(self):
        try:
            self.entry.destroy()
            self.yajirushi_canvas.destroy()
            self.extention_label.destroy()
            self.file_label.destroy()
            self.error_label.destroy()
        except:    
            pass
        try:
            self.gomibako_canvas.destroy()
            self.message_box.destroy()
            print("消したよ")
        except:
            pass


# removeの時は複数選択可能
# remove, renameの切り替え
# remove する時の注意画面
# filedialogのルートディレクトリ固定

test = ManageData()