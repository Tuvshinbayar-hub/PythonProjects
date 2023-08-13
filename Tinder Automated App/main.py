from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import selenium.common.exceptions as exceptions

import os
import time

URL = 'https://tinder.com'

options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Edge(options=options)
driver.get(url=URL)

time.sleep(0.5)
i_accept_button = driver.find_element(By.XPATH, '//*[@id="q-620494849"]/div/div[2]/div/div/div[1]/div[1]/button')
time.sleep(1)
i_accept_button.click()
time.sleep(1)
login_button = driver.find_element(By.XPATH, '//*[@id="q-620494849"]/div/div[1]/div/div/main/div/div[2]/div/div[3]/div/div/button[2]/div[2]/div[2]')
time.sleep(1)
login_button.click()
# google_login_button = driver.find_element(By.CSS_SELECTOR, 'div[tabindex="0"]')
wait_login_button = WebDriverWait(driver, 10)
google_login_button = wait_login_button.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="q1946091371"]/main/div/div/div[1]/div/div/div[2]/div[2]/span/div[2]/button')))
google_login_button.click()
time.sleep(1)
base_window = driver.window_handles[0]
fb_window = driver.window_handles[1]

print(driver.window_handles)

driver.switch_to.window(fb_window)
email_input = driver.find_element(By.XPATH, '//*[@id="email"]')
email_input.send_keys(os.environ['fb_username'])
time.sleep(0.5)
password_input = driver.find_element(By.XPATH, '//*[@id="pass"]')
password_input.send_keys(os.environ['fb_password'])
time.sleep(0.5)
fb_login_button = driver.find_element(By.NAME, 'login')
fb_login_button.send_keys(Keys.ENTER)

driver.switch_to.window(base_window)
wait_allow_button = WebDriverWait(driver, 10)
location_button = wait_allow_button.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="q1946091371"]/main/div/div/div/div[3]/button[1]')))
location_button.click()
wait_not_interested_button = WebDriverWait(driver, 10)
not_interested_button = wait_not_interested_button.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="q1946091371"]/main/div/div/div/div[3]/button[2]')))
not_interested_button.click()

wait_like_button = WebDriverWait(driver, 10)
like_button = wait_like_button.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'button') and contains(@class, 'Bgi($g-ds-background-like):a')]")))
time.sleep(1)
while True:
    time.sleep(1)
    try:
        like_button.click()
    except exceptions.NoSuchElementException:
        time.sleep(1)
    except exceptions.ElementClickInterceptedException:
        print('fix it')


# print(driver.window_handles)

