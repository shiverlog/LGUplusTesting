from selenium.webdriver.common.by import By
from base.base import Base, LocatorLoader
from config.config import USERNAME, PASSWORD
from utils import exception_handler as eh
from utils.custom_utils import *

class TestCase01(Base):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('login')
        self.by_type = self.get_by_type("css")

    def execute(self):
        """로그인 버튼을 직접 클릭하여 로그인 수행"""
        try:
            # 마이메뉴 아이콘 찾고 마우스오버
            move_to_element(self.driver, self.by_type, self.locators['myinfo'], f"마이메뉴 아이콘")
            
            # 마이메뉴 드롭메뉴 활성화 확인
            find_elements(self.driver, self.by_type, self.locators['myinfo_active'], f"마이메뉴 활성화")
           
            # 마이메뉴 안의 로그인 버튼 클릭
            clickable_link_click(self.driver, self.by_type, self.locators['login_button'], f"메인로그인 버튼")

            # 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, self.locators['login_button'], f"로그인")

            # U+ID 버튼 찾기 및 클릭
            clickable_link_click(self.driver, self.by_type, self.locators['uplus_login_button'], f"U+ID 버튼")
            
            # 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, self.locators['uplus_login_button'], f"U+ID 로그인")

            self._perform_login()

        except Exception as e:
            eh.exception_handler(self.driver, e, "로그인 테스트 실패")
            raise


    def login_from_redirect(self):
        """리다이렉션된 로그인 페이지에서 로그인 수행"""
        try:
            # U+ID 버튼 찾기 및 클릭
            clickable_link_click(self.driver, self.by_type, self.locators['uplus_login_button'], f"U+ID 버튼")
            
            # 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, self.locators['uplus_login_button'], f"U+ID 로그인")

            self._perform_login()

        except Exception as e:
            eh.exception_handler(self.driver, e, "리다이렉션 페이지 로그인 실패")
            raise


    def _perform_login(self):
        try:
            # 로그인 폼 찾기
            find_element(self.driver, self.by_type, self.locators['login_form'], f"로그인 폼")
            
            # 로그인 정보 입력
            enter_text(self.driver, self.by_type, self.locators['username_input'], USERNAME, f"아이디 입력창")
            enter_text(self.driver, self.by_type, self.locators['password_input'], PASSWORD, f"비밀번호 입력창")

            # 로그인 버튼 클릭
            clickable_link_click(self.driver, self.by_type, self.locators['login_submit_button'], f"U+ID로그인 버튼")

            # 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, self.locators['login_submit_button'], f"U+ID로그인")

            # 마이메뉴 마우스오버
            move_to_element(self.driver, self.by_type, self.locators['myinfo'], f"마이메뉴 아이콘")
            get_text(self.driver, self.by_type, " .login-info-txt", f"마이메뉴 정보 텍스트")

        except Exception as e:
            eh.exception_handler(self.driver, e, "로그인 테스트 실패")
            raise