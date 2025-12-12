import tkinter as tk
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk
import os

class OnboardingCarousel:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickCab")
        
        # Set window size
        window_width = 428
        window_height = 926
        
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Calculate center position
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        # Set geometry with centered position
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.configure(bg="#C5C6D0")
        self.root.resizable(False, False)  # Prevent resizing
        
        self.current_page = 0
        
        # Image file paths - looking in Python Frames folder
        self.image_paths = [
            "Python Frames/Opening.png",
            "Python Frames/Welcome.png",
            "Python Frames/Welcome1.png",
            "Python Frames/Welcome2.png",
            "Python Frames/Location.png",
            "Python Frames/LOGIN PAGE.png",
            "Python Frames/Sign Up.png",
            "Python Frames/home.png"
        ]
        
        self.images = []
        self.photo_images = []
        
        # Load all images
        self.load_images()
        
        # Load button images
        self.load_button_images()
        
        # Load home page icon images
        self.load_home_icons()
        
        self.canvas = Canvas(root, width=428, height=926, bg="#C5C6D0", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.canvas.bind("<Button-1>", self.next_page)
        
        # Create buttons with images (initially hidden)
        if self.get_started_photo:
            self.get_started_btn = tk.Button(
                root, 
                image=self.get_started_photo,
                border=0,
                relief="flat",
                cursor="hand2",
                command=self.next_page_btn,
                borderwidth=0,
                highlightthickness=0,
                bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
        else:
            # Fallback text button
            self.get_started_btn = tk.Button(
                root, 
                text="Get Started", 
                font=("Arial", 14, "bold"),
                bg="#3D5AFE",
                fg="white",
                width=15,
                height=2,
                border=0,
                relief="flat",
                cursor="hand2",
                command=self.next_page_btn
            )
        
        if self.allow_location_photo:
            self.allow_location_btn = tk.Button(
                root, 
                image=self.allow_location_photo,
                border=0,
                relief="flat",
                cursor="hand2",
                command=self.next_page_btn,
                borderwidth=0,
                highlightthickness=0,
                bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
        else:
            # Fallback text button
            self.allow_location_btn = tk.Button(
                root, 
                text="Allow Location", 
                font=("Arial", 14, "bold"),
                bg="#3D5AFE",
                fg="white",
                width=15,
                height=2,
                border=0,
                relief="flat",
                cursor="hand2",
                command=self.next_page_btn
            )
        
        # Create Login button
        if self.login_button_photo:
            self.login_btn = tk.Button(
                root, 
                image=self.login_button_photo,
                border=0,
                relief="flat",
                cursor="hand2",
                command=self.handle_login,
                borderwidth=0,
                highlightthickness=0,
                bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
        else:
            # Fallback text button
            self.login_btn = tk.Button(
                root, 
                text="Login", 
                font=("Arial", 14, "bold"),
                bg="#3D5AFE",
                fg="white",
                width=15,
                height=2,
                border=0,
                relief="flat",
                cursor="hand2",
                command=self.handle_login
            )
        
        # Create username and password entry fields for Login page
        self.username_entry = tk.Entry(
            root,
            font=("Arial", 13),
            bg="white",
            fg="#AAAAAA",
            relief="flat",
            borderwidth=0,
            width=28
        )
        self.username_entry.insert(0, "Username:")
        
        self.password_entry = tk.Entry(
            root,
            font=("Arial", 13),
            bg="white",
            fg="#AAAAAA",
            relief="flat",
            borderwidth=0,
            width=28,
            show=""
        )
        self.password_entry.insert(0, "Password:")
        
        # Bind events for placeholder text
        self.username_entry.bind("<FocusIn>", self.on_username_focus_in)
        self.username_entry.bind("<FocusOut>", self.on_username_focus_out)
        self.password_entry.bind("<FocusIn>", self.on_password_focus_in)
        self.password_entry.bind("<FocusOut>", self.on_password_focus_out)
        
        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda e: self.handle_login())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
        # Create Sign Up page text entries
        self.fullname_entry = tk.Entry(
            root,
            font=("Arial", 13),
            bg="white",
            fg="#AAAAAA",
            relief="flat",
            borderwidth=0,
            width=28
        )
        self.fullname_entry.insert(0, "Full Name")
        
        self.email_entry = tk.Entry(
            root,
            font=("Arial", 13),
            bg="white",
            fg="#AAAAAA",
            relief="flat",
            borderwidth=0,
            width=28
        )
        self.email_entry.insert(0, "Email")
        
        self.signup_password_entry = tk.Entry(
            root,
            font=("Arial", 13),
            bg="white",
            fg="#AAAAAA",
            relief="flat",
            borderwidth=0,
            width=28,
            show=""
        )
        self.signup_password_entry.insert(0, "Password")
        
        # Bind events for Sign Up page placeholder text
        self.fullname_entry.bind("<FocusIn>", lambda e: self.on_fullname_focus_in(e))
        self.fullname_entry.bind("<FocusOut>", lambda e: self.on_fullname_focus_out(e))
        self.email_entry.bind("<FocusIn>", lambda e: self.on_email_focus_in(e))
        self.email_entry.bind("<FocusOut>", lambda e: self.on_email_focus_out(e))
        self.signup_password_entry.bind("<FocusIn>", lambda e: self.on_signup_password_focus_in(e))
        self.signup_password_entry.bind("<FocusOut>", lambda e: self.on_signup_password_focus_out(e))
        
        # Create "Don't have an account? Sign Up" button
        if self.dont_have_acc_photo:
            self.signup_btn = tk.Button(
                root,
                image=self.dont_have_acc_photo,
                border=0,
                relief="flat",
                cursor="hand2",
                command=self.goto_signup_page,
                borderwidth=0,
                highlightthickness=0,
                bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
        else:
            self.signup_btn = tk.Button(
                root,
                text="Don't have an account? Sign Up",
                font=("Arial", 11),
                bg="#C5C6D0",
                fg="#3D5AFE",
                relief="flat",
                border=0,
                cursor="hand2",
                command=self.goto_signup_page,
                activebackground="#C5C6D0",
                activeforeground="#3D5AFE",
                highlightthickness=0,
                bd=0
            )
        
        # Create actual Sign Up button for Sign Up page
        if self.signup_button_photo:
            self.signup_page_btn = tk.Button(
                root,
                image=self.signup_button_photo,
                border=0,
                relief="flat",
                cursor="hand2",
                command=self.handle_signup_submit,
                borderwidth=0,
                highlightthickness=0,
                bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
        else:
            self.signup_page_btn = tk.Button(
                root,
                text="Sign Up",
                font=("Arial", 14, "bold"),
                bg="#3D5AFE",
                fg="white",
                width=15,
                height=2,
                border=0,
                relief="flat",
                cursor="hand2",
                command=self.handle_signup_submit
            )
        
        # Create "Already have an account? Sign In" button
        if self.alr_have_acc_photo:
            self.signin_btn = tk.Button(
                root,
                image=self.alr_have_acc_photo,
                border=0,
                relief="flat",
                cursor="hand2",
                command=self.goto_login_page,
                borderwidth=0,
                highlightthickness=0,
                bg="#C5C6D0",
                activebackground="#C5C6D0"
            )
        else:
            self.signin_btn = tk.Button(
                root,
                text="Already have an account? Sign In",
                font=("Arial", 11),
                bg="#C5C6D0",
                fg="#3D5AFE",
                relief="flat",
                border=0,
                cursor="hand2",
                command=self.goto_login_page,
                activebackground="#C5C6D0",
                activeforeground="#3D5AFE",
                highlightthickness=0,
                bd=0
            )
        
        self.draw_page()
    
    def load_images(self):
        """Load and resize images to fit the screen"""
        for img_path in self.image_paths:
            try:
                img = Image.open(img_path)
                img = img.resize((428, 926), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                self.images.append(img)
                self.photo_images.append(photo)
                print(f"✓ Loaded: {img_path}")
            except FileNotFoundError:
                print(f"✗ Image not found: {img_path}")
                print(f"  Please make sure the image is in the same folder as the script")
                placeholder = Image.new('RGB', (428, 926), color='#C5C6D0')
                photo = ImageTk.PhotoImage(placeholder)
                self.images.append(placeholder)
                self.photo_images.append(photo)
            except Exception as e:
                print(f"✗ Error loading {img_path}: {e}")
                placeholder = Image.new('RGB', (428, 926), color='#C5C6D0')
                photo = ImageTk.PhotoImage(placeholder)
                self.images.append(placeholder)
                self.photo_images.append(photo)
    
    def load_button_images(self):
        """Load button images"""
        try:
            get_started_img = Image.open("Python Frames/GET STARTED.png")
            get_started_img = get_started_img.resize((300, 75), Image.Resampling.LANCZOS)
            self.get_started_photo = ImageTk.PhotoImage(get_started_img)
            print(f"✓ Loaded: GET STARTED button")
        except Exception as e:
            print(f"✗ GET STARTED button not found: {e}")
            self.get_started_photo = None
        
        try:
            allow_location_img = Image.open("Python Frames/Location Button.png")
            allow_location_img = allow_location_img.resize((300, 75), Image.Resampling.LANCZOS)
            self.allow_location_photo = ImageTk.PhotoImage(allow_location_img)
            print(f"✓ Loaded: Location Button")
        except Exception as e:
            print(f"✗ Location Button not found: {e}")
            self.allow_location_photo = None
        
        try:
            login_btn_img = Image.open("Python Frames/LOGIN BUTTON.png")
            login_btn_img = login_btn_img.resize((300, 75), Image.Resampling.LANCZOS)
            self.login_button_photo = ImageTk.PhotoImage(login_btn_img)
            print(f"✓ Loaded: LOGIN BUTTON")
        except Exception as e:
            print(f"✗ LOGIN BUTTON not found: {e}")
            self.login_button_photo = None
        
        try:
            dont_have_acc_img = Image.open("Python Frames/dont have acc.png")
            dont_have_acc_img = dont_have_acc_img.resize((280, 70), Image.Resampling.LANCZOS)
            self.dont_have_acc_photo = ImageTk.PhotoImage(dont_have_acc_img)
            print(f"✓ Loaded: dont have acc button")
        except Exception as e:
            print(f"✗ dont have acc button not found: {e}")
            self.dont_have_acc_photo = None
        
        try:
            signup_button_img = Image.open("Python Frames/SIGN UP BUTTON.PNG")
            signup_button_img = signup_button_img.resize((300, 75), Image.Resampling.LANCZOS)
            self.signup_button_photo = ImageTk.PhotoImage(signup_button_img)
            print(f"✓ Loaded: SIGN UP BUTTON")
        except Exception as e:
            print(f"✗ SIGN UP BUTTON not found: {e}")
            self.signup_button_photo = None
        
        try:
            alr_have_acc_img = Image.open("Python Frames/alr have acc.png")
            alr_have_acc_img = alr_have_acc_img.resize((250, 60), Image.Resampling.LANCZOS)
            self.alr_have_acc_photo = ImageTk.PhotoImage(alr_have_acc_img)
            print(f"✓ Loaded: alr have acc button")
        except Exception as e:
            print(f"✗ alr have acc button not found: {e}")
            self.alr_have_acc_photo = None
    
    def load_home_icons(self):
        """Load home page icon images"""
        icon_paths = {
            'car': "Python Frames/Car.png",
            'map': "Python Frames/Map.png",
            'activity': "Python Frames/Activity.png",
            'payment': "Python Frames/Payment.png",
            'coupon': "Python Frames/Coupon.png",
            'coming_soon': "Python Frames/Coming Soon.png"
        }
        
        self.home_icons = {}
        
        for icon_name, icon_path in icon_paths.items():
            try:
                icon_img = Image.open(icon_path)
                icon_img = icon_img.resize((170, 170), Image.Resampling.LANCZOS)
                self.home_icons[icon_name] = ImageTk.PhotoImage(icon_img)
                print(f"✓ Loaded: {icon_name} icon")
            except Exception as e:
                print(f"✗ {icon_name} icon not found: {e}")
                self.home_icons[icon_name] = None
    
    def draw_page(self):
        """Display the current page image"""
        self.canvas.delete("all")
        
        # Hide all buttons and input fields first
        self.get_started_btn.place_forget()
        self.allow_location_btn.place_forget()
        self.login_btn.place_forget()
        self.username_entry.place_forget()
        self.password_entry.place_forget()
        self.signup_btn.place_forget()
        self.fullname_entry.place_forget()
        self.email_entry.place_forget()
        self.signup_password_entry.place_forget()
        self.signup_page_btn.place_forget()
        self.signin_btn.place_forget()
        
        if self.current_page < len(self.photo_images):
            # Display the image
            self.canvas.create_image(214, 463, image=self.photo_images[self.current_page])
            
            # Show appropriate button based on page
            if self.current_page in [1, 2, 3]:
                self.get_started_btn.place(x=214, y=830, anchor="center")
            elif self.current_page == 4:
                self.allow_location_btn.place(x=214, y=830, anchor="center")
            elif self.current_page == 5:
                # Login page
                self.create_rounded_rect(64, 470, 364, 515, 25, fill="white", outline="")
                self.create_rounded_rect(64, 545, 364, 590, 25, fill="white", outline="")
                
                self.username_entry.place(x=214, y=492, anchor="center")
                self.password_entry.place(x=214, y=567, anchor="center")
                self.login_btn.place(x=214, y=665, anchor="center")
                self.signup_btn.place(x=214, y=898, anchor="center")
            elif self.current_page == 6:
                # Sign Up page - same size as Login page
                self.create_rounded_rect(64, 322, 364, 372, 25, fill="white", outline="")
                self.create_rounded_rect(64, 397, 364, 447, 25, fill="white", outline="")
                self.create_rounded_rect(64, 472, 364, 522, 25, fill="white", outline="")
                
                self.fullname_entry.place(x=214, y=347, anchor="center")
                self.email_entry.place(x=214, y=422, anchor="center")
                self.signup_password_entry.place(x=214, y=497, anchor="center")
                self.signup_page_btn.place(x=214, y=583, anchor="center")
                self.signin_btn.place(x=214, y=897, anchor="center")
            elif self.current_page == 7:
                # Home page with icon buttons
                self.show_home_icons()
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle on canvas"""
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def next_page(self, event):
        """Move to the next page (click anywhere on canvas)"""
        if self.current_page == 0:
            self.current_page = self.current_page + 1
            self.draw_page()
    
    def next_page_btn(self):
        """Move to the next page (button click)"""
        if self.current_page < len(self.photo_images) - 1:
            self.current_page = self.current_page + 1
        else:
            self.current_page = 0
        self.draw_page()
    
    def goto_signup_page(self):
        """Navigate to sign up page"""
        print("Sign Up button clicked! Navigating to Sign Up page...")
        self.current_page = 6
        self.draw_page()
    
    def goto_login_page(self):
        """Navigate to login page"""
        print("Sign In button clicked! Navigating to Login page...")
        self.current_page = 5
        self.draw_page()
    
    def handle_login(self):
        """Handle login button click with authentication"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "Username:" or password == "Password:":
            messagebox.showwarning("Login Error", "Please enter username and password")
            return
        
        # Check credentials
        if username == "admin" and password == "admin123":
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            print(f"✓ Login successful - Username: {username}")
            # Navigate to home page
            self.show_home_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            print(f"✗ Login failed - Username: {username}")
    
    def handle_signup_submit(self):
        """Handle sign up form submission"""
        fullname = self.fullname_entry.get()
        email = self.email_entry.get()
        password = self.signup_password_entry.get()
        
        if fullname == "Full Name" or email == "Email" or password == "Password":
            messagebox.showwarning("Sign Up Error", "Please fill in all fields")
            return
        
        print(f"Sign Up attempt - Name: {fullname}, Email: {email}, Password: {password}")
        messagebox.showinfo("Sign Up Successful", f"Account created for {fullname}!")
    
    def on_username_focus_in(self, event):
        if self.username_entry.get() == "Username:":
            self.username_entry.delete(0, tk.END)
            self.username_entry.config(fg="black")
    
    def on_username_focus_out(self, event):
        if self.username_entry.get() == "":
            self.username_entry.insert(0, "Username:")
            self.username_entry.config(fg="#AAAAAA")
    
    def on_password_focus_in(self, event):
        if self.password_entry.get() == "Password:":
            self.password_entry.delete(0, tk.END)
            self.password_entry.config(fg="black", show="*")
    
    def on_password_focus_out(self, event):
        if self.password_entry.get() == "":
            self.password_entry.insert(0, "Password:")
            self.password_entry.config(fg="#AAAAAA", show="")
    
    def on_fullname_focus_in(self, event):
        if self.fullname_entry.get() == "Full Name":
            self.fullname_entry.delete(0, tk.END)
            self.fullname_entry.config(fg="black")
    
    def on_fullname_focus_out(self, event):
        if self.fullname_entry.get() == "":
            self.fullname_entry.insert(0, "Full Name")
            self.fullname_entry.config(fg="#AAAAAA")
    
    def on_email_focus_in(self, event):
        if self.email_entry.get() == "Email":
            self.email_entry.delete(0, tk.END)
            self.email_entry.config(fg="black")
    
    def on_email_focus_out(self, event):
        if self.email_entry.get() == "":
            self.email_entry.insert(0, "Email")
            self.email_entry.config(fg="#AAAAAA")
    
    def on_signup_password_focus_in(self, event):
        if self.signup_password_entry.get() == "Password":
            self.signup_password_entry.delete(0, tk.END)
            self.signup_password_entry.config(fg="black", show="*")
    
    def on_signup_password_focus_out(self, event):
        if self.signup_password_entry.get() == "":
            self.signup_password_entry.insert(0, "Password")
            self.signup_password_entry.config(fg="#AAAAAA", show="")
    
    def show_home_page(self):
        """Navigate to home page after successful login"""
        print("Navigating to home page...")
        self.current_page = 7
        self.draw_page()
    
    def show_home_icons(self):
        """Display clickable icon buttons on home page"""
        # Define icon positions (x, y) - matching the new target layout
        icon_positions = [
            (113, 180),   # Car icon (top-left)
            (313, 180),  # Map icon (top-right)
            (113, 380),   # Activity icon (middle-left)
            (313, 380),  # Payment icon (middle-right)
            (113, 580),   # Coupon icon (bottom-left)
            (313, 580)   # Coming Soon icon (bottom-right)
        ]
        
        icon_names = ['car', 'map', 'activity', 'payment', 'coupon', 'coming_soon']
        
        for i, (icon_name, (x, y)) in enumerate(zip(icon_names, icon_positions)):
            if self.home_icons.get(icon_name):
                btn = tk.Button(
                    self.root,
                    image=self.home_icons[icon_name],
                    border=0,
                    relief="flat",
                    cursor="hand2",
                    command=lambda name=icon_name: self.handle_home_icon_click(name),
                    borderwidth=0,
                    highlightthickness=0,
                    bg="#C5C6D0",
                    activebackground="#C5C6D0"
                )
                btn.place(x=x, y=y, anchor="center")
    
    def handle_home_icon_click(self, icon_name):
        """Handle home page icon button clicks"""
        print(f"{icon_name.upper()} icon clicked!")
        messagebox.showinfo("Feature", f"{icon_name.replace('_', ' ').title()} feature coming soon!")

if __name__ == "__main__":
    root = tk.Tk()
    app = OnboardingCarousel(root)
    root.mainloop()