class WebDriverNotFound(Exception):

    def __init__(self, driver, message="WebDriver Not Found"):
        self.driver = driver
        self.message = message
        super().__init__(self.message)


class InvalidCredentials(Exception):

    def __init__(self, username, password, message="Invalid Credentials"):
        self.password = password
        self.username = username
        self.message = message
        super().__init__(self.message)


class InvalidPayload(Exception):

    def __init__(self, payload, message="Invalid Payload"):
        self.payload = payload
        self.message = message
        super().__init__(self.message)
