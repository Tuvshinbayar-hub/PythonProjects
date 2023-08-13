from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import WebDriverException

import selenium

import time
import os

URL = 'https://www.linkedin.com/login'
username = os.environ['username']
password = os.environ['password']

options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Edge(options=options)
driver.get(url=URL)


def search_for_jobs(job_query):
    button_search = driver.find_element(By.CLASS_NAME, 'search-global-typeahead__collapsed-search-button')
    try:
        button_search.click()
    except WebDriverException:
        pass
    finally:
        search_input = driver.find_element(By.CLASS_NAME, 'search-global-typeahead__input')
        search_input.send_keys(job_query)
        search_input.send_keys(Keys.ENTER)

    messenger_toggler = driver.find_elements(By.CSS_SELECTOR, '.msg-overlay-bubble-header__control')
    messenger_toggler[1].click()
    WebDriverWait(driver, timeout=15).until(
        expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, 'button[data-control-name="entity_action_primary"]')
        )
    )
    parent_element = driver.find_element(By.CSS_SELECTOR, '.pv0.ph0.mb2.artdeco-card')
    jobs = parent_element.find_elements(By.CSS_SELECTOR, 'button[data-control-name="entity_action_primary"]')
    print(jobs)

    for job in jobs:
        job.click()


username_input = driver.find_element(By.NAME, 'session_key')
password_input = driver.find_element(By.NAME, 'session_password')
submit_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')

time.sleep(2)

username_input.send_keys(username)
time.sleep(1.5)
password_input.send_keys(password)
time.sleep(1.5)
submit_button.click()

search_for_jobs('backend')

# App only saves jobs now. It's possible to make it actually apply to saved jobs.

