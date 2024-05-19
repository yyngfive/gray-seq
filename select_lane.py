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
        
        ic(self.sh)
        self.fit_screen()
        self.show_img()
    
    def show_img(self):
        width,height = self.resize
        ic(width,height)
        canvas = ttk.Canvas(self,height=height,width=width)
        image = canvas.create_image(0,0,anchor='nw',image=self.photo)
        canvas.pack()
    
    def fit_screen(self):
        ic(self.img.size)
        coef = 0.8
        img_width,img_height = self.img.size
        if img_height < self.sh / 2 :
            resize = (img_width,img_height)
        elif img_height < self.sh:
            resize = (coef * img_width,coef * img_height)
        else:
            resize = (coef * self.sh * img_width / img_height,coef * self.sh)
        self.resize = tuple(map(int,resize))
        ic(self.resize)
        self.img_resized = self.img.resize(self.resize)
        self.photo = ImageTk.PhotoImage(self.img_resized)


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
