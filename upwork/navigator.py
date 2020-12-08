import json
import time

from dotenv import load_dotenv
from pydantic.json import pydantic_encoder
from pydantic.types import Path

from upwork.models import Profile
from upwork.reader import UpWorkReader
from upwork.utils import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from upwork.constants import SLEEP_TIME, EVENT_PRESENCE, EVENT_CLICKABLE, SLEEP_MEDIUM_TIME, API_PROFILE, PAGE_PROFILE, \
    FOLDER_SCREENSHOT, PAGE_CONTACT_INFO, FOLDER_OUTPUT, SLEEP_SHORT_TIME, SLEEP_LONG_TIME
from upwork.exceptions import WebDriverNotFound, InvalidCredentials, InvalidPayload
import logging
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class UpWorkNavigator:

    def __init__(self, driver):
        self.__driver = driver
        self.USERNAME = os.getenv("USERNAME")
        self.PASSWORD = os.getenv("PASSWORD")
        self.SECRET_ANSWER = os.getenv("SECRET_ANSWER")
        self.verbose = os.getenv("VERBOSE", False)
        self.reader = UpWorkReader()

        if not self.__driver:
            raise WebDriverNotFound(self.__driver)

    def start(self):
        """
            Main function, responsible to call the flow
        """
        # checks if have valid credentials
        if not self.USERNAME or not self.PASSWORD or not self.SECRET_ANSWER:
            raise InvalidCredentials(self.USERNAME, self.PASSWORD)

        # start trying to read the profile api
        self.load_page(API_PROFILE)

        # make sure you are redirected to the login page and then login
        self.login()

        # starting reading profile api
        profile_api_response = self.get_hxr(API_PROFILE)
        identity = profile_api_response.get("identity", {})

        if not identity:
            raise InvalidPayload("Identity not found")

        # reading profile page
        profile_url = PAGE_PROFILE.format(identity.get("ciphertext"))
        self.load_page(profile_url)
        self.reader.get_profile(self.get_html())
        self.take_screenshot("profile")

        # reading contact page
        # to access the contact page you need to go through the authorization screen at least once per device
        self.load_page(PAGE_CONTACT_INFO)
        self.check_device_authorization()
        self.check_re_enter_password_screen()
        self.take_screenshot("contact")
        self.reader.get_contact_info(self.get_html())

        # get the full profile and update with the informations that came from profile api
        profile = self.reader.get_full_profile().copy(update={
            "id": identity.get("uid"),
            "account": identity.get("userId"),
            "profile_url": profile_url,
        })
        logging.info(json.dumps(profile, indent=4, default=pydantic_encoder))

        if self.verbose:
            print(json.dumps(profile, indent=4, default=pydantic_encoder))

        self.save_file_json(profile)

    @staticmethod
    def save_file_json(profile: Profile) -> bool:
        try:

            with open(f"{FOLDER_OUTPUT}/{profile.account}_{int(time.time())}.json", 'w') as json_file:
                json.dump(profile.dict(), json_file)
                return True
        except Exception as e:
            logging.error(f"Error to save result data: {e}")
            return False

    def get_element(self, by, selector, type=EVENT_PRESENCE):
        try:
            if type == EVENT_PRESENCE:
                return WebDriverWait(self.__driver, SLEEP_MEDIUM_TIME).until(
                    EC.presence_of_element_located((by, selector))
                )
            else:
                return WebDriverWait(self.__driver, SLEEP_MEDIUM_TIME).until(
                    EC.element_to_be_clickable((by, selector))
                )
        except TimeoutException:
            return None

    def login(self):
        """
        Function to pass through login page
        :return:
        """
        input_username = self.get_element(By.ID, "login_username")

        if input_username:
            btn_submit = self.get_element(By.XPATH, "//button[@id='login_password_continue']", type=EVENT_CLICKABLE)

            input_username.send_keys(self.USERNAME)
            sleep(SLEEP_SHORT_TIME)
            btn_submit.click()

            sleep(SLEEP_SHORT_TIME)
            input_password = self.get_element(By.ID, "login_password")
            btn_submit = self.get_element(By.XPATH, "//button[@id='login_control_continue']", type=EVENT_CLICKABLE)
            input_password.send_keys(self.PASSWORD)

            sleep(SLEEP_SHORT_TIME)
            btn_submit.click()

            sleep(SLEEP_LONG_TIME)
            self.check_device_authorization_login()

        return input_username is not None

    def check_device_authorization_login(self):
        """
        Function to check and pass through check device during the login flow
        """
        input_authorization_answer = self.get_element(By.ID, "login_deviceAuthorization_answer")

        if input_authorization_answer:
            btn_submit = self.get_element(By.XPATH, "//button[@id='login_control_continue']", type=EVENT_CLICKABLE)
            input_authorization_answer.send_keys(self.SECRET_ANSWER)
            btn_submit.click()
            sleep(SLEEP_LONG_TIME)

        logging.info(f"check_device_authorization_login: {input_authorization_answer is not None}")

    def check_device_authorization(self):
        """
        Function to check and pass through check device page
        :return:
        """
        sleep(SLEEP_SHORT_TIME)
        input_answer = self.get_element(By.ID, "deviceAuth_answer")
        if input_answer:
            input_answer.send_keys(self.SECRET_ANSWER)
            sleep(SLEEP_TIME)
            btn_submit = self.get_element(By.XPATH, "//button[@id='control_save']", type=EVENT_CLICKABLE)
            btn_submit.click()
            sleep(SLEEP_LONG_TIME)

        logging.info(f"check_device_authorization: {input_answer is not None}")

        return input_answer is not None

    def check_re_enter_password_screen(self):
        """
        Function to check and pass through re-enter password page
        :return:
        """
        sleep(SLEEP_SHORT_TIME)
        input_password = self.get_element(By.ID, "sensitiveZone_password")
        if input_password:
            input_password.send_keys(self.PASSWORD)
            sleep(SLEEP_SHORT_TIME)
            btn_submit = self.get_element(By.XPATH, "//button[@id='control_continue']", type=EVENT_CLICKABLE)
            btn_submit.click()
            sleep(SLEEP_LONG_TIME)

        logging.info(f"check_re_enter_password_screen: {input_password is not None}")

        return input_password is not None

    def load_page(self, url: str):
        """
        Function to load page and sleep for few seconds to simulate a user interaction
        :param url:
        """
        self.__driver.get(url)
        sleep(SLEEP_LONG_TIME)

    def get_html(self) -> str:
        """
        Function to get source code of current page
        :return:
        """
        return self.__driver.page_source

    def get_hxr(self, url: str) -> dict:
        """
        Function used to make HXR requests
        Convert to view-source ang get tag <pre> to access the response payload
        :param url:
        :return:
        """
        self.__driver.get(f"view-source:{url}")
        content = self.__driver.find_element_by_tag_name('pre').text
        try:
            return json.loads(content)
        except Exception as e:
            raise InvalidPayload(content)

    def take_screenshot(self, key: str = "") -> object:
        """
        Function to capture the screenshot of current page
        :param key:
        """
        if os.getenv("TAKE_SCREENSHOTS"):
            self.__driver.save_screenshot(
                f"{FOLDER_SCREENSHOT}/{key}_{int(time.time())}.png")
