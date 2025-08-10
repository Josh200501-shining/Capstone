import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import tempfile

driver_path = r'D:\capstone\pythonProject\drivers\chromedriver.exe'

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    temp_dir = tempfile.TemporaryDirectory()
    chrome_options.add_argument(f"--user-data-dir={temp_dir.name}")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()
    temp_dir.cleanup()
