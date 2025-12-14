import tkinter as tk
from tkinter import messagebox
import tkintermapview
from math import radians, sin, cos, sqrt, atan2
import requests
import threading


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
        
        # Draw rounded rectangle
        self.create_arc(0, 0, h, h, start=90, extent=180, fill=self.bg_color, outline="")
        self.create_arc(w-h, 0, w, h, start=270, extent=180, fill=self.bg_color, outline="")
        self.create_rectangle(r, 0, w-r, h, fill=self.bg_color, outline="")
        
        # Draw text
        self.create_text(w/2, h/2, text=self.text, fill=self.fg_color, font=("Arial", 11, "bold"))
    
    def on_click(self, event):
        if self.command:
            self.command()


class QuickCabMapSystem:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.davao_center = (7.0731, 125.6128)

        # State
        self.pickup_marker = None
        self.destination_marker = None
        self.pickup_coords = None
        self.destination_coords = None
        self.route_path = None
        self.current_mode = "pickup"
        self.distance = 0

        # Window
        self.root = tk.Toplevel(parent_window)
        self.root.title("🚕 QuickCab - Book Your Ride")

        window_width, window_height = 428, 926
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        parent_window.withdraw()

        self.setup_header()
        self.setup_location_display()
        self.setup_map()
        self.setup_bottom_controls()

        self.root.protocol("WM_DELETE_WINDOW", self.go_back)

        print("✅ QuickCab Map System Ready")

    # ---------------- UI ---------------- #

    def setup_header(self):
        frame = tk.Frame(self.root, bg="#1e40af", height=50)
        frame.pack(fill="x")
        frame.pack_propagate(False)

        # Rounded back button
        back_btn = RoundedButton(
            frame, text="← Back", command=self.go_back,
            bg_color="#1e40af", fg_color="white", bg="#1e40af", width=80
        )
        back_btn.place(x=10, y=10, width=80, height=30)

        tk.Label(
            frame, text="🚕 QuickCab - Book Your Ride",
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

        # Rounded Clear All button
        clear_btn = RoundedButton(
            container, text="Clear All", command=self.clear_all,
            bg_color="#ef4444", fg_color="white", bg="white", width=140
        )
        clear_btn.pack(side="left", padx=5)

        # Rounded Confirm Booking button
        confirm_btn = RoundedButton(
            container, text="Confirm Booking", command=self.confirm_booking,
            bg_color="#10b981", fg_color="white", bg="white", width=180
        )
        confirm_btn.pack(side="left", padx=5)

    # ---------------- LOGIC ---------------- #

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

        fare = 40 + (self.distance * 15)

        msg = (
            f"Pickup:\n{self.reverse_geocode(*self.pickup_coords)}\n\n"
            f"Destination:\n{self.reverse_geocode(*self.destination_coords)}\n\n"
            f"Distance: {self.distance:.2f} km\n"
            f"Fare: ₱{fare:.2f}\n\nConfirm booking?"
        )

        if messagebox.askyesno("Confirm Booking", msg):
            messagebox.showinfo("Booked", "Driver arriving in 5–10 minutes 🚕")

    def go_back(self):
        self.parent_window.deiconify()
        self.root.destroy()


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    QuickCabMapSystem(root)
    root.mainloop()