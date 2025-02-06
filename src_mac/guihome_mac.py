from tkmacosx import Button
import tkinter as tk
import choice_rec_file
import real_time
import management_data
from work_enum import Work


# ホーム画面のクラス
class HomeWindow:
    def __init__(self):
        # ウィンドウの作成
        self.root = tk.Tk()
        self.root.title("faceMozaicApp") # ウィンドウ名
        self.root.geometry("1440x847+0+0") # ウィンドウサイズ
        self.root.resizable(False, False) # ウィンドウのサイズを変化できないように設定
        self.root.configure(bg="#fafaf2") # ウィンドウの背景色
        FONT = ("Helvetica", 120) # フォントとサイズ

        # 顔データの登録を実行するボタン
        registration_process_btn = Button(self.root, text="register", command=self.do_registration_process, bg="#1995ad", fg="#537072", font=FONT) # do_registration_processメソッドの呼び出し
        registration_process_btn.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        # 顔データファイルの管理を実行するボタン
        manage_process_btn = Button(self.root, text="manage", command=self.do_management, bg="#a1d6e2", fg="#537072", font=FONT) # do_managementメソッドの呼び出し
        manage_process_btn.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        # 写真の処理を実行するボタン
        image_process_btn = Button(self.root, text="image", command=self.do_imagerecpro, bg="#a1d6e2", fg="#537072",  font=FONT) # do_imagerecproメソッドの呼び出し
        image_process_btn.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        # リアルタイムで顔の処理を実行するボタン
        real_time_process_btn = Button(self.root, text="realTime", command=self.do_real_time_rec, bg="#a1d6e2", fg="#537072", font=FONT) # do_real_time_recメソッドの呼び出し
        real_time_process_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.root.mainloop() # ボタンの実行を待機

    # ---------------------------- #
    # ウィンドウの削除
    # 機能を起動するためのインスタンス化
    # ※あれば昨日の起動
    # ---------------------------- #
    def do_registration_process(self):
        self.root.destroy()
        choice_rec_file.Choices(Work.REGISTER) # 処理するファイルを選択するクラス(登録のための)
    def do_management(self):
        self.root.destroy()
        management = management_data.ManageData() # 登録済データを管理するクラス
        management.manage()
    def do_imagerecpro(self):
        self.root.destroy()
        choice_rec_file.Choices(Work.IMAGE) # 処理するファイルを選択するクラス(写真を処理するための)
    def do_real_time_rec(self):
        self.root.destroy()
        real_time_rec = real_time.BootRealTime() # リアルタイムで処理するクラスを起動するためのクラス
        real_time_rec.boot()

if __name__ == "__main__":
    window = HomeWindow()
