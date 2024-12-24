
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.custom_logger import custom_logger
from utils import exception_handler as eh
from config.config import EXPLICIT_WAIT, EXPLICIT_WAIT
from utils.custom_actionchains import move_to_element
from utils import custom_logger as cl

def find_visible_sections(driver, locators, text=""):
    """각 페이지 주요 섹션 존재 확인"""
    for key, value in locators.items():
        if '_section' in key:
            find_visible_element(driver, (By.CSS_SELECTOR, value), f"{text} {key} 영역")

 

# # find_visible_element
# def find_visible_element(driver, locator, text=""):
#     """보이는 요소를 찾는 함수"""
#     try:
#         element = WebDriverWait(driver, EXPLICIT_WAIT).until(
#             EC.visibility_of_element_located(locator)
#         )
#         if not element.is_displayed():
#             move_to_element(driver, element)
#         custom_logger.info(f"{text}{locator}(이)가 화면에 보입니다.")
#         return element
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{text}{locator}(이)가 화면에 보이지 않습니다.")
#         return None
    
# def check_section_active(driver, locator, text=""):
#     """섹션이 활성화 상태(active 클래스 포함)인지 확인하는 함수"""
#     try:
#         element = find_visible_element(driver, locator, text)  # 요소 찾기
#         if element:
#             move_to_element(driver, element, text)
#             class_name = element.get_attribute("class")
#             if "active" in class_name:
#                 custom_logger.info(f"{text} 섹션이 활성화 상태입니다.")
#                 return True
#         else:
#             return False
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{text} 섹션 활성화 상태 확인 실패")
#         return False
    
# find_visible_element
def find_visible_element(driver, locator, text=""):
    """보이는 요소를 찾는 함수"""
    try:
        element = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_element_located(locator)  # 요소가 존재하는지 확인
        )
        
        # 요소가 화면에 보이지 않으면 스크롤하여 포커싱
        if not element.is_displayed():
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            custom_logger.info(f"{text}{locator}(이)가 화면에 보이지 않아 스크롤하여 포커싱했습니다.")

        custom_logger.info(f"{text}{locator}(이)가 화면에 보입니다.")
        return element
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}{locator}(이)가 화면에 보이지 않습니다.")
        return None