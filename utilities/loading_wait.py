from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

"""
    class Wait : 페이지 로딩 대기
"""
class LoadingWait:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def wait_until(self, condition, timeout = 60):
        try:
            WebDriverWait(self.driver, timeout).until(condition)
            self.logger.info("요소 로깅이 완료되었습니다.")
            return True
        except TimeoutException:
            self.logger.error("요소 로깅이 충족되지않았습니다.")
            return False