# main.py - Main Application Entry Point

import tkinter as tk
from gui import QuickCabGUI
from database_manager import db

def main():
    """Start the QuickCab application"""
    if db.connect():
        db.disconnect()
    
    root = tk.Tk()
    app = QuickCabGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()