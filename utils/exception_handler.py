from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.custom_logger import custom_logger
from utils.screenshot import Screenshot
import traceback

def handle_exception(driver, e, message="ERROR"):
    custom_logger.error(f"{message}: {e}")
    custom_logger.error(traceback.format_exc())
    
    if isinstance(e, TimeoutException):
        custom_logger.info("페이지를 새로고침")
        driver.refresh()
    elif isinstance(e, NoSuchElementException):
        custom_logger.warning("요소를 찾을 수 없음")
        pass
    else:
        pass
    
    screenshot_taker = Screenshot(driver)
    screenshot_taker.capture("exception")
