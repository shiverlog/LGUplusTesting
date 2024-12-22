from config.config import IMPLICIT_WAIT
from utils.exception_handler import exception_handler
from utils.custom_logger import custom_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageRedirectionHandler:
    """페이지 리다이렉션 확인 공통 클래스"""

    def __init__(self, driver):
        self.driver = driver
        self.logger = custom_logger

    def verify_redirection(self, locator, attribute_name="data-gtm-click-url", timeout=IMPLICIT_WAIT):
        """
        특정 요소 클릭 후 리다이렉션 확인
        :param locator: 클릭할 요소의 locator
        :param attribute_name: 확인할 속성 이름 (기본: 'data-gtm-click-url')
        :param timeout: 대기 시간 (초)
        :return: 성공 여부 (True/False)
        """
        try:
            # 속성 값 가져오기
            expected_url = locator.get_attribute(attribute_name)
            current_url = self.driver.current_url

            # 리다이렉션 확인
            if expected_url in current_url:
                self.logger.info(f"페이지 리다이렉션 성공 URL: {current_url}")
                return True
            else:
                self.logger.error(f"리다이렉션 실패: 예상 URL({expected_url})와 현재 URL({current_url}) 불일치")
                return False

        except Exception as e:
            exception_handler(self.driver, e, "리다이렉션 확인 중 오류 발생")
            return False