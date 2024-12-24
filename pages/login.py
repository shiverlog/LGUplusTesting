from config.config import USERNAME, PASSWORD
from utils import exception_handler as eh
from selenium.webdriver.common.by import By
from base.base import Base, LocatorLoader
from utils.element_utils import *
from utils.custom_actionchains import *
from utils.page_handler import verify_redirection
import time

class TestCase01(Base):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('login')

    def execute(self):
        """로그인 버튼을 직접 클릭하여 로그인 수행"""
        try:
            # 마이메뉴 아이콘 찾기
            myinfo = find_element(self.driver, (By.CSS_SELECTOR, self.locators['myinfo']), f"마이메뉴 아이콘")
            if myinfo:
                # 마이메뉴 마우스오버
                move_to_element(self.driver, myinfo, f"마이메뉴 아이콘")

                # 마이메뉴 드롭메뉴 활성화 확인
                dropdown_elements = find_elements(self.driver, (By.CSS_SELECTOR, self.locators['myinfo_active']), f"마이메뉴 활성화 조건")
                if dropdown_elements:
                    self.logger.info("마이메뉴 마우스오버시 드롭메뉴 활성화 성공")

                    # 마이메뉴 안의 로그인 버튼 클릭
                    login_button = find_element(self.driver, (By.CSS_SELECTOR, self.locators['login_button']), f"메인로그인 버튼")
                    click(self.driver, login_button, f"메인로그인 버튼")

            # 리다이렉션 확인
            verify_redirection(self.driver, login_button, f"로그인")

            # U+ID 버튼 찾기 및 클릭
            uplus_login_button = find_clickable_element(self.driver, (By.CSS_SELECTOR, self.locators['uplus_login_button']), f"U+ID 버튼")
            if uplus_login_button:
                click(self.driver, uplus_login_button, f"U+ID 버튼")

                verify_redirection(self.driver, uplus_login_button, f"U+ID 로그인")

            self._perform_login()

        except Exception as e:
            eh.exception_handler(self.driver, e, "로그인 테스트 실패")
            raise

    def login_from_redirect(self):
        """리다이렉션된 로그인 페이지에서 로그인 수행"""
        try:
            # U+ID 버튼 찾기 및 클릭
            uplus_login_button = find_clickable_element(self.driver, (By.CSS_SELECTOR, self.locators['uplus_login_button']), f"U+ID로그인 버튼")
            if uplus_login_button:
                click(self.driver, uplus_login_button, f"U+ID 버튼")

                verify_redirection(self.driver, uplus_login_button, f"U+ID 로그인")

            self._perform_login()

        except Exception as e:
            eh.exception_handler(self.driver, e, "리다이렉션 페이지 로그인 실패")
            raise

    def _perform_login(self):
        try:
            login_form = find_element(self.driver, (By.CSS_SELECTOR, self.locators['login_form']), f"로그인 폼")
            if login_form:

                # 로그인 정보 입력
                enter_text(self.driver, (By.CSS_SELECTOR, self.locators['username_input']), USERNAME, f"아이디 입력창")
                enter_text(self.driver, (By.CSS_SELECTOR, self.locators['password_input']), PASSWORD, f"비밀번호 입력창")

                # 로그인 버튼 클릭
                submit_button = find_element(self.driver, (By.CSS_SELECTOR, self.locators['login_submit_button']), f"U+ID로그인 버튼")
                click(self.driver, submit_button, f"U+ID로그인 버튼")
                verify_redirection(self.driver, submit_button, f"메인")

                # 마이메뉴 마우스오버
                myinfo = find_element(self.driver, (By.CSS_SELECTOR, self.locators['myinfo']), f"마이메뉴 아이콘")
                if myinfo:
                    move_to_element(self.driver, myinfo, f"마이메뉴 아이콘")
                    get_text(self.driver, (By.CSS_SELECTOR, ".login-info-txt"), f"마이메뉴 정보 텍스트")
                time.sleep(2)

        except Exception as e:
            eh.exception_handler(self.driver, e, "로그인 테스트 실패")
            raise