import tkinter as tk
import choice_rec_file
import real_time
import management_data
from work_enum import Work



class Homewindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("faceMozaicApp")
        self.root.geometry("1440x847+0+0")
        self.root.resizable(False, False)
        self.root.configure(bg="#fafaf2")

        FONT = ("Helvetica", 120)

        self.registration_process_btn = tk.Button(self.root, text="register", command=self.do_registration_process, bg="#1995ad", fg="#537072", font=FONT)
        self.registration_process_btn.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.image_process_btn = tk.Button(self.root, text="manage", command=self.do_management, bg="#a1d6e2", fg="#537072", font=FONT)
        self.image_process_btn.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.movie_process_btn = tk.Button(self.root, text="image", command=self.do_imagerecpro, bg="#a1d6e2", fg="#537072",  font=FONT)
        self.movie_process_btn.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.real_time_process_btn = tk.Button(self.root, text="realTime", command=self.do_real_time_rec, bg="#a1d6e2", fg="#537072", font=FONT)
        self.real_time_process_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.root.mainloop()

    def do_registration_process(self):
        self.root.destroy()
        choice_rec_file.Dictionary(Work.REGISTER)
    def do_management(self):
        self.root.destroy()
        management = management_data.ManageData()
        management.manage()
    def do_imagerecpro(self):
        self.root.destroy()
        choice_rec_file.Dictionary(Work.IMAGE)
    def do_real_time_rec(self):
        self.root.destroy()
        real_time_rec = real_time.BootRealTime()
        real_time_rec.boot()

if __name__ == "__main__":
    window = Homewindow()
