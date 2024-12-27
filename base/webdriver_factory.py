import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

class WebDriverFactory:
    """WebDriver 인스턴스 생성을 위한 팩토리 클래스"""
    def create_driver(self, browser_name="chrome", headless=False):
        """지정된 브라우저와 옵션으로 WebDriver 인스턴스를 생성"""
        browser_name = browser_name.lower()
        options = self.get_browser_options(browser_name)

        if headless:
            options.add_argument("--headless")

        # 브라우저 드라이버 생성
        if browser_name == "chrome":
            driver = webdriver.Chrome(options=options)
        elif browser_name == "firefox":
            driver = webdriver.Firefox(options=options)
        elif browser_name == "edge":
            driver = webdriver.Edge(options=options)
        else:
            raise ValueError(f"지원하지 않는 브라우저입니다: {browser_name}")

        # 브라우저 창을 최대화
        driver.maximize_window()

        return driver

    def get_browser_options(self, browser_name):
        # 화면 크기 가져오기 (해상도)
        # screen_width, screen_height = pyautogui.size()

        # 윈도우 사이즈 90% 계산 (필요시 사용할 수 있음)
        # window_width = int(screen_width * 0.9)
        # window_height = int(screen_height * 0.9)

        # 각 브라우저의 옵션 객체 반환
        if browser_name == "chrome":
            options = ChromeOptions()
        elif browser_name == "firefox":
            options = FirefoxOptions()
        elif browser_name == "edge":
            options = EdgeOptions()
        else:
            raise ValueError(f"지원하지 않는 브라우저입니다: {browser_name}")
        
        return options
