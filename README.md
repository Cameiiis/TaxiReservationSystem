QuickCab - Taxi Booking Application
A Python-based desktop application for booking taxi rides with an integrated map system, wallet management, and voucher system.
Features

User Authentication: Login and signup with password validation
Interactive Map: Select pickup and destination points on an OpenStreetMap interface
Ride Booking: Choose between Sedan and SUV vehicles with dynamic fare calculation
Wallet System: Add funds and manage your digital wallet
Voucher System: Apply discount codes and promotional vouchers
Ride History: View all past rides with detailed information
Payment Options: Cash, Visa, or Wallet payment methods

Requirements
Python 3.7+
tkinter
Pillow (PIL)
mysql-connector-python
tkintermapview
requests
Installation

Install required packages:

bashpip install pillow mysql-connector-python tkintermapview requests

Set up MySQL database:

Create a database named quickcab_db
Update database credentials in config.py if needed


Place all image assets in the Python Frames/ folder

Usage
Run the application:
bashpython main.py
Default Login:

Username: Admin
Password: Admin123@

Project Structure

main.py - Application entry point
gui.py - Main GUI window and page navigation
config.py - Configuration settings and constants
database_manager.py - Database operations
map_system.py - Interactive map interface
payment_system.py - Payment processing
wallet_screen.py - Wallet management
voucher_screen.py - Voucher management
my_rides_screen.py - Ride history
functions.py - Helper functions and business logic

Password Requirements

Minimum 8 characters
Must start with uppercase letter
Must contain at least one number
Must contain at least one special symbol (!@#$%^&*)

Features Overview
Map System

Click to set pickup location (green marker)
Click again to set destination (red marker)
View route and distance calculation
Apply vouchers and select payment method

Wallet

Add funds to your wallet
View transaction history
Use wallet for cashless payments

Vouchers

Browse available vouchers
Apply discount codes at checkout
View expiry dates and terms
