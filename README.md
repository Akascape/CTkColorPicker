# CTkColorPicker
**A modern color picker made for customtkinter!**

![Screenshot](https://user-images.githubusercontent.com/89206401/209182773-d76bf05c-610e-4297-aec5-7bb61a11d6d3.jpg)

## Download
### [<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Akascape/CTkColorPicker?&color=white&label=Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="250">](https://github.com/Akascape/CTkColorPicker/archive/refs/heads/main.zip)

## Requirements
- customtkinter

### How to use?
```python
import customtkinter as ctk
from CTkColorPicker import AskColor

def ask_color():
    pick_color = AskColor() # Open the Color Picker
    color = pick_color.get() # Get the color
    button.configure(fg_color=color)
    
root = ctk.CTk()

button = ctk.CTkButton(master=root, text="CHOOSE COLOR", text_color="black", command=ask_color)
button.pack(padx=30, pady=20)
root.mainloop()
```

**Thats all, hope it will help!**
