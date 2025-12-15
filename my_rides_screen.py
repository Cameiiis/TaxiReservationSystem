import tkinter as tk
from tkinter import Canvas, messagebox, Scrollbar
from PIL import Image, ImageTk
import os
from functions import get_user_rides_db
import config

class MyRidesScreen:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        
        # Window dimensions
        self.window_width = 428
        self.window_height = 926
        
        # Get ride data from database
        self.rides = get_user_rides_db()
        
        # If no rides from database, use sample data as fallback
        if not self.rides:
            self.rides = [
                {
                    "id": "QC-2024-001",
                    "date": "02/05/2022",
                    "time": "02:30 PM",
                    "from": "M.Roxas Ave cor C.M Recto Ave, Davao City",
                    "to": "DPT Bldg, Ma-A Talomo, Davao City",
                    "distance": "5.2 km",
                    "duration": "15 mins",
                    "fare": 250,
                    "vehicle": "Sedan",
                    "driver": "Juan Dela Cruz",
                    "rating": 5,
                    "status": "Completed"
                },
                {
                    "id": "QC-2024-002",
                    "date": "08/05/2022",
                    "time": "09:15 AM",
                    "from": "M.Roxas Ave cor C.M Recto Ave, Davao City",
                    "to": "MacArthur Hwy, Matina Crossing Talomo, Davao City",
                    "distance": "3.8 km",
                    "duration": "12 mins",
                    "fare": 360,
                    "vehicle": "Sedan",
                    "driver": "Maria Santos",
                    "rating": 4,
                    "status": "Cancel"
                },
                {
                    "id": "QC-2024-003",
                    "date": "08/05/2022",
                    "time": "06:45 PM",
                    "from": "Toril, Davao City",
                    "to": "Mintal, Davao City",
                    "distance": "7.1 km",
                    "duration": "20 mins",
                    "fare": 150,
                    "vehicle": "SUV",
                    "driver": "Pedro Reyes",
                    "rating": 5,
                    "status": "Cancelled"
                }
            ]
        
        # Create popup window
        self.root = tk.Toplevel(parent_window)
        self.root.title("My Rides")
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - self.window_width) / 2)
        y = int((screen_height - self.window_height) / 2)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg="#D2D2DF")
        
        # Load images
        self.load_images()
        
        # Setup UI
        self.setup_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.go_back)
        
        print("✅ My Rides Screen opened")
    
    def load_images(self):
        """Load my rides screen images"""
        frames_folder = "Python Frames"
        
        self.undo_btn_img = None
        
        try:
            # Load undo button
            undo_path = os.path.join(frames_folder, "undo button.png")
            if os.path.exists(undo_path):
                img = Image.open(undo_path)
                img = img.resize((70, 50), Image.Resampling.LANCZOS)
                self.undo_btn_img = ImageTk.PhotoImage(img)
                print(f"✓ Loaded undo button.png")
                
        except Exception as e:
            print(f"Error loading images: {e}")
    
    def setup_ui(self):
        """Setup the my rides screen UI"""
        # Create main canvas
        self.canvas = Canvas(
            self.root,
            width=self.window_width,
            height=self.window_height,
            bg="#D2D2DF",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Header section with D2D2DF background (same as main bg)
        header_frame = tk.Frame(self.root, bg="#D2D2DF", height=110)
        header_frame.place(x=0, y=0, width=self.window_width)
        
        # Back/Undo button (top left) - blends with background
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
        
        # Title "History" - centered
        tk.Label(
            header_frame, text="History",
            font=("Arial", 22, "bold"), bg="#D2D2DF", fg="#333"
        ).place(relx=0.5, y=50, anchor="center")
        
        # Create scrollable rides list
        self.create_rides_list()
    
    def create_rounded_rect_on_canvas(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle on a canvas"""
        points = [
            x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
            x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
            x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
            x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
    def create_rides_list(self):
        """Create scrollable rides history list"""
        # Container frame for scrollable area - WIDER
        list_container = tk.Frame(self.root, bg="#D2D2DF", width=409, height=800)
        list_container.place(x=10, y=110)
        list_container.pack_propagate(False)
        
        # Create canvas for scrolling
        list_canvas = Canvas(
            list_container, bg="#D2D2DF", highlightthickness=0,
            width=409, height=800
        )
        
        # Scrollbar
        scrollbar = Scrollbar(
            list_container, orient="vertical", command=list_canvas.yview
        )
        
        # Frame inside canvas
        self.scrollable_frame = tk.Frame(list_canvas, bg="#D2D2DF")
        
        # Configure scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
        )
        
        # Create window in canvas
        list_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        list_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        list_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate rides
        self.populate_rides()
        
        # Enable mouse wheel scrolling
        list_canvas.bind_all("<MouseWheel>", lambda e: list_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def populate_rides(self):
        """Populate ride history items"""
        for ride in self.rides:
            self.create_ride_item(ride)
    
    def get_status_colors(self, status):
        """Get colors based on status"""
        if status == "Completed":
            return "#d1fae5", "#059669"  # Light green bg, dark green text
        elif status == "Cancel":
            return "#ffe4e6", "#e11d48"  # Light pink bg, red text
        elif status == "Cancelled":
            return "#f3f4f6", "#6b7280"  # Light gray bg, gray text
        else:
            return "#dbeafe", "#2563eb"  # Light blue bg, blue text
    
    def create_ride_item(self, ride):
        """Create a single ride item card - ULTRA CLEAN DESIGN"""
        # Container canvas for rounded rectangle - WIDER BOX
        item_canvas = Canvas(
            self.scrollable_frame, width=390, height=135,
            bg="#D2D2DF", highlightthickness=0
        )
        item_canvas.pack(pady=6, padx=0)
        
        # Draw subtle shadow
        self.create_rounded_rect_on_canvas(
            item_canvas, 2, 2, 388, 133, 18,
            fill="#b8b8b8", outline=""
        )
        
        # Draw main white rounded background - WIDER
        self.create_rounded_rect_on_canvas(
            item_canvas, 0, 0, 386, 131, 18,
            fill="white", outline=""
        )
        
        # Content frame - WIDER
        content_frame = tk.Frame(item_canvas, bg="white")
        item_canvas.create_window(193, 65, window=content_frame, width=366, height=121)
        
        # Status badge (top left) - dynamic color based on status
        status_bg, status_fg = self.get_status_colors(ride['status'])
        
        status_canvas = Canvas(content_frame, width=85, height=22, bg="white", highlightthickness=0)
        status_canvas.pack(anchor="w", padx=15, pady=(8, 6))
        
        # Draw rounded status pill
        self.create_rounded_rect_on_canvas(
            status_canvas, 0, 0, 85, 22, 11,
            fill=status_bg, outline=""
        )
        
        status_canvas.create_text(
            43, 12, text=ride['status'],
            font=("Arial", 8, "bold"), fill=status_fg
        )
        
        # Locations section
        locations_frame = tk.Frame(content_frame, bg="white")
        locations_frame.pack(fill="x", padx=15, pady=(0, 6))
        
        # Blue circle icon (pickup)
        pickup_row = tk.Frame(locations_frame, bg="white")
        pickup_row.pack(fill="x", pady=(0, 4))
        
        # Blue circle
        blue_circle = Canvas(pickup_row, width=16, height=16, bg="white", highlightthickness=0)
        blue_circle.pack(side="left", padx=(0, 6))
        blue_circle.create_oval(3, 3, 13, 13, fill="#3D5AFE", outline="")
        
        # From location
        tk.Label(
            pickup_row, text=ride['from'],
            font=("Arial", 9), bg="white", fg="#333", 
            wraplength=300, anchor="w", justify="left"
        ).pack(side="left", fill="x", expand=True)
        
        # Black dot (destination)
        dest_row = tk.Frame(locations_frame, bg="white")
        dest_row.pack(fill="x")
        
        # Black dot
        black_dot = Canvas(dest_row, width=16, height=16, bg="white", highlightthickness=0)
        black_dot.pack(side="left", padx=(0, 6))
        black_dot.create_oval(5, 5, 11, 11, fill="#000000", outline="")
        
        # To location
        tk.Label(
            dest_row, text=ride['to'],
            font=("Arial", 9), bg="white", fg="#666", 
            wraplength=300, anchor="w", justify="left"
        ).pack(side="left", fill="x", expand=True)
        
        # Bottom row (fare + date) - ALIGNED PROPERLY
        bottom_frame = tk.Frame(content_frame, bg="white")
        bottom_frame.pack(fill="x", padx=15, pady=(8, 8))
        
        # Date (LEFT side, small gray) - ALIGNED
        date_label = tk.Label(
            bottom_frame, text=ride['date'],
            font=("Arial", 7), bg="white", fg="#999", anchor="w"
        )
        date_label.pack(side="left")
        
        # Fare (RIGHT side, bold blue) - ALIGNED
        fare_label = tk.Label(
            bottom_frame, text=f"₱{ride['fare']}",
            font=("Arial", 16, "bold"), bg="white", fg="#3D5AFE", anchor="e"
        )
        fare_label.pack(side="right")
        
        # Make card clickable to view details
        def on_card_click(e):
            self.view_ride_details(ride)
        
        item_canvas.bind("<Button-1>", on_card_click)
        item_canvas.bind("<Enter>", lambda e: item_canvas.config(cursor="hand2"))
        item_canvas.bind("<Leave>", lambda e: item_canvas.config(cursor=""))
    
    def view_ride_details(self, ride):
        """View detailed ride information"""
        # Create detail popup
        detail_popup = tk.Toplevel(self.root)
        detail_popup.title("Ride Details")
        detail_popup.geometry("390x700")
        detail_popup.configure(bg="white")
        detail_popup.resizable(False, False)
        
        # Center popup
        detail_popup.transient(self.root)
        detail_popup.grab_set()
        
        # Header
        header = tk.Frame(detail_popup, bg="#3D5AFE", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header, text="🚗 Ride Details",
            font=("Arial", 18, "bold"), bg="#3D5AFE", fg="white"
        ).pack(pady=25)
        
        # Content scrollable frame
        content = tk.Frame(detail_popup, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Trip ID
        info_row(content, "Trip ID", ride['id'])
        info_row(content, "Date", ride['date'])
        info_row(content, "Time", ride['time'])
        
        # Get status color
        _, status_color = self.get_status_colors(ride['status'])
        info_row(content, "Status", ride['status'], status_color)
        
        tk.Label(content, text="", bg="white", height=1).pack()  # Spacer
        
        info_row(content, "Pickup Location", ride['from'])
        info_row(content, "Drop-off Location", ride['to'])
        
        tk.Label(content, text="", bg="white", height=1).pack()  # Spacer
        
        info_row(content, "Distance", ride['distance'])
        info_row(content, "Duration", ride['duration'])
        info_row(content, "Vehicle Type", ride['vehicle'])
        info_row(content, "Driver", ride['driver'])
        info_row(content, "Rating", "⭐" * ride['rating'])
        
        tk.Label(content, text="", bg="white", height=1).pack()  # Spacer
        
        # Fare (highlighted)
        fare_frame = tk.Frame(content, bg="#f0f9ff", highlightbackground="#3D5AFE", highlightthickness=2)
        fare_frame.pack(fill="x", pady=10)
        
        tk.Label(
            fare_frame, text="Total Fare",
            font=("Arial", 12), bg="#f0f9ff", fg="#666"
        ).pack(pady=(10, 0))
        
        tk.Label(
            fare_frame, text=f"₱{ride['fare']}",
            font=("Arial", 28, "bold"), bg="#f0f9ff", fg="#3D5AFE"
        ).pack(pady=(0, 10))
        
        # Action buttons
        btn_frame = tk.Frame(content, bg="white")
        btn_frame.pack(fill="x", pady=15)
        
        # Book Again button
        book_btn = tk.Button(
            btn_frame, text="🔄 Book Again", font=("Arial", 12, "bold"),
            bg="#3D5AFE", fg="white", border=0, relief="flat",
            cursor="hand2", command=lambda: [detail_popup.destroy(), self.book_again(ride)],
            width=18, height=2
        )
        book_btn.pack(side="left", padx=(0, 5))
        
        # Download Receipt button
        receipt_btn = tk.Button(
            btn_frame, text="📄 Receipt", font=("Arial", 12, "bold"),
            bg="#f0f0f0", fg="#333", border=0, relief="flat",
            cursor="hand2", command=lambda: self.view_receipt(ride),
            width=18, height=2
        )
        receipt_btn.pack(side="left")
        
        # Close button
        close_btn = tk.Button(
            content, text="Close", font=("Arial", 11),
            bg="white", fg="#666", border=0, relief="flat",
            cursor="hand2", command=detail_popup.destroy,
            width=20, height=1
        )
        close_btn.pack(pady=10)
    
    def book_again(self, ride):
        """Book the same ride again"""
        msg = (
            f"📍 Book This Ride Again?\n\n"
            f"From: {ride['from']}\n\n"
            f"To: {ride['to']}\n\n"
            f"Previous Fare: ₱{ride['fare']}\n"
            f"Vehicle: {ride['vehicle']}"
        )
        
        if messagebox.askyesno("Book Again", msg):
            messagebox.showinfo(
                "Ride Booked! 🚗",
                f"Opening map to book your ride...\n\n"
                f"Route: {ride['from']} → {ride['to']}"
            )
            print(f"✅ Booking again: {ride['id']}")
    
    def view_receipt(self, ride):
        """View/download receipt for a ride"""
        receipt_text = (
            f"📄 QUICKCAB RECEIPT\n"
            f"{'='*40}\n\n"
            f"Trip ID: {ride['id']}\n"
            f"Date: {ride['date']}\n"
            f"Status: {ride['status']}\n\n"
            f"TRIP DETAILS:\n"
            f"From: {ride['from']}\n"
            f"To: {ride['to']}\n"
            f"Distance: {ride['distance']}\n"
            f"Duration: {ride['duration']}\n\n"
            f"FARE BREAKDOWN:\n"
            f"Base Fare: ₱40\n"
            f"Distance Charge: ₱{ride['fare'] - 40}\n"
            f"Total Fare: ₱{ride['fare']}\n\n"
            f"DRIVER:\n"
            f"Name: {ride['driver']}\n"
            f"Vehicle: {ride['vehicle']}\n"
            f"Rating: {'⭐' * ride['rating']}\n\n"
            f"Thank you for riding with QuickCab! 🚕"
        )
        
        messagebox.showinfo("Receipt", receipt_text)
        print(f"✅ Viewing receipt: {ride['id']}")
    
    def go_back(self):
        """Close my rides screen and return"""
        self.root.destroy()
        if self.parent_window and self.parent_window.winfo_exists():
            self.parent_window.deiconify()
            self.parent_window.lift()
            self.parent_window.focus_force()
        print("← Returned from My Rides")


# Helper function for detail popup
def info_row(parent, label, value, color="#333"):
    """Create an info row in detail view"""
    row = tk.Frame(parent, bg="white")
    row.pack(fill="x", pady=5)
    
    tk.Label(
        row, text=label,
        font=("Arial", 10), bg="white", fg="#999"
    ).pack(anchor="w")
    
    tk.Label(
        row, text=value,
        font=("Arial", 11, "bold"), bg="white", fg=color
    ).pack(anchor="w")


# Test the my rides screen independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    MyRidesScreen(root)
    root.mainloop()