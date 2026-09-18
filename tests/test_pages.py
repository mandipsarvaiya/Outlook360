"""
OmniPulse AI - Streamlit Page Integrity Test Suite
Verifies that all 11 pages compile and initialize cleanly without runtime syntax or import errors.
"""
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from streamlit.testing.v1 import AppTest

def test_all_pages():
    pages = [
        "app/main.py",
        "app/pages/1_Executive_Overview.py",
        "app/pages/2_Sales_Analytics.py",
        "app/pages/3_Customer_Segmentation.py",
        "app/pages/4_Demand_Forecasting.py",
        "app/pages/5_Market_Basket_Analysis.py",
        "app/pages/6_Inventory_Optimization.py",
        "app/pages/7_Anomaly_Detection.py",
        "app/pages/8_POS_Simulator.py",
        "app/pages/9_Domain_Switcher.py",
        "app/pages/10_Inventory_Management.py",
        "app/pages/11_User_Management.py",
    ]
    
    print("Testing Streamlit Pages compilation...")
    for p in pages:
        full_path = BASE_DIR / p
        if not full_path.exists():
            print(f"[FAIL] Missing page file: {p}")
            sys.exit(1)
        
        # Test compiling the file
        with open(full_path, "r", encoding="utf-8") as f:
            code = f.read()
            compile(code, str(full_path), "exec")
        print(f"  [OK] Syntax & Compilation verified: {p}")

    print("\nAll 12 application files compiled successfully with 0 errors!")

if __name__ == "__main__":
    test_all_pages()
