# CTkColorPicker
**A modern color picker made for customtkinter!**

![Screenshot](https://user-images.githubusercontent.com/89206401/209182773-d76bf05c-610e-4297-aec5-7bb61a11d6d3.jpg)

## Download

```
pip install CTkColorPicker
```

### [<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Akascape/CTkColorPicker?&color=white&label=Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="300">](https://github.com/Akascape/CTkColorPicker/archive/refs/heads/main.zip)

## Requirements
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter)
- [pillow](https://pypi.org/project/Pillow/)

### How to use?
```python
import customtkinter as ctk
from CTkColorPicker import *

def ask_color():
    pick_color = AskColor() # open the color picker
    color = pick_color.get() # get the color string
    button.configure(fg_color=color)
    
root = ctk.CTk()

button = ctk.CTkButton(master=root, text="CHOOSE COLOR", text_color="black", command=ask_color)
button.pack(padx=30, pady=20)
root.mainloop()
```

## Options
| Arguments | Description |
|---------|-------------|
| width | set the overall size of the color picker window |
| title | change the title of color picker window |
| fg_color | change forground color of the color picker frame |
| bg_color | change background color of the color picker frame |
| button_color | change the color of the button and slider |
| button_hover_color | change the hover color of the buttons |
| text | change the default text of the 'OK' button |
| initial_color | set the default color of color picker (currently in beta stage) |
| slider_border | change the border width of slider |
| corner_radius | change the corner radius of all the widgets inside color picker |
| _**other button parameters_ | pass other button arguments if required |

# ColorPickerWidget
**This is a new color picker widget that can be placed inside a customtkinter frame.**

![Screenshot](https://github.com/Akascape/CTkColorPicker/assets/89206401/ca03751a-90a3-45e6-8ba4-745a92ab1c12)

### Usage
```python
from CTkColorPicker import *
import customtkinter

root = customtkinter.CTk()
colorpicker = CTkColorPicker(root, width=500, command=lambda e: print(e))
colorpicker.pack(padx=10, pady=10)
root.mainloop()
```

## Options
| Arguments | Description |
|---------|-------------|
| master | parent widget |
| width | set the overall size of the color picker frame |
| fg_color | change forground color of the color picker frame |
| initial_color | set the default color of color picker (currently in beta stage) |
| slider_border | change the border width of slider |
| corner_radius | change the corner radius of all the widgets inside color picker |
| command | add a command when the color is changed |
| orientation | change orientation of slider and label |
| _**other slider parameters_ | pass other slider arguments if required |

**That's all, hope it will help!**
