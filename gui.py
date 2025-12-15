# gui.py - All GUI Components and Interface (WITH INTEGRATED MENU) - UPDATED

import tkinter as tk
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk
import config
import functions
import os

INFO_HEADER_COLOR = "#D2D2DF"

class QuickCabGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickCab")
        
        # Setup window
        geometry = functions.center_window(root, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.root.geometry(geometry)
        self.root.configure(bg=config.WINDOW_BG_COLOR)
        self.root.resizable(False, False)
        
        # Initialize variables
        self.current_page = 0
        self.menu_open = False
        self.home_icon_buttons = []  # Store home icon buttons for cleanup
        self.info_frames = []  # Store references to open info frames
        
        # Load all images
        print("\n🔨 Loading QuickCab Resources...\n")
        self.images, self.photo_images = functions.load_all_page_images()
        self.button_images = functions.load_all_button_images()
        self.home_icons = functions.load_all_home_icons()
        print("\n✦ All resources loaded!\n")
        
        # Setup canvas
        self.canvas = Canvas(root, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT, 
                           bg=config.WINDOW_BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Create all UI components
        self.create_all_components()
        
        # Load menu images
        self.load_menu_images()
        
        # Create detailed menu panel
        self.create_detailed_menu()
        
        # Draw initial page
        self.draw_page()
    
    # ==================== MENU IMAGE LOADING ====================
    
    def load_menu_images(self):
        """Load all menu-specific images"""
        IMAGE_FOLDER = config.IMAGE_FOLDER
        
        # Load menu background
        try:
            img = Image.open(IMAGE_FOLDER + "Left-Menu page.png")
            img = img.resize((428, 926), Image.Resampling.LANCZOS)
            self.menu_bg = ImageTk.PhotoImage(img)
            print("✅ Loaded: Left-Menu page.png")
        except Exception as e:
            print(f"❌ Error loading menu background: {e}")
            self.menu_bg = None

        # Load white menu button
        try:
            img = Image.open(IMAGE_FOLDER + "MENU BUTTON WHITE.png")
            img = img.resize((30, 20), Image.Resampling.LANCZOS)
            self.menu_btn_white_img = ImageTk.PhotoImage(img)
            print("✅ Loaded: MENU BUTTON WHITE.png")
        except Exception as e:
            print(f"❌ Error loading white menu button: {e}")
            self.menu_btn_white_img = None

        # Load profile picture
        try:
            img = Image.open(IMAGE_FOLDER + "PROFILE FOR MENU.png")
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
            self.profile_img = ImageTk.PhotoImage(img)
            print("✅ Loaded: PROFILE FOR MENU.png")
        except Exception as e:
            print(f"❌ Error loading profile: {e}")
            self.profile_img = None
        
        # Load undo button image for info frames
        self.undo_btn_img = None
        try:
            undo_path = IMAGE_FOLDER + "undo button.png"
            if os.path.exists(undo_path):
                img = Image.open(undo_path)
                img = img.resize((70, 50), Image.Resampling.LANCZOS)
                self.undo_btn_img = ImageTk.PhotoImage(img)
                print("✅ Loaded: undo button.png")
        except Exception as e:
            print(f"❌ Error loading undo button: {e}")
    
    # ==================== DETAILED MENU CREATION ====================
    
    def create_detailed_menu(self):
        """Create detailed menu panel with canvas"""
        # Create menu frame container (covers everything)
        self.menu_frame = tk.Frame(
            self.root,
            bg="#3D5AFE",
            width=428,
            height=926
        )
        
        # Create menu canvas inside frame
        self.menu_canvas = Canvas(
            self.menu_frame,
            width=428,
            height=926,
            bg="#3D5AFE",
            highlightthickness=0,
            borderwidth=0
        )
        self.menu_canvas.pack(fill="both", expand=True)
        
        # Draw background image
        if self.menu_bg:
            self.menu_canvas.create_image(0, 0, image=self.menu_bg, anchor="nw")
        
        # Add white menu button (close button)
        if self.menu_btn_white_img:
            self.menu_canvas.create_image(25, 35, image=self.menu_btn_white_img, anchor="center")
            # Make it clickable
            close_btn_area = self.menu_canvas.create_rectangle(
                10, 20, 40, 50, fill="", outline="", tags="close_menu"
            )
            self.menu_canvas.tag_bind("close_menu", "<Button-1>", lambda e: self.close_menu())
        
        # Add profile picture
        if self.profile_img:
            self.menu_canvas.create_image(30, 90, image=self.profile_img, anchor="nw")
        
        # Draw user name from database session
        user_name = config.CURRENT_USER_FULLNAME or "Xander Calzado"
        self.menu_canvas.create_text(
            30, 185,
            text=user_name,
            font=("Poppins", 18, "bold"),
            fill="white",
            anchor="w"
        )
        
        # Draw user email if available
        if config.CURRENT_USERNAME:
            self.menu_canvas.create_text(
                30, 215,
                text=f"@{config.CURRENT_USERNAME}",
                font=("Poppins", 12),
                fill="#CCCCFF",
                anchor="w"
            )
        
        # Draw menu items with proper spacing
        menu_items = [
            ("👤 My Account", 280, self.goto_my_account),
            ("🔔 Notification", 340, self.goto_notification),
            ("ℹ️ About", 400, self.goto_about),
            ("🔒 Privacy Policy", 460, self.goto_privacy),
            ("📄 Terms & Condition", 520, self.goto_terms)
        ]
        
        for item_text, y_pos, command in menu_items:
            text_id = self.menu_canvas.create_text(
                30, y_pos,
                text=item_text,
                font=("Poppins", 16),
                fill="white",
                anchor="w",
                tags=f"menu_{item_text.replace(' ', '_').replace('👤', '').replace('🔔', '').replace(' ℹ️', '').replace('🔒', '').replace('📄', '').lower().strip()}"
            )
            # Make text clickable
            self.menu_canvas.tag_bind(f"menu_{item_text.replace(' ', '_').replace('👤', '').replace('🔔', '').replace('ℹ️', '').replace('🔒', '').replace('📄', '').lower().strip()}", 
                                     "<Button-1>", lambda e, cmd=command: cmd())
            self.menu_canvas.tag_bind(f"menu_{item_text.replace(' ', '_').replace('👤', '').replace('🔔', '').replace('ℹ️', '').replace('🔒', '').replace('📄', '').lower().strip()}", 
                                     "<Enter>", lambda e: self.root.config(cursor="hand2"))
            self.menu_canvas.tag_bind(f"menu_{item_text.replace(' ', '_').replace('👤', '').replace('🔔', '').replace('ℹ️', '').replace('🔒', '').replace('📄', '').lower().strip()}", 
                                     "<Leave>", lambda e: self.root.config(cursor=""))
        
        # Draw "Logout" text at bottom
        logout_id = self.menu_canvas.create_text(
            30, 850,
            text="🚪 Logout",
            font=("Poppins", 16),
            fill="white",
            anchor="w",
            tags="menu_logout"
        )
        # Make logout clickable
        self.menu_canvas.tag_bind("menu_logout", "<Button-1>", lambda e: self.handle_logout())
        self.menu_canvas.tag_bind("menu_logout", "<Enter>", 
                                 lambda e: self.root.config(cursor="hand2"))
        self.menu_canvas.tag_bind("menu_logout", "<Leave>", 
                                 lambda e: self.root.config(cursor=""))
        
        # Initially hide menu frame
        self.menu_frame.place_forget()
    
    # ==================== MENU HANDLERS ====================
    
    def goto_my_account(self):
        """Navigate to My Account"""
        print("My Account clicked")
        self.close_menu()
        
        # Get user data from session
        user_info = ""
        if config.CURRENT_USER_FULLNAME:
            user_info += f"👤 {config.CURRENT_USER_FULLNAME}\n\n"
        if config.CURRENT_USERNAME:
            user_info += f"📧 {config.CURRENT_USERNAME}@quickcab.com\n"
        
        # Get wallet balance from database if connected
        from functions import get_wallet_data
        wallet_data = get_wallet_data()
        
        user_info += f"💰 Wallet Balance: ₱{wallet_data['balance']:.2f}\n\n"
        user_info += "⭐ Member since: 2024\n"
        user_info += "🚗 Total Rides: 5\n"
        user_info += "🎯 User Type: Passenger"
        
        self.open_info_frame("my_account", "My Account", user_info)
    
    def goto_notification(self):
        """Navigate to Notifications"""
        print("Notification clicked")
        self.close_menu()
        
        # Get notification count from database if connected
        notification_count = 3  # Default
        
        notification_text = f"🔔 You have {notification_count} notifications:\n\n"
        notification_text += "📅 Ride completed - 2 hours ago\n"
        notification_text += "💰 Payment received - 1 day ago\n"
        notification_text += "🎉 Welcome bonus - 3 days ago\n\n"
        notification_text += "No new notifications."
        
        self.open_info_frame("notification", "Notifications", notification_text)
    
    def goto_about(self):
        """Navigate to About"""
        print("About clicked")
        self.open_info_frame("about", "About QuickCab", 
                           "QuickCab - Your trusted ride-hailing service\n\n"
                           "Version 2.0 (Database Integrated)\n"
                           "© 2024 QuickCab Inc.\n\n"
                           "Connecting you with reliable rides\n"
                           "anytime, anywhere.\n\n"
                           f"Current User: {config.CURRENT_USERNAME or 'Guest'}")
    
    def goto_privacy(self):
        """Navigate to Privacy Policy"""
        print("Privacy Policy clicked")
        self.open_info_frame("privacy", "Privacy Policy", 
                           "Your privacy is important to us.\n\n"
                           "We collect necessary information to provide\n"
                           "you with the best ride-hailing experience.\n\n"
                           "Your data is securely stored and never shared\n"
                           "with third parties without your consent.")
    
    def goto_terms(self):
        """Navigate to Terms & Conditions"""
        print("Terms & Condition clicked")
        self.open_info_frame("terms", "Terms & Conditions", 
                           "By using QuickCab, you agree to:\n\n"
                           "1. Use the service responsibly\n"
                           "2. Treat drivers with respect\n"
                           "3. Pay all fares promptly\n"
                           "4. Follow all local laws and regulations\n\n"
                           "Violation may result in account suspension.")
    
    def handle_logout(self):
        """Handle logout"""
        print("Logout clicked")
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            messagebox.showinfo("Logged Out", "You have been logged out successfully!")
            
            # Close menu first
            self.close_menu()
            
            # Clear user session
            config.CURRENT_USER_ID = None
            config.CURRENT_USERNAME = None
            config.CURRENT_USER_TYPE = None
            config.CURRENT_USER_FULLNAME = None
            
            # Clear all entry fields
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, "Username:")
            self.username_entry.config(fg=config.GRAY_TEXT)
            
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, "Password:")
            self.password_entry.config(fg=config.GRAY_TEXT, show="")
            
            # Navigate to login page
            self.current_page = config.PAGE_LOGIN
            self.draw_page()
            
            print("✅ Logged out successfully")
    
    # ==================== INFO FRAME DISPLAY ====================
    
    def open_info_frame(self, frame_type, title, content):
        """Open an information frame with undo button"""
        # Close menu first
        self.close_menu()
        
        # Create frame window
        frame_window = tk.Toplevel(self.root)
        frame_window.title(title)
        
        # Set window size to match main window
        frame_window.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        frame_window.resizable(False, False)
        frame_window.configure(bg=config.WINDOW_BG_COLOR)
        
        # Center the window
        self.center_window(frame_window)
        
        # Create canvas
        canvas = tk.Canvas(
            frame_window, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT,
            bg=config.WINDOW_BG_COLOR, highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)
        
        # Try to load specific frame image
        image_loaded = False
        if frame_type == "about":
            image_path = config.IMAGE_FOLDER + "About.png"
            image_loaded = self.load_frame_image(canvas, image_path)
        elif frame_type == "privacy":
            image_path = config.IMAGE_FOLDER + "Privacy Policy.png"
            image_loaded = self.load_frame_image(canvas, image_path)
        elif frame_type == "terms":
            image_path = config.IMAGE_FOLDER + "Terms & Condition.png"
            image_loaded = self.load_frame_image(canvas, image_path)
        
        if not image_loaded:
            # For My Account, Notification, or if image loading failed
            self.create_custom_info_frame(canvas, title, content)
        
        # Add undo button
        self.add_undo_button(frame_window, canvas)
        
        # Store reference
        self.info_frames.append(frame_window)
        
        # Handle window close
        frame_window.protocol("WM_DELETE_WINDOW", lambda: self.close_frame(frame_window))
        
        print(f"✅ {title} frame opened")
    
    def center_window(self, window):
        """Center a window on screen"""
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (config.WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (config.WINDOW_HEIGHT // 2)
        window.geometry(f"+{x}+{y}")
    
    def load_frame_image(self, canvas, image_path):
        """Load and display frame image, return True if successful"""
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Keep reference to prevent garbage collection
                canvas.image = photo
                canvas.create_image(0, 0, image=photo, anchor="nw")
                print(f"✅ Loaded frame: {image_path}")
                return True
        except Exception as e:
            print(f"❌ Error loading frame image: {e}")
        return False
    
    def create_custom_info_frame(self, canvas, title, content):
        """Create a custom information frame when image is not available"""
        # Draw header
        canvas.create_rectangle(
            0, 0, config.WINDOW_WIDTH, 120,
            fill=INFO_HEADER_COLOR, outline=""
        )
        
        canvas.create_text(
            config.WINDOW_WIDTH // 2, 70,
            text=title,
            font=("Poppins", 24, "bold"),
            fill="#333333"
        )
        
        # Draw content area
        canvas.create_rectangle(
            20, 140, config.WINDOW_WIDTH - 20, config.WINDOW_HEIGHT - 100,
            fill="white", outline="", width=0
        )
        
        # Add content text (with word wrapping)
        content_lines = content.split('\n')
        y_position = 180
        for line in content_lines:
            canvas.create_text(
                config.WINDOW_WIDTH // 2, y_position,
                text=line,
                font=("Poppins", 14),
                fill="#333",
                width=config.WINDOW_WIDTH - 60
            )
            y_position += 40
    
    def add_undo_button(self, frame_window, canvas):
        """Add undo button to the frame"""
        # Try to use pre-loaded undo button image
        if self.undo_btn_img:
            undo_btn = tk.Button(
                frame_window, image=self.undo_btn_img, border=0, relief="flat",
                cursor="hand2", command=lambda: self.close_frame(frame_window),
                borderwidth=0, highlightthickness=0, bg=config.WINDOW_BG_COLOR,
                activebackground=config.WINDOW_BG_COLOR
            )
            undo_btn.place(x=10, y=20)
            return
        
        # Fallback to text button
        undo_btn = tk.Button(
            frame_window, text="← Back", font=("Arial", 12, "bold"),
            bg=config.PRIMARY_COLOR, fg="white", border=0, relief="flat",
            cursor="hand2", command=lambda: self.close_frame(frame_window),
            width=8, height=1
        )
        undo_btn.place(x=20, y=30)
    
    def close_frame(self, frame_window):
        """Close the info frame"""
        if frame_window in self.info_frames:
            self.info_frames.remove(frame_window)
        frame_window.destroy()
        print("← Closed info frame")
    
    # ==================== UI COMPONENT CREATION ====================
    
    def create_all_components(self):
        """Create all UI components"""
        self.create_buttons()
        self.create_entry_fields()
        self.create_menu()
    
    def create_buttons(self):
        """Create all buttons"""
        # Get Started Button
        self.get_started_btn = self.create_image_button(
            self.button_images.get('get_started'),
            self.next_page_btn,
            "Get Started"
        )
        
        # Allow Location Button
        self.allow_location_btn = self.create_image_button(
            self.button_images.get('allow_location'),
            self.next_page_btn,
            "Allow Location"
        )
        
        # Login Button
        self.login_btn = self.create_image_button(
            self.button_images.get('login_button'),
            self.handle_login,
            "Login"
        )
        
        # Don't Have Account Button
        self.signup_btn = self.create_image_button(
            self.button_images.get('dont_have_acc'),
            self.goto_signup_page,
            "Don't have an account? Sign Up",
            is_link=True
        )
        
        # Sign Up Button
        self.signup_page_btn = self.create_image_button(
            self.button_images.get('signup_button'),
            self.handle_signup_submit,
            "Sign Up"
        )
        
        # Already Have Account Button
        self.signin_btn = self.create_image_button(
            self.button_images.get('alr_have_acc'),
            self.goto_login_page,
            "Already have an account? Sign In",
            is_link=True
        )
    
    def create_entry_fields(self):
        """Create all entry fields"""
        # Login entries
        self.username_entry = self.create_entry("Username:")
        self.password_entry = self.create_entry("Password:", is_password=True)
        
        self.username_entry.bind("<Return>", lambda e: self.handle_login())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
        # Signup entries
        self.fullname_entry = self.create_entry("Full Name")
        self.email_entry = self.create_entry("Email")
        self.signup_password_entry = self.create_entry("Password", is_password=True)
    
    def create_menu(self):
        """Create menu components"""
        # Regular menu button (for home page)
        menu_img = self.button_images.get('menu_button')
        if menu_img:
            self.menu_btn = tk.Button(
                self.root, image=menu_img, border=0, relief="flat",
                cursor="hand2", command=self.toggle_menu, borderwidth=0,
                highlightthickness=0, bg=config.WINDOW_BG_COLOR,
                activebackground=config.WINDOW_BG_COLOR
            )
        else:
            self.menu_btn = tk.Button(
                self.root, text="☰", font=("Arial", 20), border=0,
                relief="flat", cursor="hand2", command=self.toggle_menu,
                bg=config.WINDOW_BG_COLOR, fg=config.PRIMARY_COLOR
            )
    
    def create_image_button(self, image_photo, command, fallback_text, is_link=False):
        """Create a button with image or fallback text"""
        if image_photo:
            return tk.Button(
                self.root, image=image_photo, border=0, relief="flat",
                cursor="hand2", command=command, borderwidth=0,
                highlightthickness=0, bg=config.WINDOW_BG_COLOR,
                activebackground=config.WINDOW_BG_COLOR
            )
        else:
            if is_link:
                return tk.Button(
                    self.root, text=fallback_text, font=("Arial", 11),
                    bg=config.WINDOW_BG_COLOR, fg=config.PRIMARY_COLOR,
                    relief="flat", border=0, cursor="hand2", command=command,
                    activebackground=config.WINDOW_BG_COLOR,
                    activeforeground=config.PRIMARY_COLOR
                )
            else:
                return tk.Button(
                    self.root, text=fallback_text, font=("Arial", 14, "bold"),
                    bg=config.PRIMARY_COLOR, fg="white", width=15, height=2,
                    border=0, relief="flat", cursor="hand2", command=command
                )
    
    def create_entry(self, placeholder, is_password=False):
        """Create an entry field with placeholder"""
        entry = tk.Entry(
            self.root, font=("Arial", 13), bg=config.WHITE,
            fg=config.GRAY_TEXT, relief="flat", borderwidth=0, width=28, show=""
        )
        entry.insert(0, placeholder)
        
        # Bind focus events
        entry.bind("<FocusIn>", lambda e: self.on_entry_focus_in(e, placeholder, is_password))
        entry.bind("<FocusOut>", lambda e: self.on_entry_focus_out(e, placeholder, is_password))
        
        return entry
    
    # ==================== PAGE RENDERING ====================
    
    def draw_page(self):
        """Draw the current page"""
        self.canvas.delete("all")
        self.hide_all_components()
        
        # Make sure menu is closed when changing pages
        if self.menu_open:
            self.close_menu()
        
        if self.current_page < len(self.photo_images):
            self.canvas.create_image(214, 463, image=self.photo_images[self.current_page])
            
            # Show components based on page
            if self.current_page in config.PAGE_WELCOME:
                self.get_started_btn.place(x=214, y=830, anchor="center")
            
            elif self.current_page == config.PAGE_LOCATION:
                self.allow_location_btn.place(x=214, y=830, anchor="center")
            
            elif self.current_page == config.PAGE_LOGIN:
                self.draw_login_page()
            
            elif self.current_page == config.PAGE_SIGNUP:
                self.draw_signup_page()
            
            elif self.current_page == config.PAGE_HOME:
                self.draw_home_page()
    
    def draw_login_page(self):
        """Draw login page components"""
        self.create_rounded_rect(64, 470, 364, 515, 25, fill="white", outline="")
        self.create_rounded_rect(64, 545, 364, 590, 25, fill="white", outline="")
        
        self.username_entry.place(x=214, y=492, anchor="center")
        self.password_entry.place(x=214, y=567, anchor="center")
        self.login_btn.place(x=214, y=665, anchor="center")
        self.signup_btn.place(x=214, y=898, anchor="center")
    
    def draw_signup_page(self):
        """Draw signup page components"""
        self.create_rounded_rect(64, 322, 364, 372, 25, fill="white", outline="")
        self.create_rounded_rect(64, 397, 364, 447, 25, fill="white", outline="")
        self.create_rounded_rect(64, 472, 364, 522, 25, fill="white", outline="")
        
        self.fullname_entry.place(x=214, y=347, anchor="center")
        self.email_entry.place(x=214, y=422, anchor="center")
        self.signup_password_entry.place(x=214, y=497, anchor="center")
        self.signup_page_btn.place(x=214, y=583, anchor="center")
        self.signin_btn.place(x=214, y=897, anchor="center")
    
    def draw_home_page(self):
        """Draw home page components"""
        self.menu_btn.place(x=25, y=35, anchor="center")
        
        # Clear any existing home icon buttons
        for btn in self.home_icon_buttons:
            btn.destroy()
        self.home_icon_buttons.clear()
        
        # Create home icon buttons
        icon_names = ['car', 'map', 'activity', 'payment', 'coupon', 'coming_soon']
        for icon_name, (x, y) in zip(icon_names, config.HOME_ICON_POSITIONS):
            if self.home_icons.get(icon_name):
                btn = tk.Button(
                    self.root, image=self.home_icons[icon_name], border=0,
                    relief="flat", cursor="hand2",
                    command=lambda name=icon_name: functions.handle_home_icon_click(name, self.root),
                    borderwidth=0, highlightthickness=0, bg=config.WINDOW_BG_COLOR,
                    activebackground=config.WINDOW_BG_COLOR
                )
                btn.place(x=x, y=y, anchor="center")
                self.home_icon_buttons.append(btn)  # Store reference
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle"""
        points = functions.create_rounded_rect_points(x1, y1, x2, y2, radius)
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def hide_all_components(self):
        """Hide all UI components"""
        components = [
            self.get_started_btn, self.allow_location_btn, self.login_btn,
            self.username_entry, self.password_entry, self.signup_btn,
            self.fullname_entry, self.email_entry, self.signup_password_entry,
            self.signup_page_btn, self.signin_btn, self.menu_btn
        ]
        for component in components:
            component.place_forget()
        
        # Hide all home icon buttons
        for btn in self.home_icon_buttons:
            btn.place_forget()
    
    # ==================== EVENT HANDLERS ====================
    
    def on_canvas_click(self, event):
        """Handle canvas clicks"""
        if self.current_page == config.PAGE_OPENING:
            self.current_page += 1
            self.draw_page()
    
    def next_page_btn(self):
        """Go to next page"""
        if self.current_page < len(self.photo_images) - 1:
            self.current_page += 1
        else:
            self.current_page = 0
        self.draw_page()
    
    def goto_signup_page(self):
        """Navigate to signup page"""
        print("Navigating to Sign Up page...")
        self.current_page = config.PAGE_SIGNUP
        self.draw_page()
    
    def goto_login_page(self):
        """Navigate to login page"""
        print("Navigating to Login page...")
        self.current_page = config.PAGE_LOGIN
        self.draw_page()
    
    def goto_home_page(self):
        """Navigate to home page"""
        print("Navigating to home page...")
        self.current_page = config.PAGE_HOME
        self.draw_page()
    
    # ==================== MENU ====================
    
    def toggle_menu(self):
        """Toggle menu panel"""
        if self.menu_open:
            self.close_menu()
        else:
            self.open_menu()
    
    def open_menu(self):
        """Open detailed menu panel"""
        # Show menu frame on top of everything - covers entire window
        self.menu_frame.place(x=0, y=0, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT)
        self.menu_frame.lift()
        self.menu_frame.tkraise()
        
        # Hide menu button while menu is open
        self.menu_btn.place_forget()
        
        self.menu_open = True
        print("Menu opened")
    
    def close_menu(self):
        """Close menu panel"""
        self.menu_frame.place_forget()
        self.menu_open = False
        
        # Show menu button again if on home page
        if self.current_page == config.PAGE_HOME:
            self.menu_btn.place(x=25, y=35, anchor="center")
        
        print("Menu closed")
    
    # ==================== AUTHENTICATION ====================
    
    def handle_login(self):
        """Handle login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        success, message = functions.validate_login(username, password)
        
        if success:
            messagebox.showinfo("Login Successful", message)
            print(f"✅ Login successful - Username: {username}")
            self.goto_home_page()
        else:
            messagebox.showerror("Login Failed", message)
            print(f"❌ Login failed - Username: {username}")
    
    def handle_signup_submit(self):
        """Handle signup"""
        fullname = self.fullname_entry.get()
        email = self.email_entry.get()
        password = self.signup_password_entry.get()
        
        success, message = functions.validate_signup(fullname, email, password)
        
        if success:
            messagebox.showinfo("Sign Up Successful", message)
            print(f"✅ Sign Up successful - Name: {fullname}, Email: {email}")
            # Auto login after signup
            config.CURRENT_USERNAME = email.split('@')[0]
            config.CURRENT_USER_FULLNAME = fullname
            self.goto_home_page()
        else:
            messagebox.showwarning("Sign Up Error", message)
            print(f"❌ Sign Up failed")
    
    # ==================== ENTRY FIELD HANDLERS ====================
    
    def on_entry_focus_in(self, event, placeholder, is_password):
        """Handle entry field focus in"""
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=config.BLACK_TEXT)
            if is_password:
                entry.config(show="*")
    
    def on_entry_focus_out(self, event, placeholder, is_password):
        """Handle entry field focus out"""
        entry = event.widget
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg=config.GRAY_TEXT)
            if is_password:
                entry.config(show="")