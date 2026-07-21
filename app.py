import tkinter as tk

# main window
root = tk.Tk()
root.title("My First Tkinter App")
root.geometry("300x200")

# Add a simple test text
label = tk.Label(root, text="SPOTHASH!", font=("Arial", 16))
label.pack(pady=50)

# Start the app loop
root.mainloop()