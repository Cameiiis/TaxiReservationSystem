# database_manager.py - Database Management Class

import mysql.connector
from mysql.connector import Error
import hashlib
from datetime import datetime
import config

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=config.DB_HOST,
                database=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                port=config.DB_PORT
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                return True
                
        except Error as e:
            print(f"❌ Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # ==================== USER MANAGEMENT ====================
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        try:
            hashed_password = self._hash_password(password)
            
            query = """
                SELECT user_id, username, full_name, email, user_type, account_status
                FROM users 
                WHERE username = %s AND password_hash = %s AND account_status = 'active'
            """
            
            self.cursor.execute(query, (username, hashed_password))
            user = self.cursor.fetchone()
            
            if user:
                # Update last login
                update_query = "UPDATE users SET last_login = NOW() WHERE user_id = %s"
                self.cursor.execute(update_query, (user['user_id'],))
                self.connection.commit()
                
                return user
            
            return None
            
        except Error as e:
            print(f"❌ Authentication error: {e}")
            return None
    
    def create_user(self, full_name, email, password, username=None, user_type='passenger'):
        """Create new user account"""
        try:
            # Generate username from email if not provided
            if not username:
                username = email.split('@')[0]
            
            hashed_password = self._hash_password(password)
            
            query = """
                INSERT INTO users (username, email, password_hash, full_name, user_type)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            self.cursor.execute(query, (username, email, hashed_password, full_name, user_type))
            self.connection.commit()
            
            return True
            
        except Error as e:
            print(f"❌ User creation error: {e}")
            return False
    
    def get_user_info(self, user_id):
        """Get user information"""
        try:
            query = """
                SELECT user_id, username, full_name, email, phone_number, 
                       user_type, date_registered, last_login
                FROM users 
                WHERE user_id = %s AND account_status = 'active'
            """
            
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()
            
        except Error as e:
            print(f"❌ Error fetching user info: {e}")
            return None
    
    # ==================== WALLET MANAGEMENT ====================
    
    def get_wallet_balance(self, user_id):
        """Get user's wallet balance"""
        try:
            query = "SELECT balance FROM wallet WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            
            return result['balance'] if result else 0.00
            
        except Error as e:
            print(f"❌ Error fetching wallet balance: {e}")
            return 0.00
    
    def add_wallet_funds(self, user_id, amount, description="Wallet top-up"):
        """Add funds to user's wallet"""
        try:
            # Get current balance and wallet_id
            query = "SELECT wallet_id, balance FROM wallet WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            wallet = self.cursor.fetchone()
            
            if not wallet:
                return None
            
            wallet_id = wallet['wallet_id']
            old_balance = float(wallet['balance'])  # Convert Decimal to float
            new_balance = old_balance + float(amount)
            
            # Update wallet balance
            update_query = "UPDATE wallet SET balance = %s WHERE wallet_id = %s"
            self.cursor.execute(update_query, (new_balance, wallet_id))
            
            # Record transaction
            trans_query = """
                INSERT INTO wallet_transactions 
                (wallet_id, user_id, transaction_type, amount, balance_before, balance_after, description)
                VALUES (%s, %s, 'deposit', %s, %s, %s, %s)
            """
            self.cursor.execute(trans_query, (wallet_id, user_id, amount, old_balance, new_balance, description))
            
            self.connection.commit()
            return new_balance
            
        except Error as e:
            print(f"❌ Error adding wallet funds: {e}")
            self.connection.rollback()
            return None
    
    def deduct_wallet_funds(self, user_id, amount, description="Payment"):
        """Deduct funds from user's wallet"""
        try:
            # Get current balance and wallet_id
            query = "SELECT wallet_id, balance FROM wallet WHERE user_id = %s"
            self.cursor.execute(query, (user_id,))
            wallet = self.cursor.fetchone()
            
            if not wallet:
                return None
            
            wallet_id = wallet['wallet_id']
            old_balance = float(wallet['balance'])  # Convert Decimal to float
            
            # Check sufficient balance
            if old_balance < float(amount):
                print("❌ Insufficient wallet balance")
                return None
            
            new_balance = old_balance - float(amount)
            
            # Update wallet balance
            update_query = "UPDATE wallet SET balance = %s WHERE wallet_id = %s"
            self.cursor.execute(update_query, (new_balance, wallet_id))
            
            # Record transaction
            trans_query = """
                INSERT INTO wallet_transactions 
                (wallet_id, user_id, transaction_type, amount, balance_before, balance_after, description)
                VALUES (%s, %s, 'withdrawal', %s, %s, %s, %s)
            """
            self.cursor.execute(trans_query, (wallet_id, user_id, amount, old_balance, new_balance, description))
            
            self.connection.commit()
            return new_balance
            
        except Error as e:
            print(f"❌ Error deducting wallet funds: {e}")
            self.connection.rollback()
            return None
    
    def get_transaction_history(self, user_id, limit=10):
        """Get user's transaction history"""
        try:
            query = """
                SELECT transaction_type, amount, balance_after, description,
                       DATE_FORMAT(transaction_date, '%%d %%b %%I:%%i %%p') as date_display
                FROM wallet_transactions
                WHERE user_id = %s
                ORDER BY transaction_date DESC
                LIMIT %s
            """
            
            self.cursor.execute(query, (user_id, limit))
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"❌ Error fetching transaction history: {e}")
            return []
    
    # ==================== RIDE MANAGEMENT ====================
    
    def create_ride(self, passenger_id, ride_type, pickup_lat, pickup_lon, pickup_addr,
                   dest_lat, dest_lon, dest_addr, distance_km, fare, payment_method):
        """Create a new ride booking"""
        try:
            # Generate unique ride code
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            ride_code = f"QC-{timestamp[-6:]}"
            
            # Calculate fare breakdown
            base_fare = 40 if ride_type == 'sedan' else 60
            distance_fare = fare - base_fare
            
            query = """
                INSERT INTO rides 
                (ride_code, passenger_id, ride_type, pickup_latitude, pickup_longitude, 
                 pickup_address, destination_latitude, destination_longitude, destination_address,
                 distance_km, base_fare, distance_fare, final_fare, payment_method, ride_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending')
            """
            
            self.cursor.execute(query, (ride_code, passenger_id, ride_type, pickup_lat, pickup_lon,
                                       pickup_addr, dest_lat, dest_lon, dest_addr, distance_km,
                                       base_fare, distance_fare, fare, payment_method))
            
            self.connection.commit()
            return ride_code
            
        except Error as e:
            print(f"❌ Error creating ride: {e}")
            self.connection.rollback()
            return None
    
    def get_user_rides(self, user_id, limit=20):
        """Get user's ride history"""
        try:
            query = """
                SELECT ride_id, ride_code, ride_type, pickup_address, destination_address,
                       distance_km, final_fare, ride_status, payment_method,
                       DATE_FORMAT(booking_time, '%%m/%%d/%%Y') as date,
                       DATE_FORMAT(booking_time, '%%h:%%i %%p') as time
                FROM rides
                WHERE passenger_id = %s
                ORDER BY booking_time DESC
                LIMIT %s
            """
            
            self.cursor.execute(query, (user_id, limit))
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"❌ Error fetching rides: {e}")
            return []
    
    def update_ride_status(self, ride_id, new_status):
        """Update ride status"""
        try:
            query = "UPDATE rides SET ride_status = %s WHERE ride_id = %s"
            self.cursor.execute(query, (new_status, ride_id))
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"❌ Error updating ride status: {e}")
            return False
    
    def complete_ride(self, ride_id, rating=None, review=None):
        """Complete a ride and process payment"""
        try:
            # Get ride details
            query = "SELECT passenger_id, final_fare, payment_method FROM rides WHERE ride_id = %s"
            self.cursor.execute(query, (ride_id,))
            ride = self.cursor.fetchone()
            
            if not ride:
                return False
            
            # If payment method is wallet, deduct funds
            if ride['payment_method'] == 'wallet':
                result = self.deduct_wallet_funds(
                    ride['passenger_id'], 
                    ride['final_fare'],
                    f"Payment for ride #{ride_id}"
                )
                if not result:
                    return False
            
            # Update ride status
            update_query = """
                UPDATE rides 
                SET ride_status = 'completed', end_time = NOW(), rating = %s, review_comment = %s
                WHERE ride_id = %s
            """
            self.cursor.execute(update_query, (rating, review, ride_id))
            self.connection.commit()
            
            return True
            
        except Error as e:
            print(f"❌ Error completing ride: {e}")
            self.connection.rollback()
            return False
    
    # ==================== VOUCHER MANAGEMENT ====================
    
    def get_user_vouchers(self, user_id):
        """Get user's available vouchers"""
        try:
            query = """
                SELECT v.voucher_id, v.voucher_code, v.voucher_type, v.discount_value,
                       v.min_fare, v.description, v.voucher_status,
                       DATE_FORMAT(v.expiry_date, '%%d/%%m/%%Y') as expiry,
                       CASE 
                           WHEN v.expiry_date < CURDATE() THEN 'Expired'
                           WHEN uv.times_used >= v.usage_limit THEN 'Used'
                           ELSE 'Active'
                       END as status
                FROM vouchers v
                JOIN user_vouchers uv ON v.voucher_id = uv.voucher_id
                WHERE uv.user_id = %s
                ORDER BY v.expiry_date DESC
            """
            
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"❌ Error fetching vouchers: {e}")
            return []
    
    def validate_voucher(self, voucher_code, user_id, fare_amount):
        """Validate if voucher can be used"""
        try:
            query = """
                SELECT v.voucher_id, v.voucher_type, v.discount_value, v.min_fare, 
                       v.max_discount, v.usage_limit, uv.times_used
                FROM vouchers v
                JOIN user_vouchers uv ON v.voucher_id = uv.voucher_id
                WHERE v.voucher_code = %s 
                  AND uv.user_id = %s
                  AND v.voucher_status = 'active'
                  AND v.expiry_date >= CURDATE()
            """
            
            self.cursor.execute(query, (voucher_code, user_id))
            voucher = self.cursor.fetchone()
            
            if not voucher:
                return None, "Invalid or expired voucher"
            
            # Check usage limit
            if voucher['times_used'] >= voucher['usage_limit']:
                return None, "Voucher usage limit reached"
            
            # Check minimum fare
            if fare_amount < voucher['min_fare']:
                return None, f"Minimum fare of ₱{voucher['min_fare']} required"
            
            # Calculate discount
            if voucher['voucher_type'] == 'percentage':
                discount = fare_amount * (voucher['discount_value'] / 100)
                if voucher['max_discount'] and discount > voucher['max_discount']:
                    discount = voucher['max_discount']
            else:
                discount = voucher['discount_value']
            
            return discount, None
            
        except Error as e:
            print(f"❌ Error validating voucher: {e}")
            return None, "Error validating voucher"
    
    def use_voucher(self, voucher_code, user_id, ride_id, discount_applied):
        """Mark voucher as used for a ride"""
        try:
            # Get voucher ID
            query = "SELECT voucher_id FROM vouchers WHERE voucher_code = %s"
            self.cursor.execute(query, (voucher_code,))
            result = self.cursor.fetchone()
            
            if not result:
                return False
            
            voucher_id = result['voucher_id']
            
            # Update usage count
            update_query = """
                UPDATE user_vouchers 
                SET times_used = times_used + 1, last_used = NOW()
                WHERE user_id = %s AND voucher_id = %s
            """
            self.cursor.execute(update_query, (user_id, voucher_id))
            
            # Record voucher usage for ride
            insert_query = """
                INSERT INTO ride_vouchers (ride_id, voucher_id, discount_applied)
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(insert_query, (ride_id, voucher_id, discount_applied))
            
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"❌ Error using voucher: {e}")
            self.connection.rollback()
            return False
    
    def assign_voucher_to_user(self, user_id, voucher_code):
        """Assign a voucher to a user"""
        try:
            # Get voucher ID
            query = "SELECT voucher_id FROM vouchers WHERE voucher_code = %s"
            self.cursor.execute(query, (voucher_code,))
            result = self.cursor.fetchone()
            
            if not result:
                return False
            
            voucher_id = result['voucher_id']
            
            # Assign to user
            insert_query = """
                INSERT INTO user_vouchers (user_id, voucher_id, times_used)
                VALUES (%s, %s, 0)
                ON DUPLICATE KEY UPDATE date_claimed = NOW()
            """
            self.cursor.execute(insert_query, (user_id, voucher_id))
            self.connection.commit()
            
            return True
            
        except Error as e:
            print(f"❌ Error assigning voucher: {e}")
            return False
    
    # ==================== DRIVER MANAGEMENT ====================
    
    def get_available_drivers(self, ride_type):
        """Get available drivers for ride type"""
        try:
            query = """
                SELECT d.driver_id, u.full_name, d.vehicle_plate, d.vehicle_model,
                       d.rating, d.driver_status
                FROM drivers d
                JOIN users u ON d.user_id = u.user_id
                WHERE d.driver_status = 'available' 
                  AND d.vehicle_type = %s
                  AND d.verification_status = 'verified'
                ORDER BY d.rating DESC
                LIMIT 5
            """
            
            self.cursor.execute(query, (ride_type,))
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"❌ Error fetching drivers: {e}")
            return []
    
    # ==================== NOTIFICATIONS ====================
    
    def create_notification(self, user_id, notification_type, title, message):
        """Create a notification for user"""
        try:
            query = """
                INSERT INTO notifications (user_id, notification_type, title, message)
                VALUES (%s, %s, %s, %s)
            """
            
            self.cursor.execute(query, (user_id, notification_type, title, message))
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"❌ Error creating notification: {e}")
            return False
    
    def get_user_notifications(self, user_id, limit=10):
        """Get user's notifications"""
        try:
            query = """
                SELECT notification_id, notification_type, title, message, is_read,
                       DATE_FORMAT(created_at, '%%d %%b %%I:%%i %%p') as date_display
                FROM notifications
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """
            
            self.cursor.execute(query, (user_id, limit))
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"❌ Error fetching notifications: {e}")
            return []
    
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        try:
            query = "UPDATE notifications SET is_read = TRUE WHERE notification_id = %s"
            self.cursor.execute(query, (notification_id,))
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"❌ Error marking notification as read: {e}")
            return False


# ⚠️ CRITICAL: This line creates the global instance
# DO NOT DELETE THIS LINE!
db = DatabaseManager()