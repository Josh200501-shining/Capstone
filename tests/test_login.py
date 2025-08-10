from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import os

driver_path = r'D:\capstone\pythonProject\drivers\chromedriver.exe'
print("ChromeDriver found:", os.path.isfile(driver_path))

service = Service(driver_path)
driver = webdriver.Chrome(service=service)

driver.get("file:///D:/capstone/pythonProject/login.html")

print("PASSED.")


# Keep browser open for 60 seconds so you can interact manually
time.sleep(12)

driver.quit()
