from config.config import EXPLICIT_WAIT
from utils.exception_handler import exception_handler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.custom_logger import custom_logger

def page_handler(driver, element, text=""):
    """특정 요소 클릭 후 리다이렉션 확인"""
    try:
        # 클릭한 요소의 URL 가져오기 (data-gtm-click-url 속성 값)
        expected_url = element.get_attribute("data-gtm-click-url")
        
        if expected_url:
            # data-gtm-click-url 속성 값이 있을 경우 로그 출력
            custom_logger.info(f"클릭 요소안의 URL: {expected_url}")

            # expected_url이 있을 경우 URL 변경이 일어날 때까지 대기
            WebDriverWait(driver, EXPLICIT_WAIT).until(EC.url_to_be(expected_url))

            # 현재 URL 가져오기
            current_url = driver.current_url

            # expected_url이 있을 경우 URL 비교
            if current_url == expected_url:
                custom_logger.info(f"{text}페이지 리다이렉션 성공 URL: {current_url}")
                return True
            else:
                custom_logger.error(f"{text}페이지 리다이렉션 실패: 예상 URL({expected_url})와 현재 URL({current_url}) 불일치")
                return False
        else:
            # 클릭한 요소의 expected_url이 없을 경우 URL 변경이 일어날 때까지 대기
            WebDriverWait(driver, EXPLICIT_WAIT).until(EC.url_changes(driver.current_url))
            
            current_url = driver.current_url
            custom_logger.info(f"{text}페이지 리다이렉션 확인 URL: {current_url}")
            return True

    except Exception as e:
        exception_handler(driver, e, "리다이렉션 시간초과")
        raise e