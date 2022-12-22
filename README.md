# CTkColorPicker
**A modern color picker made for customtkinter!**

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

