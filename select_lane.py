import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from icecream import ic
from collections import defaultdict
from curve_plot import plot as curve_plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


UPDATE_DELAY = 100

class Curve(ttk.Toplevel):
    def __init__(self, master, info):
        super().__init__(master)
        self.master = master
        self.info = info
        self.show_cruve()

    def show_cruve(self):
        file_name = self.info['file_name']
        base_info = self.info['base_info']
        threshold = self.info['threshold']
        title = self.info['title']
        ref = self.info['ref']
        fig = curve_plot(file_name,base_info,ref,title,threshold)
        self.canvas = FigureCanvasTkAgg(fig,self)
        self.canvas.get_tk_widget().place(x=0,y=0)
    
    
    

class Img(ttk.Toplevel):
    def __init__(self, master, img):
        super().__init__(master)
        self.master = master
        self.sw = self.winfo_screenwidth()
        self.sh = self.winfo_screenheight()
        self.img = img
        self.focus = False
        self.pos_nw = (0,0)
        self.nw = False
        self.pos_se = (0,0)
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
        if not self.nw:
            self.pos_nw = (event.x,event.y)
            self.nw = True
        self.canvas_x = event.x
        self.canvas_y = event.y
        self.update_id = self.after(UPDATE_DELAY,self.update_rec)
    
    def set_pos_se(self,event):
        
        self.pos_se = (event.x,event.y)
        ic(self.pos_nw,self.pos_se)
        self.after_cancel(self.update_id)
        self.nw = False
         
    
    def update_rec(self):
        self.draw_rec()
        self.update_id = self.after(UPDATE_DELAY,self.update_rec)

    def draw_rec(self):
        if self.nw:
            self.canvas.delete(self.rec)
            #ic(self.pos_nw)
            #ic(self.canvas_x)
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

        self.file_name = "./test2.png"
        self.img = Image.open(self.file_name)
        self.img_x = 0
        self.current_base = 'N'
        self.base_pos = {'A':(0,0),
                         'C':(0,0),
                         'T':(0,0),
                         'G':(0,0),}
        self.control_buttons = defaultdict(ttk.Button)
        self.show_img()
        self.show_control_box()
        self.show_content()
        self.show_info_bar()
        
    def show_content(self):
        self.base_pos_text = ttk.StringVar()
        self.content = ttk.Frame(self)
        self.content.pack(fill=X,pady=1)
        c_label = ttk.Label(self.content,textvariable=self.base_pos_text)
        c_label.pack()

    def show_info_bar(self):
        self.info_bar = ttk.Frame(self)
        self.info_bar.pack(fill=X, pady=1, side=BOTTOM)
        self.img_pos = ttk.StringVar()
        self.img_pos.set("")
        pos_label = ttk.Label(self.info_bar, textvariable=self.img_pos)
        pos_label.pack(side=LEFT,padx=3)
        self.base_string = ttk.StringVar()
        base_label = ttk.Label(self.info_bar,textvariable=self.base_string)
        base_label.pack(side=LEFT,padx=3)
        
    def show_control_box(self):
        self.control_box = ttk.Frame(self)
        self.control_box.pack(fill=X, pady=1)
        bases = {'A':'A','C':'C','T':'T','G':'G'}
        for base in self.base_pos.keys():
            b = ttk.Button(self.control_box,text=f'Lane {base}',command=lambda   base_h = bases[base]:self.choose_base(base_h))
            b.pack(side=LEFT,padx = 10)
            self.control_buttons[f'b_base_{base}'] = b
        b = ttk.Button(self.control_box,text='Plot',command=self.show_plot)
        b.pack(side=RIGHT,padx=5)
        self.control_buttons['plot'] = b

    
            
            
    def choose_base(self,base):
        self.current_base = base
        ic(self.current_base)
        

    def create_menubar(self):
        menubar = ttk.Menu(self)
        menu_file = ttk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Open", command=self.open_img)
        menubar.add_cascade(label="File", menu=menu_file)
        self.master.config(menu=menubar)

    def open_img(self):
        self.img = Image.open(self.file_name)
        self.show_img()

    def show_img(self):
        self.img_window = Img(self, self.img)
        # self.wait_window(self.img_window)
        self.after(UPDATE_DELAY, self.update)
    
    def show_plot(self):
        self.info = {
            'file_name':self.file_name,
            'base_info':self.base_pos,
            'ref':'TTCGGACCAATGAAGACTGATCGAGACTATCTCGAACTCCAGAGATTATC',
            'title':self.file_name,
            'threshold':0.1
        }
        self.plot_window = Curve(self,self.info)

    def update(self):
        
        img_w = self.img_window
        if img_w.focus:
            x = self.img_window.x
            y = self.img_window.y
            # ic(x)
            self.img_pos.set(f"x = {int(x)}, y = {int(y)}")
        
        if True:
            self.base_pos[self.current_base] = (int(img_w.pos_nw[0] * img_w.resize_coef),int(img_w.pos_se[0] * img_w.resize_coef))
            self.base_string.set(f'Base: {self.current_base} (x1 = {img_w.pos_nw[0]}, x2 = {img_w.pos_se[0]})')
        A = self.base_pos['A']
        C = self.base_pos['C']
        T = self.base_pos['T']
        G = self.base_pos['G']
        self.base_pos_text.set(f'A: {A[0]},{A[1]}\nC: {C[0]},{C[1]}\nT: {T[0]},{T[1]}\nG: {G[0]},{G[1]}')
        self.after(UPDATE_DELAY, self.update)



