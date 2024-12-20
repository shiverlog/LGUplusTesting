from selenium.webdriver.common.by import By
from utils.element_utils import find_element
from utils.custom_actionchains import move_to_element
from utils.exception_handler import handle_exception


class TestCase01:
    PAGE_URLS = {
        "MY_MENU": "ul.header-menu-list-1 > li:last-child", 
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
    MY_MENU = "ul.header-menu-list-1 > li:last-child"
    MY_INFO = "a.icon-myInfo-1.is-active, div.myInfo-list.is-show"
    
    def execute(self):
        try:
            # 마이메뉴 마우스오버 및 드롭메뉴 활성화 확인
            move_to_element(self.driver, By.CSS_SELECTOR, self.MY_MENU)
            
            # 마이메뉴 드롭메뉴 활성화 확인
            find_element(self.driver, By.CSS_SELECTOR, self.MY_INFO)
            
            # 
            
            
        except Exception as e:
            handle_exception(self.driver, e, "테스트 실패")