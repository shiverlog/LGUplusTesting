from selenium.webdriver.common.by import By
import utils.custom_logger as custom_logger
from utils.exception_handler import handle_exception

# find_element
def find_element(driver, locator):
    return driver.find_element(By.XPATH, locator)

# highlight_element
def highlight_element(driver, locator):
    try:
        element = find_element(driver, locator)
        if element:
            original_style = element.get_attribute("style")
            driver.execute_script("arguments[0].style.border='3px solid red'", element)
            custom_logger.info(f"{locator} 요소를 강조 표시")
            driver.execute_script(f"arguments[0].style.border='{original_style}'", element)
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소 강조 표시 실패")