from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from base.base import Base, LocatorLoader
from utils import exception_handler as eh
from utils.custom_utils import *
import random, string, time

class TestCase11(Base):
    
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m5')
        self.by_type = self.get_by_type("css")

    def execute(self):
        """자주 찾는 검색어 항목 텍스트 비교 및 검색 테스트"""
        try:
            # 고객지원 메뉴 찾고 클릭
            support_menu = find_element(self.driver, self.by_type, self.locators['support_menu'], "고객지원")
            click(self.driver, support_menu, f"고객지원 메뉴")
            
            # 고객지원 페이지로 이동 확인
            page_redirect_confirm(self.driver, self.by_type, support_menu, f"고객지원")

            # 고객지원 섹션 포커싱
            move_to_element(self.driver, self.by_type, self.locators['search_section'], f"검색어 입력창")
            
            # 자주 찾는 검색어 목록 확인 및 랜덤 선택
            select_keword, select_keword_text = select_random_item(self.driver, self.by_type, self.locators['search_keyword'], "text", f"자주 찾는 검색어")
            enter_text(self.driver, self.by_type, self.locators['search_input'], select_keword_text, f"검색어 입력창")
            # click(self.driver, select_keword, f"검색 버튼")
            clickable_link_click(self.driver, self.by_type, self.locators['search_button'], f"검색 버튼")
            
            # 검색 결과 확인
            # input_value = find_element(self.driver, self.by_type, self.locators['search_input']).get_attribute('value')
            
            input_value = get_text(self.driver, self.by_type, self.locators['r_search_input'], f"인풋 안 텍스트")
            search_result_text = get_text(self.driver, self.by_type, self.locators['search_result_text'], f"검색 결과 텍스트")
            compare_values(select_keword_text, input_value, search_result_text, f"검색어 입력값")
   
        except Exception as e:
            eh.exception_handler(self.driver, e, "검색어 테스트 실패")
            raise

class TestCase12(Base):
   
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m5')
        self.special_characters = ''.join(random.choice(string.punctuation) for _ in range(10))
        self.by_type = self.get_by_type("css")

    def execute(self):
        """특수문자 검색 테스트"""
        try:
            # 검색창 클리어 버튼 클릭
            search_input = find_element(self.driver, self.by_type, self.locators['search_input'], f"검색어 입력창")
            release(self.driver, search_input, f"검색어 입력창")

            clickable_link_click(self.driver, self.by_type, self.locators['clear_button'], f"검색어 클리어")

            # 검색어 입력창, 검색 버튼 확인
            clear_button = find_element(self.driver, self.by_type, self.locators['clear_button'], f"검색어 클리어 버튼")
            search_input = find_element(self.driver, self.by_type, self.locators['search_input'], f"검색어 입력창")
            search_button = find_element(self.driver, self.by_type, self.locators['search_button'], f"검색 버튼")
            time.sleep(5)
            clear_button.click()
            custom_logger.info("검색어 클리어 버튼 클릭")
            # 검색창 클릭
            clickable_link_click(self.driver, self.by_type, self.locators['search_input'], f"검색어 입력창")

            # 특수문자 입력 및 검색
            input_special_text = enter_text(self.driver, self.by_type, self.locators['search_input'], self.special_characters, f"검색어 입력창")

            # 검색 버튼 클릭
            clickable_link_click(self.driver, self.by_type, self.locators['search_button'], f"검색 버튼")
            
            # 검색 결과 확인
            input_value = get_text(self.driver, self.by_type, self.locators['r_search_input'], f"인풋 안 텍스트")
            search_result_text = get_text(self.driver, self.by_type, self.locators['search_result_text'], f"검색 결과 텍스트")
            compare_values(input_special_text, input_value, search_result_text, f"검색어 입력값")

            # 검색 결과가 없는 경우 메시지 확인
            find_element(self.driver, self.by_type, self.locators['no_result_message'], "검색 결과 메시지")
            get_text(self.driver, self.by_type, self.locators['no_result_message'], "검색 결과 메시지")
            clear_button = find_element(self.driver, (By.CSS_SELECTOR, self.locators['clear_button']))


#             # 특수문자 입력 및 검색
#             move_to_element(self.driver, search_input)
#             click(self.driver, search_input)
#             send_keys_to_element(self.driver, search_input, self.special_characters)
#             time.sleep(5)
#             click(self.driver, search_button)
#             time.sleep(5)
#             # # ActionChains(self.driver).move_to_element(search_input).click().perform()
#             # search_input.send_keys(self.special_characters)
#             # # search_input.send_keys(Keys.ENTER)
#             # time.sleep(5)
#             # click(self.driver, search_button)


#             # 검색 결과 확인
#             input_value = self.driver.find_element(By.CSS_SELECTOR, self.locators['search_input']).get_attribute('value')
#             faq_url = self.driver.current_url
            
#             if input_value == self.special_characters:
#                 self.logger.info(f"검색어 '{self.special_characters}'이(가) 입력되었습니다. URL: {faq_url}")
#             else:
#                 self.logger.warning(f"검색어 입력 실패")

#             try:
#                 no_data_element = self.driver.find_element(By.CSS_SELECTOR, self.locators['no_result_message'])
#                 if no_data_element.text == "검색 결과가 존재하지 않습니다.":
#                     self.logger.info("'검색 결과가 존재하지 않습니다.' 메시지가 확인되었습니다.")
#                 else:
#                     self.logger.info(f"검색 결과: {no_data_element.text}")
#             except NoSuchElementException:
#                 self.logger.info("'검색 결과가 존재하지 않습니다.' 메시지를 찾을 수 없습니다.")

#         except Exception as e:
#             eh.exception_handler(self.driver, e, "특수문자 검색 테스트 실패")
#             raise
        except Exception as e:
            eh.exception_handler(self.driver, e, "특수문자 검색 테스트 실패")
            raise
