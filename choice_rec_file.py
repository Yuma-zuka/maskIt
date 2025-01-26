import tkinter as tk
import tkinter.filedialog, tkinter.messagebox
import os
import save_dictionary

class Dictionary:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        # 表示するファイルの拡張子を限定する
        self.file_Type = [("","*.JPG"),("","*.jpeg"),("","*.jpg"),("","*.PNG"),("","*.png"),("","*.HEIC")]
        # 表示する初期ディレクトリーを指定する
        self.userDirectry = os.path.expanduser("~")
        tkinter.messagebox.showinfo('','処理ファイルを選択')
        self.file = tkinter.filedialog.askopenfilename(filetypes = self.file_Type,initialdir = self.userDirectry)
        save_file = save_dictionary.Register()
        if (self.file != ""):
            save_file.recSave(self.file)
        else:
            save_file.back_home()

if __name__ == "__main__":
    save_data = Dictionary()