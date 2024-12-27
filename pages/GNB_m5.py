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
            # 검색창 클릭
            move_to_element(self.driver, self.by_type, self.locators['search_input'], f"검색어 입력창")

            # 임시 함수 사용해서 해결
            click_element(self.driver, self.by_type, self.locators['clear_button'], f"검색 클리어 버튼")
            click_element(self.driver, self.by_type, self.locators['search_input'], f"검색 입력창")
            push_special_characters = self.special_characters
            enter_text(self.driver, self.by_type, self.locators['search_input'], push_special_characters, f"검색어 입력창")
            click_element(self.driver, self.by_type, self.locators['search_button'], f"검색 입력 버튼")

            # 검색 결과 확인
            input_value = get_text(self.driver, self.by_type, self.locators['r_search_input'], f"인풋 안 텍스트")
            search_result_text = get_text(self.driver, self.by_type, self.locators['search_result_text'], f"검색 결과 텍스트")
            compare_values(push_special_characters, input_value, search_result_text, f"검색어 입력값")

            # 검색 결과가 없는 경우 메시지 확인
            find_element(self.driver, self.by_type, self.locators['no_result_message'], "검색 결과 메시지")
            get_text(self.driver, self.by_type, self.locators['no_result_message'], "검색 결과 메시지")
            
        except Exception as e:
            eh.exception_handler(self.driver, e, "특수문자 검색 테스트 실패")
            raise
