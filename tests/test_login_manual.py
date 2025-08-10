import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = r'D:\capstone\pythonProject\drivers\chromedriver.exe'

@pytest.fixture
def driver():
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

def open_login_page(driver):
    driver.get("file:///D:/capstone/pythonProject/login.html")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

def test_manual_login(driver):
    open_login_page(driver)

    print("Please enter username and password manually in the browser, then click Login.")
    input("After clicking Login in the browser, press Enter here to continue the test...")

    # After user clicks login manually, wait for message to appear on page
    message = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "message"))
    )
    login_result = message.text
    print(f"\nLogin message from page: {login_result}")

    # Now assert based on expected message
    if login_result == "Login successful!":
        print("Test PASSED")
    elif login_result == "Invalid username or password.":
        print("Test FAILED: Invalid credentials")
        pytest.fail("Invalid username or password.")
    else:
        print("Test FAILED: Unexpected message")
        pytest.fail(f"Unexpected message: {login_result}")
