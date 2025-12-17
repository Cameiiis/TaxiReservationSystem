import tkinter as tk
from tkinter import Canvas, messagebox, Scrollbar
from PIL import Image, ImageTk
import os
from datetime import datetime
from functions import get_wallet_data, add_wallet_funds_db
import config

class WalletScreen:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        
        self.window_width = 428
        self.window_height = 926
        
        wallet_data = get_wallet_data()
        self.balance = wallet_data["balance"]
        self.transaction_history = wallet_data["transactions"]
        
        self.root = tk.Toplevel(parent_window)
        self.root.title("Wallet")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - self.window_width) / 2)
        y = int((screen_height - self.window_height) / 2)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg="#D2D2DF")
        
        self.load_images()
        
        self.setup_ui()
        
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
    
    def load_images(self):
        frames_folder = "Python Frames"
        
        self.undo_btn_img = None
        self.add_money_btn_img = None
        
        try:
            undo_path = os.path.join(frames_folder, "undo button.png")
            if os.path.exists(undo_path):
                img = Image.open(undo_path)
                img = img.resize((70, 50), Image.Resampling.LANCZOS)
                self.undo_btn_img = ImageTk.PhotoImage(img)
            
            coupon_path = os.path.join(frames_folder, "apply coupon button.png")
            if os.path.exists(coupon_path):
                img = Image.open(coupon_path)
                img = img.resize((385, 72), Image.Resampling.LANCZOS)
                self.apply_coupon_img = ImageTk.PhotoImage(img)
                
        except Exception as e:
            pass
    
    def setup_ui(self):
        self.canvas = Canvas(
            self.root,
            width=self.window_width,
            height=self.window_height,
            bg="#D2D2DF",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        if self.undo_btn_img:
            undo_btn = tk.Button(
                self.root, image=self.undo_btn_img, border=0, relief="flat",
                cursor="hand2", command=self.go_back,
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            undo_btn.image = self.undo_btn_img
            undo_btn.place(x=5, y=15)
        else:
            undo_btn = tk.Button(
                self.root, text="← Back", font=("Arial", 12, "bold"),
                bg="#3D5AFE", fg="white", border=0, relief="flat",
                cursor="hand2", command=self.go_back,
                width=8, height=1
            )
            undo_btn.place(x=20, y=55)
        
        tk.Label(
            self.root, text="Wallet", font=("Arial", 20, "bold"),
            bg="#D2D2DF", fg="#333"
        ).place(x=214, y=60, anchor="center")
        
        balance_canvas = Canvas(
            self.root, width=390, height=100,
            bg="#D2D2DF", highlightthickness=0
        )
        balance_canvas.place(x=19, y=110)
        
        self.create_rounded_rect_on_canvas(
            balance_canvas, 2, 2, 388, 98, 20,
            fill="#e0e0e0", outline=""
        )
        self.create_rounded_rect_on_canvas(
            balance_canvas, 0, 0, 386, 96, 20,
            fill="white", outline=""
        )
        
        balance_frame = tk.Frame(balance_canvas, bg="white")
        balance_canvas.create_window(193, 48, window=balance_frame)
        
        tk.Label(
            balance_frame, text="Available Balance",
            font=("Arial", 12), bg="white", fg="#999"
        ).pack(anchor="w", padx=15, pady=(12, 0))
        
        self.balance_label = tk.Label(
            balance_frame, text=f"₱{self.balance}",
            font=("Arial", 24, "bold"), bg="white", fg="#333"
        )
        self.balance_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        history_label = tk.Label(
            self.root, text="Transaction History",
            font=("Arial", 14, "bold"), bg="#D2D2DF", fg="#333"
        )
        history_label.place(x=20, y=230)
        
        self.create_transaction_list()
        
        add_btn = tk.Button(
            self.root, text="➕ Add Money", font=("Arial", 14, "bold"),
            bg="#3D5AFE", fg="white", border=0, relief="flat",
            cursor="hand2", command=self.show_add_money_dialog,
            width=35, height=2
        )
        add_btn.place(x=214, y=860, anchor="center")
    
    def create_rounded_rect_on_canvas(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
            x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
            x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
            x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def create_transaction_list(self):
        list_container = tk.Frame(self.root, bg="#D2D2DF", width=390, height=560)
        list_container.place(x=19, y=260)
        list_container.pack_propagate(False)
        
        list_canvas = Canvas(
            list_container, bg="#D2D2DF", highlightthickness=0,
            width=390, height=560
        )
        
        scrollbar = Scrollbar(
            list_container, orient="vertical", command=list_canvas.yview
        )
        
        self.scrollable_frame = tk.Frame(list_canvas, bg="#D2D2DF")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
        )
        
        list_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        list_canvas.configure(yscrollcommand=scrollbar.set)
        
        list_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.populate_transactions()
        
        list_canvas.bind_all("<MouseWheel>", lambda e: list_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def populate_transactions(self):
        for transaction in self.transaction_history:
            self.create_transaction_item(transaction)
    
    def create_transaction_item(self, transaction):
        item_canvas = Canvas(
            self.scrollable_frame, width=370, height=85,
            bg="#D2D2DF", highlightthickness=0
        )
        item_canvas.pack(pady=8, padx=0)
        
        border_color = "#3D5AFE" if transaction["type"] == "deposit" else "#ef4444"
        
        self.create_rounded_rect_on_canvas(
            item_canvas, 3, 3, 368, 83, 15,
            fill="#c0c0c0", outline=""
        )
        
        self.create_rounded_rect_on_canvas(
            item_canvas, 0, 0, 365, 80, 15,
            fill="white", outline=""
        )
        
        self.create_rounded_rect_on_canvas(
            item_canvas, 8, 15, 12, 65, 2,
            fill=border_color, outline=""
        )
        
        content_frame = tk.Frame(item_canvas, bg="white")
        item_canvas.create_window(190, 40, window=content_frame, width=330)
        
        title_text = f"Money Deposited by {transaction['by']}" if transaction["type"] == "deposit" else f"Money Withdrawn by {transaction['by']}"
        tk.Label(
            content_frame, text=title_text,
            font=("Arial", 11, "bold"), bg="white", fg="#333"
        ).pack(anchor="w", padx=15)
        
        amount_color = "#10b981" if transaction["type"] == "deposit" else "#ef4444"
        amount_prefix = "+" if transaction["type"] == "deposit" else "-"
        tk.Label(
            content_frame, text=f"{amount_prefix}₱{transaction['amount']}",
            font=("Arial", 14, "bold"), bg="white", fg=amount_color
        ).pack(anchor="w", padx=15, pady=(2, 0))
        
        tk.Label(
            content_frame, text=transaction['date'],
            font=("Arial", 9), bg="white", fg="#999"
        ).pack(anchor="w", padx=15, pady=(2, 0))
    
    def show_add_money_dialog(self):
        popup_height = int(self.window_height * 0.55)
        
        popup = tk.Frame(self.root, bg="white", borderwidth=0, highlightthickness=0)
        
        popup.bind("<Button-1>", lambda e: "break")
        
        popup_y = self.window_height - popup_height
        popup.place(x=0, y=popup_y, width=self.window_width, height=popup_height)
        
        popup_canvas = Canvas(popup, width=self.window_width, height=popup_height, 
                             bg="white", highlightthickness=0)
        popup_canvas.place(x=0, y=0)
        
        self.create_rounded_rect_on_canvas(
            popup_canvas, 0, 0, self.window_width, popup_height, 25,
            fill="white", outline=""
        )
        
        header = tk.Frame(popup, bg="#3D5AFE", height=70)
        header.place(x=0, y=0, width=self.window_width)
        header.pack_propagate(False)
        
        tk.Label(
            header, text="💰 Add Money to Wallet",
            font=("Arial", 18, "bold"), bg="#3D5AFE", fg="white"
        ).pack(side="left", padx=25, pady=20)
        
        close_btn = tk.Button(
            header, text="✕", font=("Arial", 22, "bold"), bg="#3D5AFE", fg="white",
            border=0, relief="flat", cursor="hand2", 
            command=lambda: popup.destroy(),
            width=3, height=1, activebackground="#2D4AEE", activeforeground="white"
        )
        close_btn.pack(side="right", padx=15, pady=15)
        
        content = tk.Frame(popup, bg="white")
        content.place(x=0, y=70, width=self.window_width, height=popup_height-70)
        
        tk.Label(
            content, text="Enter Amount",
            font=("Arial", 15, "bold"), bg="white", fg="#333"
        ).pack(pady=(20, 15))
        
        entry_canvas = Canvas(content, width=380, height=80, bg="white", highlightthickness=0)
        entry_canvas.pack(pady=10)
        
        self.create_rounded_rect_on_canvas(
            entry_canvas, 2, 2, 378, 78, 20,
            fill="#e0e0e0", outline=""
        )
        self.create_rounded_rect_on_canvas(
            entry_canvas, 0, 0, 376, 76, 20,
            fill="#f8f8f8", outline="#3D5AFE", width=2
        )
        
        entry_frame = tk.Frame(entry_canvas, bg="#f8f8f8")
        entry_canvas.create_window(188, 38, window=entry_frame)
        
        tk.Label(
            entry_frame, text="₱", font=("Arial", 32, "bold"),
            bg="#f8f8f8", fg="#3D5AFE"
        ).pack(side="left", padx=(15, 8))
        
        amount_entry = tk.Entry(
            entry_frame, font=("Arial", 32, "bold"), width=8,
            relief="flat", borderwidth=0, bg="#f8f8f8", fg="#333",
            insertbackground="#3D5AFE"
        )
        amount_entry.pack(side="left", fill="x", expand=True)
        amount_entry.focus()
        
        tk.Label(
            content, text="Quick Select",
            font=("Arial", 13, "bold"), bg="white", fg="#666"
        ).pack(pady=(20, 12))
        
        quick_frame = tk.Frame(content, bg="white")
        quick_frame.pack(pady=12)
        
        quick_amounts = [100, 500, 1000]
        
        for amount in quick_amounts:
            btn_canvas = Canvas(quick_frame, width=115, height=55, bg="white", highlightthickness=0)
            btn_canvas.pack(side="left", padx=6)
            
            self.create_rounded_rect_on_canvas(
                btn_canvas, 2, 2, 113, 53, 15,
                fill="#d0d0d0", outline=""
            )
            rect_id = self.create_rounded_rect_on_canvas(
                btn_canvas, 0, 0, 111, 51, 15,
                fill="#f0f0f0", outline="#3D5AFE", width=2
            )
            
            text_id = btn_canvas.create_text(
                56, 26, text=f"₱{amount}",
                font=("Arial", 15, "bold"), fill="#3D5AFE"
            )
            
            def on_click(a=amount, c=btn_canvas):
                amount_entry.delete(0, tk.END)
                amount_entry.insert(0, str(a))
            
            btn_canvas.bind("<Button-1>", lambda e, cmd=on_click: cmd())
            btn_canvas.bind("<Enter>", lambda e, c=btn_canvas: c.config(cursor="hand2"))
            btn_canvas.bind("<Leave>", lambda e, c=btn_canvas: c.config(cursor=""))
        
        def confirm_add():
            try:
                amount = int(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Invalid Amount", "Please enter a positive amount")
                    return
                
                success, message = add_wallet_funds_db(amount)
                
                if success:
                    self.balance += amount
                    self.balance_label.config(text=f"₱{self.balance}")
                    
                    new_transaction = {
                        "type": "deposit",
                        "amount": amount,
                        "by": "user",
                        "date": datetime.now().strftime("%d %b %I:%M %p")
                    }
                    self.transaction_history.insert(0, new_transaction)
                    
                    for widget in self.scrollable_frame.winfo_children():
                        widget.destroy()
                    self.populate_transactions()
                    
                    popup.destroy()
                    
                    messagebox.showinfo("Success ✓", message)
                    
            except ValueError:
                messagebox.showerror("Invalid Amount", "Please enter a valid number")
        
        confirm_canvas = Canvas(content, width=340, height=60, bg="white", highlightthickness=0)
        confirm_canvas.pack(pady=25)
        
        self.create_rounded_rect_on_canvas(
            confirm_canvas, 2, 2, 338, 58, 15,
            fill="#2D4AEE", outline=""
        )
        self.create_rounded_rect_on_canvas(
            confirm_canvas, 0, 0, 336, 56, 15,
            fill="#3D5AFE", outline=""
        )
        
        confirm_canvas.create_text(
            168, 28, text="💳 Add Money Now",
            font=("Arial", 16, "bold"), fill="white"
        )
        
        confirm_canvas.bind("<Button-1>", lambda e: confirm_add())
        confirm_canvas.bind("<Enter>", lambda e: confirm_canvas.config(cursor="hand2"))
        confirm_canvas.bind("<Leave>", lambda e: confirm_canvas.config(cursor=""))
    
    def go_back(self):
        self.root.destroy()
        if self.parent_window and self.parent_window.winfo_exists():
            self.parent_window.deiconify()
            self.parent_window.lift()
            self.parent_window.focus_force()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    WalletScreen(root)
    root.mainloop()