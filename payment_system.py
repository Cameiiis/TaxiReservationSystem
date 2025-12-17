import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from database_manager import db
import config

class PaymentMethodScreen:
    def __init__(self, parent_window, ride_type, fare, pickup_address, destination_address, distance, pickup_coords=None, destination_coords=None):
        self.parent_window = parent_window
        self.ride_type = ride_type
        self.fare = fare
        self.original_fare = fare
        self.pickup_address = pickup_address
        self.destination_address = destination_address
        self.distance = distance
        self.pickup_coords = pickup_coords
        self.destination_coords = destination_coords
        self.selected_payment = "cash"
        self.coupon_applied = False
        self.applied_voucher_code = None
        
        self.window_width = 428
        self.window_height = 926
        
        self.root = tk.Toplevel(parent_window)
        self.root.title("Payment Method")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - self.window_width) / 2)
        y = int((screen_height - self.window_height) / 2)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.resizable(False, False)
        
        self.load_images()
        
        self.setup_ui()
        
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
    
    def load_images(self):
        frames_folder = "Python Frames"
        
        self.payment_frame_img = None
        self.apply_coupon_img = None
        self.apply_btn_img = None
        self.visa_btn_img = None
        self.wallet_btn_img = None
        self.cash_btn_img = None
        self.book_ride_btn_img = None
        self.undo_btn_img = None
        
        try:
            frame_path = os.path.join(frames_folder, "payment method.png")
            if os.path.exists(frame_path):
                img = Image.open(frame_path)
                img = img.resize((self.window_width, self.window_height), Image.Resampling.LANCZOS)
                self.payment_frame_img = ImageTk.PhotoImage(img)
            
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
            
            apply_path = os.path.join(frames_folder, "apply button.png")
            if os.path.exists(apply_path):
                img = Image.open(apply_path)
                img = img.resize((125, 70), Image.Resampling.LANCZOS)
                self.apply_btn_img = ImageTk.PhotoImage(img)
            
            visa_path = os.path.join(frames_folder, "visa button.png")
            if os.path.exists(visa_path):
                img = Image.open(visa_path)
                img = img.resize((385, 85), Image.Resampling.LANCZOS)
                self.visa_btn_img = ImageTk.PhotoImage(img)
            
            wallet_path = os.path.join(frames_folder, "wallet button.png")
            if os.path.exists(wallet_path):
                img = Image.open(wallet_path)
                img = img.resize((385, 85), Image.Resampling.LANCZOS)
                self.wallet_btn_img = ImageTk.PhotoImage(img)
            
            cash_path = os.path.join(frames_folder, "cash button.png")
            if os.path.exists(cash_path):
                img = Image.open(cash_path)
                img = img.resize((385, 85), Image.Resampling.LANCZOS)
                self.cash_btn_img = ImageTk.PhotoImage(img)
            
            book_path = os.path.join(frames_folder, "book ride button.png")
            if os.path.exists(book_path):
                img = Image.open(book_path)
                img = img.resize((285, 65), Image.Resampling.LANCZOS)
                self.book_ride_btn_img = ImageTk.PhotoImage(img)
                
        except Exception as e:
            pass
    
    def setup_ui(self):
        self.canvas = tk.Canvas(
            self.root, width=self.window_width, height=self.window_height,
            bg="#C5C6D0", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        if self.payment_frame_img:
            self.canvas.create_image(0, 0, image=self.payment_frame_img, anchor="nw")
        
        if self.undo_btn_img:
            undo_btn = tk.Button(
                self.root, image=self.undo_btn_img, border=0, relief="flat",
                cursor="hand2", command=self.go_back,
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            undo_btn.image = self.undo_btn_img
            undo_btn.place(x=5, y=15)
        
        if self.apply_coupon_img:
            apply_coupon_btn = tk.Button(
                self.root, image=self.apply_coupon_img, border=0, relief="flat",
                cursor="hand2", command=self.open_voucher_screen,
                borderwidth=0, highlightthickness=0, bg="#C5C6D0", 
                activebackground="#C5C6D0"
            )
            apply_coupon_btn.image = self.apply_coupon_img
            apply_coupon_btn.place(x=20, y=325)
        
        self.create_rounded_rect(30, 402, 267, 457, 20, fill="white", outline="")
        
        self.coupon_entry = tk.Entry(
            self.root, font=("Arial", 12), bg="white",
            fg="#AAAAAA", relief="flat", borderwidth=0, width=24, show=""
        )
        self.coupon_entry.place(x=45, y=417)
        self.coupon_entry.insert(0, "Enter coupon code")
        
        self.coupon_entry.bind("<FocusIn>", self.on_coupon_focus_in)
        self.coupon_entry.bind("<FocusOut>", self.on_coupon_focus_out)
        self.coupon_entry.bind("<Return>", lambda e: self.apply_coupon())
        
        if self.apply_btn_img:
            apply_btn = tk.Button(
                self.root, image=self.apply_btn_img, border=0, relief="flat",
                cursor="hand2", command=self.apply_coupon,
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            apply_btn.image = self.apply_btn_img
            apply_btn.place(x=277, y=395, width=125, height=65)
        
        if self.visa_btn_img:
            self.visa_btn = tk.Button(
                self.root, image=self.visa_btn_img, border=0, relief="flat",
                cursor="hand2", command=lambda: self.select_payment("visa"),
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            self.visa_btn.image = self.visa_btn_img
            self.visa_btn.place(x=22, y=520)
        
        if self.wallet_btn_img:
            self.wallet_btn = tk.Button(
                self.root, image=self.wallet_btn_img, border=0, relief="flat",
                cursor="hand2", command=lambda: self.select_payment("wallet"),
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            self.wallet_btn.image = self.wallet_btn_img
            self.wallet_btn.place(x=22, y=620)
        
        if self.cash_btn_img:
            self.cash_btn = tk.Button(
                self.root, image=self.cash_btn_img, border=0, relief="flat",
                cursor="hand2", command=lambda: self.select_payment("cash"),
                borderwidth=0, highlightthickness=0, bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
            self.cash_btn.image = self.cash_btn_img
            self.cash_btn.place(x=22, y=720)
        
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
        points = [
            x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
            x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
            x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
            x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def on_coupon_focus_in(self, event):
        if self.coupon_entry.get() == "Enter coupon code":
            self.coupon_entry.delete(0, tk.END)
            self.coupon_entry.config(fg="#333")
    
    def on_coupon_focus_out(self, event):
        if self.coupon_entry.get() == "":
            self.coupon_entry.insert(0, "Enter coupon code")
            self.coupon_entry.config(fg="#AAAAAA")
    
    def open_voucher_screen(self):
        try:
            from voucher_screen import VoucherScreen
            VoucherScreen(self.root, payment_screen=self)
        except Exception as e:
            messagebox.showerror("Voucher Error", f"Could not open voucher screen!\n\nError: {e}")
    
    def apply_voucher_from_list(self, voucher):
        if self.coupon_applied:
            messagebox.showwarning("Coupon Already Applied", "You can only use one coupon per ride.")
            return False
        
        if self.original_fare < voucher['min_fare']:
            return False
        
        if voucher['type'] == "percentage":
            discount = self.original_fare * (voucher['discount_value'] / 100)
        else:
            discount = voucher['discount_value']
        
        self.fare = self.original_fare - discount
        if self.fare < 0:
            self.fare = 0
        
        self.price_label.config(text=f"P{self.fare:.0f}")
        self.coupon_applied = True
        self.applied_voucher_code = voucher['code']
        
        self.coupon_entry.delete(0, tk.END)
        self.coupon_entry.insert(0, f"{voucher['code']} applied!")
        self.coupon_entry.config(state="disabled", fg="#10b981")
        
        return True
    
    def apply_coupon(self):
        if self.coupon_applied:
            messagebox.showwarning("Coupon Already Applied", "You can only use one coupon per ride")
            return
        
        coupon = self.coupon_entry.get().strip().upper()
        if not coupon or coupon == "ENTER COUPON CODE":
            messagebox.showwarning("No Coupon", "Please enter a coupon code")
            return
        
        discount = 0
        
        if coupon == "SAVE20":
            discount = self.original_fare * 0.20
        elif coupon == "FIRST10":
            discount = 10
        elif coupon == "HALFOFF":
            discount = self.original_fare * 0.50
        else:
            messagebox.showerror("Invalid Coupon", "Coupon code not valid")
            return
        
        self.fare = self.original_fare - discount
        if self.fare < 0:
            self.fare = 0
        
        self.price_label.config(text=f"P{self.fare:.0f}")
        self.coupon_applied = True
        self.applied_voucher_code = coupon
        
        self.coupon_entry.delete(0, tk.END)
        self.coupon_entry.insert(0, "Coupon applied!")
        self.coupon_entry.config(state="disabled", fg="#10b981")
        
        messagebox.showinfo("Coupon Applied", f"Discount applied! You saved ₱{discount:.2f}")
    
    def select_payment(self, method):
        self.selected_payment = method
        payment_methods = {'visa': '💳 Visa', 'wallet': '💛 Wallet', 'cash': '💵 Cash'}
        messagebox.showinfo("Payment Method Selected", f"{payment_methods.get(method, method.title())} selected")
    
    def confirm_payment(self):
        if not config.CURRENT_USER_ID:
            messagebox.showerror("Not Logged In", "Please log in to book a ride")
            return
        
        display_pickup = self.pickup_address
        display_destination = self.destination_address
        
        if "Loading" in display_pickup and self.pickup_coords:
            display_pickup = f"{self.pickup_coords[0]:.5f}, {self.pickup_coords[1]:.5f}"
        
        if "Loading" in display_destination and self.destination_coords:
            display_destination = f"{self.destination_coords[0]:.5f}, {self.destination_coords[1]:.5f}"
        
        msg = (
            f"📋 Booking Summary\n\n"
            f"Ride Type: {self.ride_type}\n"
            f"Distance: {self.distance:.2f} km\n"
            f"Fare: ₱{self.fare:.2f}\n"
            f"Payment: {self.selected_payment.title()}\n\n"
            f"From: {display_pickup}\n\n"
            f"To: {display_destination}\n\n"
            f"Confirm payment?"
        )
        
        if messagebox.askyesno("Confirm Payment", msg):
            success = self.save_ride_to_database()
            
            if success:
                messagebox.showinfo(
                    "Booking Complete! 🎉", 
                    f"Your {self.ride_type} is on the way!\n"
                    f"Driver arriving in 5-10 minutes 🚕\n\n"
                    f"Total Paid: ₱{self.fare:.2f}\n\n"
                    f"Check 'My Rides' to view your booking."
                )
                self.close_and_return_to_map()
            else:
                messagebox.showerror("Booking Failed", "Could not save your booking. Please try again.")
    
    def save_ride_to_database(self):
        try:
            if not db.connect():
                return False
            
            pickup_lat = self.pickup_coords[0] if self.pickup_coords else 7.0731
            pickup_lon = self.pickup_coords[1] if self.pickup_coords else 125.6128
            dest_lat = self.destination_coords[0] if self.destination_coords else 7.0833
            dest_lon = self.destination_coords[1] if self.destination_coords else 125.6200
            
            ride_code = db.create_ride(
                passenger_id=config.CURRENT_USER_ID,
                ride_type=self.ride_type.lower(),
                pickup_lat=pickup_lat,
                pickup_lon=pickup_lon,
                pickup_addr=self.pickup_address,
                dest_lat=dest_lat,
                dest_lon=dest_lon,
                dest_addr=self.destination_address,
                distance_km=self.distance,
                fare=self.fare,
                payment_method=self.selected_payment
            )
            
            db.disconnect()
            
            if ride_code:
                return True
            return False
                
        except Exception as e:
            if db.connection and db.connection.is_connected():
                db.disconnect()
            return False
    
    def go_back(self):
        self.close_and_return_to_map()
    
    def close_and_return_to_map(self):
        self.root.destroy()
        if self.parent_window and self.parent_window.winfo_exists():
            self.parent_window.deiconify()
            self.parent_window.lift()
            self.parent_window.focus_force()