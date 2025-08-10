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

def login(driver, username, password):
    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(username)

    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)

    driver.find_element(By.ID, "loginButton").click()

    message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "message")))
    return message.text

@pytest.mark.parametrize("username,password", [
    ("admin", "password123"),
    ("wronguser", "wrongpass"),
    ("admin", "wrongpass"),
    ("", ""),
])
def test_login_regression(driver, username, password):
    open_login_page(driver)
    actual_message = login(driver, username, password)

    print(f"Testing login with username={repr(username)} password={repr(password)}")
    print(f"Login message from page: {repr(actual_message)}")

    if actual_message.strip() == "Login successful!":
        assert True  # Pass the test
    else:
        pytest.fail(f"Test failed: Expected successful login but got {repr(actual_message)}")
