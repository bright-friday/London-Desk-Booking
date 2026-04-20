import subprocess
import sys

def run_all_tests():
    """Run all test suites"""
    test_files = [
        "tests/e2e_booking_creation.py",
        "tests/e2e_cancellation_checkin.py",
        "tests/e2e_reporting_analytics.py"
    ]
    
    all_passed = True
    
    for test_file in test_files:
        print(f"\n{'='*60}")
        print(f"Running {test_file}")
        print('='*60)
        
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v"],
            cwd="."
        )
        
        if result.returncode != 0:
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 
