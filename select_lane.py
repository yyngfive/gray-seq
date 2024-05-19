import ttkbootstrap as ttk
from PIL import Image, ImageTk
import numpy as np
from ttkbootstrap.constants import *
from icecream import ic


root = ttk.Window()


class Img(ttk.Toplevel):
    def __init__(self, master, img):
        super().__init__(master)
        self.master = master
        self.sw = self.winfo_screenwidth()
        self.sh = self.winfo_screenheight()
        self.img = img
        ic(self.sw)
        img = Image.open('./test1.tif')
        photo = ImageTk.PhotoImage(img)
        self.show_img(photo)
    
    def show_img(self,photo):
        canvas = ttk.Canvas(self,height=400,width=500)
        image = canvas.create_image(100,50,anchor='center',image=photo)
        canvas.pack()


class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill=BOTH, expand=YES)

        self.create_menubar()

        self.file_name = "./test1.tif"
        self.img = Image.open(self.file_name)
        self.show_img()

    def create_menubar(self):
        menubar = ttk.Menu(self)
        menu_file = ttk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Open", command=self.open_img)
        menubar.add_cascade(label="File", menu=menu_file)
        root.config(menu=menubar)

    def open_img(self):
        self.img = Image.open(self.file_name)
        self.show_img()

    def show_img(self):

        self.img_window = Img(self,self.img)


App(root)
root.mainloop()
