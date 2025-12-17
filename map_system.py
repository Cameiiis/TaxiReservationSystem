import tkinter as tk
from tkinter import messagebox
import tkintermapview
from math import radians, sin, cos, sqrt, atan2
import requests
import threading
from PIL import Image, ImageTk
import os


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color, fg_color, **kwargs):
        super().__init__(parent, height=50, highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.text = text
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Configure>", self.draw_button)
        
    def draw_button(self, event=None):
        self.delete("all")
        w = self.winfo_width()
        h = self.winfo_height()
        r = h // 2
        
        self.create_arc(0, 0, h, h, start=90, extent=180, fill=self.bg_color, outline="")
        self.create_arc(w-h, 0, w, h, start=270, extent=180, fill=self.bg_color, outline="")
        self.create_rectangle(r, 0, w-r, h, fill=self.bg_color, outline="")
        
        self.create_text(w/2, h/2, text=self.text, fill=self.fg_color, font=("Arial", 11, "bold"))
    
    def on_click(self, event):
        if self.command:
            self.command()


class RideSelectionPopup:
    def __init__(self, parent, distance, pickup_coords, destination_coords, on_book):
        self.parent = parent
        self.distance = distance
        self.pickup_coords = pickup_coords
        self.destination_coords = destination_coords
        self.on_book = on_book
        self.selected_ride = None
        self.is_closing = False
        
        self.pickup_address = "Loading..."
        self.destination_address = "Loading..."
        
        self.window_width = 428
        self.window_height = 926
        
        self.load_images()
        
        self.popup = tk.Label(parent, bg="white", borderwidth=0, highlightthickness=0)
        
        self.popup.bind("<Button-1>", lambda e: "break")
        
        if self.popup_frame_img:
            self.popup.config(image=self.popup_frame_img)
        
        self.popup.place(x=0, y=self.window_height, width=self.window_width, height=self.popup_height)
        
        self.setup_popup()
        
        popup_y = self.window_height - self.popup_height
        self.popup.place(x=0, y=popup_y, width=self.window_width, height=self.popup_height)
        
        self.fetch_addresses_async()
    
    def load_images(self):
        self.sedan_icon = None
        self.suv_icon = None
        self.book_btn_img = None
        self.available_rides_img = None
        self.popup_frame_img = None
        self.popup_height = 500
        
        frames_folder = "Python Frames"
        
        try:
            popup_frame_path = os.path.join(frames_folder, "pop up.png")
            if os.path.exists(popup_frame_path):
                img = Image.open(popup_frame_path)
                original_width, original_height = img.size
                
                new_width = self.window_width
                new_height = int((original_height / original_width) * new_width)
                
                max_height = int(self.window_height * 0.4)
                if new_height > max_height:
                    new_height = max_height
                    new_width = int((original_width / original_height) * new_height)
                
                img = img.resize((new_width, new_height), Image.Resampling.BILINEAR)
                self.popup_frame_img = ImageTk.PhotoImage(img)
                self.popup_height = new_height
            
            sedan_path = os.path.join(frames_folder, "sedan.png")
            if os.path.exists(sedan_path):
                img = Image.open(sedan_path)
                img = img.resize((385, 85), Image.Resampling.BILINEAR)
                self.sedan_icon = ImageTk.PhotoImage(img)
            
            suv_path = os.path.join(frames_folder, "suv.png")
            if os.path.exists(suv_path):
                img = Image.open(suv_path)
                img = img.resize((385, 85), Image.Resampling.BILINEAR)
                self.suv_icon = ImageTk.PhotoImage(img)
            
            book_btn_path = os.path.join(frames_folder, "book ride button.png")
            if os.path.exists(book_btn_path):
                img = Image.open(book_btn_path)
                img = img.resize((400, 85), Image.Resampling.BILINEAR)
                self.book_btn_img = ImageTk.PhotoImage(img)
            
            available_rides_path = os.path.join(frames_folder, "available rides.png")
            if os.path.exists(available_rides_path):
                img = Image.open(available_rides_path)
                img = img.resize((250, 50), Image.Resampling.BILINEAR)
                self.available_rides_img = ImageTk.PhotoImage(img)
                
        except Exception as e:
            pass
    
    def fetch_addresses_async(self):
        def task():
            try:
                pickup = self.reverse_geocode(*self.pickup_coords)
                destination = self.reverse_geocode(*self.destination_coords)
                
                self.popup.after(0, lambda: self.update_addresses(pickup, destination))
            except Exception as e:
                self.popup.after(0, lambda: self.update_addresses(
                    f"{self.pickup_coords[0]:.5f}, {self.pickup_coords[1]:.5f}",
                    f"{self.destination_coords[0]:.5f}, {self.destination_coords[1]:.5f}"
                ))
        
        threading.Thread(target=task, daemon=True).start()
    
    def update_addresses(self, pickup, destination):
        self.pickup_address = pickup
        self.destination_address = destination
    
    def reverse_geocode(self, lat, lon):
        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                "lat": lat,
                "lon": lon,
                "format": "json",
                "zoom": 18,
                "addressdetails": 1
            }
            headers = {"User-Agent": "QuickCab/1.0"}
            r = requests.get(url, params=params, headers=headers, timeout=5)
            addr = r.json().get("address", {})

            road = addr.get("road") or addr.get("residential")
            barangay = addr.get("suburb") or addr.get("neighbourhood")
            city = addr.get("city") or "Davao City"

            return ", ".join(filter(None, [road, barangay, city]))

        except:
            return f"{lat:.5f}, {lon:.5f}"
    
    def setup_popup(self):
        available_y = self.popup_height * 0.07
        sedan_y = self.popup_height * 0.28
        suv_y = self.popup_height * 0.56
        book_y = self.popup_height * 0.83
        
        if self.available_rides_img:
            header_btn = tk.Label(self.popup, image=self.available_rides_img, borderwidth=0, bg="white")
            header_btn.image = self.available_rides_img
            header_btn.place(x=214, y=available_y, anchor="center")
        else:
            header_label = tk.Label(
                self.popup, text="Available Rides", 
                font=("Arial", 16, "bold"), bg="white", fg="#1e40af"
            )
            header_label.place(x=214, y=available_y, anchor="center")
        
        if self.sedan_icon:
            self.sedan_btn = tk.Button(
                self.popup, image=self.sedan_icon, border=0, relief="flat",
                cursor="hand2", command=lambda: self.select_ride_type("Sedan"),
                borderwidth=0, highlightthickness=0, bg="white", activebackground="white"
            )
            self.sedan_btn.image = self.sedan_icon
            self.sedan_btn.place(x=214, y=sedan_y, anchor="center")
        
        if self.suv_icon:
            self.suv_btn = tk.Button(
                self.popup, image=self.suv_icon, border=0, relief="flat",
                cursor="hand2", command=lambda: self.select_ride_type("SUV"),
                borderwidth=0, highlightthickness=0, bg="white", activebackground="white"
            )
            self.suv_btn.image = self.suv_icon
            self.suv_btn.place(x=214, y=suv_y, anchor="center")
        
        if self.book_btn_img:
            self.book_button = tk.Button(
                self.popup, image=self.book_btn_img, border=0, relief="flat",
                cursor="hand2", command=self.book_ride,
                borderwidth=0, highlightthickness=0, bg="white", activebackground="white"
            )
            self.book_button.image = self.book_btn_img
            self.book_button.place(x=214, y=book_y, anchor="center")
    
    def select_ride_type(self, ride_type):
        self.selected_ride = ride_type
        fare = self.calculate_fare(ride_type.lower())
    
    def calculate_fare(self, ride_type):
        base_fare = 40 if ride_type == "sedan" else 60
        return base_fare + (self.distance * 15)
    
    def book_ride(self):
        if not self.selected_ride:
            messagebox.showwarning("No Selection", "Please select a ride type (Sedan or SUV)")
            return
        
        fare = self.calculate_fare(self.selected_ride.lower())
        
        self.close()
        
        if self.on_book:
            self.on_book(self.selected_ride, fare, self.pickup_address, self.destination_address)
    
    def close(self):
        if self.is_closing:
            return
        self.is_closing = True
        self.popup.destroy()


class QuickCabMapSystem:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.davao_center = (7.0731, 125.6128)

        self.pickup_marker = None
        self.destination_marker = None
        self.pickup_coords = None
        self.destination_coords = None
        self.route_path = None
        self.current_mode = "pickup"
        self.distance = 0
        self.active_popup = None

        self.root = tk.Toplevel(parent_window)
        self.root.title("QuickCab")

        window_width, window_height = 428, 926
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)

        parent_window.withdraw()

        self.setup_header()
        self.setup_location_display()
        self.setup_map()
        self.setup_bottom_controls()

        self.root.protocol("WM_DELETE_WINDOW", self.go_back)

    def setup_header(self):
        frame = tk.Frame(self.root, bg="#1e40af", height=50)
        frame.pack(fill="x")
        frame.pack_propagate(False)

        back_btn = RoundedButton(
            frame, text="← Back", command=self.go_back,
            bg_color="#1e40af", fg_color="white", bg="#1e40af", width=80
        )
        back_btn.place(x=10, y=10, width=80, height=30)

        tk.Label(
            frame, text="QuickCab",
            bg="#1e40af", fg="white",
            font=("Arial", 13, "bold")
        ).pack(pady=12)

    def setup_location_display(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill="x")

        tk.Label(
            frame, text="Where do you want to go?",
            bg="white", font=("Arial", 13, "bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        self.pickup_label = self.create_location_box(frame, "●", "#3b82f6", "Current Location")
        self.destination_label = self.create_location_box(frame, "●", "#111111", "Enter Destination")

    def create_location_box(self, parent, icon, color, text):
        box = tk.Frame(parent, bg="#f5f5f5", highlightbackground="#ddd", highlightthickness=1)
        box.pack(fill="x", padx=15, pady=6)

        inner = tk.Frame(box, bg="#f5f5f5")
        inner.pack(fill="x", padx=12, pady=12)

        tk.Label(inner, text=icon, fg=color, bg="#f5f5f5", font=("Arial", 14)).pack(side="left", padx=(0, 8))

        label = tk.Label(inner, text=text, bg="#f5f5f5", fg="#666", font=("Arial", 12), anchor="w")
        label.pack(side="left", fill="x", expand=True)

        return label

    def setup_map(self):
        self.map_widget = tkintermapview.TkinterMapView(self.root, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)

        self.map_widget.set_position(*self.davao_center)
        self.map_widget.set_zoom(13)
        self.map_widget.add_left_click_map_command(self.map_click)

    def setup_bottom_controls(self):
        frame = tk.Frame(self.root, bg="white", height=80)
        frame.pack(fill="x", side="bottom")
        frame.pack_propagate(False)

        container = tk.Frame(frame, bg="white")
        container.pack(expand=True)

        frames_folder = "Python Frames"
        clear_btn_img = None
        confirm_btn_img = None
        
        try:
            clear_btn_width = 175
            clear_btn_height = 50
            clear_path = os.path.join(frames_folder, "clear all button.png")
            if os.path.exists(clear_path):
                img = Image.open(clear_path)
                img = img.resize((clear_btn_width, clear_btn_height), Image.Resampling.BILINEAR)
                clear_btn_img = ImageTk.PhotoImage(img)
            
            confirm_btn_width = 200
            confirm_btn_height = 50
            confirm_path = os.path.join(frames_folder, "confirm booking button.png")
            if os.path.exists(confirm_path):
                img = Image.open(confirm_path)
                img = img.resize((confirm_btn_width, confirm_btn_height), Image.Resampling.BILINEAR)
                confirm_btn_img = ImageTk.PhotoImage(img)
        except Exception as e:
            pass
        
        if clear_btn_img:
            self.clear_button = tk.Button(
                container, image=clear_btn_img, border=0, relief="flat",
                cursor="hand2", command=self.clear_all,
                borderwidth=0, highlightthickness=0, bg="white", activebackground="white"
            )
            self.clear_button.image = clear_btn_img
            self.clear_button.pack(side="left", padx=5)
        else:
            clear_btn = RoundedButton(
                container, text="Clear All", command=self.clear_all,
                bg_color="#ef4444", fg_color="white", bg="white", width=140
            )
            clear_btn.pack(side="left", padx=5)

        if confirm_btn_img:
            self.confirm_button = tk.Button(
                container, image=confirm_btn_img, border=0, relief="flat",
                cursor="hand2", command=self.confirm_booking,
                borderwidth=0, highlightthickness=0, bg="white", activebackground="white"
            )
            self.confirm_button.image = confirm_btn_img
            self.confirm_button.pack(side="left", padx=5)
        else:
            confirm_btn = RoundedButton(
                container, text="Confirm Booking", command=self.confirm_booking,
                bg_color="#10b981", fg_color="white", bg="white", width=180
            )
            confirm_btn.pack(side="left", padx=5)

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        a = sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2
        return R * 2 * atan2(sqrt(a), sqrt(1-a))

    def reverse_geocode(self, lat, lon):
        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                "lat": lat,
                "lon": lon,
                "format": "json",
                "zoom": 18,
                "addressdetails": 1
            }
            headers = {"User-Agent": "QuickCab/1.0"}
            r = requests.get(url, params=params, headers=headers, timeout=5)
            addr = r.json().get("address", {})

            road = addr.get("road") or addr.get("residential")
            barangay = addr.get("suburb") or addr.get("neighbourhood")
            city = addr.get("city") or "Davao City"

            return ", ".join(filter(None, [road, barangay, city]))

        except:
            return f"{lat:.5f}, {lon:.5f}"

    def update_label_async(self, label, lat, lon):
        def task():
            address = self.reverse_geocode(lat, lon)
            label.after(0, lambda: label.config(text=address, fg="#111"))
        threading.Thread(target=task, daemon=True).start()

    def update_location_displays(self):
        if self.pickup_coords:
            self.update_label_async(self.pickup_label, *self.pickup_coords)
        else:
            self.pickup_label.config(text="Current Location", fg="#666")

        if self.destination_coords:
            self.update_label_async(self.destination_label, *self.destination_coords)
        else:
            self.destination_label.config(text="Enter Destination", fg="#666")

    def map_click(self, coords):
        if self.active_popup and not self.active_popup.is_closing:
            self.active_popup.close()
            self.active_popup = None
            return
        
        if self.current_mode == "pickup":
            if self.pickup_marker:
                self.pickup_marker.delete()

            self.pickup_marker = self.map_widget.set_marker(
                coords[0], coords[1], text="Pickup",
                marker_color_circle="green", marker_color_outside="darkgreen"
            )
            self.pickup_coords = coords
            self.current_mode = "destination"

        else:
            if self.destination_marker:
                self.destination_marker.delete()

            self.destination_marker = self.map_widget.set_marker(
                coords[0], coords[1], text="Destination",
                marker_color_circle="red", marker_color_outside="darkred"
            )
            self.destination_coords = coords

            if self.route_path:
                self.map_widget.delete(self.route_path)

            self.route_path = self.map_widget.set_path(
                [self.pickup_coords, self.destination_coords],
                color="#3b82f6", width=4
            )

            self.distance = self.calculate_distance(*self.pickup_coords, *self.destination_coords)

        self.update_location_displays()

    def clear_all(self):
        for obj in [self.pickup_marker, self.destination_marker, self.route_path]:
            if obj:
                obj.delete()

        self.pickup_marker = self.destination_marker = self.route_path = None
        self.pickup_coords = self.destination_coords = None
        self.current_mode = "pickup"
        self.update_location_displays()

    def confirm_booking(self):
        if not self.pickup_coords or not self.destination_coords:
            messagebox.showwarning("Incomplete", "Select pickup and destination")
            return

        self.active_popup = RideSelectionPopup(
            self.root, 
            self.distance,
            self.pickup_coords,
            self.destination_coords,
            self.on_booking_confirmed
        )

    def on_booking_confirmed(self, ride_type, fare, pickup_address, destination_address):
        try:
            from payment_system import PaymentMethodScreen
            
            PaymentMethodScreen(
                self.root,
                ride_type=ride_type,
                fare=fare,
                pickup_address=pickup_address,
                destination_address=destination_address,
                distance=self.distance
            )
            
        except ImportError as e:
            messagebox.showerror(
                "Payment Error",
                f"Could not import payment_system.py!\n\nMake sure payment_system.py is in the same folder.\n\nError: {e}"
            )
        except Exception as e:
            messagebox.showerror("Payment Error", f"Could not open payment screen!\n\nError: {e}")

    def go_back(self):
        self.parent_window.deiconify()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    QuickCabMapSystem(root)
    root.mainloop()