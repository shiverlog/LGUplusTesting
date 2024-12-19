
import pyautogui
from selenium import webdriver

class WebDriverFactory:

    def create_driver(self, browser_name="chrome", headless=False):
        """
        지정된 브라우저와 옵션으로 WebDriver 인스턴스를 생성

        Args:
            browser_name: 브라우저 이름 (chrome, firefox, edge 등)
            headless: headless 모드 실행 여부 (True/False) 브라우저의 GUI 없이 백그라운드에서 브라우저를 실행
        Returns:
            WebDriver 인스턴스
        """
        if browser_name.lower() == "chrome":
            options = self.get_screen_size()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
        # elif browser_name.lower() == "firefox":
        #     options = webdriver.FirefoxOptions()
        #     if headless:
        #         options.add_argument("--headless")
        #     driver = webdriver.Firefox(options=options)
        # elif browser_name.lower() == "edge":
        #     options = webdriver.EdgeOptions()
        #     if headless:
        #         options.add_argument("--headless")
        #     driver = webdriver.Edge(options=options)
        else:
            raise ValueError(f"지원하지 않는 브라우저입니다: {browser_name}")
        
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars") # 정보 바의 종류를 제거

        # driver.maximize_window()
        driver = webdriver.Chrome(options=options)
        return driver
    
    def get_screen_size(self):
        screen_width, screen_height = pyautogui.size()

        # 윈도우 사이즈 90% 계산
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)

        options = webdriver.ChromeOptions()
        options.add_argument(f"--window-size={window_width},{window_height}")
        return options