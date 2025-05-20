import os
import sys
import subprocess

def check_python_version():
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required")
        sys.exit(1)

def create_directories():
    os.makedirs("output", exist_ok=True)

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        print("Failed to install requirements")
        sys.exit(1)

def main():
    print("Setting up 591 Rental Housing Project...")
    
    print("Checking Python version...")
    check_python_version()
    
    print("Creating necessary directories...")
    create_directories()
    
    print("Installing requirements...")
    install_requirements()
    
    print("Setup completed successfully!")

if __name__ == "__main__":
    main() 