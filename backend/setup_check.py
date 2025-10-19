"""
Utility script to help with Mirai setup and testing.
Run this script to verify your environment and setup.
"""
import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.9+"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print("✓ Python version OK:", f"{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("✗ Python 3.9+ required. Current:", f"{version.major}.{version.minor}.{version.micro}")
        return False


def check_file_exists(filepath, name):
    """Check if a required file exists"""
    if Path(filepath).exists():
        print(f"✓ {name} found")
        return True
    else:
        print(f"✗ {name} not found at {filepath}")
        return False


def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("✗ .env file not found. Copy .env.example to .env and configure it.")
        return False
    
    required_vars = [
        "AWARIO_API_KEY",
        "FIREBASE_CREDENTIALS_PATH",
        "JWT_SECRET_KEY"
    ]
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    missing = []
    for var in required_vars:
        if f"{var}=your" in content or f"{var}=" not in content:
            missing.append(var)
    
    if missing:
        print(f"✗ .env file missing or incomplete: {', '.join(missing)}")
        return False
    
    print("✓ .env file configured")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import firebase_admin
        import sqlalchemy
        print("✓ Python dependencies installed")
        return True
    except ImportError as e:
        print(f"✗ Missing Python dependency: {e.name}")
        print("  Run: pip install -r requirements.txt")
        return False


def run_tests():
    """Run test suite"""
    print("\nRunning tests...")
    try:
        result = subprocess.run(
            ["pytest", "tests/", "-v", "--tb=short"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ All tests passed")
            return True
        else:
            print("✗ Some tests failed")
            print(result.stdout)
            return False
    except FileNotFoundError:
        print("✗ pytest not found. Run: pip install pytest")
        return False


def create_test_database():
    """Initialize test database"""
    print("\nInitializing database...")
    try:
        from app.database import init_db
        import asyncio
        
        asyncio.run(init_db())
        print("✓ Database initialized")
        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {str(e)}")
        return False


def main():
    """Main setup verification function"""
    print("=" * 60)
    print("Mirai Backend Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Firebase Credentials", lambda: check_file_exists("firebase-credentials.json", "Firebase credentials")),
        ("Dependencies", check_dependencies),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        results.append(check_func())
    
    # Optional checks
    print("\n" + "=" * 60)
    print("Optional Checks")
    print("=" * 60)
    
    # Database initialization
    if all(results):
        create_test_database()
    
    # Run tests
    if all(results):
        run_tests()
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if all(results):
        print("\n✓ Setup verification PASSED!")
        print("\nYou can now run the server:")
        print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("\n✗ Setup verification FAILED!")
        print("\nPlease fix the issues above and run this script again.")
        print("\nFor help, see:")
        print("  - README.md")
        print("  - QUICKSTART.md")
        sys.exit(1)


if __name__ == "__main__":
    # Change to backend directory if not already there
    if Path("app").exists() and Path("requirements.txt").exists():
        main()
    elif Path("backend").exists():
        os.chdir("backend")
        main()
    else:
        print("Error: Could not find backend directory.")
        print("Please run this script from the project root or backend directory.")
        sys.exit(1)
