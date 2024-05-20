import ttkbootstrap as ttk
from PIL import Image, ImageTk
import numpy as np
from ttkbootstrap.constants import *
from icecream import ic

UPDATE_DELAY = 100

root = ttk.Window(size=(500, 200))


class Img(ttk.Toplevel):
    def __init__(self, master, img):
        super().__init__(master)
        self.master = master
        self.sw = self.winfo_screenwidth()
        self.sh = self.winfo_screenheight()
        self.img = img
        self.focus = False
        self.nw = None
        self.se = None
        self.rec = None
        self.update_id = None
        ic(self.sh)
        self.fit_screen()
        self.show_img()
        self.get_lane()

    def get_lane(self):
        self.canvas.bind("<Motion>", self.get_pos)
        self.canvas.bind("<B1-Motion>", self.set_pos_nw)
        self.canvas.bind("<ButtonRelease-1>",self.set_pos_se)

    def get_pos(self, event):
        self.focus = True
        self.x = event.x * self.resize_coef
        self.y = event.y * self.resize_coef
        self.canvas_x = event.x
        self.canvas_y = event.y
        # ic(event.x,event.y)

    def set_pos_nw(self,event):
        
        self.pos_nw = (event.x,event.y)
        self.update_id = self.after(UPDATE_DELAY,self.update_rec)
    
    def set_pos_se(self,event):
        
        self.pos_se = (self.x,self.y)
        self.pos_nw = None
        self.after_cancel(self.update_id)
         
    
    def update_rec(self):
        self.draw_rec()
        self.update_id = self.after(UPDATE_DELAY,self.update_rec)

    def draw_rec(self):
        if self.pos_nw:
            self.canvas.delete(self.rec)
            self.rec = self.canvas.create_rectangle(self.pos_nw[0],self.pos_nw[1],self.canvas_x,self.canvas_y,fill='',outline='blue',width=2)
    
    def show_img(self):
        width, height = self.resize
        ic(width, height)
        self.canvas = ttk.Canvas(self, height=height, width=width)
        image = self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.canvas.pack()

    def fit_screen(self):
        ic(self.img.size)
        coef = 0.8
        img_width, img_height = self.img.size
        if img_height < self.sh / 2:
            resize = (img_width, img_height)
        elif img_height < self.sh:
            resize = (coef * img_width, coef * img_height)
        else:
            resize = (coef * self.sh * img_width / img_height, coef * self.sh)
        self.resize = tuple(map(int, resize))
        self.resize_coef = img_width / self.resize[0]
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
        self.img_x = 0
        self.show_img()
        self.show_info_bar()

    def show_info_bar(self):
        self.info_bar = ttk.Frame(self)
        self.info_bar.pack(fill=X, pady=1, side=BOTTOM)
        self.img_pos = ttk.StringVar()
        self.img_pos.set("")
        pos_label = ttk.Label(self.info_bar, textvariable=self.img_pos)
        pos_label.pack()

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
        self.img_window = Img(self, self.img)
        # self.wait_window(self.img_window)
        self.after(UPDATE_DELAY, self.update)

    def update(self):
        # ic(self.img_window.focus)
        if self.img_window.focus:
            x = self.img_window.x
            y = self.img_window.y
            # ic(x)
            self.img_pos.set(f"x = {int(x)}, y = {int(y)}")
        self.after(UPDATE_DELAY, self.update)


App(root)
root.mainloop()
