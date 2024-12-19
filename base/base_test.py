import logging
import pytest
from utils.screenshot import screenshot

class BaseTest:
    """
    모든 테스트 케이스에서 상속받는 기본 클래스
    """

    def __init__(self):
        self.logger = logging.getLogger(type(self).__name__)
    
    # 테스트 실행 전 환경을 설정하는 메서드
    def setup_method(self, method):
        from webdriver_factory import WebDriverFactory
        self.driver = WebDriverFactory().create_driver()  # WebDriver 인스턴스 생성
        self.logger = logging.getLogger(type(self).__name__)  # 로거 초기화

    # 테스트 실행 후 환경을 정리하는 메서드
    def teardown_method(self, method):
        if self.driver:
            try:
                # 테스트 실패 시 스크린샷 찍기 (pytest 예시)
                if hasattr(pytest, 'config'):
                    if pytest.config.option.lastfailed:
                        screenshot(self.driver, method.__name__)
                else:
                    screenshot(self.driver, method.__name__)
            except Exception as e:
                self.logger.error(f"스크린샷 찍는 중 오류 발생: {e}")
            finally:
                self.driver.quit()