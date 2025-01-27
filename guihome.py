import tkinter as tk
import choice_rec_file # type: ignore
import imagerecpro
import movierecpro
import recyunet



class Homewindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("faceMozaicApp")
        self.root.geometry("1000x800+200+50")
        self.root.resizable(False, False)
        self.root.configure(bg="#fafaf2")

        self.registration_process_btn = tk.Button(self.root, text="register", command=self.do_registration_process, bg="#1995ad", fg="#537072", font=("Helvetica", 120))
        self.registration_process_btn.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.image_process_btn = tk.Button(self.root, text="image", command=self.do_imagerecpro, bg="#a1d6e2", fg="#537072", font=("Helvetica", 120))
        self.image_process_btn.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.movie_process_btn = tk.Button(self.root, text="movie", command=self.do_movierecpro, bg="#a1d6e2", fg="#537072",  font=("Helvetica", 120))
        self.movie_process_btn.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.real_time_process_btn = tk.Button(self.root, text="realTime", command=self.do_real_time_rec, bg="#a1d6e2", fg="#537072", font=("Helvetica", 120))
        self.real_time_process_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.root.mainloop()

    def do_registration_process(self):
        self.root.destroy()
        registration = choice_rec_file.Dictionary()
        registration.recSave("/Users/yuma/opencv/yumaFace2.png")
    def do_imagerecpro(self):
        self.root.destroy()
        imagerp = imagerecpro.ImageRecPro()
        imagerp.rec_image()
    def do_movierecpro(self):
        self.root.destroy()
        movierp = movierecpro.MovieRecPro()
        movierp.movierecpro()
    def do_real_time_rec(self):
        self.root.destroy()
        realtimerp = recyunet.RealTimeRec()
        realtimerp.rec_real_time()

if __name__ == "__main__":
    window = Homewindow()
