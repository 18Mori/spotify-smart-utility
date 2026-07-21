import tkinter as tk
import keyboard

class SpothashWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg="#191414")
        
        # Window setup: Dimensions and position
        self.expanded_width = 150
        self.collapsed_width = 5
        self.height = 40
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Media button setup
        btn_prev = tk.Button(self.root, text='⏮', command=self.prev_track, fg="white", bg="#191414", bd=0, font=("Arial", 12))
        
        btn_play = tk.Button(self.root, text='⏯', command=self.play_pause, fg="#1DB954", bg="#191414", bd=0, font=("Arial", 12))
        
        btn_next = tk.Button(self.root, text='⏭', command=self.next_track, fg="white", bg="#191414", bd=0, font=("Arial", 12))
        
        btn_prev.pack(side=tk.LEFT, padx=5)
        btn_play.pack(side=tk.LEFT, padx=5)
        btn_next.pack(side=tk.LEFT, padx=5)
        
    #Media key trigger setup
    def play_pause(self):
            keyboard.send("play/pause media")
            
    def prev_track(self):
            keyboard.send("previous track")
            
    def next_track(self):
            keyboard.send("next track")
            
        

if __name__ == "__main__":
    app = SpothashWidget()
    app.root.mainloop()