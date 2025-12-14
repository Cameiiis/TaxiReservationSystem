# functions.py - All Business Logic and Helper Functions

from PIL import Image, ImageTk
from tkinter import messagebox
import config

# ==================== IMAGE LOADING ====================

def load_image(path, size):
    """Load and resize an image"""
    try:
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        print(f"✅ Loaded: {path}")
        return img, photo
    except Exception as e:
        print(f"❌ Error loading {path}: {e}")
        placeholder = Image.new('RGB', size, color=config.WINDOW_BG_COLOR)
        return placeholder, ImageTk.PhotoImage(placeholder)

def load_all_page_images():
    """Load all page images"""
    images = []
    photo_images = []
    
    for img_name in config.PAGE_IMAGES:
        img_path = config.IMAGE_FOLDER + img_name
        img, photo = load_image(img_path, (config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        images.append(img)
        photo_images.append(photo)
    
    return images, photo_images

def load_all_button_images():
    """Load all button images"""
    button_images = {}
    
    for key, (filename, size) in config.BUTTON_IMAGES.items():
        path = config.IMAGE_FOLDER + filename
        _, photo = load_image(path, size)
        button_images[key] = photo
    
    return button_images

def load_all_home_icons():
    """Load all home page icons"""
    home_icons = {}
    
    for icon_name, filename in config.HOME_ICONS.items():
        path = config.IMAGE_FOLDER + filename
        _, photo = load_image(path, config.ICON_SIZE)
        home_icons[icon_name] = photo
    
    return home_icons

# ==================== AUTHENTICATION ====================

def validate_login(username, password):
    """Validate login credentials"""
    if username == "Username:" or password == "Password:":
        return False, "Please enter username and password"
    
    if username == config.DEFAULT_USERNAME and password == config.DEFAULT_PASSWORD:
        return True, f"Welcome, {username}!"
    
    return False, "Invalid username or password"

def validate_signup(fullname, email, password):
    """Validate signup form"""
    if fullname == "Full Name" or email == "Email" or password == "Password":
        return False, "Please fill in all fields"
    
    # Add more validation here (email format, password strength, etc.)
    return True, f"Account created for {fullname}!"

# ==================== UTILITY FUNCTIONS ====================

def center_window(window, width, height):
    """Calculate centered window geometry"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    center_x = int(screen_width/2 - width/2)
    center_y = int(screen_height/2 - height/2)
    
    return f'{width}x{height}+{center_x}+{center_y}'

def create_rounded_rect_points(x1, y1, x2, y2, radius):
    """Generate points for a rounded rectangle"""
    points = [
        x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
        x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
        x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
        x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
    ]
    return points

# ==================== FEATURE HANDLERS ====================

def handle_home_icon_click(icon_name, parent_window):
    """Handle home page icon clicks"""
    print(f"{icon_name.upper()} icon clicked!")
    
    if icon_name == 'map':
        open_map_window(parent_window)
    elif icon_name == 'payment':
        open_wallet_window(parent_window)
    elif icon_name == 'activity':
        open_my_rides_window(parent_window)
    elif icon_name == 'coupon':
        open_voucher_window(parent_window)
    else:
        messagebox.showinfo("Feature", f"{icon_name.replace('_', ' ').title()} feature coming soon!")

def open_map_window(parent_window):
    """Open the QuickCab map booking system"""
    try:
        from map_system import QuickCabMapSystem
        map_system = QuickCabMapSystem(parent_window)
        print("✅ QuickCab Map window opened successfully!")
    except ImportError as e:
        messagebox.showerror(
            "QuickCab Error", 
            f"Could not import map_system.py!\n\nMake sure map_system.py is in the same folder.\n\nError: {e}"
        )
        print(f"❌ Import error: {e}")
    except Exception as e:
        messagebox.showerror("QuickCab Error", f"Could not open map window!\n\nError: {e}")
        print(f"❌ Error opening map: {e}")

def open_wallet_window(parent_window):
    """Open the Wallet screen"""
    try:
        from wallet_screen import WalletScreen
        wallet = WalletScreen(parent_window)
        print("✅ Wallet window opened successfully!")
    except ImportError as e:
        messagebox.showerror(
            "QuickCab Error", 
            f"Could not import wallet_screen.py!\n\nMake sure wallet_screen.py is in the same folder.\n\nError: {e}"
        )
        print(f"❌ Import error: {e}")
    except Exception as e:
        messagebox.showerror("QuickCab Error", f"Could not open wallet window!\n\nError: {e}")
        print(f"❌ Error opening wallet: {e}")

def open_my_rides_window(parent_window):
    """Open the My Rides screen"""
    try:
        from my_rides_screen import MyRidesScreen
        my_rides = MyRidesScreen(parent_window)
        print("✅ My Rides window opened successfully!")
    except ImportError as e:
        messagebox.showerror(
            "QuickCab Error", 
            f"Could not import my_rides_screen.py!\n\nMake sure my_rides_screen.py is in the same folder.\n\nError: {e}"
        )
        print(f"❌ Import error: {e}")
    except Exception as e:
        messagebox.showerror("QuickCab Error", f"Could not open My Rides window!\n\nError: {e}")
        print(f"❌ Error opening My Rides: {e}")

def open_voucher_window(parent_window):
    """Open the Voucher screen"""
    try:
        from voucher_screen import VoucherScreen
        voucher = VoucherScreen(parent_window)
        print("✅ Voucher window opened successfully!")
    except ImportError as e:
        messagebox.showerror(
            "QuickCab Error", 
            f"Could not import voucher_screen.py!\n\nMake sure voucher_screen.py is in the same folder.\n\nError: {e}"
        )
        print(f"❌ Import error: {e}")
    except Exception as e:
        messagebox.showerror("QuickCab Error", f"Could not open Voucher window!\n\nError: {e}")
        print(f"❌ Error opening Voucher: {e}")