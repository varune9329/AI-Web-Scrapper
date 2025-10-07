# check_driver.py
import sys
import platform

# 1) Detect installed Chrome version on Windows via registry
def get_chrome_version_windows():
    try:
        import winreg  # built-in on Windows
    except ImportError:
        return None

    reg_paths = [
        r"SOFTWARE\Google\Chrome\BLBeacon",
        r"SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon",
    ]
    for root in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for path in reg_paths:
            try:
                key = winreg.OpenKey(root, path)
                version, _ = winreg.QueryValueEx(key, "version")
                return version
            except OSError:
                continue
    return None

def print_local_chrome_version():
    if platform.system() == "Windows":
        ver = get_chrome_version_windows()
        print(f"Local Chrome (Windows registry): {ver or 'Not found'}")
    else:
        print("Local Chrome: OS not Windows – skipping registry check")

# 2) Launch Selenium and print the resolved versions
def check_selenium_versions():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    opts = Options()
    # Headless is optional; comment out if you want to see the window
    #opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    # Let Selenium Manager resolve and download the correct driver
    driver = webdriver.Chrome(options=opts)
    try:
        caps = driver.capabilities or {}
        browser_version = caps.get("browserVersion")
        # chromedriver version is usually in caps["chrome"]["chromedriverVersion"]
        chrome_dict = caps.get("chrome", {})
        chromedriver_ver = chrome_dict.get("chromedriverVersion")

        print(f"Selenium browserVersion: {browser_version}")
        print(f"Selenium chromedriverVersion: {chromedriver_ver}")
    finally:
        driver.quit()

def main():
    print_local_chrome_version()
    try:
        check_selenium_versions()
    except Exception as e:
        print("\nError starting Selenium/driver:")
        print(e)
        print("\nTips:")
        print("  • Ensure selenium is up to date:  python -m pip install -U selenium")
        print("  • Run inside your venv (prompt should show (ai) or (venv)).")
        print("  • If corporate proxy exists, set HTTPS_PROXY/HTTP_PROXY env vars.")

if __name__ == "__main__":
    print(f"Python: {sys.version.split()[0]}  |  Platform: {platform.system()} {platform.release()}")
    main()
