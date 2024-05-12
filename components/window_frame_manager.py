import tkinter as tk

class DraggableWindow:
    def __init__(self, root:tk.Tk):
        self.root = root

        # Create a Frame to hold the custom buttons
        
        frame = tk.Frame(self.root, bg="#1F1F1F")
        frame.pack(fill="x")
        # Add custom close button
        close_button = tk.Button(frame,
                                    bg="#1F1F1F",
                                    fg="white",
                                    text="X",
                                    bd=0,
                                    padx=5,
                                    font=("Times New Roman", 12, "bold"),
                                    command=lambda: self.root.destroy())
        close_button.pack(side="right")

        #

        frame.bind("<ButtonPress-1>", self.start_move)
        frame.bind("<ButtonRelease-1>", self.stop_move)
        frame.bind("<B1-Motion>", self.on_move)
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        
    def stop_move(self, event):
        self.x = None
        self.y = None
        
    def on_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

