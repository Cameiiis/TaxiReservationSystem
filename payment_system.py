# payment_system.py - Payment Method Screen

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class PaymentMethodScreen:
    def __init__(self, parent_window, ride_type, fare, pickup_address, destination_address, distance):
        self.parent_window = parent_window
        self.ride_type = ride_type
        self.fare = fare
        self.original_fare = fare  # Keep original fare for coupon calculations
        self.pickup_address = pickup_address
        self.destination_address = destination_address
        self.distance = distance
        self.selected_payment = "visa"  # Default selection
        self.coupon_applied = False
        
        # Window dimensions
        self.window_width = 428
        self.window_height = 926
        
        # Create popup window
        self.root = tk.Toplevel(parent_window)
        self.root.title("Payment Method")
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - self.window_width) / 2)
        y = int((screen_height - self.window_height) / 2)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.resizable(False, False)
        
        # Load images
        self.load_images()
        
        # Setup UI
        self.setup_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        
        print("✅ Payment Method Screen opened")
    
    def load_images(self):
        """Load all payment screen images"""
        frames_folder = "Python Frames"
        
        # Initialize all images
        self.payment_frame_img = None
        self.apply_coupon_img = None
        self.apply_btn_img = None
        self.visa_btn_img = None
        self.wallet_btn_img = None
        self.cash_btn_img = None
        self.book_ride_btn_img = None
        self.undo_btn_img = None
        
        try:
            # Load payment frame background
            frame_path = os.path.join(frames_folder, "payment method.png")
            if os.path.exists(frame_path):
                img = Image.open(frame_path)
                img = img.resize((self.window_width, self.window_height), Image.Resampling.LANCZOS)
                self.payment_frame_img = ImageTk.PhotoImage(img)
                print(f"✓ Loaded payment method.png")
            
            # Load undo button (back button)
            undo_path = os.path.join(frames_folder, "undo button.png")
            if os.path.exists(undo_path):
                img = Image.open(undo_path)
                img = img.resize((70, 50), Image.Resampling.LANCZOS)
                self.undo_btn_img = ImageTk.PhotoImage(img)
                print(f"✓ Loaded undo button.png")
            
            # Load apply coupon button
            coupon_path = os.path.join(frames_folder, "apply coupon button.png")
            if os.path.exists(coupon_path):
                img = Image.open(coupon_path)
                img = img.resize((385, 72), Image.Resampling.LANCZOS)
                self.apply_coupon_img = ImageTk.PhotoImage(img)
                print(f"✓ Loaded apply coupon button.png")
            
            # Load apply button
            apply_path = os.path.join(frames_folder, "apply button.png")
            if os.path.exists(apply_path):
                img = Image.open(apply_path)
                img = img.resize((125, 70), Image.Resampling.LANCZOS)
                self.apply_btn_img = ImageTk.PhotoImage(img)
                print(f"✓ Loaded apply button.png")
            
            # Load visa button
            visa_path = os.path.join(frames_folder, "visa button.png")
            if os.path.exists(visa_path):
                img = Image.open(visa_path)
                img = img.resize((385, 85), Image.Resampling.LANCZOS)
                self.visa_btn_img = ImageTk.PhotoImage(img)
                print(f"✓ Loaded visa button.png")
            
            # Load wallet button
            wallet_path = os.path.join(frames_folder, "wallet button.png")
            if os.path.exists(wallet_path):
                img = Image.open(wallet_path)
                img = img.resize((385, 85), Image.Resampling.LANCZOS)
                self.wallet_btn_img = ImageTk.PhotoImage(img)
                print(f"✓ Loaded wallet button.png")
            
            # Load cash button
            cash_path = os.path.join(frames_folder, "cash button.png")
            if os.path.exists(cash_path):
                img = Image.open(cash_path)
                img = img.resize((385, 85), Image.Resampling.LANCZOS)
                self.cash_btn_img = ImageTk.PhotoImage(img)
                print(f"✓ Loaded cash button.png")
            
            # Load book ride button
            book_path = os.path.join(frames_folder, "book ride button.png")
            if os.path.exists(book_path):
                img = Image.open(book_path)
                img = img.resize((285, 65), Image.Resampling.LANCZOS)
                self.book_ride_btn_img = ImageTk.PhotoImage(img)
                print(f"✓ Loaded book ride button.png")
                
        except Exception as e:
            print(f"Error loading payment images: {e}")
    
    def setup_ui(self):
        """Setup the payment screen UI"""
        # Create canvas first for rounded rectangles
        self.canvas = tk.Canvas(
            self.root, width=self.window_width, height=self.window_height,
            bg="#C5C6D0", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Add background image on canvas
        if self.payment_frame_img:
            self.canvas.create_image(0, 0, image=self.payment_frame_img, anchor="nw")
        
        # Back/Undo button (top left corner)
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
            # Fallback text button if image not found
            undo_btn = tk.Button(
                self.root, text="← Back", font=("Arial", 12, "bold"),
                bg="#3D5AFE", fg="white", border=0, relief="flat",
                cursor="hand2", command=self.go_back,
                width=8, height=1
            )
            undo_btn.place(x=20, y=55)
        
        # Apply Coupon button - NOW OPENS VOUCHER SCREEN
        if self.apply_coupon_img:
            apply_coupon_btn = tk.Button(
                self.root, image=self.apply_coupon_img, border=0, relief="flat",
                cursor="hand2", command=self.open_voucher_screen,
                borderwidth=0, highlightthickness=0, bg="#C5C6D0", 
                activebackground="#C5C6D0"
            )
            apply_coupon_btn.image = self.apply_coupon_img
            apply_coupon_btn.place(x=20, y=325)
        
        # Create rounded rectangle for text entry (237x55)
        self.create_rounded_rect(30, 402, 267, 457, 20, fill="white", outline="")
        
        # Coupon text entry
        self.coupon_entry = tk.Entry(
            self.root, font=("Arial", 12), bg="white",
            fg="#AAAAAA", relief="flat", borderwidth=0, width=24, show=""
        )
        self.coupon_entry.place(x=45, y=417)
        self.coupon_entry.insert(0, "Enter coupon code")
        
        # Bind focus events for placeholder
        self.coupon_entry.bind("<FocusIn>", self.on_coupon_focus_in)
        self.coupon_entry.bind("<FocusOut>", self.on_coupon_focus_out)
        self.coupon_entry.bind("<Return>", lambda e: self.apply_coupon())
        
        # Apply button
        if self.apply_btn_img:
            apply_btn = tk.Button(
                self.root, image=self.apply_btn_img, border=0, relief="flat",
                cursor="hand2", command=self.apply_coupon,
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            apply_btn.image = self.apply_btn_img
            apply_btn.place(x=277, y=395, width=125, height=65)
        else:
            # Fallback blue rounded button
            apply_btn = tk.Button(
                self.root, text="Apply", font=("Arial", 12, "bold"),
                bg="#3D5AFE", fg="white", border=0, relief="flat",
                cursor="hand2", command=self.apply_coupon
            )
            apply_btn.place(x=218, y=365, width=125, height=65)
        
        # Visa button
        if self.visa_btn_img:
            self.visa_btn = tk.Button(
                self.root, image=self.visa_btn_img, border=0, relief="flat",
                cursor="hand2", command=lambda: self.select_payment("visa"),
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            self.visa_btn.image = self.visa_btn_img
            self.visa_btn.place(x=22, y=520)
        
        # Wallet button
        if self.wallet_btn_img:
            self.wallet_btn = tk.Button(
                self.root, image=self.wallet_btn_img, border=0, relief="flat",
                cursor="hand2", command=lambda: self.select_payment("wallet"),
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            self.wallet_btn.image = self.wallet_btn_img
            self.wallet_btn.place(x=22, y=620)
        
        # Cash button
        if self.cash_btn_img:
            self.cash_btn = tk.Button(
                self.root, image=self.cash_btn_img, border=0, relief="flat",
                cursor="hand2", command=lambda: self.select_payment("cash"),
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            self.cash_btn.image = self.cash_btn_img
            self.cash_btn.place(x=22, y=720)
        
        # Price display (left side, bottom) - with D2D2DF background
        self.price_label = tk.Label(
            self.root, text=f"P{self.fare:.0f}", 
            font=("Arial", 26, "bold"), bg="#D2D2DF", fg="#3D5AFE"
        )
        self.price_label.place(x=25, y=850)
        
        price_text = tk.Label(
            self.root, text="Price", 
            font=("Arial", 11), bg="#D2D2DF", fg="#666"
        )
        price_text.place(x=25, y=885)
        
        # Book Ride button (bottom center)
        if self.book_ride_btn_img:
            book_btn = tk.Button(
                self.root, image=self.book_ride_btn_img, border=0, relief="flat",
                cursor="hand2", command=self.confirm_payment,
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            book_btn.image = self.book_ride_btn_img
            book_btn.place(x=125, y=850)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle on canvas"""
        points = [
            x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
            x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
            x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
            x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def on_coupon_focus_in(self, event):
        """Handle coupon entry focus in"""
        if self.coupon_entry.get() == "Enter coupon code":
            self.coupon_entry.delete(0, tk.END)
            self.coupon_entry.config(fg="#333")
    
    def on_coupon_focus_out(self, event):
        """Handle coupon entry focus out"""
        if self.coupon_entry.get() == "":
            self.coupon_entry.insert(0, "Enter coupon code")
            self.coupon_entry.config(fg="#AAAAAA")
    
    def open_voucher_screen(self):
        """Open voucher screen to select a voucher"""
        try:
            from voucher_screen import VoucherScreen
            # Open voucher screen with reference to this payment screen
            VoucherScreen(self.root, payment_screen=self)
            print("✅ Voucher screen opened from payment")
        except ImportError as e:
            messagebox.showerror(
                "Voucher Error",
                f"Could not import voucher_screen.py!\n\nMake sure voucher_screen.py is in the same folder.\n\nError: {e}"
            )
        except Exception as e:
            messagebox.showerror("Voucher Error", f"Could not open voucher screen!\n\nError: {e}")
    
    def apply_voucher_from_list(self, voucher):
        """Apply a voucher selected from the voucher screen"""
        # Check if already applied
        if self.coupon_applied:
            messagebox.showwarning(
                "Coupon Already Applied", 
                "You can only use one coupon per ride. Remove the current coupon first."
            )
            return False
        
        # Check minimum fare requirement
        if self.original_fare < voucher['min_fare']:
            return False
        
        # Calculate discount
        if voucher['type'] == "percentage":
            discount = self.original_fare * (voucher['discount_value'] / 100)
        else:  # fixed
            discount = voucher['discount_value']
        
        # Apply discount
        self.fare = self.original_fare - discount
        if self.fare < 0:
            self.fare = 0
        
        # Update price display
        self.price_label.config(text=f"P{self.fare:.0f}")
        self.coupon_applied = True
        
        # Update entry field
        self.coupon_entry.delete(0, tk.END)
        self.coupon_entry.insert(0, f"{voucher['code']} applied!")
        self.coupon_entry.config(state="disabled", fg="#10b981")
        
        print(f"✓ Voucher {voucher['code']} applied - Discount: ₱{discount:.2f}, New fare: ₱{self.fare:.2f}")
        return True
    
    def show_coupon_options(self):
        """Show coupon options"""
        messagebox.showinfo(
            "Apply Coupon", 
            "Available Coupons:\n\n"
            "SAVE20 - 20% discount\n"
            "FIRST10 - ₱10 off first ride\n"
            "HALFOFF - 50% discount\n\n"
            "Enter code below and click Apply"
        )
    
    def apply_coupon(self):
        """Apply coupon code"""
        if self.coupon_applied:
            messagebox.showwarning("Coupon Already Applied", "You can only use one coupon per ride")
            return
        
        coupon = self.coupon_entry.get().strip().upper()
        if not coupon or coupon == "ENTER COUPON CODE":
            messagebox.showwarning("No Coupon", "Please enter a coupon code")
            return
        
        discount = 0
        discount_msg = ""
        
        # Check coupon codes
        if coupon == "SAVE20":
            discount = self.original_fare * 0.20
            discount_msg = f"20% discount applied!\nYou saved ₱{discount:.2f}"
        elif coupon == "FIRST10":
            discount = 10
            discount_msg = f"₱10 off first ride applied!\nYou saved ₱{discount:.2f}"
        elif coupon == "HALFOFF":
            discount = self.original_fare * 0.50
            discount_msg = f"50% discount applied!\nYou saved ₱{discount:.2f}"
        else:
            messagebox.showerror("Invalid Coupon", "Coupon code not valid")
            return
        
        # Apply discount
        self.fare = self.original_fare - discount
        if self.fare < 0:
            self.fare = 0
        
        # Update price display
        self.price_label.config(text=f"P{self.fare:.0f}")
        self.coupon_applied = True
        
        # Clear entry and disable
        self.coupon_entry.delete(0, tk.END)
        self.coupon_entry.insert(0, "Coupon applied!")
        self.coupon_entry.config(state="disabled", fg="#10b981")
        
        messagebox.showinfo("Coupon Applied", discount_msg)
        print(f"✓ Coupon {coupon} applied - New fare: ₱{self.fare:.2f}")
    
    def select_payment(self, method):
        """Select payment method"""
        self.selected_payment = method
        print(f"Selected payment method: {method}")
        
        # Visual feedback
        payment_methods = {
            'visa': '💳 Visa',
            'wallet': '💛 Wallet',
            'cash': '💵 Cash'
        }
        
        messagebox.showinfo(
            "Payment Method Selected", 
            f"{payment_methods.get(method, method.title())} selected as payment method"
        )
    
    def confirm_payment(self):
        """Confirm payment and complete booking"""
        msg = (
            f"📋 Booking Summary\n\n"
            f"Ride Type: {self.ride_type}\n"
            f"Distance: {self.distance:.2f} km\n"
            f"Fare: ₱{self.fare:.2f}\n"
            f"Payment: {self.selected_payment.title()}\n\n"
            f"From: {self.pickup_address}\n\n"
            f"To: {self.destination_address}\n\n"
            f"Confirm payment?"
        )
        
        if messagebox.askyesno("Confirm Payment", msg):
            messagebox.showinfo(
                "Booking Complete! 🎉", 
                f"Payment successful!\n\n"
                f"Your {self.ride_type} is on the way!\n"
                f"Driver arriving in 5-10 minutes 🚕\n\n"
                f"Total Paid: ₱{self.fare:.2f}"
            )
            print(f"✅ Booking complete - {self.ride_type} - ₱{self.fare:.2f} via {self.selected_payment}")
            
            # Close payment window and return to map
            self.close_and_return_to_map()
    
    def go_back(self):
        """Go back to map screen"""
        self.close_and_return_to_map()
        print("← Returned to map screen")
    
    def close_and_return_to_map(self):
        """Close payment window and return to map screen"""
        # Destroy payment window
        self.root.destroy()
        
        # Make sure parent (map) window is visible and focused
        if self.parent_window and self.parent_window.winfo_exists():
            self.parent_window.deiconify()  # Show map window
            self.parent_window.lift()  # Bring to front
            self.parent_window.focus_force()  # Give it focus


# Test the payment screen independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    PaymentMethodScreen(
        root, 
        ride_type="Sedan", 
        fare=150, 
        pickup_address="J.P. Laurel Avenue, Poblacion District, Davao City",
        destination_address="MacArthur Highway, Ma-a, Davao City",
        distance=5.5
    )
    root.mainloop()