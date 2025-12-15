# test_database.py - Complete Database Testing Script

import sys
from database_manager import db
import config

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def test_database_connection():
    """Test 1: Database Connection"""
    print_header("TEST 1: Database Connection")
    
    print_info(f"Attempting to connect to: {config.DB_NAME}")
    print_info(f"Host: {config.DB_HOST}:{config.DB_PORT}")
    print_info(f"User: {config.DB_USER}")
    
    if db.connect():
        print_success("Database connected successfully!")
        
        # Get database info
        try:
            db.cursor.execute("SELECT DATABASE(), VERSION()")
            result = db.cursor.fetchone()
            print_info(f"Connected to database: {result['DATABASE()']}")
            print_info(f"MySQL/MariaDB version: {result['VERSION()']}")
        except Exception as e:
            print_error(f"Error getting database info: {e}")
        
        db.disconnect()
        return True
    else:
        print_error("Failed to connect to database!")
        print_info("Check the following:")
        print_info("  1. MySQL/MariaDB service is running")
        print_info("  2. DB_PASSWORD in config.py is correct")
        print_info("  3. Database 'quickcab_db' exists")
        print_info("  4. Run: mysql -u root -p < quickcab_schema.sql")
        return False

def test_tables_exist():
    """Test 2: Check if tables exist"""
    print_header("TEST 2: Database Tables")
    
    if not db.connect():
        print_error("Cannot connect to database")
        return False
    
    try:
        # List all tables
        db.cursor.execute("SHOW TABLES")
        tables = db.cursor.fetchall()
        
        expected_tables = [
            'users', 'wallet', 'wallet_transactions', 'rides', 
            'drivers', 'vouchers', 'user_vouchers', 'ride_vouchers',
            'notifications'
        ]
        
        found_tables = [list(table.values())[0] for table in tables]
        
        print_info(f"Found {len(found_tables)} tables:")
        for table in found_tables:
            print(f"  • {table}")
        
        # Check if all expected tables exist
        missing_tables = [t for t in expected_tables if t not in found_tables]
        
        if missing_tables:
            print_error(f"Missing tables: {', '.join(missing_tables)}")
            print_info("Run the SQL schema script to create missing tables")
            db.disconnect()
            return False
        else:
            print_success("All required tables exist!")
            db.disconnect()
            return True
            
    except Exception as e:
        print_error(f"Error checking tables: {e}")
        db.disconnect()
        return False

def test_sample_data():
    """Test 3: Check sample data"""
    print_header("TEST 3: Sample Data")
    
    if not db.connect():
        print_error("Cannot connect to database")
        return False
    
    try:
        # Check users
        db.cursor.execute("SELECT COUNT(*) as count FROM users")
        user_count = db.cursor.fetchone()['count']
        print_info(f"Users in database: {user_count}")
        
        if user_count == 0:
            print_error("No users found! Run the SQL schema to insert sample data")
            db.disconnect()
            return False
        
        # Check specific users
        db.cursor.execute("SELECT username, full_name, user_type FROM users")
        users = db.cursor.fetchall()
        
        print_success(f"Found {len(users)} users:")
        for user in users:
            print(f"  • {user['username']} ({user['full_name']}) - {user['user_type']}")
        
        # Check wallet
        db.cursor.execute("SELECT COUNT(*) as count FROM wallet")
        wallet_count = db.cursor.fetchone()['count']
        print_info(f"Wallets in database: {wallet_count}")
        
        # Check rides
        db.cursor.execute("SELECT COUNT(*) as count FROM rides")
        ride_count = db.cursor.fetchone()['count']
        print_info(f"Rides in database: {ride_count}")
        
        # Check vouchers
        db.cursor.execute("SELECT COUNT(*) as count FROM vouchers")
        voucher_count = db.cursor.fetchone()['count']
        print_info(f"Vouchers in database: {voucher_count}")
        
        db.disconnect()
        return True
        
    except Exception as e:
        print_error(f"Error checking sample data: {e}")
        db.disconnect()
        return False

def test_authentication():
    """Test 4: User Authentication"""
    print_header("TEST 4: User Authentication")
    
    if not db.connect():
        print_error("Cannot connect to database")
        return False
    
    try:
        # Test admin login
        print_info("Testing admin login (username: admin, password: admin123)")
        user = db.authenticate_user("admin", "admin123")
        
        if user:
            print_success(f"Authentication successful!")
            print_info(f"Logged in as: {user['full_name']}")
            print_info(f"User ID: {user['user_id']}")
            print_info(f"Email: {user['email']}")
            print_info(f"User Type: {user['user_type']}")
        else:
            print_error("Authentication failed!")
            print_info("Check if admin user exists in database")
            db.disconnect()
            return False
        
        # Test wrong password
        print_info("\nTesting wrong password...")
        wrong_user = db.authenticate_user("admin", "wrongpassword")
        
        if wrong_user:
            print_error("Security issue: Wrong password was accepted!")
            db.disconnect()
            return False
        else:
            print_success("Correctly rejected wrong password")
        
        db.disconnect()
        return True
        
    except Exception as e:
        print_error(f"Error testing authentication: {e}")
        db.disconnect()
        return False

def test_wallet_operations():
    """Test 5: Wallet Operations"""
    print_header("TEST 5: Wallet Operations")
    
    if not db.connect():
        print_error("Cannot connect to database")
        return False
    
    try:
        user_id = 2  # Test with user ID 2
        
        # Get initial balance
        initial_balance = db.get_wallet_balance(user_id)
        print_info(f"Initial wallet balance: ₱{initial_balance:.2f}")
        
        # Test adding funds
        print_info("Testing add ₱100 to wallet...")
        new_balance = db.add_wallet_funds(user_id, 100.00, "Test deposit")
        
        if new_balance:
            print_success(f"Funds added! New balance: ₱{new_balance:.2f}")
            
            # Verify balance increased
            if new_balance == initial_balance + 100:
                print_success("Balance calculation correct!")
            else:
                print_error("Balance calculation incorrect!")
        else:
            print_error("Failed to add funds")
            db.disconnect()
            return False
        
        # Test transaction history
        print_info("\nTesting transaction history...")
        transactions = db.get_transaction_history(user_id, 5)
        
        if transactions:
            print_success(f"Found {len(transactions)} transactions:")
            for trans in transactions[:3]:  # Show first 3
                print(f"  • {trans['transaction_type']}: ₱{trans['amount']} - {trans['description']}")
        else:
            print_error("No transactions found")
        
        db.disconnect()
        return True
        
    except Exception as e:
        print_error(f"Error testing wallet: {e}")
        db.disconnect()
        return False

def test_ride_operations():
    """Test 6: Ride Operations"""
    print_header("TEST 6: Ride Operations")
    
    if not db.connect():
        print_error("Cannot connect to database")
        return False
    
    try:
        user_id = 2
        
        # Get user rides
        print_info("Fetching user ride history...")
        rides = db.get_user_rides(user_id, 10)
        
        if rides:
            print_success(f"Found {len(rides)} rides:")
            for ride in rides[:3]:  # Show first 3
                print(f"  • {ride['ride_code']} - {ride['ride_type']} - ₱{ride['final_fare']} - {ride['ride_status']}")
        else:
            print_info("No rides found (this is OK for new users)")
        
        # Test creating a ride
        print_info("\nTesting ride creation...")
        ride_code = db.create_ride(
            passenger_id=user_id,
            ride_type='sedan',
            pickup_lat=7.0731,
            pickup_lon=125.6128,
            pickup_addr='Davao City Center',
            dest_lat=7.0833,
            dest_lon=125.6200,
            dest_addr='Matina, Davao City',
            distance_km=5.5,
            fare=120.00,
            payment_method='cash'
        )
        
        if ride_code:
            print_success(f"Ride created successfully! Ride code: {ride_code}")
        else:
            print_error("Failed to create ride")
        
        db.disconnect()
        return True
        
    except Exception as e:
        print_error(f"Error testing rides: {e}")
        db.disconnect()
        return False

def test_voucher_operations():
    """Test 7: Voucher Operations"""
    print_header("TEST 7: Voucher Operations")
    
    if not db.connect():
        print_error("Cannot connect to database")
        return False
    
    try:
        user_id = 2
        
        # Get user vouchers
        print_info("Fetching user vouchers...")
        vouchers = db.get_user_vouchers(user_id)
        
        if vouchers:
            print_success(f"Found {len(vouchers)} vouchers:")
            for voucher in vouchers:
                status_icon = "✅" if voucher['status'] == 'Active' else "❌"
                print(f"  {status_icon} {voucher['voucher_code']} - {voucher['description']} ({voucher['status']})")
        else:
            print_info("No vouchers found")
        
        db.disconnect()
        return True
        
    except Exception as e:
        print_error(f"Error testing vouchers: {e}")
        db.disconnect()
        return False

def test_all_imports():
    """Test 8: Python Module Imports"""
    print_header("TEST 8: Python Module Imports")
    
    modules_to_test = [
        ('config', 'Configuration'),
        ('database_manager', 'Database Manager'),
        ('functions', 'Functions'),
        ('gui', 'GUI'),
        ('map_system', 'Map System'),
        ('payment_system', 'Payment System'),
        ('wallet_screen', 'Wallet Screen'),
        ('my_rides_screen', 'My Rides Screen'),
        ('voucher_screen', 'Voucher Screen'),
    ]
    
    all_passed = True
    
    for module_name, display_name in modules_to_test:
        try:
            __import__(module_name)
            print_success(f"{display_name} imported successfully")
        except ImportError as e:
            print_error(f"{display_name} import failed: {e}")
            all_passed = False
        except Exception as e:
            print_error(f"{display_name} error: {e}")
            all_passed = False
    
    return all_passed

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("🚕" * 30)
    print("  QUICKCAB DATABASE TEST SUITE")
    print("🚕" * 30)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Database Tables", test_tables_exist),
        ("Sample Data", test_sample_data),
        ("User Authentication", test_authentication),
        ("Wallet Operations", test_wallet_operations),
        ("Ride Operations", test_ride_operations),
        ("Voucher Operations", test_voucher_operations),
        ("Python Imports", test_all_imports),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}\n")
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {test_name}")
    
    print("\n" + "=" * 60)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Database is working perfectly!")
        print("=" * 60)
        print("\n✅ You can now run: python main.py")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("=" * 60)
        
        # Provide helpful suggestions
        if not results[0][1]:  # Connection failed
            print("\n💡 NEXT STEPS:")
            print("1. Check if MySQL/MariaDB is running")
            print("2. Verify DB_PASSWORD in config.py")
            print("3. Make sure database exists: mysql -u root -p < quickcab_schema.sql")
        
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)