from base.webdriver_factory import WebDriverFactory
from utils import custom_logger as cl
from config.config import BASE_URL
from selenium.webdriver.common.by import By
from utils.exception_handler import exception_handler as eh
import os, json

class Base:
    """모든 테스트 케이스에서 상속받는 기본 클래스"""
    def __init__(self):
        self.driver_factory = WebDriverFactory()
        self.driver = None
        self.logger = None
        self.locators = None
        # WebDriver 인스턴스, Logger 인스턴스, 로케이터 JSON 파일을 저장하는 변수
        self.initialize()

    def initialize(self):
        """WebDriver와 Logger를 초기화"""
        if not self.driver:
            self.driver = self.driver_factory.create_driver()
            self.driver.get(BASE_URL)
        if not self.logger:
            self.logger = cl.Logger().get_logger()
    
    def load_locators(self, section):
        """로케이터 JSON 파일 로드"""
        self.locators = LocatorLoader.load_locators(section)
    
    def get_by_type(self, locatorType):
        """LocatorType을 By 객체로 변환하는 함수"""
        locator_type = locatorType.lower()
        if locator_type == "id":
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "link":
            return By.LINK_TEXT
        elif locator_type == "tag":
            return By.TAG_NAME
        elif locator_type == "partial_link":
            return By.PARTIAL_LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
            return False

    def setup_method(self, method):
        """테스트 실행 전 환경 설정"""
        if not self.driver:
            self.initialize()

    def teardown_method(self, method):
        """테스트 실행 후 환경 정리"""
        if self.driver:
            self.quit_driver()

    def get_driver(self):
        """WebDriver 인스턴스 반환"""
        return self.driver

    def quit_driver(self):
        """WebDriver 종료"""
        if self.driver:
            self.driver.quit()
            self.driver = None

class LocatorLoader:
    @staticmethod
    def load_locators(section):
        """로케이터 JSON 파일 로드"""
        try:
            # 로케이터 파일 경로
            locators_path = os.path.join('locators', 'locators.json')
            # JSON 파일 로드
            with open(locators_path, 'r', encoding='utf-8') as f:
                # 로드한 JSON 파일에서 해당 섹션의 로케이터 반환
                return json.load(f)[section]
        except Exception as e:
            eh.exception_handler(None, e, "로케이터 파일 로드 실패")
            raise
