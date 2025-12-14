# main.py - Main Application Entry Point

import tkinter as tk
from gui import QuickCabGUI

def main():
    """Start the QuickCab application"""
    root = tk.Tk()
    app = QuickCabGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()