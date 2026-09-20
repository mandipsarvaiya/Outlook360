"""
Test page routing on Streamlit server.
"""
import urllib.request

for path in ["/", "/1_Executive_Overview", "/Executive_Overview"]:
    url = f"http://localhost:8501{path}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            print(f"Path {path}: status {response.getcode()}")
    except Exception as e:
        print(f"Path {path}: failed ({e})")
