# main.py - Main Application Entry Point

import tkinter as tk
from gui import QuickCabGUI
from database_manager import db

def main():
    """Start the QuickCab application"""
    # Test database connection on startup
    print("=" * 50)
    print("🚕 QUICKCAB APPLICATION")
    print("=" * 50)
    print("\n🔌 Testing database connection...")
    
    if db.connect():
        print("✅ Database connection successful")
        db.disconnect()
    else:
        print("⚠️  Database connection failed - running in offline mode")
        print("Note: Some features may use sample data")
    
    print("\n🚀 Starting QuickCab GUI...")
    root = tk.Tk()
    app = QuickCabGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()