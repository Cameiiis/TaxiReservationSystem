# gui.py - Main GUI

import tkinter as tk
from tkinter import Canvas, messagebox
import config
import functions
from gui_components import UIComponents
from menu_manager import MenuManager

class QuickCabGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickCab")
        
        geometry = functions.center_window(root, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.root.geometry(geometry)
        self.root.configure(bg=config.WINDOW_BG_COLOR)
        self.root.resizable(False, False)
        
        self.current_page = 0
        self.home_icon_buttons = []
        
        self.images, self.photo_images = functions.load_all_page_images()
        
        self.canvas = Canvas(
            root, width=config.WINDOW_WIDTH, height=config.WINDOW_HEIGHT,
            bg=config.WINDOW_BG_COLOR, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        self.menu_manager = MenuManager(root, self)
        
        self.ui_components = UIComponents(root, self.canvas)
        self.components = {}
        self.create_all_components()
        
        self.draw_page()
    
    def create_all_components(self):
        """Create all UI components"""
        button_components = self.ui_components.create_all_buttons()
        self.components.update(button_components)
        
        entry_components = self.ui_components.create_all_entries()
        self.components.update(entry_components)
        
        self.components['get_started_btn'].config(command=self.next_page_btn)
        self.components['allow_location_btn'].config(command=self.next_page_btn)
        self.components['login_btn'].config(command=self.handle_login)
        self.components['signup_btn'].config(command=self.goto_signup_page)
        self.components['signup_page_btn'].config(command=self.handle_signup_submit)
        self.components['signin_btn'].config(command=self.goto_login_page)
        self.components['menu_btn'].config(command=self.menu_manager.toggle)
        
        self.components['show_password_btn'].config(command=self.toggle_login_password)
        self.components['show_signup_password_btn'].config(command=self.toggle_signup_password)
        
        self.bind_entry_events()
    
    def bind_entry_events(self):
        """Bind entry field events"""
        entries = [
            (self.components['username_entry'], "Username:", False),
            (self.components['password_entry'], "Password:", True),
            (self.components['fullname_entry'], "Full Name", False),
            (self.components['email_entry'], "Email", False),
            (self.components['signup_password_entry'], "Password", True),
        ]
        
        for entry, placeholder, is_password in entries:
            entry.bind("<FocusIn>", lambda e, p=placeholder, pw=is_password: 
                      self.on_entry_focus_in(e, p, pw))
            entry.bind("<FocusOut>", lambda e, p=placeholder, pw=is_password: 
                      self.on_entry_focus_out(e, p, pw))
        
        self.components['username_entry'].bind("<Return>", lambda e: self.handle_login())
        self.components['password_entry'].bind("<Return>", lambda e: self.handle_login())
    
    def toggle_login_password(self):
        """Toggle login password visibility"""
        self.ui_components.password_visible = not self.ui_components.password_visible
        
        if self.ui_components.password_visible:
            self.components['password_entry'].config(show="")
            self.components['show_password_btn'].config(text="🙈")
        else:
            if self.components['password_entry'].get() != "Password:":
                self.components['password_entry'].config(show="*")
            self.components['show_password_btn'].config(text="👁")
    
    def toggle_signup_password(self):
        """Toggle signup password visibility"""
        self.ui_components.signup_password_visible = not self.ui_components.signup_password_visible
        
        if self.ui_components.signup_password_visible:
            self.components['signup_password_entry'].config(show="")
            self.components['show_signup_password_btn'].config(text="🙈")
        else:
            if self.components['signup_password_entry'].get() != "Password":
                self.components['signup_password_entry'].config(show="*")
            self.components['show_signup_password_btn'].config(text="👁")
    
    def draw_page(self):
        """Draw the current page"""
        self.canvas.delete("all")
        self.hide_all_components()
        
        if self.menu_manager.menu_open:
            self.menu_manager.close()
        
        if self.current_page < len(self.photo_images):
            self.canvas.create_image(214, 463, image=self.photo_images[self.current_page])
            
            if self.current_page in config.PAGE_WELCOME:
                self.components['get_started_btn'].place(x=214, y=830, anchor="center")
            
            elif self.current_page == config.PAGE_LOCATION:
                self.components['allow_location_btn'].place(x=214, y=830, anchor="center")
            
            elif self.current_page == config.PAGE_LOGIN:
                self.draw_login_page()
            
            elif self.current_page == config.PAGE_SIGNUP:
                self.draw_signup_page()
            
            elif self.current_page == config.PAGE_HOME:
                self.draw_home_page()
    
    def draw_login_page(self):
        """Draw login page with show password button"""
        self.create_rounded_rect(64, 470, 364, 515, 25, fill="white", outline="")
        self.create_rounded_rect(64, 545, 364, 590, 25, fill="white", outline="")
        
        self.components['username_entry'].place(x=214, y=492, anchor="center")
        self.components['password_entry'].place(x=200, y=567, anchor="center")
        
        self.components['show_password_btn'].place(x=340, y=567, anchor="center")
        
        self.components['login_btn'].place(x=214, y=665, anchor="center")
        self.components['signup_btn'].place(x=214, y=898, anchor="center")
    
    def draw_signup_page(self):
        """Draw signup page with show password button"""
        self.create_rounded_rect(64, 322, 364, 372, 25, fill="white", outline="")
        self.create_rounded_rect(64, 397, 364, 447, 25, fill="white", outline="")
        self.create_rounded_rect(64, 472, 364, 522, 25, fill="white", outline="")
        
        self.components['fullname_entry'].place(x=214, y=347, anchor="center")
        self.components['email_entry'].place(x=214, y=422, anchor="center")
        self.components['signup_password_entry'].place(x=200, y=497, anchor="center")
        
        self.components['show_signup_password_btn'].place(x=340, y=497, anchor="center")
        
        self.components['signup_page_btn'].place(x=214, y=583, anchor="center")
        self.components['signin_btn'].place(x=214, y=897, anchor="center")
    
    def draw_home_page(self):
        """Draw home page"""
        self.components['menu_btn'].place(x=25, y=35, anchor="center")
        
        for btn in self.home_icon_buttons:
            btn.destroy()
        self.home_icon_buttons.clear()
        
        icon_data = self.ui_components.create_home_icon_buttons()
        for btn, x, y, icon_name in icon_data:
            btn.config(command=lambda name=icon_name: functions.handle_home_icon_click(name, self.root))
            btn.place(x=x, y=y, anchor="center")
            self.home_icon_buttons.append(btn)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create rounded rectangle"""
        points = functions.create_rounded_rect_points(x1, y1, x2, y2, radius)
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def hide_all_components(self):
        """Hide all UI components"""
        for component in self.components.values():
            component.place_forget()
        
        for btn in self.home_icon_buttons:
            btn.place_forget()
    
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
        """Navigate to signup"""
        self.current_page = config.PAGE_SIGNUP
        self.draw_page()
    
    def goto_login_page(self):
        """Navigate to login"""
        self.current_page = config.PAGE_LOGIN
        self.draw_page()
    
    def goto_home_page(self):
        """Navigate to home"""
        self.current_page = config.PAGE_HOME
        self.draw_page()
    
    def handle_login(self):
        """Handle login"""
        username = self.components['username_entry'].get()
        password = self.components['password_entry'].get()
        
        success, message = functions.validate_login(username, password)
        
        if success:
            from terms_popup import show_terms_popup
            
            def on_terms_accepted():
                messagebox.showinfo("Login Successful", message)
                self.goto_home_page()
            
            show_terms_popup(self.root, on_terms_accepted)
        else:
            messagebox.showerror("Login Failed", message)
    
    def handle_signup_submit(self):
        """Handle signup with password validation"""
        fullname = self.components['fullname_entry'].get()
        email = self.components['email_entry'].get()
        password = self.components['signup_password_entry'].get()
        
        success, message = functions.validate_signup(fullname, email, password)
        
        if success:
            messagebox.showinfo("Sign Up Successful", message)
            config.CURRENT_USERNAME = email.split('@')[0]
            config.CURRENT_USER_FULLNAME = fullname
            self.goto_home_page()
        else:
            messagebox.showwarning("Sign Up Error", message)
    
    def on_entry_focus_in(self, event, placeholder, is_password):
        """Handle entry focus in"""
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=config.BLACK_TEXT)
            if is_password:
                if entry == self.components['password_entry']:
                    if not self.ui_components.password_visible:
                        entry.config(show="*")
                elif entry == self.components['signup_password_entry']:
                    if not self.ui_components.signup_password_visible:
                        entry.config(show="*")
    
    def on_entry_focus_out(self, event, placeholder, is_password):
        """Handle entry focus out"""
        entry = event.widget
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg=config.GRAY_TEXT)
            if is_password:
                entry.config(show="")