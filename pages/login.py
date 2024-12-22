from config.config import USERNAME, PASSWORD
from utils import element_utils as eu
from utils.page_handler import PageRedirectionHandler as ph
from utils import custom_actionchains as ca
from utils import exception_handler as eh
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from base.base import Base, LocatorLoader
import time

class TestCase01(Base):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('login')

    def execute(self):
        try:
            # 마이메뉴 마우스오버 및 드롭메뉴 활성화 확인
            myinfo = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['myinfo']))
            )
            ActionChains(self.driver).move_to_element(myinfo).perform()
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.locators['myinfo_dropdown_elements']))
            )
            
            if (self.driver.find_element(By.CSS_SELECTOR, self.locators['myinfo_active']) and 
                self.driver.find_element(By.CSS_SELECTOR, self.locators['myinfo_dropdown'])):
                self.logger.info("마이메뉴 마우스오버시 드롭메뉴 활성화 성공")
            else:
                self.logger.info("마이메뉴 드롭메뉴 활성화 실패")

            # 로그인 버튼 클릭
            login_button = self.driver.find_element(By.CSS_SELECTOR, self.locators['login_button'])
            login_button.click()
            time.sleep(1)
            # U+ID 버튼 클릭
            uplus_id_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['uplus_id_button']))
            )
            uplus_id_button.click()
            time.sleep(1)
            # 로그인 정보 입력
            self.driver.find_element(By.CSS_SELECTOR, self.locators['username_input']).send_keys(USERNAME)
            self.driver.find_element(By.CSS_SELECTOR, self.locators['password_input']).send_keys(PASSWORD)
            self.logger.info(f"입력한 ID: {USERNAME} 입력한 PW: {PASSWORD}")

            # 로그인 버튼 클릭
            self.driver.find_element(By.CSS_SELECTOR, self.locators['login_submit_button']).click()
            time.sleep(1)
            # 로그인 성공 확인
            myinfo = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['myinfo_header']))
            )
            ActionChains(self.driver).move_to_element(myinfo).pause(1).perform()
            time.sleep(1)
            login_info_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['login_info_text']))
            ).text
            self.logger.info(f"로그인 정보: {login_info_text}")

        except Exception as e:
            eh.handle_exception(self.driver, e, "로그인 테스트 실패")
            raise