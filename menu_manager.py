# menu_manager.py - Menu System Management

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import config

class MenuManager:
    """Handles the side menu and info screens"""
    
    def __init__(self, root, gui_instance):
        self.root = root
        self.gui = gui_instance
        self.menu_frame = None
        self.menu_canvas = None
        self.menu_open = False
        self.info_frames = []
        
        self.load_menu_images()
        self.create_menu_panel()
    
    def load_menu_images(self):
        """Load all menu-specific images"""
        IMAGE_FOLDER = config.IMAGE_FOLDER
        
        self.menu_bg = None
        self.menu_btn_white_img = None
        self.profile_img = None
        self.undo_btn_img = None
        
        try:
            img = Image.open(IMAGE_FOLDER + "Left-Menu page.png")
            img = img.resize((428, 926), Image.Resampling.LANCZOS)
            self.menu_bg = ImageTk.PhotoImage(img)
            
            img = Image.open(IMAGE_FOLDER + "MENU BUTTON WHITE.png")
            img = img.resize((30, 20), Image.Resampling.LANCZOS)
            self.menu_btn_white_img = ImageTk.PhotoImage(img)
            
            img = Image.open(IMAGE_FOLDER + "PROFILE FOR MENU.png")
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
            self.profile_img = ImageTk.PhotoImage(img)
            
            undo_path = IMAGE_FOLDER + "undo button.png"
            if os.path.exists(undo_path):
                img = Image.open(undo_path)
                img = img.resize((70, 50), Image.Resampling.LANCZOS)
                self.undo_btn_img = ImageTk.PhotoImage(img)
                
        except Exception:
            pass
    
    def create_menu_panel(self):
        """Create detailed menu panel"""
        self.menu_frame = tk.Frame(
            self.root, bg="#3D5AFE", width=428, height=926
        )
        
        self.menu_canvas = tk.Canvas(
            self.menu_frame, width=428, height=926,
            bg="#3D5AFE", highlightthickness=0, borderwidth=0
        )
        self.menu_canvas.pack(fill="both", expand=True)
        
        if self.menu_bg:
            self.menu_canvas.create_image(0, 0, image=self.menu_bg, anchor="nw")
        
        if self.menu_btn_white_img:
            self.menu_canvas.create_image(25, 35, image=self.menu_btn_white_img, anchor="center")
            self.menu_canvas.create_rectangle(10, 20, 40, 50, fill="", outline="", tags="close_menu")
            self.menu_canvas.tag_bind("close_menu", "<Button-1>", lambda e: self.close())
        
        if self.profile_img:
            self.menu_canvas.create_image(30, 90, image=self.profile_img, anchor="nw")
        
        user_name = config.CURRENT_USER_FULLNAME or "Xander Calzado"
        self.menu_canvas.create_text(
            30, 185, text=user_name, font=("Poppins", 18, "bold"),
            fill="white", anchor="w"
        )
        
        if config.CURRENT_USERNAME:
            self.menu_canvas.create_text(
                30, 215, text=f"@{config.CURRENT_USERNAME}",
                font=("Poppins", 12), fill="#CCCCFF", anchor="w"
            )
        
        menu_items = [
            ("My Account", 280, self.goto_my_account),
            ("Notification", 340, self.goto_notification),
            ("About", 400, self.goto_about),
            ("Privacy & Policy", 460, self.goto_privacy),
        ]
        
        for item_text, y_pos, command in menu_items:
            tag_name = f"menu_{item_text.replace(' ', '_').lower()}"
            self.menu_canvas.create_text(
                30, y_pos, text=item_text, font=("Poppins", 16),
                fill="white", anchor="w", tags=tag_name
            )
            self.menu_canvas.tag_bind(tag_name, "<Button-1>", lambda e, cmd=command: cmd())
            self.menu_canvas.tag_bind(tag_name, "<Enter>", lambda e: self.root.config(cursor="hand2"))
            self.menu_canvas.tag_bind(tag_name, "<Leave>", lambda e: self.root.config(cursor=""))
        
        self.menu_canvas.create_text(
            30, 850, text="Logout", font=("Poppins", 16),
            fill="white", anchor="w", tags="menu_logout"
        )
        self.menu_canvas.tag_bind("menu_logout", "<Button-1>", lambda e: self.handle_logout())
        self.menu_canvas.tag_bind("menu_logout", "<Enter>", lambda e: self.root.config(cursor="hand2"))
        self.menu_canvas.tag_bind("menu_logout", "<Leave>", lambda e: self.root.config(cursor=""))
        
        self.menu_frame.place_forget()
    
    def toggle(self):
        """Toggle menu open/close"""
        if self.menu_open:
            self.close()
        else:
            self.open()
    
    def open(self):
        """Open menu"""
        self.menu_frame.place(x=0, y=0, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT)
        self.menu_frame.lift()
        self.menu_open = True
    
    def close(self):
        """Close menu"""
        self.menu_frame.place_forget()
        self.menu_open = False
    
    def goto_my_account(self):
        """Open My Account screen"""
        self.close()
        self.open_my_account_screen()
    
    def open_my_account_screen(self):
        """Open My Account screen"""
        from gui_screens import MyAccountScreen
        MyAccountScreen(self.root, self)
    
    def goto_notification(self):
        """Open Notifications"""
        self.close()
        from gui_screens import NotificationScreen
        NotificationScreen(self.root, self)
    
    def goto_about(self):
        """Open About with full-screen image"""
        self.close()
        from gui_screens import ImageScreen
        ImageScreen(self.root, self, "About QuickCab", "about.png")
    
    def goto_privacy(self):
        """Open Privacy Policy with full-screen image"""
        self.close()
        from gui_screens import ImageScreen
        ImageScreen(self.root, self, "Privacy Policy", "Privacy Policy.png")
    
    def show_image_popup(self, title, image_filename):
        """Show a popup window with an image"""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg="white")
        
        try:
            # Load the image
            img_path = config.IMAGE_FOLDER + image_filename
            img = Image.open(img_path)
            
            # Get image dimensions
            img_width, img_height = img.size
            
            # Calculate window size (add padding)
            window_width = min(img_width + 40, 800)
            window_height = min(img_height + 100, 900)
            
            # Resize image if needed
            if img_width > 760 or img_height > 800:
                ratio = min(760/img_width, 800/img_height)
                new_size = (int(img_width * ratio), int(img_height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            
            # Center the popup window
            popup.update_idletasks()
            x = (popup.winfo_screenwidth() // 2) - (window_width // 2)
            y = (popup.winfo_screenheight() // 2) - (window_height // 2)
            popup.geometry(f"{window_width}x{window_height}+{x}+{y}")
            popup.resizable(False, False)
            
            # Add header
            header = tk.Frame(popup, bg="#3D5AFE", height=60)
            header.pack(fill="x")
            header.pack_propagate(False)
            
            tk.Label(header, text=title, font=("Arial", 18, "bold"),
                    bg="#3D5AFE", fg="white").pack(pady=15)
            
            # Add image
            img_label = tk.Label(popup, image=photo, bg="white")
            img_label.image = photo  # Keep reference
            img_label.pack(pady=20)
            
            # Add close button
            tk.Button(popup, text="Close", font=("Arial", 12, "bold"),
                     bg="#3D5AFE", fg="white", width=15, height=2,
                     border=0, cursor="hand2",
                     command=popup.destroy).pack(pady=10)
            
        except FileNotFoundError:
            messagebox.showerror("Error", f"Image file '{image_filename}' not found in images folder!")
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
            popup.destroy()
    
    def handle_logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            messagebox.showinfo("Logged Out", "You have been logged out successfully!")
            
            self.close()
            
            config.CURRENT_USER_ID = None
            config.CURRENT_USERNAME = None
            config.CURRENT_USER_TYPE = None
            config.CURRENT_USER_FULLNAME = None
            
            self.gui.goto_login_page()