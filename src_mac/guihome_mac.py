import tkinter as tk
import os
import sys
import choice_rec_file
import real_time
import management_data
from work_enum import Work


# ホーム画面のクラス
class HomeWindow:
    def __init__(self):
        try:
            if hasattr(sys, "_MEIPASS"):
                self.base_path = sys._MEIPASS
            else:
                self.base_path = os.path.abspath(".")

            BACKGROUND_COLOR = "#fafaf2" # 全体の背景色
            TITLE_FONT = ("Helvetica", 120) # タイトルのフォントとサイズ
            BUTTON_LABEL_FONT = ("Helvetica", 40) # ボタンの下のラベルのフォントとサイズ
            # ウィンドウの作成
            self.root = tk.Tk()
            self.root.title("maskIt") # ウィンドウ名
            self.root.geometry("1440x847+0+0") # ウィンドウサイズ
            self.root.resizable(False, False) # ウィンドウのサイズを変化できないように設定
            self.root.configure(bg=BACKGROUND_COLOR) # ウィンドウの背景色

            # ボタンに表示する画像の読み込み
            register_icon = tk.PhotoImage(file=os.path.join(self.base_path, "material/register_icon.png"))
            manage_icon = tk.PhotoImage(file=os.path.join(self.base_path, "material/manage_icon.png"))
            image_icon = tk.PhotoImage(file=os.path.join(self.base_path, "material/image_icon.png"))
            real_time_icon = tk.PhotoImage(file=os.path.join(self.base_path, "material/realtime_icon.png"))

            # タイトルラベル
            title_label = tk.Label(self.root, text="maskIt", font=TITLE_FONT, bg="#ffffff")
            title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
            # 顔データの登録を実行するボタンとラベル
            registration_process_btn = tk.Canvas(self.root, width=230, height=230)
            registration_process_btn.place(relx=0.3, rely=0.35, anchor="center")
            registration_process_btn.bind("<Button-1>", self.do_registration_process) # do_registration_processメソッドの呼び出し
            registration_process_btn.create_image(4, 4, image=register_icon, anchor="nw")
            registration_process_label = tk.Label(self.root, text="顔を登録する", font=BUTTON_LABEL_FONT, bg=BACKGROUND_COLOR, fg="#537072")
            registration_process_label.place(relx=0.3, rely=0.535, anchor="center")
            # 顔データファイルの管理を実行するボタンとラベル
            manage_process_btn = tk.Canvas(self.root, width=230, height=230)
            manage_process_btn.place(relx=0.7, rely=0.35, anchor="center")
            manage_process_btn.bind("<Button-1>", self.do_management) # do_managementメソッドの呼び出し
            manage_process_btn.create_image(4, 4, image=manage_icon, anchor="nw")
            manage_process_label = tk.Label(self.root, text="登録データの編集", font=BUTTON_LABEL_FONT, bg=BACKGROUND_COLOR, fg="#537072")
            manage_process_label.place(relx=0.7, rely=0.535, anchor="center")
            # 写真の処理を実行するボタンとラベル
            image_process_btn = tk.Canvas(self.root, width=230, height=230)
            image_process_btn.place(relx=0.3, rely=0.75, anchor="center")
            image_process_btn.bind("<Button-1>", self.do_imagerecpro) # do_imagerecproメソッドの呼び出し
            image_process_btn.create_image(4, 4, image=image_icon, anchor="nw")
            image_process_label = tk.Label(self.root, text="写真にモザイク処理", font=BUTTON_LABEL_FONT, bg=BACKGROUND_COLOR, fg="#537072")
            image_process_label.place(relx=0.3, rely=0.935, anchor="center")
            # リアルタイムで顔の処理を実行するボタンとラベル
            real_time_process_btn = tk.Canvas(self.root, width=230, height=230)
            real_time_process_btn.place(relx=0.7, rely=0.75, anchor="center")
            real_time_process_btn.bind("<Button-1>", self.do_real_time_rec) # do_real_time_recメソッドの呼び出し
            real_time_process_btn.create_image(4, 4, image=real_time_icon, anchor="nw")
            real_time_process_label = tk.Label(self.root, text="リアルタイムでモザイク処理", font=BUTTON_LABEL_FONT, bg=BACKGROUND_COLOR, fg="#537072")
            real_time_process_label.place(relx=0.7, rely=0.935, anchor="center")

            self.root.mainloop() # ボタンの実行を待機
        except Exception as e:
            print(f"Error: {e}")

    # ---------------------------- #
    # ウィンドウの削除
    # 機能を起動するためのインスタンス化
    # ※あれば昨日の起動
    # ---------------------------- #
    def do_registration_process(self, _):
        self.root.destroy()
        choice_rec_file.Choices(Work.REGISTER) # 処理するファイルを選択するクラス(登録のための)
    def do_management(self, _):
        self.root.destroy()
        management = management_data.ManageData() # 登録済データを管理するクラス
        management.manage()
    def do_imagerecpro(self, _):
        self.root.destroy()
        choice_rec_file.Choices(Work.IMAGE) # 処理するファイルを選択するクラス(写真を処理するための)
    def do_real_time_rec(self, _):
        self.root.destroy()
        real_time_rec = real_time.BootRealTime() # リアルタイムで処理するクラスを起動するためのクラス
        real_time_rec.boot()

if __name__ == "__main__":
    window = HomeWindow()
