import logging
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from typing import Union

class WebDriverFactory:
    """WebDriver 인스턴스 생성을 위한 팩토리 클래스"""

    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def create_driver(self, browser_name = "chrome", headless = False):
        """지정된 브라우저와 옵션으로 WebDriver 인스턴스를 생성"""
        browser_name = browser_name.lower()
        options = self.get_browser_options(browser_name)

        if headless:
            options.add_argument("--headless")

        try:
            if browser_name == self.CHROME:
                driver = webdriver.Chrome(options=options)
            elif browser_name == self.FIREFOX:
                driver = webdriver.Firefox(options=options)
            elif browser_name == self.EDGE:
                driver = webdriver.Edge(options=options)
            else:
                raise ValueError(f"지원하지 않는 브라우저입니다: {browser_name}")

            driver.maximize_window()
            self.logger.info(f"{browser_name} 드라이버가 성공적으로 생성되었습니다.")
            return driver
        except Exception as e:
            self.logger.error(f"{browser_name} 드라이버 생성 중 오류 발생: {str(e)}")
            raise

    def get_browser_options(self, browser_name: str) -> Union[ChromeOptions, FirefoxOptions, EdgeOptions]:
        """브라우저별 옵션 객체 반환"""
        if browser_name == self.CHROME:
            return self._set_chrome_options()
        elif browser_name == self.FIREFOX:
            return self._set_firefox_options()
        elif browser_name == self.EDGE:
            return self._set_edge_options()
        else:
            raise ValueError(f"지원하지 않는 브라우저입니다: {browser_name}")

    def _set_chrome_options(self) -> ChromeOptions:
        options = ChromeOptions()
        # Chrome 특정 옵션 설정
        return options

    def _set_firefox_options(self) -> FirefoxOptions:
        options = FirefoxOptions()
        # Firefox 특정 옵션 설정
        return options

    def _set_edge_options(self) -> EdgeOptions:
        options = EdgeOptions()
        # Edge 특정 옵션 설정
        return options
