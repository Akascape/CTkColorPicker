# CTk Color Picker for ctk
# Original Author: Akash Bora (Akascape)
# Contributers: iamironman0

import math
import os
import re
import tkinter

import customtkinter as ctk
from PIL import Image, ImageTk

PATH = os.path.dirname(os.path.realpath(__file__))
LOGO = f"{PATH}\\logo.ico"


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_height = int((screen_width / 2) - (width / 2))
    window_width = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{window_height}+{window_width}")


class AskColor(ctk.CTkToplevel):

    def __init__(self,
                 width: int = 300,
                 title: str = "Choose Color",
                 initial_color: str = None,
                 bg_color: str = None,
                 fg_color: str = None,
                 button_color: str = None,
                 button_hover_color: str = None,
                 text: str = "OK",
                 corner_radius: int = 8,
                 slider_border: int = 1):

        super().__init__()

        self.title(title)
        WIDTH = width if width >= 200 else 200
        HEIGHT = WIDTH + 150
        self.image_dimension = self._apply_window_scaling(WIDTH - 100)
        self.target_dimension = self._apply_window_scaling(20)

        self.maxsize(WIDTH, HEIGHT)
        self.minsize(WIDTH, HEIGHT)
        self.resizable(width=False, height=False)
        center_window(self, WIDTH, HEIGHT)
        self.transient(self.master)
        self.after(250, lambda: self.iconbitmap(LOGO))
        self.after(100, self.lift)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.after(10)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.default_hex_color = "#ffffff"
        self.default_rgb = [255, 255, 255]
        self.rgb_color = self.default_rgb[:]
        self.initial_color = initial_color
        self.light_color = "#ffffff"
        self.dark_color = "#ffffff"
        self.list_color = [self.light_color, self.dark_color]

        self.configure_colors(bg_color, fg_color, button_color, button_hover_color)

        self.button_text = text
        self.corner_radius = corner_radius
        self.slider_border = 10 if slider_border >= 10 else slider_border

        self.config(bg=self.bg_color)

        self.segmented_button = ctk.CTkSegmentedButton(self, values=["Light", "Dark", "Custom"],
                                                       command=self.change_mode)
        self.segmented_button.set("Light")
        self.segmented_button.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")

        self.frame = ctk.CTkFrame(master=self, fg_color=self.fg_color, bg_color=self.bg_color)
        self.frame.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")

        self.change_mode("Light")

        self.grab_set()

    def configure_colors(self, bg_color, fg_color, button_color, button_hover_color):
        theme = ctk.ThemeManager.theme
        self.bg_color = self._apply_appearance_mode(theme["CTkFrame"]["fg_color"]) if bg_color is None else bg_color
        self.fg_color = self._apply_appearance_mode(theme["CTkFrame"]["top_fg_color"]) if fg_color is None else fg_color
        self.button_color = self._apply_appearance_mode(
            theme["CTkButton"]["fg_color"]) if button_color is None else button_color
        self.button_hover_color = self._apply_appearance_mode(
            theme["CTkButton"]["hover_color"]) if button_hover_color is None else button_hover_color

    def clear_widgets(self):
        for widget in self.frame.winfo_children():
            widget.pack_forget()

    def update_color_if_valid(self, index, color):
        if self.is_valid_hex_color(color):
            self.list_color[index] = color

    def change_mode(self, value):
        self.clear_widgets()

        if value == "Light":
            self.create_color_widgets(self.light_color)
            self.set_initial_color(self.light_color)
        elif value == "Dark":
            self.create_color_widgets(self.dark_color)
            self.set_initial_color(self.dark_color)
        else:
            self.create_custom_widgets()

        print(self.list_color)

    def create_custom_widgets(self):
        light_label = ctk.CTkLabel(self.frame, text="Light Color (HEX)")
        light_label.pack(padx=20, pady=(20, 5), fill="both")
        self.light_entry = ctk.CTkEntry(self.frame, placeholder_text="#ffffff")
        self.light_entry.pack(padx=20, pady=(5, 10), fill="both")

        dark_label = ctk.CTkLabel(self.frame, text="Dark Color (HEX)")
        dark_label.pack(padx=20, pady=(10, 5), fill="both")
        self.dark_entry = ctk.CTkEntry(self.frame, placeholder_text="#ffffff")
        self.dark_entry.pack(padx=20, pady=(5, 10), fill="both")

        button = ctk.CTkButton(master=self.frame, text=self.button_text, command=self.custom_callback)
        button.pack(padx=20, pady=20, fill="both")

    def create_color_widgets(self, color_mode):
        self.canvas = tkinter.Canvas(self.frame, height=self.image_dimension, width=self.image_dimension,
                                     highlightthickness=0, bg=self.fg_color)
        self.canvas.pack(pady=20)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        self.img1 = Image.open(os.path.join(PATH, 'color_wheel.png')).resize(
            (self.image_dimension, self.image_dimension), Image.Resampling.LANCZOS)
        self.img2 = Image.open(os.path.join(PATH, 'target.png')).resize((self.target_dimension, self.target_dimension),
                                                                        Image.Resampling.LANCZOS)

        self.wheel = ImageTk.PhotoImage(self.img1)
        self.target = ImageTk.PhotoImage(self.img2)

        self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.wheel)
        self.set_initial_color(self.initial_color)

        self.brightness_slider_value = ctk.IntVar()
        self.brightness_slider_value.set(255)

        self.slider = ctk.CTkSlider(master=self.frame, height=20, border_width=self.slider_border,
                                    button_length=15, progress_color=color_mode, from_=0, to=255,
                                    variable=self.brightness_slider_value, number_of_steps=256,
                                    button_corner_radius=self.corner_radius, corner_radius=self.corner_radius,
                                    button_color=self.button_color,
                                    button_hover_color=self.button_hover_color,
                                    command=lambda x: self.update_colors())
        self.slider.pack(fill="both", pady=(0, 15), padx=20 - self.slider_border)

        self.label = ctk.CTkLabel(master=self.frame, text_color="#000000", height=40,
                                  fg_color=color_mode,
                                  corner_radius=self.corner_radius, text=color_mode)
        self.label.pack(fill="both", padx=10)

        self.button = ctk.CTkButton(master=self.frame, text=self.button_text, height=50,
                                    corner_radius=self.corner_radius, fg_color=self.button_color,
                                    hover_color=self.button_hover_color, command=self._ok_event)
        self.button.pack(fill="both", padx=10, pady=20)

        self.after(150, lambda: self.label.focus())

    def custom_callback(self):
        self.update_color_if_valid(0, self.light_entry.get())
        self.update_color_if_valid(1, self.dark_entry.get())
        self._ok_event()

    @staticmethod
    def is_valid_hex_color(color):
        return bool(re.fullmatch(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color))

    def get(self):
        self.master.wait_window(self)
        return self.list_color

    def _ok_event(self, event=None):
        self.grab_release()
        self.destroy()
        del self.img1
        del self.img2
        del self.wheel
        del self.target

    def _on_closing(self):
        self.list_color = None
        self.grab_release()
        self.destroy()
        del self.img1
        del self.img2
        del self.wheel
        del self.target

    def on_mouse_drag(self, event):
        self.canvas.delete("all")
        self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.wheel)

        d_from_center = self.calculate_distance_from_center(event.x, event.y)

        self.update_target_position(d_from_center, event.x, event.y)

        self.canvas.create_image(self.target_x, self.target_y, image=self.target)

        self.get_target_color()
        self.update_colors()

    def calculate_distance_from_center(self, x, y):
        return math.sqrt(((self.image_dimension / 2) - x) ** 2 + ((self.image_dimension / 2) - y) ** 2)

    def update_target_position(self, d_from_center, x, y):
        if d_from_center < self.image_dimension / 2:
            self.target_x, self.target_y = x, y
        else:
            self.target_x, self.target_y = self.projection_on_circle(x, y, self.image_dimension / 2,
                                                                     self.image_dimension / 2,
                                                                     self.image_dimension / 2 - 1)

    def get_target_color(self):
        try:
            self.rgb_color = self.extract_rgb_color(self.img1.getpixel((self.target_x, self.target_y)))
        except AttributeError:
            self.rgb_color = self.default_rgb

    @staticmethod
    def extract_rgb_color(color):
        r, g, b = color[:3]
        return [r, g, b]

    def update_colors(self):
        brightness = self.brightness_slider_value.get()

        self.get_target_color()

        self.update_rgb_color(brightness)

        if self.segmented_button.get() == "Light":
            self.default_hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)
            self.light_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)
            self.slider.configure(progress_color=self.light_color)
            self.label.configure(fg_color=self.light_color)

            self.label.configure(text=str(self.light_color))
        elif self.segmented_button.get() == "Dark":
            self.default_hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)
            self.dark_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)
            self.slider.configure(progress_color=self.dark_color)
            self.label.configure(fg_color=self.dark_color)

            self.label.configure(text=str(self.dark_color))

        self.list_color = [self.light_color, self.dark_color]

        self.update_text_color()

    def update_rgb_color(self, brightness):
        r = int(self.rgb_color[0] * (brightness / 255))
        g = int(self.rgb_color[1] * (brightness / 255))
        b = int(self.rgb_color[2] * (brightness / 255))

        self.rgb_color = [r, g, b]

    def update_text_color(self):
        if self.brightness_slider_value.get() < 70 or str(self.label._fg_color) == "black":
            self.label.configure(text_color="white")
        else:
            self.label.configure(text_color="black")

    def projection_on_circle(self, point_x, point_y, circle_x, circle_y, radius):
        angle = math.atan2(point_y - circle_y, point_x - circle_x)
        projection_x = circle_x + radius * math.cos(angle)
        projection_y = circle_y + radius * math.sin(angle)

        return projection_x, projection_y

    def set_initial_color(self, initial_color):
        if initial_color and initial_color.startswith("#"):
            try:
                r, g, b = tuple(int(initial_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
            except ValueError:
                return

            self.default_hex_color = initial_color
            if not self.set_target_to_matching_color(r, g, b):
                self.set_target_to_center()

    def set_target_to_matching_color(self, r, g, b):
        for i in range(0, self.image_dimension):
            for j in range(0, self.image_dimension):
                self.rgb_color = self.img1.getpixel((i, j))
                if (self.rgb_color[0], self.rgb_color[1], self.rgb_color[2]) == (r, g, b):
                    self.canvas.create_image(i, j, image=self.target)
                    self.target_x = i
                    self.target_y = j
                    return True
        return False

    def set_target_to_center(self):
        self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.target)


if __name__ == "__main__":
    app = AskColor()
    app.mainloop()
