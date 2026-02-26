import os
import sqlite3

# Find the database file
db_path = 'studyshare.db'
instance_db_path = os.path.join('instance', 'studyshare.db')

# Check if database exists in current directory
if os.path.exists(db_path):
    print(f"Found database at: {os.path.abspath(db_path)}")
    try:
        os.remove(db_path)
        print("✓ Database deleted successfully!")
    except Exception as e:
        print(f"Error deleting: {e}")

# Check if database exists in instance folder
elif os.path.exists(instance_db_path):
    print(f"Found database at: {os.path.abspath(instance_db_path)}")
    try:
        os.remove(instance_db_path)
        print("✓ Database deleted successfully!")
    except Exception as e:
        print(f"Error deleting: {e}")

else:
    print("Database file not found in standard locations.")
    print("Searching for any .db files...")
    
    # Search for any .db files
    found = False
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.db'):
                print(f"Found: {os.path.join(root, file)}")
                found = True
    
    if not found:
        print("No .db files found. The database will be created fresh when you run app.py")

print("\nYou can now run: python app.py")