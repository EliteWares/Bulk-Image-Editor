import tkinter as tk

def minimize_window():
    root.iconify()

def close_window():
    root.destroy()

# Create a Tkinter window
root = tk.Tk()

# Remove window decorations
root.overrideredirect(True)



# Add your content here...

# Run the Tkinter event loop
root.mainloop()
