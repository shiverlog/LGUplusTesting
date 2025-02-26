from typing import Dict, Any, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from base.webdriver_factory import WebDriverFactory
from utils import custom_logger as cl
from config.config import BASE_URL
from utils.exception_handler import exception_handler 
import os
import json

class Base:
    """모든 테스트 케이스에서 상속받는 기본 클래스"""
    def setup_method(self, method) -> None:
        """테스트 실행 전 환경 설정"""
        self.driver_factory: WebDriverFactory = WebDriverFactory()
        self.driver: Optional[WebDriver] = None
        self.logger: Optional[Any] = None
        self.locators: Optional[Dict[str, Any]] = None
        self.initialize()
        self.logger.info(f"Setting up test method: {method.__name__}")

    def initialize(self) -> None:
        """WebDriver와 Logger를 초기화"""
        if not self.driver:
            self.driver = self.driver_factory.create_driver()
            self.driver.get(BASE_URL)
        if not self.logger:
            self.logger = cl.Logger().get_logger()
        self.logger.info("Base class initialized")
    
    def load_locators(self, section: str) -> None:
        """로케이터 JSON 파일 로드"""
        self.locators = LocatorLoader.load_locators(section)
        self.logger.info(f"Locators loaded for section: {section}")
    
    def get_by_type(self, locator_type: str) -> Any:
        """LocatorType을 By 객체로 변환하는 함수"""
        locator_type = locator_type.lower()
        locator_types = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME,
            "link": By.LINK_TEXT,
            "tag": By.TAG_NAME,
            "partial_link": By.PARTIAL_LINK_TEXT
        }
        if locator_type not in locator_types:
            self.logger.error(f"Locator type {locator_type} not correct/supported")
            return False
        return locator_types[locator_type]

    def setup_method(self, method) -> None:
        """테스트 실행 전 환경 설정"""
        if not self.driver:
            self.initialize()
        self.logger.info(f"Setting up test method: {method.__name__}")

    def teardown_method(self, method) -> None:
        """테스트 실행 후 환경 정리"""
        if self.driver:
            self.quit_driver()
        self.logger.info(f"Tearing down test method: {method.__name__}")

    def get_driver(self) -> Optional[WebDriver]:
        """WebDriver 인스턴스 반환"""
        return self.driver

    def quit_driver(self) -> None:
        """WebDriver 종료"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.logger.info("WebDriver quit")

class LocatorLoader:
    @staticmethod
    def load_locators(section: str) -> Dict[str, Any]:
        """로케이터 JSON 파일 로드"""
        locators_path = os.path.join('locators', 'locators.json')
        try:
            with open(locators_path, 'r', encoding='utf-8') as f:
                locators = json.load(f)
            if section not in locators:
                raise KeyError(f"Section '{section}' not found in locators file")
            return locators[section]
        except FileNotFoundError:
            exception_handler(None, FileNotFoundError(f"Locator file not found: {locators_path}"), "로케이터 파일을 찾을 수 없음")
        except json.JSONDecodeError as e:
            exception_handler(None, e, "로케이터 파일 JSON 파싱 실패")
        except KeyError as e:
            exception_handler(None, e, f"로케이터 파일에서 섹션 '{section}' 찾기 실패")
        except Exception as e:
            exception_handler(None, e, "로케이터 파일 로드 중 예상치 못한 오류 발생")
        raise
