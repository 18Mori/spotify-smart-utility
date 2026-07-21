import tkinter as tk
import keyboard, logging
from tkinter import messagebox


# Configure lightweight logging for runtime debugging
logging.basicConfig(level=logging.ERROR, format="%(asctime)s [%(levelname)s] %(message)s")

class SpothashWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg="#191414")
        # self.root.overrideredirect(True)
        self.root.resizable(False, False)
        
        self.geolocation = self.root.winfo_screenwidth() - 700, 100
        self.root.geometry(f"150x40+{self.geolocation[0]}+{self.geolocation[1]}")
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Media button setup
        btn_prev = tk.Button(self.root, text='⏮', command=self.prev_track, fg="white", bg="#191414", bd=0, font=("Arial", 15))
        
        btn_play = tk.Button(self.root, text='⏯', command=self.play_pause, fg="#1DB954", bg="#191414", bd=0, font=("Arial", 15))
        
        btn_next = tk.Button(self.root, text='⏭', command=self.next_track, fg="white", bg="#191414", bd=0, font=("Arial", 15))
        
        btn_prev.pack(side=tk.LEFT, padx=5)
        btn_play.pack(side=tk.LEFT, padx=5)
        btn_next.pack(side=tk.LEFT, padx=5)
        
        
    def send_media_key(self, key_command: str) -> None:
        
        try:
            keyboard.send(key_command)
        except Exception as e:
            error_msg = f"Failed to send media key command '{key_command}': {e}"
            logging.error(error_msg)
            
            # Non-fatal user feedback dialog
            messagebox.showerror(
                title="SpotHash - Media Control Error",
                message=(
                    f"Could not dispatch media key: '{key_command}'.\n\n"
                    f"Error details: {e}\n"
                    "Note: Ensure the app is running with appropriate OS access rights."
                ),
                parent=self.root
            )
        
    #Media key trigger setup
    def play_pause(self):
            self.send_media_key("play/pause media")
            
    def prev_track(self):
            self.send_media_key("previous track")
            
    def next_track(self):
            self.send_media_key("next track")
            
        

if __name__ == "__main__":
    app = SpothashWidget()
    app.root.mainloop()