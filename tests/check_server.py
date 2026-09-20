"""
Verify HTTP connection to Streamlit server and inspect health.
"""
import urllib.request
import urllib.error

def check_streamlit():
    url = "http://localhost:8501/_stcore/health"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
            print(f"Health check status: {status}, body: {body}")
    except Exception as e:
        print(f"Health check failed: {e}")

    main_url = "http://localhost:8501"
    try:
        with urllib.request.urlopen(main_url, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
            print(f"Main URL status: {status}, HTML content length: {len(body)}")
            print("Title in HTML:", "Outlook360" in body)
    except Exception as e:
        print(f"Main URL fetch failed: {e}")

if __name__ == "__main__":
    check_streamlit()
