import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from selenium.common.exceptions import WebDriverException
from upwork.constants import FOLDER_LOG
from upwork.driver_manager import ManagerDriver
from upwork.navigator import UpWorkNavigator
from upwork.reader import UpWorkReader

logging.basicConfig(format='%(asctime)s %(message)s',
                    filename=f'{FOLDER_LOG}/upwork.log',
                    filemode='w',
                    level=logging.INFO)
load_dotenv(dotenv_path=Path('.') / '.env')

if __name__ == '__main__':

    DRIVER_PATH = os.environ.get('DRIVER_PATH')
    print("DRIVER_PATH", DRIVER_PATH)
    manager = ManagerDriver(default_path=DRIVER_PATH)
    navigator = UpWorkNavigator(manager.driver())
    reader = UpWorkReader()

    try:

        navigator.start()

    except WebDriverException as e:
        logging.error(e)
        message = "Execution finished with error: Address not found or inaccessible"
        logging.error(message)
        print(message)
    except Exception as e:
        message = f"Execution Exception {e}"
        logging.error(message)
        print(message)
    finally:
        message = "Execution finished"
        print(message)
