import tkinter as tk

class SpothashWidget:
    def __init__(self):
      self.root = tk.Tk()
      
      # Window setup: Dimensions and position
      self.expanded_width = 150
      self.collapsed_width = 5
      self.height = 40
      
      self.screen_width = self.root.winfo_screenwidth()
      self.screen_height = self.root.winfo_screenheight()
      
      
if __name__ == "__main__":
    app = SpothashWidget()
    app.root.mainloop()