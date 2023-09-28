import os
import time
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as ec

similar_account = 'Naruto Uzumaki'
insta_username = os.environ['insta_username']
insta_password = os.environ['insta_password']
URL = 'https://www.instagram.com/accounts/login/'


class InstaFollower:
    def __init__(self):
        options = Options()
        options.add_experimental_option('detach', True)
        self.driver = webdriver.Edge(options=options)
        self.driver.get(url=URL)

    def login(self):
        self.webdriver_wait_send_key(ec.element_to_be_clickable, By.NAME, 'username', insta_username)
        time.sleep(0.5)
        self.webdriver_wait_send_key(ec.element_to_be_clickable, By.NAME, 'password', insta_password)
        time.sleep(0.5)
        self.webdriver_wait_click(ec.element_to_be_clickable, By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
        time.sleep(1.5)
        self.webdriver_wait_click(ec.presence_of_element_located, By.CSS_SELECTOR, 'div.x1i10hfl')
        self.webdriver_wait_click(ec.presence_of_element_located, By.CSS_SELECTOR, 'button._a9--._a9_1')

        xpath = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a"
        self.webdriver_wait_send_key(ec.presence_of_element_located, By.XPATH, xpath, Keys.ENTER)
        self.webdriver_wait_send_key(ec.presence_of_element_located, By.XPATH,
                                     "//input[@aria-label='Search input']", send_key=similar_account)
        xpath_search_results = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/a[1]'
        self.webdriver_wait_click(ec.presence_of_element_located, By.XPATH, xpath_search_results)
        xpath_followers = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a'
        self.webdriver_wait_click(ec.presence_of_element_located, By.XPATH, xpath_followers)

    def find_followers(self):
        follower_list = self.webdriver_wait_send_key(ec.presence_of_element_located, By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]')

        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", follower_list)

    def follow(self):
        # parent_element = self.webdriver_wait_send_key(ec.presence_of_element_located, By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div')
        time.sleep(2)
        wait_buttons = WebDriverWait(self.driver, 10)
        try:
            list_buttons = wait_buttons.until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '._acan._acap._acas._aj1-')))
            for button in list_buttons:
                time.sleep(0.75)
                try:
                    button.click()
                except exceptions.ElementClickInterceptedException:
                    self.webdriver_wait_click(ec.presence_of_element_located, By.CSS_SELECTOR, '._a9--._a9_1')
                    # self.find_followers()
            list_buttons.clear()
        except exceptions.TimeoutException:
            pass

    def webdriver_wait_click(self, ec_condition, by_condition, query):
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(ec_condition((by_condition, query)))
        element.click()
        return element

    # Check this out if it's working as intended // DONE
    def webdriver_wait_send_key(self, ec_condition, by_condition, query, send_key=None) -> WebElement:
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(ec_condition((by_condition, query)))
        if send_key is not None:
            element.send_keys(send_key)
        return element


insta_follow = InstaFollower()
insta_follow.login()
while True:
    insta_follow.follow()
    insta_follow.find_followers()
