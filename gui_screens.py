# gui_screens.py - Enhanced GUI Screens

import tkinter as tk
from tkinter import Canvas, Scrollbar, messagebox
from PIL import Image, ImageTk
import os
import config
from database_manager import db

class BaseInfoScreen:
    """Base class for enhanced info screens"""
    
    def __init__(self, root, menu_manager, title):
        self.root = root
        self.menu_manager = menu_manager
        self.title = title
        
        self.window = tk.Toplevel(root)
        self.window.title(title)
        self.window.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.window.resizable(False, False)
        self.window.configure(bg="#F5F5F5")
        
        self.center_window()
        self.window.protocol("WM_DELETE_WINDOW", self.back_to_menu)
    
    def center_window(self):
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (config.WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (config.WINDOW_HEIGHT // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def back_to_menu(self):
        self.window.destroy()
        self.menu_manager.open()
    
    def add_back_button(self):
        if hasattr(self.menu_manager, 'undo_btn_img') and self.menu_manager.undo_btn_img:
            back_btn = tk.Button(
                self.window, image=self.menu_manager.undo_btn_img,
                border=0, relief="flat", cursor="hand2",
                command=self.back_to_menu, borderwidth=0,
                highlightthickness=0, bg=self.window['bg'],
                activebackground=self.window['bg']
            )
            back_btn.image = self.menu_manager.undo_btn_img
            back_btn.place(x=10, y=20)


class MyAccountScreen(BaseInfoScreen):
    """Enhanced My Account Screen"""
    
    def __init__(self, root, menu_manager):
        super().__init__(root, menu_manager, "My Account")
        self.profile_img = None
        self.load_profile_image()
        self.setup_ui()
    
    def load_profile_image(self):
        """Load the profile image from menu"""
        try:
            img_path = config.IMAGE_FOLDER + "PROFILE FOR MENU.png"
            img = Image.open(img_path)
            img = img.resize((120, 120), Image.Resampling.LANCZOS)
            self.profile_img = ImageTk.PhotoImage(img)
        except Exception:
            self.profile_img = None
    
    def setup_ui(self):
        # Header with light gray background
        header = tk.Frame(self.window, bg="#D2D2DF", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        self.add_back_button()
        
        # Title
        tk.Label(header, text="Edit Profile", font=("Arial", 20, "bold"),
                bg="#D2D2DF", fg="#333").place(relx=0.5, y=50, anchor="center")
        
        # Main content area
        container = tk.Frame(self.window, bg="#D2D2DF")
        container.pack(fill="both", expand=True)
        
        # Profile picture section
        profile_frame = tk.Frame(container, bg="#D2D2DF")
        profile_frame.pack(pady=30)
        
        profile_canvas = Canvas(profile_frame, width=150, height=150, 
                               bg="#D2D2DF", highlightthickness=0)
        profile_canvas.pack()
        profile_canvas.create_oval(10, 10, 140, 140, fill="white", width=3, outline="#3D5AFE")
        
        # Display profile image if loaded, otherwise show emoji
        if self.profile_img:
            profile_canvas.create_image(75, 75, image=self.profile_img)
        else:
            profile_canvas.create_text(75, 75, text="👤", font=("Arial", 60))
        
        # Input fields with Xander Calzado data
        fields = [
            ("👤", "Xander Calzado"),
            ("✉️", "xandercalzado@gmail.com"),
            ("🔑", ""),
            ("🎂", "")
        ]
        
        for icon, placeholder in fields:
            field_frame = tk.Frame(container, bg="white", 
                                  highlightbackground="#E0E0E0", highlightthickness=1)
            field_frame.pack(fill="x", padx=35, pady=8)
            
            # Icon
            tk.Label(field_frame, text=icon, font=("Arial", 18), 
                    bg="white", fg="#666").pack(side="left", padx=15, pady=15)
            
            # Entry field
            entry = tk.Entry(field_frame, font=("Arial", 13), bg="white", 
                           fg="#333", relief="flat", borderwidth=0)
            entry.insert(0, placeholder)
            entry.pack(side="left", fill="both", expand=True, pady=15, padx=(0, 15))
        
        # Update Profile button at bottom
        btn_frame = tk.Frame(container, bg="#D2D2DF")
        btn_frame.pack(side="bottom", fill="x", padx=35, pady=30)
        
        tk.Button(btn_frame, text="Update Profile", font=("Arial", 14, "bold"),
                 bg="#3D5AFE", fg="white", height=2, border=0, cursor="hand2",
                 command=lambda: messagebox.showinfo("Success", "Profile updated!")
                 ).pack(fill="x")
    
    def edit_profile(self):
        EditProfileDialog(self.window)


class EditProfileDialog:
    """Enhanced Edit Profile Dialog"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Edit Profile")
        self.window.geometry("400x650")
        self.window.configure(bg="white")
        self.window.resizable(False, False)
        
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - 200
        y = (self.window.winfo_screenheight() // 2) - 325
        self.window.geometry(f"+{x}+{y}")
        
        header = tk.Frame(self.window, bg="#3D5AFE", height=120)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="✏️ Edit Profile", font=("Arial", 20, "bold"),
                bg="#3D5AFE", fg="white").pack(pady=40)
        
        profile = tk.Frame(self.window, bg="white")
        profile.pack(pady=20)
        
        canvas = Canvas(profile, width=100, height=100, bg="white", highlightthickness=0)
        canvas.pack()
        canvas.create_oval(10, 10, 90, 90, fill="#E3F2FD", outline="#3D5AFE", width=3)
        canvas.create_text(50, 50, text="👤", font=("Arial", 40))
        
        tk.Button(profile, text="📷 Change", font=("Arial", 10), bg="#3D5AFE",
                 fg="white", border=0, cursor="hand2").pack(pady=5)
        
        fields = [
            ("👤", "Full Name", config.CURRENT_USER_FULLNAME or "Guest"),
            ("📧", "Email", f"{config.CURRENT_USERNAME}@quickcab.com"),
            ("📱", "Phone", "+63 XXX XXX XXXX")
        ]
        
        for icon, label, value in fields:
            frame = tk.Frame(self.window, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
            frame.pack(fill="x", padx=20, pady=8)
            
            tk.Label(frame, text=icon, font=("Arial", 16), bg="white").pack(side="left", padx=15, pady=12)
            
            entry_frame = tk.Frame(frame, bg="white")
            entry_frame.pack(side="left", fill="both", expand=True, pady=12, padx=(0, 15))
            
            tk.Label(entry_frame, text=label, font=("Arial", 9), bg="white", fg="#999").pack(anchor="w")
            entry = tk.Entry(entry_frame, font=("Arial", 12), bg="white", fg="#333", relief="flat", borderwidth=0)
            entry.insert(0, value)
            entry.pack(fill="x")
        
        tk.Button(self.window, text="💾 Save Changes", font=("Arial", 14, "bold"),
                 bg="#3D5AFE", fg="white", height=2, border=0, cursor="hand2",
                 command=lambda: [messagebox.showinfo("Success", "Profile updated!"), self.window.destroy()]
                 ).pack(fill="x", side="bottom", padx=20, pady=20)


class NotificationScreen(BaseInfoScreen):
    """Enhanced Notification Screen"""
    
    def __init__(self, root, menu_manager):
        super().__init__(root, menu_manager, "Notifications")
        self.setup_ui()
    
    def setup_ui(self):
        header = tk.Frame(self.window, bg="#D2D2DF", height=120)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        self.add_back_button()
        
        tk.Label(header, text="🔔 Notifications", font=("Arial", 22, "bold"),
                bg="#D2D2DF", fg="black").pack(pady=45)
        
        content_frame = tk.Frame(self.window, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        notifications = [
            {
                "icon": "🚕",
                "title": "Ride Completed",
                "message": "Your ride to Makati has been completed successfully!",
                "time": "5 mins ago",
                "color": "#10b981"
            },
            {
                "icon": "🎉",
                "title": "New Promo Available",
                "message": "Get 20% off on your next 3 rides. Check your vouchers!",
                "time": "1 hour ago",
                "color": "#f59e0b"
            },
            {
                "icon": "💳",
                "title": "Payment Successful",
                "message": "₱250.00 has been charged to your wallet",
                "time": "3 hours ago",
                "color": "#3D5AFE"
            },
            {
                "icon": "⭐",
                "title": "Rate Your Driver",
                "message": "How was your experience with Juan? Please rate your ride.",
                "time": "1 day ago",
                "color": "#8b5cf6"
            }
        ]
        
        for notif in notifications:
            self.create_notification_card(content_frame, notif)
        
        if not notifications:
            tk.Label(content_frame, text="📭", font=("Arial", 48),
                    bg="white", fg="#CCC").pack(pady=100)
            tk.Label(content_frame, text="No notifications yet",
                    font=("Arial", 16), bg="white", fg="#999").pack()
    
    def create_notification_card(self, parent, notif):
        card = tk.Frame(parent, bg="white", highlightbackground=notif['color'], 
                       highlightthickness=2)
        card.pack(fill="x", pady=5)
        
        content = tk.Frame(card, bg="white")
        content.pack(fill="x", padx=15, pady=12)
        
        tk.Label(content, text=notif['icon'], font=("Arial", 24),
                bg="white").pack(side="left", padx=(0, 10))
        
        details = tk.Frame(content, bg="white")
        details.pack(side="left", fill="both", expand=True)
        
        title_frame = tk.Frame(details, bg="white")
        title_frame.pack(fill="x")
        
        tk.Label(title_frame, text=notif['title'], font=("Arial", 13, "bold"),
                bg="white", fg="#333").pack(side="left")
        
        tk.Label(title_frame, text=notif['time'], font=("Arial", 9),
                bg="white", fg="#999").pack(side="right")
        
        tk.Label(details, text=notif['message'], font=("Arial", 11),
                bg="white", fg="#666", wraplength=300, anchor="w",
                justify="left").pack(anchor="w", pady=(3, 0))


class CarBookingFeature:
    """Enhanced Car Booking Feature Window"""
    
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Reserve a Taxi")
        self.window.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.window.resizable(False, False)
        self.window.configure(bg="#F5F5F5")
        
        self.vehicle_images = {}
        self.load_vehicle_images()
        
        self.center_window()
        self.setup_ui()
    
    def center_window(self):
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (config.WINDOW_WIDTH // 2)
        y = (self.window.winfo_screenheight() // 2) - (config.WINDOW_HEIGHT // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def load_vehicle_images(self):
        """Load vehicle images"""
        self.vehicle_images = {}
        image_folder = config.IMAGE_FOLDER if hasattr(config, 'IMAGE_FOLDER') else "images/"
        
        try:
            sedan_path = os.path.join(image_folder, "Economy Sedan.png")
            sedan_img = Image.open(sedan_path)
            sedan_img = sedan_img.resize((120, 80), Image.Resampling.LANCZOS)
            self.vehicle_images['sedan'] = ImageTk.PhotoImage(sedan_img)
        except Exception:
            self.vehicle_images['sedan'] = None
        
        try:
            suv_path = os.path.join(image_folder, "Premium Suv.png")
            suv_img = Image.open(suv_path)
            suv_img = suv_img.resize((120, 80), Image.Resampling.LANCZOS)
            self.vehicle_images['suv'] = ImageTk.PhotoImage(suv_img)
        except Exception:
            self.vehicle_images['suv'] = None
    
    def setup_ui(self):
        header = tk.Frame(self.window, bg="#3D5AFE", height=120)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Button(header, text="←", font=("Arial", 20), bg="#3D5AFE", fg="white",
                 border=0, cursor="hand2", command=self.window.destroy).place(x=15, y=40)
        
        tk.Label(header, text="🚕 Reserve a Taxi", font=("Arial", 22, "bold"),
                bg="#3D5AFE", fg="white").pack(pady=45)
        
        container = tk.Frame(self.window, bg="#F5F5F5")
        container.pack(fill="both", expand=True)
        
        canvas = Canvas(container, bg="#F5F5F5", highlightthickness=0)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#F5F5F5")
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        info_banner = tk.Frame(scroll_frame, bg="#E3F2FD", highlightbackground="#3D5AFE", highlightthickness=2)
        info_banner.pack(fill="x", padx=20, pady=20)
        
        tk.Label(info_banner, text="ℹ️", font=("Arial", 24), bg="#E3F2FD").pack(pady=(15, 5))
        tk.Label(info_banner, text="QuickCab Taxi Reservation", font=("Arial", 16, "bold"),
                bg="#E3F2FD", fg="#3D5AFE").pack()
        tk.Label(info_banner, text="Choose your vehicle type and book instantly",
                font=("Arial", 10), bg="#E3F2FD", fg="#666").pack(pady=(5, 15))
        
        vehicles = [
            {
                "name": "Economy Sedan",
                "image_key": "sedan",
                "base_fare": "₱40",
                "per_km": "₱15/km",
                "capacity": "4 passengers",
                "features": ["Air-conditioned", "Standard comfort", "Daily commute"],
                "color": "#10b981"
            },
            {
                "name": "Premium SUV",
                "image_key": "suv",
                "base_fare": "₱80",
                "per_km": "₱25/km",
                "capacity": "6 passengers",
                "features": ["Luxury comfort", "Extra luggage space", "Airport transfers"],
                "color": "#3D5AFE"
            }
        ]
        
        for vehicle in vehicles:
            self.create_vehicle_card(scroll_frame, vehicle)
        
        tk.Label(scroll_frame, text="📋 Booking Features", font=("Arial", 16, "bold"),
                bg="#F5F5F5", fg="#333").pack(anchor="w", padx=20, pady=(20, 10))
        
        features_frame = tk.Frame(scroll_frame, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        features_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        features = [
            "✅ Instant booking confirmation",
            "✅ Real-time driver tracking",
            "✅ Safe & verified drivers",
            "✅ Multiple payment options",
            "✅ 24/7 customer support",
            "✅ Cashless transactions"
        ]
        
        for feature in features:
            tk.Label(features_frame, text=feature, font=("Arial", 11),
                    bg="white", fg="#333", anchor="w").pack(anchor="w", padx=20, pady=8)
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def create_vehicle_card(self, parent, vehicle):
        card = tk.Frame(parent, bg="white", highlightbackground=vehicle['color'], highlightthickness=2)
        card.pack(fill="x", padx=20, pady=10)
        
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if vehicle.get('image_key') and self.vehicle_images.get(vehicle['image_key']):
            img_label = tk.Label(content_frame, image=self.vehicle_images[vehicle['image_key']], 
                                bg="white", borderwidth=2, relief="solid")
            img_label.image = self.vehicle_images[vehicle['image_key']]
            img_label.pack(side="left", padx=(0, 20))
        
        details = tk.Frame(content_frame, bg="white")
        details.pack(side="left", fill="both", expand=True)
        
        tk.Label(details, text=vehicle['name'], font=("Arial", 14, "bold"),
                bg="white", fg="#333").pack(anchor="w")
        
        price_frame = tk.Frame(details, bg="white")
        price_frame.pack(anchor="w", pady=(3, 3))
        tk.Label(price_frame, text=f"{vehicle['base_fare']} base", font=("Arial", 11, "bold"),
                bg="white", fg=vehicle['color']).pack(side="left")
        tk.Label(price_frame, text=f" + {vehicle['per_km']}", font=("Arial", 10),
                bg="white", fg="#666").pack(side="left")
        
        tk.Label(details, text=f"👥 {vehicle['capacity']}", font=("Arial", 9),
                bg="white", fg="#666").pack(anchor="w", pady=(3, 8))
        
        for feature in vehicle['features']:
            tk.Label(details, text=f"• {feature}", font=("Arial", 9),
                    bg="white", fg="#666").pack(anchor="w", pady=1)
        
        tk.Button(card, text="Reserve Now", font=("Arial", 11, "bold"),
                 bg=vehicle['color'], fg="white", border=0, cursor="hand2",
                 width=12, height=2,
                 command=lambda: self.reserve_taxi(vehicle['name'])).pack(side="right", padx=20, pady=(0, 20))
    
    def reserve_taxi(self, vehicle_name):
        """Handle taxi reservation"""
        messagebox.showinfo(
            "Taxi Reservation", 
            f"🚕 Reserving {vehicle_name}...\n\n"
            "Next steps:\n"
            "• Enter pickup location\n"
            "• Enter destination\n"
            "• Choose payment method\n"
            "• Confirm booking\n\n"
            "A driver will be assigned to you shortly!"
        )


class ImageScreen:
    """Full-screen image display with only undo button"""
    
    def __init__(self, root, menu_manager, title, image_filename):
        self.root = root
        self.menu_manager = menu_manager
        self.title = title
        self.image_filename = image_filename
        
        self.window = tk.Toplevel(root)
        self.window.title(title)
        self.window.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.window.resizable(False, False)
        
        self.center_window()
        self.window.protocol("WM_DELETE_WINDOW", self.back_to_menu)
        
        self.load_and_display_image()
    
    def center_window(self):
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (config.WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (config.WINDOW_HEIGHT // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def back_to_menu(self):
        self.window.destroy()
        self.menu_manager.open()
    
    def load_and_display_image(self):
        """Load and display the full-screen image"""
        try:
            img_path = config.IMAGE_FOLDER + self.image_filename
            img = Image.open(img_path)
            
            # Resize to exact window dimensions
            img = img.resize((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            
            # Create canvas and display image
            canvas = Canvas(self.window, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT,
                          highlightthickness=0, borderwidth=0)
            canvas.pack(fill="both", expand=True)
            canvas.create_image(0, 0, image=self.photo, anchor="nw")
            
            # Add undo button at top-left
            if hasattr(self.menu_manager, 'undo_btn_img') and self.menu_manager.undo_btn_img:
                back_btn = tk.Button(
                    self.window, image=self.menu_manager.undo_btn_img,
                    border=0, relief="flat", cursor="hand2",
                    command=self.back_to_menu, borderwidth=0,
                    highlightthickness=0, bg=self.window['bg'],
                    activebackground=self.window['bg']
                )
                back_btn.image = self.menu_manager.undo_btn_img
                back_btn.place(x=10, y=20)
            
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image file '{self.image_filename}' not found!")
            self.back_to_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
            self.back_to_menu()


class InfoScreen(BaseInfoScreen):
    """Generic info screen for About, Privacy, etc."""
    
    def __init__(self, root, menu_manager, screen_type, title, content):
        super().__init__(root, menu_manager, title)
        self.content = content
        self.setup_ui()
    
    def setup_ui(self):
        header = tk.Frame(self.window, bg="#3D5AFE", height=120)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        self.add_back_button()
        
        tk.Label(header, text=self.title, font=("Arial", 22, "bold"),
                bg="#3D5AFE", fg="white").pack(pady=45)
        
        content_frame = tk.Frame(self.window, bg="white")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        tk.Label(content_frame, text=self.content, font=("Arial", 12),
                bg="white", fg="#333", justify="left", wraplength=350).pack(pady=20)


__all__ = ['MyAccountScreen', 'NotificationScreen', 'CarBookingFeature', 'InfoScreen', 'ImageScreen']