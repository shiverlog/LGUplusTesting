import pyautogui
from selenium import webdriver

class WebDriverFactory:

    def create_driver(self, browser_name="chrome", headless=False):
        """
        지정된 브라우저와 옵션으로 WebDriver 인스턴스를 생성

        Args:
            browser_name: 브라우저 이름 (chrome, firefox, edge 등)
            headless: headless 모드 실행 여부 (True/False)
        Returns:
            WebDriver 인스턴스
        """
        if browser_name.lower() == "chrome":
            options = self.get_screen_size(browser_name)
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            return driver  # 바로 반환
        elif browser_name.lower() == "firefox":
            options = self.get_screen_size(browser_name)
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
            return driver  # 바로 반환
        elif browser_name.lower() == "edge":
            options = self.get_screen_size(browser_name)
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Edge(options=options)
            return driver  # 바로 반환
        else:
            raise ValueError(f"지원하지 않는 브라우저입니다: {browser_name}")

    def get_screen_size(self, browser_name="chrome"):
        screen_width, screen_height = pyautogui.size()

        # 윈도우 사이즈 90% 계산
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)

        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
        elif browser_name.lower() == "firefox":
            options = webdriver.FirefoxOptions()
        elif browser_name.lower() == "edge":
            options = webdriver.EdgeOptions()
        else:
            raise ValueError(f"지원하지 않는 브라우저입니다: {browser_name}")

        options.add_argument(f"--window-size={window_width},{window_height}")
        return options