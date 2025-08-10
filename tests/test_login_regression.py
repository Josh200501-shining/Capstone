import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile

# Path to your chromedriver (change if needed)
driver_path = r'D:\capstone\pythonProject\drivers\chromedriver.exe'

@pytest.fixture
def driver():
    # Setup Chrome options for CI-friendly run (headless + temp user data dir)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")  # Recommended for CI
    chrome_options.add_argument("--disable-dev-shm-usage")  # Recommended for CI

    # Create a temporary directory for user data to avoid session conflicts
    temp_dir = tempfile.TemporaryDirectory()
    chrome_options.add_argument(f"--user-data-dir={temp_dir.name}")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver

    driver.quit()
    temp_dir.cleanup()

def open_login_page(driver):
    driver.get("file:///D:/capstone/pythonProject/login.html")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

def login(driver, username, password):
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "loginButton").click()

    message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "message")))
    return message.text.strip()

@pytest.mark.parametrize("username,password,expected_message", [
    ("admin", "password123", "Login successful!"),
    ("wronguser", "wrongpass", "Invalid username or password."),
    ("admin", "wrongpass", "Invalid username or password."),
    ("", "", "Invalid username or password."),
])
def test_login_regression(driver, username, password, expected_message):
    open_login_page(driver)
    actual_message = login(driver, username, password)

    print(f"Testing login with username={repr(username)} password={repr(password)}")
    print(f"Expected message: {repr(expected_message)}")
    print(f"Actual message  : {repr(actual_message)}")

    assert actual_message == expected_message, f"Expected '{expected_message}', but got '{actual_message}'"
