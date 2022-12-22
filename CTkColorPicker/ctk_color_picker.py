# CTk Color Picker by Akash Bora (Akascape)

import tkinter
import customtkinter
from PIL import Image, ImageTk
from colour import Color
import sys
import os

if sys.platform.startswith("win"):
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(0)
    
HEIGHT = 450
WIDTH = 300
PATH = os.path.dirname(os.path.realpath(__file__))

class AskColor(customtkinter.CTkToplevel):
    
    def __init__(self):
        
        super().__init__()
        
        self.title("Choose Color")
        self.maxsize(WIDTH, HEIGHT)
        self.minsize(WIDTH, HEIGHT)
        self.attributes("-topmost", True)
        self.lift()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.after(10)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(padx=20, pady=20, sticky="nswe")
        
        if customtkinter.get_appearance_mode()=="Dark":
            o = 1
        else:
            o = 0
            
        self.canvas = tkinter.Canvas(self.frame, height=200, width=200, highlightthickness=0,
                                bg=customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"][o])
        self.canvas.pack(pady=20)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        self.img1 = Image.open(PATH+'//color_wheel.png').resize((200, 200), Image.Resampling.LANCZOS)
        self.img2 = Image.open(PATH+'//target.png').resize((20, 20), Image.Resampling.LANCZOS)

        self.wheel = ImageTk.PhotoImage(self.img1)
        self.target = ImageTk.PhotoImage(self.img2)

        self.canvas.create_image(100,100, image=self.wheel)
        self.canvas.create_image(100, 100, image=self.target)

        self.slider = customtkinter.CTkSlider(master=self.frame, height=20, border_width=1,
                                              button_length=15, progress_color="white", from_=1, to=100,
                                              number_of_steps=100, command=self.change_shade, button_hover_color=None)
        self.slider.pack(fill="both", pady=(0,15), padx=20)
        self.slider.set(100)

        self.label = customtkinter.CTkLabel(master=self.frame, text_color="#000000", height=50, fg_color="#ffffff",
                                            corner_radius=24, text="#ffffff")
        self.label.pack(fill="both", padx=10)
        
        self.colors = list(Color("#000000").range_to(Color(self.label._fg_color), 101))

        self.button = customtkinter.CTkButton(master=self.frame, text="OK", height=50, corner_radius=24,
                                              command=self._ok_event)
        self.button.pack(fill="both", padx=10, pady=20)
        
        self.after(150, lambda: self.label.focus())
        
        self.grab_set()
        
    def get(self):
        self._color = self.label._fg_color
        self.master.wait_window(self)
        return self._color
    
    def _ok_event(self, event=None):
        self._color = self.label._fg_color
        self.grab_release()
        self.destroy()
        
    def _on_closing(self):
        self._color = None
        self.grab_release()
        self.destroy()
        
    def on_mouse_drag(self, event):
        x = event.x
        y = event.y
        self.canvas.delete("all")
        self.canvas.create_image(100, 100, image=self.wheel)
        self.canvas.create_image(x, y, image=self.target)
        
        try:
            rgb_color = self.img1.getpixel((x,y))
            hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_color)
            self.label.configure(fg_color=hex_color, text=str(hex_color), text_color="black")
            if hex_color=="black":
               self.label.configure(text_color="white")
            self.colors = list(Color("black").range_to(Color(self.label._fg_color), 100))
            self.change_shade(self.slider.get())
        except:
            self.label.configure(text_color="white")
            
        
    def change_shade(self, value):
        self.slider.configure(progress_color=str(self.colors[int(value)-1]))
        self.label.configure(fg_color=self.slider._progress_color, text=self.colors[int(value)-1])
        
        if self.slider.get()<30:
            self.label.configure(text_color="white")
        else:
            self.label.configure(text_color="black")
            
        if str(self.label._fg_color)=="black":
            self.label.configure(text_color="white")


if __name__ == "__main__":
    app = AskColor()               
