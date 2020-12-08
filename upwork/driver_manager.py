import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from upwork.constants import FOLDER_LOG

IS_DOCKER_INSTANCE = os.environ.get('IS_DOCKER_INSTANCE', False)


class ManagerDriver():
    caps = DesiredCapabilities.FIREFOX

    def __init__(self, default_path=None):
        if default_path:
            self.path = default_path
        self.caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        self._driver = None
        self.load_driver()

    def driver(self):
        return self._driver

    def load_driver(self):
        """
        Function to create a instance of Webdrive
        """
        if not os.path.exists(self.path) and not IS_DOCKER_INSTANCE:
            self.path = GeckoDriverManager(cache_valid_range=0, log_level=10).install()

        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)

        options = Options()
        if IS_DOCKER_INSTANCE:
            options.headless = True
        print(self.path)
        self._driver = webdriver.Firefox(firefox_profile=profile,
                                         executable_path=self.path,
                                         desired_capabilities=self.caps,
                                         service_log_path=f'./{FOLDER_LOG}/geckodriver.log',
                                         options=options)
        self.clean_selenim_params()

    def clean_selenim_params(self):
        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
