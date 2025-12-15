import tkinter as tk
from tkinter import Canvas, messagebox, Scrollbar
from PIL import Image, ImageTk
import os
from functions import get_user_vouchers_db
import config

class VoucherScreen:
    def __init__(self, parent_window, payment_screen=None):
        self.parent_window = parent_window
        self.payment_screen = payment_screen  # NEW: Store reference to payment screen
        
        # Window dimensions
        self.window_width = 428
        self.window_height = 926
        
        # Get voucher data from database
        db_vouchers = get_user_vouchers_db()
        
        # Use database data if available, otherwise use sample data
        if db_vouchers:
            self.vouchers = db_vouchers
        else:
            self.vouchers = [
                {
                    "code": "SAVE20",
                    "title": "20% Off Your Ride",
                    "description": "Get 20% discount on your next ride",
                    "discount": "20%",
                    "discount_value": 20,
                    "min_fare": 100,
                    "expiry": "31/12/2024",
                    "status": "Active",
                    "type": "percentage"
                },
                {
                    "code": "FIRST50",
                    "title": "₱50 Off First Ride",
                    "description": "New user exclusive - ₱50 off",
                    "discount": "₱50",
                    "discount_value": 50,
                    "min_fare": 150,
                    "expiry": "31/01/2025",
                    "status": "Active",
                    "type": "fixed"
                },
                {
                    "code": "HALFOFF",
                    "title": "50% Discount",
                    "description": "Half price on rides above ₱200",
                    "discount": "50%",
                    "discount_value": 50,
                    "min_fare": 200,
                    "expiry": "15/12/2024",
                    "status": "Active",
                    "type": "percentage"
                }
            ]
        
        # Create popup window
        self.root = tk.Toplevel(parent_window)
        self.root.title("My Vouchers")
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - self.window_width) / 2)
        y = int((screen_height - self.window_height) / 2)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg="#D2D2DF")
        
        # Load images
        self.load_images()
        
        # Setup UI
        self.setup_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        
        print("✅ Voucher Screen opened")
    
    def load_images(self):
        """Load voucher screen images"""
        frames_folder = "Python Frames"
        
        self.undo_btn_img = None
        
        try:
            # Load undo button
            undo_path = os.path.join(frames_folder, "undo button.png")
            if os.path.exists(undo_path):
                img = Image.open(undo_path)
                img = img.resize((70, 50), Image.Resampling.LANCZOS)
                self.undo_btn_img = ImageTk.PhotoImage(img)
                print(f"✓ Loaded undo button.png")
                
        except Exception as e:
            print(f"Error loading images: {e}")
    
    def setup_ui(self):
        """Setup the voucher screen UI - PREMIUM DESIGN"""
        # Create main canvas
        self.canvas = Canvas(
            self.root,
            width=self.window_width,
            height=self.window_height,
            bg="#D2D2DF",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Header section - cleaner design
        header_frame = tk.Frame(self.root, bg="#D2D2DF", height=100)
        header_frame.place(x=0, y=0, width=self.window_width)
        
        # Back/Undo button (top left)
        if self.undo_btn_img:
            undo_btn = tk.Button(
                self.root, image=self.undo_btn_img, border=0, relief="flat",
                cursor="hand2", command=self.go_back,
                borderwidth=0, highlightthickness=0, bg="#D2D2DF",
                activebackground="#D2D2DF"
            )
            undo_btn.image = self.undo_btn_img
            undo_btn.place(x=5, y=15)
        else:
            # Fallback button
            undo_btn = tk.Button(
                self.root, text="← Back", font=("Arial", 12, "bold"),
                bg="#3D5AFE", fg="white", border=0, relief="flat",
                cursor="hand2", command=self.go_back,
                width=8, height=1
            )
            undo_btn.place(x=20, y=50)
        
        # Title "My Vouchers" - centered, simple and clean
        tk.Label(
            header_frame, text="My Vouchers",
            font=("Arial", 24, "bold"), bg="#D2D2DF", fg="#1a1a1a"
        ).place(relx=0.5, y=55, anchor="center")
        
        # Create scrollable vouchers list
        self.create_vouchers_list()
    
    def create_rounded_rect_on_canvas(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle on a canvas"""
        points = [
            x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
            x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
            x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
            x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def create_vouchers_list(self):
        """Create scrollable vouchers list"""
        # Container frame for scrollable area
        list_container = tk.Frame(self.root, bg="#D2D2DF", width=409, height=810)
        list_container.place(x=10, y=105)
        list_container.pack_propagate(False)
        
        # Create canvas for scrolling
        list_canvas = Canvas(
            list_container, bg="#D2D2DF", highlightthickness=0,
            width=409, height=810
        )
        
        # Scrollbar
        scrollbar = Scrollbar(
            list_container, orient="vertical", command=list_canvas.yview
        )
        
        # Frame inside canvas
        self.scrollable_frame = tk.Frame(list_canvas, bg="#D2D2DF")
        
        # Configure scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
        )
        
        # Create window in canvas
        list_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        list_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        list_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate vouchers
        self.populate_vouchers()
        
        # Enable mouse wheel scrolling
        list_canvas.bind_all("<MouseWheel>", lambda e: list_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def populate_vouchers(self):
        """Populate voucher items"""
        for voucher in self.vouchers:
            self.create_voucher_item(voucher)
    
    def get_status_colors(self, status):
        """Get colors based on status"""
        if status == "Active":
            return "#d1fae5", "#059669"  # Light green bg, dark green text
        elif status == "Expired":
            return "#fee2e2", "#dc2626"  # Light red bg, red text
        else:
            return "#f3f4f6", "#6b7280"  # Light gray bg, gray text
    
    def create_voucher_item(self, voucher):
        """Create a single voucher item card - ULTRA PREMIUM DESIGN"""
        # Container canvas for rounded rectangle - TALLER CARD
        item_canvas = Canvas(
            self.scrollable_frame, width=390, height=175,
            bg="#D2D2DF", highlightthickness=0
        )
        item_canvas.pack(pady=8, padx=0)
        
        # Get colors based on status and type
        if voucher['status'] == "Expired":
            bg_color = "#e8e8e8"
            card_shadow = "#a0a0a0"
        else:
            bg_color = "white"
            card_shadow = "#a8a8a8"
        
        # Accent color based on discount type
        if voucher['type'] == "percentage":
            accent_color = "#3D5AFE"  # Blue for percentage
            accent_light = "#E3F2FD"
        else:
            accent_color = "#10b981"  # Green for fixed amount
            accent_light = "#D1FAE5"
        
        # Draw deeper shadow for depth
        self.create_rounded_rect_on_canvas(
            item_canvas, 4, 4, 390, 174, 22,
            fill=card_shadow, outline=""
        )
        
        # Draw main rounded background
        self.create_rounded_rect_on_canvas(
            item_canvas, 0, 0, 386, 170, 22,
            fill=bg_color, outline=""
        )
        
        # Draw colorful top accent bar (thicker)
        self.create_rounded_rect_on_canvas(
            item_canvas, 0, 0, 386, 12, 22,
            fill=accent_color, outline=""
        )
        
        # Content frame
        content_frame = tk.Frame(item_canvas, bg=bg_color)
        item_canvas.create_window(193, 91, window=content_frame, width=360, height=158)
        
        # Top section - Status badge and large discount
        top_section = tk.Frame(content_frame, bg=bg_color)
        top_section.pack(fill="x", padx=20, pady=(18, 12))
        
        # Status badge (left) - pill shaped
        status_bg, status_fg = self.get_status_colors(voucher['status'])
        status_canvas = Canvas(top_section, width=70, height=24, bg=bg_color, highlightthickness=0)
        status_canvas.pack(side="left")
        
        self.create_rounded_rect_on_canvas(
            status_canvas, 0, 0, 70, 24, 12,
            fill=status_bg, outline=""
        )
        status_canvas.create_text(
            35, 12, text=voucher['status'],
            font=("Arial", 8, "bold"), fill=status_fg
        )
        
        # Large discount circle (right) - eye-catching
        discount_canvas = Canvas(top_section, width=90, height=90, bg=bg_color, highlightthickness=0)
        discount_canvas.pack(side="right")
        
        # Draw circular background with gradient effect (multiple circles)
        for i in range(5, 0, -1):
            discount_canvas.create_oval(
                45-i*9, 45-i*9, 45+i*9, 45+i*9,
                fill=accent_light if i % 2 == 0 else accent_color,
                outline=""
            )
        
        # Main discount circle
        discount_canvas.create_oval(5, 5, 85, 85, fill=accent_color, outline="")
        
        # Discount text
        discount_canvas.create_text(
            45, 45, text=voucher['discount'],
            font=("Arial", 24, "bold"), fill="white"
        )
        
        # Title section
        title_frame = tk.Frame(content_frame, bg=bg_color)
        title_frame.pack(fill="x", padx=20, pady=(0, 8))
        
        tk.Label(
            title_frame, text=voucher['title'],
            font=("Arial", 14, "bold"), bg=bg_color, fg="#1a1a1a", anchor="w"
        ).pack(fill="x")
        
        # Description
        tk.Label(
            content_frame, text=voucher['description'],
            font=("Arial", 10), bg=bg_color, fg="#666", anchor="w"
        ).pack(fill="x", padx=20, pady=(0, 12))
        
        # Bottom info section with better layout
        bottom_section = tk.Frame(content_frame, bg=bg_color)
        bottom_section.pack(fill="x", padx=20, pady=(0, 15))
        
        # Code section (left)
        code_container = tk.Frame(bottom_section, bg=bg_color)
        code_container.pack(side="left")
        
        tk.Label(
            code_container, text="Code:",
            font=("Arial", 8), bg=bg_color, fg="#999"
        ).pack(side="left", padx=(0, 5))
        
        # Code in colored box
        code_label_canvas = Canvas(code_container, width=70, height=22, bg=bg_color, highlightthickness=0)
        code_label_canvas.pack(side="left")
        
        self.create_rounded_rect_on_canvas(
            code_label_canvas, 0, 0, 70, 22, 11,
            fill=accent_light, outline=""
        )
        code_label_canvas.create_text(
            35, 11, text=voucher['code'],
            font=("Arial", 9, "bold"), fill=accent_color
        )
        
        # Expiry section (right)
        expiry_container = tk.Frame(bottom_section, bg=bg_color)
        expiry_container.pack(side="right")
        
        tk.Label(
            expiry_container, text="⏰",
            font=("Arial", 11), bg=bg_color
        ).pack(side="left", padx=(0, 5))
        
        tk.Label(
            expiry_container, text=voucher['expiry'],
            font=("Arial", 9), bg=bg_color, fg="#666"
        ).pack(side="left")
        
        # Overlay for expired vouchers - ENHANCED
        if voucher['status'] == "Expired":
            # Diagonal stripes overlay
            for i in range(-10, 40, 3):
                item_canvas.create_line(
                    i*20, 0, i*20+170, 170,
                    fill="#cccccc", width=8, stipple="gray50"
                )
            
            # Semi-transparent rounded overlay
            self.create_rounded_rect_on_canvas(
                item_canvas, 0, 0, 386, 170, 22,
                fill="gray", outline="", stipple="gray75"
            )
            
            # Expired stamp - centered, larger, more prominent
            stamp_x = 193
            stamp_y = 85
            stamp_width = 140
            stamp_height = 50
            
            # Draw stamp shadow
            self.create_rounded_rect_on_canvas(
                item_canvas, 
                stamp_x - stamp_width//2 + 2, stamp_y - stamp_height//2 + 2,
                stamp_x + stamp_width//2 + 2, stamp_y + stamp_height//2 + 2,
                10, fill="#000000", outline="", stipple="gray50"
            )
            
            # Draw stamp background
            self.create_rounded_rect_on_canvas(
                item_canvas, 
                stamp_x - stamp_width//2, stamp_y - stamp_height//2,
                stamp_x + stamp_width//2, stamp_y + stamp_height//2,
                10, fill="#dc2626", outline="white", width=3
            )
            
            # Draw stamp text
            item_canvas.create_text(
                stamp_x, stamp_y, text="EXPIRED",
                font=("Arial", 16, "bold"), fill="white"
            )
        
        # Make card clickable if active - with hover effect
        if voucher['status'] == "Active":
            def on_card_click(e):
                self.use_voucher(voucher)
            
            def on_enter(e):
                item_canvas.config(cursor="hand2")
                # Add subtle highlight
                self.create_rounded_rect_on_canvas(
                    item_canvas, 0, 0, 386, 170, 22,
                    fill="", outline=accent_color, width=3, tags="highlight"
                )
            
            def on_leave(e):
                item_canvas.config(cursor="")
                item_canvas.delete("highlight")
            
            item_canvas.bind("<Button-1>", on_card_click)
            item_canvas.bind("<Enter>", on_enter)
            item_canvas.bind("<Leave>", on_leave)
    
    def use_voucher(self, voucher):
        """Use/Apply voucher"""
        # If opened from payment screen, apply directly
        if self.payment_screen:
            self.apply_voucher_to_payment(voucher)
            return
        
        # Otherwise show dialog
        self.show_voucher_dialog(voucher)
    
    def apply_voucher_to_payment(self, voucher):
        """Apply voucher directly to payment screen"""
        # Check if payment screen exists and has the method
        if not self.payment_screen or not hasattr(self.payment_screen, 'apply_voucher_from_list'):
            messagebox.showerror("Error", "Cannot apply voucher - payment screen not found")
            return
        
        # Apply the voucher
        success = self.payment_screen.apply_voucher_from_list(voucher)
        
        if success:
            # Close voucher screen
            self.go_back()
            messagebox.showinfo(
                "Voucher Applied! 🎉",
                f"Voucher '{voucher['code']}' has been applied!\n\n"
                f"Discount: {voucher['discount']}"
            )
        else:
            messagebox.showwarning(
                "Cannot Apply",
                f"This voucher requires a minimum fare of ₱{voucher['min_fare']}"
            )
    
    def show_voucher_dialog(self, voucher):
        """Show voucher dialog for standalone use"""
        # Create custom confirmation dialog
        confirm_dialog = tk.Toplevel(self.root)
        confirm_dialog.title("Use Voucher")
        confirm_dialog.geometry("400x480")
        confirm_dialog.configure(bg="white")
        confirm_dialog.resizable(False, False)
        confirm_dialog.transient(self.root)
        confirm_dialog.grab_set()
        
        # Center dialog
        confirm_dialog.update_idletasks()
        x = (confirm_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (confirm_dialog.winfo_screenheight() // 2) - (480 // 2)
        confirm_dialog.geometry(f"+{x}+{y}")
        
        # Accent color
        accent_color = "#3D5AFE" if voucher['type'] == "percentage" else "#10b981"
        
        # Header
        header = tk.Frame(confirm_dialog, bg=accent_color, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header, text="🎟️",
            font=("Arial", 32), bg=accent_color
        ).pack(pady=(20, 5))
        
        tk.Label(
            header, text="Use Voucher",
            font=("Arial", 18, "bold"), bg=accent_color, fg="white"
        ).pack()
        
        # Content
        content = tk.Frame(confirm_dialog, bg="white")
        content.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Voucher title
        tk.Label(
            content, text=voucher['title'],
            font=("Arial", 15, "bold"), bg="white", fg="#1a1a1a"
        ).pack(pady=(0, 20))
        
        # Discount display
        discount_canvas = Canvas(content, width=150, height=150, bg="white", highlightthickness=0)
        discount_canvas.pack(pady=15)
        
        for i in range(75, 60, -5):
            discount_canvas.create_oval(
                75-i, 75-i, 75+i, 75+i,
                fill="#f0f9ff" if voucher['type'] == "percentage" else "#d1fae5",
                outline=""
            )
        
        discount_canvas.create_oval(15, 15, 135, 135, fill=accent_color, outline="")
        discount_canvas.create_text(
            75, 75, text=voucher['discount'],
            font=("Arial", 40, "bold"), fill="white"
        )
        
        # Details
        details_frame = tk.Frame(content, bg="white")
        details_frame.pack(fill="x", pady=20)
        
        info_items = [
            ("Voucher Code", voucher['code']),
            ("Minimum Fare", f"₱{voucher['min_fare']}"),
            ("Valid Until", voucher['expiry'])
        ]
        
        for label, value in info_items:
            row = tk.Frame(details_frame, bg="white")
            row.pack(fill="x", pady=6)
            
            tk.Label(
                row, text=label,
                font=("Arial", 10), bg="white", fg="#999"
            ).pack(side="left")
            
            tk.Label(
                row, text=value,
                font=("Arial", 11, "bold"), bg="white", fg="#1a1a1a"
            ).pack(side="right")
        
        # Info
        info_frame = tk.Frame(content, bg="#f0f9ff" if voucher['type'] == "percentage" else "#d1fae5")
        info_frame.pack(fill="x", pady=(15, 20))
        
        tk.Label(
            info_frame, text="💡 Code will be copied to clipboard",
            font=("Arial", 9), bg=info_frame['bg'], fg="#666"
        ).pack(pady=8)
        
        # Buttons
        btn_frame = tk.Frame(content, bg="white")
        btn_frame.pack(fill="x", pady=5)
        
        def confirm_use():
            self.root.clipboard_clear()
            self.root.clipboard_append(voucher['code'])
            confirm_dialog.destroy()
            messagebox.showinfo(
                "Voucher Copied! 🎉",
                f"Voucher code '{voucher['code']}' copied!\n\n"
                f"Apply it at checkout to get {voucher['discount']} off."
            )
        
        use_btn = tk.Button(
            btn_frame, text="✓ Use This Voucher", font=("Arial", 13, "bold"),
            bg=accent_color, fg="white", border=0, relief="flat",
            cursor="hand2", command=confirm_use, height=2
        )
        use_btn.pack(fill="x", pady=(0, 8))
        
        cancel_btn = tk.Button(
            btn_frame, text="Cancel", font=("Arial", 11),
            bg="white", fg="#666", border=0, relief="flat",
            cursor="hand2", command=confirm_dialog.destroy,
            highlightbackground="#ddd", highlightthickness=1, height=2
        )
        cancel_btn.pack(fill="x")
    
    def go_back(self):
        """Close voucher screen and return"""
        self.root.destroy()
        if self.parent_window and self.parent_window.winfo_exists():
            self.parent_window.deiconify()
            self.parent_window.lift()
            self.parent_window.focus_force()
        print("← Returned from Vouchers")


# Test the voucher screen independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VoucherScreen(root)
    root.mainloop()