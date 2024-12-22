import random
import string
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from base.base import Base, LocatorLoader
from utils import exception_handler as eh

class TestCase11(Base):
    """자주 찾는 검색어 항목 텍스트 비교 및 검색 테스트"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m5')

    def execute(self):
        try:
            # 고객지원 메뉴 클릭
            support = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, self.locators['support_menu']))
            )
            self.support_url = support.get_attribute("data-gtm-click-url")
            support.click()
            time.sleep(2)

            if "support" in self.support_url:
                self.logger.info(f"고객지원 페이지로 이동 URL: {self.support_url}")
            else:
                self.logger.info(f"고객지원 페이지로 이동 실패 URL: {self.support_url}")

            # 자주 찾는 검색어 목록 확인
            search_keyword_div = self.driver.find_element(By.CLASS_NAME, self.locators['keyword_container'])
            keywords = search_keyword_div.find_elements(By.TAG_NAME, "a")
            self.keyword_list = [keyword.text for keyword in keywords]
            self.logger.info(self.keyword_list)
            self.keyword_random = random.choice(self.keyword_list)

            # 검색어 입력 및 검색
            search_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['search_section'])
            search_input = search_section.find_element(By.CSS_SELECTOR, self.locators['search_input'])
            search_button = search_section.find_element(By.CSS_SELECTOR, self.locators['search_button'])
            
            search_input.send_keys(self.keyword_random)
            search_button.click()
            time.sleep(2)

            # 검색 결과 확인
            input_value = self.driver.execute_script("return document.querySelector('input.c-inp').value;")
            faq_url = self.driver.current_url
            
            if input_value == self.keyword_random:
                self.logger.info(f"검색어 '{self.keyword_random}'이(가) 입력되었습니다. URL: {faq_url}")
            else:
                self.logger.warning(f"검색어 입력 실패")

            search_input_value = self.driver.find_element(By.ID, self.locators['search_input_id']).get_attribute("value")
            element = self.driver.find_element(By.XPATH, self.locators['search_result_text'])
            span_text = element.get_attribute('innerHTML').strip()
            
            self.logger.info(f"입력값: {search_input_value} 검색결과: {span_text}")
            
            if self.keyword_random == search_input_value == span_text:
                self.logger.info(f"데이터가 일치합니다: {span_text}")
            else:
                self.logger.info(f"데이터가 불일치합니다")

        except Exception as e:
            eh.handle_exception(self.driver, e, "검색어 테스트 실패")
            raise

class TestCase12(Base):
    """특수문자 검색 테스트"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m5')
        self.special_characters = ''.join(random.choice(string.punctuation) for _ in range(10))

    def execute(self):
        try:
            # 검색창 초기화
            search_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['search_section'])
            clear_button = search_section.find_element(By.CSS_SELECTOR, self.locators['clear_button'])
            search_input = search_section.find_element(By.CSS_SELECTOR, self.locators['search_input'])
            search_button = search_section.find_element(By.CSS_SELECTOR, self.locators['search_button'])
            
            clear_button.click()

            # 특수문자 입력 및 검색
            ActionChains(self.driver).move_to_element(search_input).click().perform()
            search_input.send_keys(self.special_characters)
            search_input.send_keys(Keys.ENTER)
            search_button.click()
            time.sleep(5)

            # 검색 결과 확인
            input_value = self.driver.find_element(By.CSS_SELECTOR, self.locators['search_input']).get_attribute('value')
            faq_url = self.driver.current_url
            
            if input_value == self.special_characters:
                self.logger.info(f"검색어 '{self.special_characters}'이(가) 입력되었습니다. URL: {faq_url}")
            else:
                self.logger.warning(f"검색어 입력 실패")

            try:
                no_data_element = self.driver.find_element(By.CSS_SELECTOR, self.locators['no_result_message'])
                if no_data_element.text == "검색 결과가 존재하지 않습니다.":
                    self.logger.info("'검색 결과가 존재하지 않습니다.' 메시지가 확인되었습니다.")
                else:
                    self.logger.info(f"검색 결과: {no_data_element.text}")
            except NoSuchElementException:
                self.logger.info("'검색 결과가 존재하지 않습니다.' 메시지를 찾을 수 없습니다.")

        except Exception as e:
            eh.handle_exception(self.driver, e, "특수문자 검색 테스트 실패")
            raise
