import tkinter as tk
from tkmacosx import Button
import tkinter.filedialog, tkinter.messagebox
import os
import sys
import guihome_mac 
from work_enum import Work 

# 登録してあるデータファイルを管理するクラス
class ManageData:
    def __init__(self):
        if hasattr(sys, "_MEIPASS"):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.abspath(".")

        # 特徴を抽出してできたデータファイルを保存するディレクトリのパス
        self.DATA_DIRECTRY = os.path.expanduser(os.path.join(self.base_path, "features"))
        # 拡張子の限定
        self.DATA_EXTENTION = [("","*.npy")]
        # ゴミ箱の画像のパス
        self.GOMIBAKO_IMAGE = os.path.expanduser(os.path.join(self.base_path, "material/gomibako.png"))
        # 矢印の画像のパス
        self.YAJIRUSHI_IMAGE = os.path.expanduser(os.path.join(self.base_path, "material/yajirushi.png"))
        # 変更か削除かの切り替えのための定義
        self.work = None
    
    # 管理するメソッド
    def manage(self):
        # ウィンドウの作成
        self.root = tk.Tk()
        self.root.title("manage") # ウィンドウ名
        self.root.geometry("1440x847+0+0") # ウィンドウサイズと位置
        self.root.resizable(False, False) # ウィンドウのサイズを変化できないように設定
        
        # 戻るボタンの画像を取得
        self.BACK_BUTTON_IMAGE = tk.PhotoImage(file=os.path.join(self.base_path, "material/back.png"))
        # 実行するボタンの画像を取得
        self.RETRY_BUTTON_IMAGE = tk.PhotoImage(file=os.path.join(self.base_path, "material/process.png"))
        
        back_button = tk.Canvas(self.root, width=180, height=70) # ボタンのキャンバスを作成
        back_button.place(x=120, y=790, anchor="center") # "戻る"ボタンの配置
        back_button.create_image(0, 0, image=self.BACK_BUTTON_IMAGE, anchor="nw") # イメージの貼り付け
        back_label = tk.Label(back_button, text="戻る", bg="#bcbabe", fg="#000000", font=("Helvetica", 54)) # 戻るボタンのラベルの設定
        back_label.place(x=70, y=3) # "戻る"ボタンのラベルの配置
        back_button.bind("<Button-1>", self.back_home) # back_homeメソッドの呼び出し
        back_label.bind("<Button-1>", self.back_home) # back_homeメソッドの呼び出し
        retry_button = tk.Canvas(self.root, width=180, height=70) # ボタンのキャンバスを作成
        retry_button.place(x=1315, y=790, anchor="center") # "実行"ボタンの配置
        retry_button.create_image(0, 0, image=self.RETRY_BUTTON_IMAGE, anchor="nw") # イメージの貼り付け
        retry_label = tk.Label(retry_button, text="実行", bg="#f0cb45", fg="#ffffff", font=("Helvetica", 54)) # 実行するボタンのラベルの設定
        retry_label.place(x=70, y=3) # "実行"ボタンのラベルの配置
        retry_button.bind("<Button-1>", self.enter_changing) # enter_changingメソッドの呼び出し
        retry_label.bind("<Button-1>", self.enter_changing) # enter_changingメソッドの呼び出し

        remove_button = Button(self.root, text="ファイルを削除", bg="#bbdceb", fg="#000000", command=self.remove_file, font=("Helvetica", 80), relief="raised") # ファイル削除ボタンの設定 remove_fileメソッドの呼び出し
        remove_button.place(x=80,y=50) # "ファイルを削除"ボタンの配置
        rename_button = Button(self.root, text="ファイル名変更", bg="#bbdceb", fg="#000000", command=self.rename_file, font=("Helvetica", 80), relief="raised") # ファイル名変更ボタンの設定 rename_fileメソッドの呼び出し
        rename_button.place(x=760,y=50) # "ファイル名変更"ボタンの配置

        self.root.mainloop() # ボタンの実行を待機

    # 登録しているデータファイルを削除するメソッド
    def remove_file(self):
        self.remove_item() # remove_itemメソッドの呼び出し

        message_files = "" # メッセージを定義
        self.file = tkinter.filedialog.askopenfilenames(filetypes = self.DATA_EXTENTION,initialdir = self.DATA_DIRECTRY) # 消去するファイルを尋ねる
        remainder = len(self.file) - 10 # 10を超えた分のファイル数(あまり)を出す 10以下の場合はこの変数は使用しない
        file_count = 0 # 繋げたファイルの数を数えるために変数を定義
        for remove_file in self.file: # ファイルの数だけ繰り返す
            message_files += os.path.split(remove_file)[1] # 削除するファイル名を繋げていく
            if len(self.file) > 10: # 繋げたファイルの数が10を超えるならば
                file_count += 1 # 削除したファイルの数を数える
                if file_count == 10: # ファイルを10個繋げたら
                    message_files += f"    ...その他{remainder}件" # 残り幾つのファイルがあるかを繋げる
                    break
            message_files += "\n" # 改行
        # 削除するファイルがあるならば
        if len(self.file) != 0:
            # 削除するファイルの表示
            self.message_box = tk.Message(self.root, justify="center", width=1300, text=message_files, font=("Helvetica", 30)) # ファイル名を表示するmessageを作成
            self.message_box.place(x=720, y=340, anchor="center") # messageboxの配置
            # ファイルを選択したらゴミ箱を表示する
            self.gomibako_canvas = tk.Canvas(self.root, width=200, height=200) # Canvas作成
            gomibako_image_tk  = tk.PhotoImage(file=self.GOMIBAKO_IMAGE, master=self.root) # ゴミ箱画像読み込み
            self.gomibako_canvas.place(x=720, y=670, anchor='center') # Canvas配置
            self.gomibako_canvas.create_image(0, 0, image=gomibako_image_tk, anchor='nw') # ImageTk画像配置
            self.work = Work.REMOVE # この仕事はファイル削除の仕事だと定義する
            self.root.mainloop() # ボタンの実行を待機

    # 登録しているデータファイル名を変更するメソッド
    def rename_file(self):
        self.remove_item() # remove_itemメソッドの呼び出し

        self.file = tkinter.filedialog.askopenfilename(filetypes = self.DATA_EXTENTION,initialdir = self.DATA_DIRECTRY) # 消去するファイルを尋ねる
        if self.file != "": # 変更するファイルがあるならば
            file_name = "変更前    " + os.path.split(self.file)[1] # ファイル名を摘出
            self.file_label = tk.Label(self.root, text=file_name, font=("Helvetica", 40)) # ファイルラベルの設定
            self.file_label.place(x=720, y=300, anchor="center") # ファイルラベルの配置
            self.yajirushi_canvas = tk.Canvas(self.root, width=200, height=200) # Canvasの作成
            yajirushi_image_tk  = tk.PhotoImage(file=self.YAJIRUSHI_IMAGE, master=self.root) # 矢印画像読み込み
            self.yajirushi_canvas.place(x=720, y=480, anchor='center') # Canvasの配置
            self.yajirushi_canvas.create_image(0, 0, image=yajirushi_image_tk, anchor='nw') # ImageTk 画像配置
            self.entry = tk.Entry(self.root, justify="center", width=15, font=("Helvetica", 40), disabledbackground="#ffffff", disabledforeground="#aa8713") # 入力欄の作成
            self.entry.place(x=720, y=670, anchor="center") # entryの配置
            self.after_label = tk.Label(self.root, text="変更後", font=("Helvetica", 40)) # "変更後"ラベルの設定
            self.after_label.place(x=440, y=670, anchor="center") # "変更後"ラベルの配置
            self.extention_label = tk.Label(self.root, text=".npy", font=("Helvetica", 40)) # 拡張子ラベルの作成
            self.extention_label.place(x=940, y=670, anchor="center") # 拡張子ラベルの配置
            self.work = Work.RENAME # この仕事はファイル変更の仕事だと定義する
            self.root.mainloop() # ボタンの実行を待機

    # 取得した文字列が英数字か判定するメソッド
    def is_ok(self, text):
        if not text.encode('utf-8').isalnum():
            return False # 英数字でないならFalse
        return True # 英数字ならTrue

    # 実行ボタンを押したときのメソッド
    def enter_changing(self, _):
        match self.work: # 働きでふるいにかける
            case Work.REMOVE: # 仕事が削除なら
                for file in self.file: # ファイルの数だけ
                    os.remove(file) # ファイルを削除
                self.message_box.destroy() # メッセージボックスを削除
                self.work = None # 仕事を何もしていない状況と定義する
            case Work.RENAME: # 仕事が名前変更なら
                try:
                    self.error_label.destroy() # エラーラベルがあるなら消す
                except:
                    pass
                if self.is_ok(self.entry.get()): # isOkメソッドの呼び出し
                    self.after_label.configure(text="変更済")
                    renamed_file_name = self.entry.get() # 変更後の名前を変数に代入
                    after_file_name = renamed_file_name + ".npy" # 変更後の名前からファイル名を作成
                    after_file_path = os.path.join(self.DATA_DIRECTRY, after_file_name) # ファイル名からパスを作成
                    os.rename(self.file, after_file_path) # 名前変更
                    self.file_label.destroy() # ラベルを削除
                    self.entry.configure(state="disabled") # entryを入力不可能にする
                    self.work = None # 仕事を何もしていない状況と定義する
                else: # entryの入力が半角英数字でなかったとき
                    self.error_label = tk.Label(self.root, fg="#ff0000", text="※半角英数字で入力", font=("Helvetica", 40)) # errorラベルの設定
                    self.error_label.place(x=720, y=750, anchor="center") # errorラベルの配置
        self.file = "" # 入力ファイル変数の初期化
    # ホーム画面に戻るメソッド
    def back_home(self, _):
        self.root.destroy()
        guihome_mac.HomeWindow()

    # いろんなものを削除、非表示にする
    def remove_item(self):
        try:
            self.gomibako_canvas.destroy() # ゴミ箱の画像を削除
            self.message_box.destroy() # メッセージボックスを削除
        except:
            pass
        try:
            self.after_label.destroy()
            self.entry.destroy() # 入力の削除
            self.yajirushi_canvas.destroy() # 画像の削除
            self.extention_label.destroy() # 拡張子ラベルの削除
            self.file_label.destroy() # 入力したファイルのラベルを削除
            self.error_label.destroy() # 半角英数字でなかったときに警告を出すラベルを削除
        except:    
            pass

if __name__ == "__main__":
    main = ManageData()
    main.manage()