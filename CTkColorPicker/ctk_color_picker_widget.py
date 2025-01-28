# CTk Color Picker widget for customtkinter
# Author: Akash Bora (Akascape)
# Contributors: Marini Pietro (marini-pietro) TODO: search for potential optimizations

from PIL import Image, ImageTk
from math import atan2, cos, sin, sqrt
import sys, os, customtkinter, tkinter

PATH = os.path.dirname(os.path.realpath(__file__))

class CTkColorPicker(customtkinter.CTkFrame):
    
    def __init__(self,
                 master: any = None,
                 width: int = 300,
                 initial_hex_color: str = "#ffffff",
                 fg_color: str = None,
                 slider_border: int = 1,
                 corner_radius: int = 24,
                 command = None,
                 orientation = "vertical",
                 rgb_entries: bool = False,
                 **slider_kwargs) -> None:
    
        super().__init__(master=master, corner_radius=corner_radius)
        
        WIDTH: int = width if width>=200 else 200 # width cannot be less than 200
        HEIGHT: int = WIDTH + 150 # height cannot be less than 350
        self.are_rgb_entries_present: bool = rgb_entries # Store the value of rgb_entries parameter (useful to consult later when updating the value of entries)
        self.image_dimension: int = int(self._apply_widget_scaling(WIDTH - 100)) # image dimension
        self.target_dimension: int = int(self._apply_widget_scaling(20)) # target dimension
        self.lift() # lift the widget to the top

        self.after(10)       
        self.hex_color: str = initial_hex_color # Set hex color string to parameter
        self.default_rgb: list[int] = [255, 255, 255] # default color is white
        self.rgb_color: list[int] = self.default_rgb[:] # default color is white (slicing is used to create a deep copy of list)
        
        self.corner_radius: int = corner_radius # corner radius of the slider
        self.command = command # command to execute when the color is changed
        self.slider_border: int = 10 if slider_border>=10 else slider_border # slider border cannot be less than 10
        
        # set the foreground color of the slider
        self.fg_color: str = self._apply_appearance_mode(self._fg_color) if fg_color is None else fg_color
        self.configure(fg_color=self.fg_color) # set the foreground color
          
        # create the canvas
        self.canvas: tkinter.Canvas = tkinter.Canvas(self, height=self.image_dimension, width=self.image_dimension, highlightthickness=0, bg=self.fg_color)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag) # bind the mouse drag event to the canvas

        # load the images
        self.color_wheel_image: Image = Image.open(os.path.join(PATH, 'color_wheel.png')).resize((self.image_dimension, self.image_dimension), Image.Resampling.LANCZOS)
        self.target_image: Image = Image.open(os.path.join(PATH, 'target.png')).resize((self.target_dimension, self.target_dimension), Image.Resampling.LANCZOS)

        # convert the images to tkinter images
        self.wheel: ImageTk.PhotoImage = ImageTk.PhotoImage(self.color_wheel_image)
        self.target: ImageTk.PhotoImage = ImageTk.PhotoImage(self.target_image)

        # draw the images on the canvas
        self.canvas.create_image(self.image_dimension/2, self.image_dimension/2, image=self.wheel) # draw the wheel
        self.set_initial_color(initial_hex_color) # set the initial color of the widget on the color wheel
        
        # create the slider
        self.brightness_slider_value: customtkinter.IntVar = customtkinter.IntVar() 
        self.brightness_slider_value.set(255) # set value of brightness slider to 255
        
        self.slider: customtkinter.CTkSlider = customtkinter.CTkSlider(master=self, width=20, border_width=self.slider_border,
                                              button_length=15, progress_color=self.hex_color, from_=0, to=255,
                                              variable=self.brightness_slider_value, number_of_steps=256,
                                              button_corner_radius=self.corner_radius, corner_radius=self.corner_radius,
                                              command=lambda x:self.update_colors(), orientation=orientation, **slider_kwargs)
        
        # create the entry widget
        self.entry: customtkinter.CTkEntry = customtkinter.CTkEntry(master=self, text_color="#000000", width=10, fg_color=self.hex_color,
                            corner_radius=self.corner_radius, textvariable=tkinter.StringVar(value=self.hex_color))
        self.entry.bind("<KeyRelease>", self.on_key_released) # bind key release event to the label
        self.entry.configure(validate='key', validatecommand=(master.register(self.validate_hex_entry), '%P')) # add the validation command to the entry

        # create the rgb entries if required
        if rgb_entries:
            self.rgb_frame: customtkinter.CTkFrame = customtkinter.CTkFrame(master=self, fg_color=self.fg_color) # create a frame for rgb values
            colors: list[str] = ("#000000", "#ffffff") # text colors (automatically selected based on appearance mode (light, dark))
            self.couple_frames: list[customtkinter.CTkFrame] = [customtkinter.CTkFrame(master=self.rgb_frame, fg_color=self.fg_color) for i in range(3)] # create 3 frames to couple the labels and entries
            channel_letters: list[str] = ["R", "G", "B"] # channel letters
            self.rgb_labels: list[customtkinter.CTkLabel] = [customtkinter.CTkLabel(master=self.couple_frames[channel_letters.index(channel_letter)], text_color=colors, text=channel_letter, corner_radius=self.corner_radius) for channel_letter in channel_letters] # create 3 label widgets for rgb values
            self.rgb_entries: list[customtkinter.CTkEntry] = [customtkinter.CTkEntry(master=self.couple_frames[i], text_color=colors, width=50, corner_radius=self.corner_radius,
                                                              textvariable=tkinter.StringVar(value=str(self.rgb_color[i]))) for i in range(3)] # create 3 entry widgets for rgb values
            self.rgb_frame.pack(side="bottom", pady=10, padx=10) # pack the frame

            for i in range(3): # loop through the rgb labels and entries
                self.rgb_labels[i].pack(side="top", padx=(0, 5))

                self.rgb_entries[i].configure(validate='key', validatecommand=(master.register(self.validate_rgb_entry), '%P')) # add the validation command to the entry
                self.rgb_entries[i].pack(side="bottom", padx=(0, 10))
                self.rgb_entries[i].bind("<KeyRelease>", self.on_rgb_key_released) # bind key release event to the rgb entries

                self.couple_frames[i].pack(side="left", pady=(0, 5))

        # pack the widgets based on orientation
        if orientation=="vertical":
            self.canvas.pack(pady=20, side="left", padx=(10,0))
            self.slider.pack(fill="y", pady=15, side="right", padx=(0,10-self.slider_border))
            self.entry.pack(expand=True, fill="both", padx=10, pady=15)
        else:
            self.canvas.pack(pady=15, padx=15)
            self.slider.pack(fill="x", pady=(0,10-self.slider_border), padx=15)
            self.entry.pack(expand=True, fill="both", padx=15, pady=(0,15))
            
    def validate_hex_entry(self, new_value):
        """
        Validate the entry widget key.

        params:
            new_value: str The new value of the entry widget.

        returns:
            bool True if the value is valid, False otherwise.
        """
        return new_value.startswith("#") and len(new_value) <= 7 and all(c in "0123456789abcdefABCDEF" for c in new_value[1:])

    def validate_rgb_entry(self, new_value):
        """
        Validate the rgb entry widget key.

        params:
            new_value: str The new value of the entry widget.

        returns:
            bool True if the value is a digit and it does make the rgb value exceed 255, False otherwise.
        """

        return new_value == "" or (new_value.isdigit() and 0 <= int(new_value) <= 255) # empty string is used to allow deletion of the entry
        
    def on_key_released(self, event) -> None:
        """
        Update the color when the enter key is pressed.
        
        params:
            event: tkinter.Event The event object.
        raises:
            None
        returns:
            None
        """
        
        self.hex_color = self.entry.get() # get the hex color from the entry widget

        if len(self.hex_color) < 7: # if the length of the hex color is not 7 (6 numbers and #)
            self.hex_color = "not valid"
            self.entry.configure(fg_color="#ffffff")
            self.slider.configure(state="disabled") # disable the slider
            self.slider.configure(progress_color="#ffffff") # update the progress color of the slider
        else:
            brightness = self.brightness_slider_value.get() # get the brightness value
            self.rgb_color: list[int] = [int(int(self.hex_color[1:3], 16) * (brightness / 255)), 
                                         int(int(self.hex_color[3:5], 16) * (brightness / 255)), 
                                         int(int(self.hex_color[5:7], 16) * (brightness / 255))] # update the rgb color
            
            self.hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color) # update the hex color based on the rgb color

            self.slider.configure(progress_color=self.hex_color) # update the progress color of the slider
            self.slider.configure(state="normal") # enable the slider

            # update the text color of the label
            self.entry.configure(fg_color=self.hex_color)

        self.update_rgb_entries() # update the rgb entries
        if event.keysym.isdigit(): # if the key is a digit (not backspace or delete because hex code always need 6 characters) TODO: modify the code so the function is not called if the user tries to add an eighth character
            self.update_pointer_position_on_wheel() # update the pointer position on the wheel

    def on_rgb_key_released(self, event) -> None:
        """
        Method used to update the color when any key is released in the rgb entry widgets.

        params:
            event: tkinter.Event The event object.
        raises:
            None
        returns:
            None
        """

        for i, entry in enumerate(self.rgb_entries):
            value = entry.get().lstrip('0') or '0'  # get the value of the entry and remove leading zeros
            self.rgb_color[i] = int(value)  # update the rgb_color list
            entry.configure(textvariable=tkinter.StringVar(value=value))  # update the text variable of the entry
            
        # Gather the rgb values from the entries
        self.rgb_color = [int(entry.get()) for entry in self.rgb_entries]

        #Update the hex color
        self.hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color)

        self.entry.configure(textvariable=tkinter.StringVar(value=self.hex_color)) #Update the text of the entry
        self.entry.configure(fg_color=self.hex_color) # update the text color of the label

        self.slider.configure(progress_color=self.hex_color) # update the progress color of the slider

        if event.keysym.isdigit() or event.keysym in ('BackSpace', 'Delete'): # if the key is a digit or backspace or delete
            self.update_pointer_position_on_wheel() # update the pointer position on the wheel

    def update_rgb_entries(self) -> None:
        """
        Update the rgb entries based on the rgb color.

        params:
            None
        raises:
            None
        returns:
            None
        """
        
        # update the text of the rgb entries
        if self.are_rgb_entries_present: [self.rgb_entries[i].configure(textvariable=tkinter.StringVar(value=str(self.rgb_color[i]))) for i in range(3)] # update the text of the rgb entries (only if they are present) 

    def on_mouse_drag(self, event) -> None:
        """
        Get the color of the target pixel and update the colors.
        
        params:
            event: tkinter.Event The event object.
        raises:
            None
        returns:
            None
        """

        self.canvas.delete("all") # clear the canvas
        self.canvas.create_image(self.image_dimension/2, self.image_dimension/2, image=self.wheel) # redraw the wheel
        
        x, y = event.x, event.y # get the x and y coordinates of the mouse
        d_from_center = sqrt(((self.image_dimension/2)-x)**2 + ((self.image_dimension/2)-y)**2) # distance from center
        
        if d_from_center < self.image_dimension // 2: # if the distance from the center is less than the radius of the wheel
            self.target_x, self.target_y = x, y # set the target coordinates
        else: # if the distance from the center is greater than the radius of the wheel (still track mouse movement if outside the wheel)
            self.target_x, self.target_y = self.projection_on_circle(x, y, self.image_dimension/2, self.image_dimension/2, self.image_dimension/2 -1)

        self.canvas.create_image(self.target_x, self.target_y, image=self.target) # draw the target
        
        self.get_target_color() # get the color of the target pixel
        self.update_colors() # update the colors
        self.update_rgb_entries() # update the rgb entries
    
    def update_colors(self) -> None:
        """
        Update the colors of the slider and the label.

        params:
            None
        raises:
            None
        returns:
            None
        """

        brightness = self.brightness_slider_value.get() # get the brightness value

        self.get_target_color() # get the color of the target pixel

        self.rgb_color = [int(self.rgb_color[0] * (brightness/255)), 
                          int(self.rgb_color[1] * (brightness/255)),
                          int(self.rgb_color[2] * (brightness/255))] # update the rgb color
        
        #update the rgb entries
        self.update_rgb_entries()

        self.hex_color = "#{:02x}{:02x}{:02x}".format(*self.rgb_color) # update the hex color
        
        self.slider.configure(progress_color=self.hex_color) # update the progress color of the slider
        self.entry.configure(fg_color=self.hex_color)  # update the text color of the label
        
        label_text = tkinter.StringVar(value=self.hex_color)
        self.entry.configure(textvariable=label_text) # update the text of the label
        
        # change text color based on brightness
        if self.brightness_slider_value.get() < 70: self.entry.configure(text_color="white")
        else: self.entry.configure(text_color="black")
            
        if str(self.entry._fg_color)=="black": self.entry.configure(text_color="white")

        if self.command: self.command(self.get())

    def get_target_color(self) -> None:
        """
        Get the color of the target pixel.
        
        params:
            None
        raises:
            AttributeError if the target pixel is out of bounds
        returns:
            None
        """

        try:
            self.rgb_color = self.color_wheel_image.getpixel((self.target_x, self.target_y))
            
            r = self.rgb_color[0]
            g = self.rgb_color[1]
            b = self.rgb_color[2]    
            self.rgb_color = [r, g, b]
            
        except AttributeError:
            self.rgb_color = self.default_rgb

    def set_initial_color(self, initial_color):
        """
        Set the initial color of the widget on the color wheel.
        Still in beta stage cannot find all colors accurately.

        params:
            initial_color: str The initial color of the widget.
        raises:
            None
        returns:
            None
        """
        
        self.rgb_color = [int(initial_color[1:3], 16), int(initial_color[3:5], 16), int(initial_color[5:7], 16)] # get the rgb color from the hex color
        self.target_x, self.target_y = self.find_color_coords(self.rgb_color) # find the coordinates of the color on the color wheel
                    
        self.canvas.create_image(self.target_x, self.target_y, image=self.target) # draw the target

    def update_pointer_position_on_wheel(self) -> None:
        """
        Update the position of the pointer on the wheel based on the rgb color.

        params:
            None
        raises:
            None
        returns:
            None
        """
        
        # Find the coordinates of the color on the color wheel
        self.target_x, self.target_y = self.find_color_coords(self.rgb_color)
        print(f" - updating pointer position on wheel to {self.target_x, self.target_y}")

        # Update the position of the pointer
        self.canvas.delete("all")
        self.canvas.create_image(self.image_dimension / 2, self.image_dimension / 2, image=self.wheel)
        self.canvas.create_image(self.target_x, self.target_y, image=self.target)

    def find_color_coords(self, color) -> tuple[int, int]:
        """
        Find the coordinates of a color on the color wheel.

        params:
            color: tuple[int, int, int] - tuple The color (r, g, b).
        raises:
            None
        returns:
            tuple[int, int] The x and y coordinates of the color. 
            tuple[int, int] The middle of the image if the color is not found.
        """
        width = height = self.image_dimension
        
        for i in range(width):
            for j in range(height):
                r, g, b = self.color_wheel_image.getpixel((i, j))[:-1]
                if (color[0], color[1], color[2]) == (r, g, b):
                    print(f"Found color at {i, j}", end=" ")
                    return i, j
                
        print("Color not found defaulting to center of the image", end=" ")
        return width//2, height//2
        
    def projection_on_circle(self, point_x, point_y, circle_x, circle_y, radius) -> tuple[int, int]:
        """
        Get the projection of a point on a circle.
        Used to figure out the closest point on the circle to the given point to place the target on the color wheel even if the user presses outside of it.

        params:
            point_x: int The x-coordinate of the point.
            point_y: int The y-coordinate of the point.
            circle_x: int The x-coordinate of the center of the circle.
            circle_y: int The y-coordinate of the center of the circle.
            radius: int The radius of the circle.
        raises:
            None
        returns:
            tuple[int, int] The x and y coordinates of the projection.
        """
        angle = atan2(point_y - circle_y, point_x - circle_x)
        projection_x = circle_x + radius * cos(angle)
        projection_y = circle_y + radius * sin(angle)

        return projection_x, projection_y
    
    def get(self):
        """
        Get the color of the widget.
        Returns not valid if the color is not valid.
        """
        self._color = self.entry._fg_color
        return self._color
    
    def destroy(self) -> None:
        """
        Destroy the widget and its elements.
        
        params:
            None
        raises:
            None
        returns:
            None
        """

        super().destroy()
        del self.color_wheel_image
        del self.target_image
        del self.wheel
        del self.target
        