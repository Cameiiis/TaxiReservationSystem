# config.py - Configuration Settings

# Window Settings
WINDOW_WIDTH = 428
WINDOW_HEIGHT = 926
WINDOW_BG_COLOR = "#C5C6D0"

# Colors
PRIMARY_COLOR = "#3D5AFE"
WHITE = "white"
GRAY_TEXT = "#AAAAAA"
BLACK_TEXT = "black"

# Image Paths
IMAGE_FOLDER = "Python Frames/"

PAGE_IMAGES = [
    "Opening.png",
    "Welcome.png",
    "Welcome1.png",
    "Welcome2.png",
    "Location.png",
    "LOGIN PAGE.png",
    "Sign Up.png",
    "home.png"
]

BUTTON_IMAGES = {
    'get_started': ("GET STARTED.png", (300, 75)),
    'allow_location': ("Location Button.png", (300, 75)),
    'login_button': ("LOGIN BUTTON.png", (300, 75)),
    'dont_have_acc': ("dont have acc.png", (280, 70)),
    'signup_button': ("SIGN UP BUTTON.PNG", (300, 75)),
    'alr_have_acc': ("alr have acc.png", (250, 60)),
    'menu_button': ("menu button.png", (30, 20)),
    'menu_button_white': ("menu button white.png", (30, 20)),
    'menu_panel': ("Left Menu page.png", (428, 926))
}

HOME_ICONS = {
    'car': "Car.png",
    'map': "Map.png",
    'activity': "Activity.png",
    'payment': "Payment.png",
    'coupon': "Coupon.png",
    'coming_soon': "Coming Soon.png"
}

ICON_SIZE = (170, 170)

HOME_ICON_POSITIONS = [
    (113, 180), (313, 180),
    (113, 380), (313, 380),
    (113, 580), (313, 580)
]

# Authentication
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"

# Page Indices
PAGE_OPENING = 0
PAGE_WELCOME = [1, 2, 3]
PAGE_LOCATION = 4
PAGE_LOGIN = 5
PAGE_SIGNUP = 6
PAGE_HOME = 7