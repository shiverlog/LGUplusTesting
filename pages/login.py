from config.config import USERNAME, PASSWORD
from utils import exception_handler as eh
from selenium.webdriver.common.by import By
from base.base import Base, LocatorLoader
from utils.element_utils import *
from utils.custom_actionchains import *

class TestCase01(Base):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('login')

    def login_from_main(self):
        try:
            # 마이메뉴 아이콘 찾기
            myinfo = find_element(self.driver, (By.CSS_SELECTOR, self.locators['myinfo']))
            if myinfo:
                # 마이메뉴 마우스오버
                move_to_element(self.driver, myinfo)

                # 마이메뉴 드롭메뉴 활성화 확인
                dropdown_elements = find_elements(self.driver, (By.CSS_SELECTOR, self.locators['myinfo_dropdown_elements']))
                if dropdown_elements:
                    if find_element(self.driver, (By.CSS_SELECTOR, self.locators['myinfo_active'])):
                        self.logger.info("마이메뉴 마우스오버시 드롭메뉴 활성화 성공")
                    else:
                        self.logger.info("마이메뉴 드롭메뉴 활성화 실패")

            # 로그인 버튼 클릭
            click(self.driver, find_element(self.driver, (By.CSS_SELECTOR, self.locators['login_button'])))
            
            # 로그인 페이지 이동 확인
            # login_a_url = get_attribute(self.driver, (By.CSS_SELECTOR, self.locators['login_button']), "data-gtm-click-url")
            # current_url = self.driver.current_url
            # if login_a_url in current_url:
            #     self.logger.info(f"로그인 페이지로 이동 URL: {current_url}")
            # else:
            #     self.logger.error(f"로그인 페이지로 이동 실패 URL: {current_url}")

            self._perform_login()

        except Exception as e:
            eh.exception_handler(self.driver, e, "로그인 테스트 실패")
            raise
    
    def login_from_redirect(self):
        """리다이렉션된 로그인 페이지에서 로그인 수행"""
        try:
            # U+ID 버튼 찾기 및 클릭
            uplus_login_button = find_clickable_element(self.driver, (By.CSS_SELECTOR, self.locators['uplus_id_button']))
            if uplus_login_button:
                click(self.driver, uplus_login_button)
                
            self._perform_login()
            
        except Exception as e:
            eh.exception_handler(self.driver, e, "리다이렉션 페이지 로그인 실패")
            raise

    def _perform_login(self):
        try:
            # U+ID 버튼 클릭
            uplus_login_button = find_clickable_element(self.driver, (By.CSS_SELECTOR, self.locators['uplus_id_button']))
            if uplus_login_button:
                click(self.driver, uplus_login_button)

            # 로그인 정보 입력
            enter_text(self.driver, (By.CSS_SELECTOR, self.locators['username_input']), USERNAME)
            enter_text(self.driver, (By.CSS_SELECTOR, self.locators['password_input']), PASSWORD)

            # 로그인 버튼 클릭
            click(self.driver, find_element(self.driver, (By.CSS_SELECTOR, self.locators['login_submit_button'])))

            # 로그인 성공 확인
            # 마이메뉴 마우스오버
            myinfo = find_element(self.driver, (By.CSS_SELECTOR, self.locators['myinfo']))
            if myinfo:
                move_to_element(self.driver, myinfo)
                login_info_text = find_element(self.driver, (By.CSS_SELECTOR, ".login-info-txt")).get_attribute('textContent')
                if login_info_text:
                    self.logger.info(f"로그인 정보: {login_info_text}")
                else:
                    self.logger.error("로그인 정보 텍스트 가져오기 실패")
        
        except Exception as e:
            eh.exception_handler(self.driver, e, "로그인 프로세스 실패")
            raise