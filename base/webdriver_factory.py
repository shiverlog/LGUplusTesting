import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

class WebDriverFactory:
    """WebDriver 인스턴스 생성을 위한 팩토리 클래스"""
    def create_driver(self, browser_name="chrome", headless=False):
        """ 지정된 브라우저와 옵션으로 WebDriver 인스턴스를 생성 """
        browser_name = browser_name.lower()
        options = self.get_browser_options(browser_name)
        
        if headless:
            options.add_argument("--headless")

        if browser_name == "chrome":
            return webdriver.Chrome(options=options)
        elif browser_name == "firefox":
            return webdriver.Firefox(options=options)
        elif browser_name == "edge":
            return webdriver.Edge(options=options)
        else:
            raise ValueError(f"지원하지 않는 브라우저입니다: {browser_name}")

    def get_browser_options(self, browser_name):
        screen_width, screen_height = pyautogui.size()

        # 윈도우 사이즈 90% 계산
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)

        if browser_name == "chrome":
            options = ChromeOptions()
        elif browser_name == "firefox":
            options = FirefoxOptions()
        elif browser_name == "edge":
            options = EdgeOptions()
        else:
            raise ValueError(f"지원하지 않는 브라우저입니다: {browser_name}")

        options.add_argument(f"--window-size={window_width},{window_height}")
        return options