import os
import shutil

# List all possible database locations
possible_paths = [
    'studyshare.db',
    'instance/studyshare.db',
    '../studyshare.db',
    '../../studyshare.db',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'studyshare.db'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'studyshare.db'),
]

print("Searching for database files...\n")

found = False
for path in possible_paths:
    abs_path = os.path.abspath(path)
    if os.path.exists(path):
        print(f"✓ Found: {abs_path}")
        try:
            os.remove(path)
            print(f"✓ Deleted successfully!\n")
            found = True
        except Exception as e:
            print(f"✗ Error deleting: {e}\n")
    else:
        print(f"✗ Not found: {abs_path}")

# Also search entire project directory
print("\n" + "="*50)
print("Searching entire project for .db files...")
print("="*50 + "\n")

project_dir = os.path.dirname(os.path.abspath(__file__))
for root, dirs, files in os.walk(project_dir):
    # Skip Python virtual environment folders
    if 'venv' in root or 'env' in root or '__pycache__' in root or 'site-packages' in root:
        continue
    
    for file in files:
        if file.endswith('.db'):
            full_path = os.path.join(root, file)
            print(f"✓ Found database: {full_path}")
            try:
                os.remove(full_path)
                print(f"✓ Deleted: {full_path}\n")
                found = True
            except Exception as e:
                print(f"✗ Could not delete: {e}\n")

if not found:
    print("\nNo database files found. The new database will be created when you run app.py")
else:
    print("\n✓ All database files deleted!")
    
print("\nYou can now run: python app.py")