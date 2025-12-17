# terms_popup.py - Terms & Conditions Image Popup with Checkbox

import tkinter as tk
from PIL import Image, ImageTk
import os

def show_terms_popup(parent, on_accept_callback):
    """Show Terms & Conditions popup"""
    popup = tk.Toplevel(parent)
    popup.title("Terms & Conditions")
    popup.geometry("428x926")
    popup.configure(bg="white")
    popup.resizable(False, False)
    
    popup.transient(parent)
    popup.grab_set()
    
    popup.update_idletasks()
    x = (popup.winfo_screenwidth() // 2) - (428 // 2)
    y = (popup.winfo_screenheight() // 2) - (926 // 2)
    popup.geometry(f"+{x}+{y}")
    
    canvas = tk.Canvas(
        popup, width=428, height=926,
        bg="white", highlightthickness=0
    )
    canvas.pack(fill="both", expand=True)
    
    frames_folder = "Python Frames"
    terms_img = None
    undo_btn_img = None
    
    try:
        terms_path = os.path.join(frames_folder, "Terms & Condition.png")
        if os.path.exists(terms_path):
            img = Image.open(terms_path)
            img = img.resize((428, 926), Image.Resampling.LANCZOS)
            terms_img = ImageTk.PhotoImage(img)
            canvas.image = terms_img
            canvas.create_image(0, 0, image=terms_img, anchor="nw")
        else:
            canvas.create_text(
                214, 100, text="Terms & Conditions",
                font=("Arial", 24, "bold"), fill="#333"
            )
            canvas.create_text(
                214, 463, 
                text="Terms & Condition.png not found\nin Python Frames folder",
                font=("Arial", 14), fill="#999", justify="center"
            )
    except Exception as e:
        canvas.create_text(
            214, 463, 
            text=f"Error loading image:\n{e}",
            font=("Arial", 12), fill="red", justify="center"
        )
    
    try:
        undo_path = os.path.join(frames_folder, "undo button.png")
        if os.path.exists(undo_path):
            img = Image.open(undo_path)
            img = img.resize((70, 50), Image.Resampling.LANCZOS)
            undo_btn_img = ImageTk.PhotoImage(img)
    except Exception:
        pass
    
    accept_var = tk.BooleanVar(value=False)
    
    checkbox_frame = tk.Frame(popup, bg="white")
    checkbox_frame.place(x=25, y=565)
    
    checkbox_canvas = tk.Canvas(
        checkbox_frame, width=28, height=28, 
        bg="white", highlightthickness=0, cursor="hand2"
    )
    checkbox_canvas.pack(side="left")
    
    def draw_checkbox():
        """Draw the checkbox based on current state"""
        checkbox_canvas.delete("all")
        if accept_var.get():
            checkbox_canvas.create_rectangle(
                2, 2, 26, 26, fill="#3D5AFE", outline="#3D5AFE", width=2
            )
            checkbox_canvas.create_text(
                14, 14, text="✓", font=("Arial", 18, "bold"), fill="white"
            )
        else:
            checkbox_canvas.create_rectangle(
                2, 2, 26, 26, fill="white", outline="#999", width=2
            )
    
    def toggle_checkbox(event=None):
        """Toggle checkbox state"""
        accept_var.set(not accept_var.get())
        draw_checkbox()
        update_button_state()
    
    checkbox_canvas.bind("<Button-1>", toggle_checkbox)
    
    draw_checkbox()
    
    if undo_btn_img:
        decline_btn = tk.Button(
            popup, image=undo_btn_img, border=0, relief="flat",
            cursor="hand2", command=popup.destroy,
            borderwidth=0, highlightthickness=0, bg="white",
            activebackground="white"
        )
        decline_btn.image = undo_btn_img
        decline_btn.place(x=5, y=15)
    else:
        decline_btn = tk.Button(
            popup, text="← Back", 
            font=("Arial", 11, "bold"),
            bg="#ef4444", fg="white", border=0, relief="flat",
            cursor="hand2", command=popup.destroy,
            width=8, height=1, activebackground="#dc2626"
        )
        decline_btn.place(x=10, y=20)
    
    accept_btn = tk.Button(
        popup, text="Accept the Terms & Condition", 
        font=("Arial", 14, "bold"),
        bg="#cccccc", fg="white", border=0, relief="flat",
        width=30, height=2, state="disabled", cursor="arrow"
    )
    accept_btn.place(x=214, y=880, anchor="center")
    
    def update_button_state():
        """Enable/disable accept button based on checkbox"""
        if accept_var.get():
            accept_btn.config(
                bg="#3D5AFE", 
                state="normal", 
                cursor="hand2",
                activebackground="#2D4AEE",
                command=lambda: [popup.destroy(), on_accept_callback()]
            )
        else:
            accept_btn.config(
                bg="#cccccc", 
                state="disabled", 
                cursor="arrow",
                command=None
            )
    
    update_button_state()
    
    def on_closing():
        popup.destroy()
    
    popup.protocol("WM_DELETE_WINDOW", on_closing)
    
    popup.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    def on_accept():
        root.quit()
    
    show_terms_popup(root, on_accept)
    root.mainloop()