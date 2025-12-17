# gui_components.py - UI Component Creation

import tkinter as tk
from PIL import Image, ImageTk
import config
import functions

class UIComponents:
    """Handles creation of UI components like buttons, entries, etc."""
    
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.button_images = functions.load_all_button_images()
        self.home_icons = functions.load_all_home_icons()
        self.components = {}
        
        self.password_visible = False
        self.signup_password_visible = False
    
    def create_all_buttons(self):
        """Create all buttons"""
        self.components['get_started_btn'] = self.create_image_button(
            self.button_images.get('get_started'), "Get Started"
        )
        
        self.components['allow_location_btn'] = self.create_image_button(
            self.button_images.get('allow_location'), "Allow Location"
        )
        
        self.components['login_btn'] = self.create_image_button(
            self.button_images.get('login_button'), "Login"
        )
        
        self.components['signup_btn'] = self.create_image_button(
            self.button_images.get('dont_have_acc'), 
            "Don't have an account? Sign Up", is_link=True
        )
        
        self.components['signup_page_btn'] = self.create_image_button(
            self.button_images.get('signup_button'), "Sign Up"
        )
        
        self.components['signin_btn'] = self.create_image_button(
            self.button_images.get('alr_have_acc'),
            "Already have an account? Sign In", is_link=True
        )
        
        self.components['menu_btn'] = self.create_menu_button()
        
        return self.components
    
    def create_all_entries(self):
        """Create all entry fields with show/hide password buttons"""
        self.components['username_entry'] = self.create_entry("Username:")
        self.components['password_entry'] = self.create_entry("Password:", is_password=True)
        self.components['fullname_entry'] = self.create_entry("Full Name")
        self.components['email_entry'] = self.create_entry("Email")
        self.components['signup_password_entry'] = self.create_entry("Password", is_password=True)
        
        self.components['show_password_btn'] = self.create_show_password_button('login')
        self.components['show_signup_password_btn'] = self.create_show_password_button('signup')
        
        return self.components
    
    def create_show_password_button(self, form_type):
        """Create show/hide password button"""
        btn = tk.Button(
            self.root, text="ðŸ‘", font=("Arial", 12),
            bg="white", fg="#666", relief="flat", border=0,
            cursor="hand2", width=2, height=1,
            activebackground="white", activeforeground="#3D5AFE"
        )
        return btn
    
    def create_image_button(self, image_photo, fallback_text, is_link=False):
        """Create a button with image or fallback text"""
        if image_photo:
            return tk.Button(
                self.root, image=image_photo, border=0, relief="flat",
                cursor="hand2", borderwidth=0, highlightthickness=0,
                bg=config.WINDOW_BG_COLOR, activebackground=config.WINDOW_BG_COLOR
            )
        else:
            if is_link:
                return tk.Button(
                    self.root, text=fallback_text, font=("Arial", 11),
                    bg=config.WINDOW_BG_COLOR, fg=config.PRIMARY_COLOR,
                    relief="flat", border=0, cursor="hand2",
                    activebackground=config.WINDOW_BG_COLOR,
                    activeforeground=config.PRIMARY_COLOR
                )
            else:
                return tk.Button(
                    self.root, text=fallback_text, font=("Arial", 14, "bold"),
                    bg=config.PRIMARY_COLOR, fg="white", width=15, height=2,
                    border=0, relief="flat", cursor="hand2"
                )
    
    def create_menu_button(self):
        """Create menu button"""
        menu_img = self.button_images.get('menu_button')
        if menu_img:
            return tk.Button(
                self.root, image=menu_img, border=0, relief="flat",
                cursor="hand2", borderwidth=0, highlightthickness=0,
                bg=config.WINDOW_BG_COLOR, activebackground=config.WINDOW_BG_COLOR
            )
        else:
            return tk.Button(
                self.root, text="â˜°", font=("Arial", 20), border=0,
                relief="flat", cursor="hand2",
                bg=config.WINDOW_BG_COLOR, fg=config.PRIMARY_COLOR
            )
    
    def create_entry(self, placeholder, is_password=False):
        """Create an entry field with placeholder"""
        entry = tk.Entry(
            self.root, font=("Arial", 13), bg=config.WHITE,
            fg=config.GRAY_TEXT, relief="flat", borderwidth=0, width=24, show=""
        )
        entry.insert(0, placeholder)
        return entry
    
    def create_home_icon_buttons(self):
        """Create home page icon buttons"""
        icon_buttons = []
        icon_names = ['car', 'map', 'activity', 'payment', 'coupon', 'coming_soon']
        
        for icon_name, (x, y) in zip(icon_names, config.HOME_ICON_POSITIONS):
            if self.home_icons.get(icon_name):
                btn = tk.Button(
                    self.root, image=self.home_icons[icon_name], border=0,
                    relief="flat", cursor="hand2", borderwidth=0,
                    highlightthickness=0, bg=config.WINDOW_BG_COLOR,
                    activebackground=config.WINDOW_BG_COLOR
                )
                icon_buttons.append((btn, x, y, icon_name))
        
        return icon_buttons