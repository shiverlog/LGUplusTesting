from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import os
import traceback
from selenium.webdriver.support import expected_conditions as EC

class UPlusLogin:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def login(self):
        try:
            # 1. "U+ID" 버튼 클릭
            uplus_id_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'section.new-mem-section ul.iconLoginList li:nth-of-type(4) button'))
            )
            uplus_id_button.click()
            time.sleep(2)

            # 2. 버튼 클릭 후 /login/onid-login 페이지로 리다이렉션 확인
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/login/onid-login")
            )
            Uplus_login_url = self.driver.current_url

            # /login/onid-login 해당 url로 이동하는지 확인
            if "/login/onid-login" in Uplus_login_url:
                self.logger.info(f"U+ 로그인 페이지로 이동 URL: {Uplus_login_url}")
            else:
                self.logger.info(f"U+ 로그인 페이지로 이동 실패 URL: {Uplus_login_url}")

            # 3. ID 및 비밀번호 입력 (sysdm.cpl 환경변수 사용)
            uplus_id = os.getenv('UPLUS_ID')
            uplus_pw = os.getenv('UPLUS_PW')

            id_input = self.driver.find_element(By.ID, "username-1-6")
            id_input.send_keys(uplus_id)
            pw_input = self.driver.find_element(By.ID, "password-1")
            pw_input.send_keys(uplus_pw)
            time.sleep(5)

            # 4. U+ID 로그인 버튼 클릭
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button.c-btn-solid-1.nm-login-btn')
            login_button.click()
            time.sleep(2)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            self.logger.error(traceback.format_exc())
            traceback.print_stack()