from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

"""
    class PageNavigationHandler: 페이지 리다이렉션 확인
        bool: 리다이렉션 성공 여부
"""
PAGE_URLS = {
    "main   ": "/", 
    "login": "/login",
    "UPLUS": "/login/onid-login",
    "mypage": "/mypage",
    "payinfo": "/mypage/payinfo",
    "mobile": "/mobile",
    "internet-iptv": "/internet-iptv",
    "benefit": "/benefit",
    "support": "/support",
    "bill": "/mypage/bilv"
}

class PageRedirectionHandler:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger



    def page_redirection(self, expected_url_part, button_element=None, button_url_attribute=None, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(expected_url_part))
            current_url = self.driver.current_url
           
            if button_element and button_url_attribute:
                button_url = button_element.get_attribute(button_url_attribute)
                if button_url == expected_url_part and expected_url_part in current_url:
                    self.logger.info(f"페이지가 정상적으로 리다이렉션되었습니다. URL: {current_url}")
                    return True
                else:
                    self.logger.warning(f"페이지 리다이렉션에 문제가 있습니다.")
                    self.logger.warning(f"현재 URL: {current_url}")
                    self.logger.warning(f"버튼 URL: {button_url}")
                    return False
            else:
                if expected_url_part in current_url:
                    self.logger.info(f"페이지가 정상적으로 리다이렉션되었습니다. URL: {current_url}")
                    return True
                else:
                    self.logger.warning(f"페이지 리다이렉션에 문제가 있습니다.")
                    self.logger.warning(f"현재 URL: {current_url}")
                    return False
        except TimeoutException:
            self.logger.error(f"페이지가 {expected_url_part}로 리다이렉션되지 않았습니다.")
            return False