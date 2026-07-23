import tkinter as tk
import keyboard, logging
from tkinter import messagebox


# Configure logging for safe error reporting without crashing the app
logger = logging.getLogger(__name__)

class SpothashWidget:
    def __init__(self):
        self.root = tk.Tk()
        
        self.root.configure(bg="#191414")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self.root.wm_attributes("-alpha", 0.9)
        
        
        # Dimensions
        self.y_position = 100
        self.expanded_width = 155
        self.collapsed_width = 5
        self.height = 40

        # Screen positioning
        self.screen_width = self.root.winfo_screenwidth()
        self.x_collapsed = self.screen_width - self.collapsed_width
        self.x_expanded = self.screen_width - self.expanded_width
        
        # Initial window positioning (start collapsed)
        self.root.geometry(f"{self.collapsed_width}x{self.height}+{self.x_collapsed}+{self.y_position}")
        self.root.configure(bg="#1DB954", highlightthickness=1, highlightbackground="#1DB954", highlightcolor="#1DB954")
        
        # Create control frame (DO NOT pack here so it starts truly collapsed)
        self.control_frame = tk.Frame(self.root, bg="#191414")

        # Media button setup
        btn_prev = tk.Button(self.control_frame, text='⏮', command=self.prev_track, fg="white", bg="#191414", bd=0, font=("Arial", 11), activebackground="#191414", activeforeground="#1DB954", cursor="hand2")
        
        btn_play = tk.Button(self.control_frame, text='⏯', command=self.play_pause, fg="#1DB954", bg="#191414", bd=0, font=("Arial", 15), activebackground="#191414", activeforeground="red", cursor="hand2")
        
        btn_next = tk.Button(self.control_frame, text='⏭', command=self.next_track, fg="white", bg="#191414", bd=0, font=("Arial", 11), activebackground="#191414", activeforeground="#1DB954", cursor="hand2")
        
        btn_exit = tk.Button(self.control_frame, text='✖', command=self.root.destroy, fg="white", bg="#191414", bd=0, font=("Arial", 10), activebackground="#191414", activeforeground="red", cursor="hand2")
        
        btn_prev.pack(side=tk.LEFT, padx=5, pady=5)
        btn_play.pack(side=tk.LEFT, padx=5, pady=5)
        btn_next.pack(side=tk.LEFT, padx=5, pady=5)
        btn_exit.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Bind hover events to the root window
        self.root.bind("<Enter>", self.on_hover)
        self.root.bind("<Leave>", self.on_leave)
        
    def on_hover(self, event):
        # Show the control frame on hover
        self.control_frame.pack(fill=tk.BOTH, expand=True)
        # Expand to full width on hover
        self.root.geometry(f"{self.expanded_width}x{self.height}+{self.x_expanded}+{self.y_position}")
            
    def on_leave(self, event):
        # Hide the control frame when the mouse leaves
        self.control_frame.pack_forget()
        # Return to collapsed state
        self.root.geometry(f"{self.collapsed_width}x{self.height}+{self.x_collapsed}+{self.y_position}")
        
    def send_media_key(self, key_command: str) -> None:
        try:
            keyboard.send(key_command)
        except Exception as e:
            error_msg = f"Failed to send media key command '{key_command}': {e}"
            logger.error(error_msg)
            
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
        
    def play_pause(self):
        self.send_media_key("play/pause media")
            
    def prev_track(self):
        self.send_media_key("previous track")
            
    def next_track(self):
        self.send_media_key("next track")
            
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    # Configure lightweight logging for runtime debugging
    logging.basicConfig(level=logging.ERROR, format="%(asctime)s [%(levelname)s] %(message)s")
    
    app = SpothashWidget()
    app.run()