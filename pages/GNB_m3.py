import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import exception_handler as eh
from base.base import Base, LocatorLoader
from pages.login import TestCase01 as UPlusLogin
from utils.custom_utils import *

class TestCase07(Base):
    
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m3')
        self.by_type = self.get_by_type("css")

    def combine_locators(self, *locator_keys):
        return ' '.join(self.locators[key] for key in locator_keys)
    
    def execute(self):
        """청구내역 영역 청구월 무작위 월, 청구금액 데이터 추출 후 클릭, 페이지 이동 후 해당 월, 청구금액 일치 여부 확인"""
        try:
            # 마이페이지 메뉴 클릭
            mypage_menu = find_element(self.driver, self.by_type, self.locators['mypage_menu'], f"마이페이지 메뉴")
            click(self.driver, mypage_menu, f"마이페이지 메뉴")

            # 로그인 화면으로 리다이렉션 확인 시 
            page_redirect_confirm(self.driver, self.by_type, mypage_menu, f"마이페이지")

            # 로그인 확인 및 처리
            if "/login" in self.driver.current_url:
                custom_logger.info("로그인 페이지로 리다이렉션 되었습니다.")

                # 로그인 실행
                UPlusLogin(self.driver, self.logger).login_from_redirect()

                # 로그인 후 마이페이지 리다이렉션 확인
            else:
                custom_logger.info("현재 로그인 상태입니다.")

            # 청구 및 납부 정보 확인
            move_to_element(self.driver, self.by_type, self.locators['billing_info_section'], f"청구 및 납부 정보 섹션")
            
            # 청구 및 납부 정보 섹션 내 [사용기간, 사용년월, 청구요금] 확인
            before_values = show_elements_list(self.driver, self.by_type, self.locators['billing_info_section'] + " ul.my-payment-section li","text", f"청구 및 납부 정보")
            
            # 요금/납부 메뉴 클릭
            clickable_link_click(self.driver, self.by_type, self.locators['billing_menu'], f"요금/납부 메뉴")
        
            # 요금/납부 페이지 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, self.locators['billing_menu'], f"요금/납부 페이지")

            # 가장 최근 청구월, 청구금액 데이터 추출
            after_values = show_elements_list(self.driver, self.by_type, self.combine_locators('billing_table','first_billing_row'), "text", f"청구내역 테이블")
        
            # 청구 및 납부 정보 섹션 내 [사용기간, 사용년월, 청구요금]과 청구내역 테이블의 가장 최근 청구월, 청구금액 일치 여부 확인
            results = compare_billing_data(before_values, after_values)
            for result in results:
                print(result)

        except Exception as e:
            eh.exception_handler(self.driver, e, "청구내역 확인 테스트 실패")
            raise

class TestCase08(Base):

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m3')
        self.by_type = self.get_by_type("css")

    def combine_locators(self, *locator_keys):
        return ' '.join(self.locators[key] for key in locator_keys)

    def execute(self):
        """'월별사용량조회' 탭 클릭 후 하단 '월별 사용량 상세조회' 클릭, 탭 리스트(국내통화 이용내역, 데이터 이용내역 등) 정상 노출 확인"""
        try:
           # 마이페이지 메뉴 클릭
            mypage_menu = find_element(self.driver, self.by_type, self.locators['mypage_menu'], f"마이페이지 메뉴")
            click(self.driver, mypage_menu, f"마이페이지 메뉴")

            # 로그인 화면으로 리다이렉션 확인 시 
            page_redirect_confirm(self.driver, self.by_type, mypage_menu, f"마이페이지")

            # 로그인 확인 및 처리
            if "/login" in self.driver.current_url:
                custom_logger.info("로그인 페이지로 리다이렉션 되었습니다.")

                # 로그인 실행
                UPlusLogin(self.driver, self.logger).login_from_redirect()

                # 로그인 후 마이페이지 리다이렉션 확인
                # page_redirect_confirm(self.driver, self.by_type, mypage_menu, "마이페이지")
            else:
                custom_logger.info("현재 로그인 상태입니다.")

            # 마이페이지 가입/사용 현황 클릭
            side_title_menu = find_elements(self.driver, self.by_type, self.locators['side_title_menu'], f"가입/사용 현황")
            click(self.driver, side_title_menu[1], f"가입/사용 현황")

            # 가입/사용 현황 탭 아코디언 활성화 상태 확인
            check_active(self.driver, side_title_menu[1], f"가입/사용 현황")

            # 사용내역 조회 클릭
            sibling_element = side_title_menu[1].find_element(By.XPATH, "following-sibling::*[1]")
            fourth_li_a = sibling_element.find_element(By.XPATH, ".//div/ul/li[4]/a")
            click(self.driver, fourth_li_a, f"사용내역 조회")

            # 사용내역 조회 페이지 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, fourth_li_a, f"사용내역 조회")

            # 가입/사용 현황 탭 종류
            show_elements_list(self.driver, self.by_type, self.locators['tab_list'],"text", f"사용내역 조회 탭")
            tab_list = find_elements(self.driver, self.by_type, self.locators['tab_list'], f"사용내역 조회 탭")
            click(self.driver, tab_list[1], f"월별사용량조회")

            # 월별 사용량 상세조회 클릭
            move_to_element(self.driver, self.by_type, self.locators['usage_details_button'], f"월별 사용량 상세조회")
            click_element(self.driver, self.by_type, self.locators['usage_details_button'], f"월별 사용량 상세조회")
            
            # 월별 사용량 상세조회 안 탭 리스트(국내통화 이용내역, 데이터 이용내역 등) 정상 노출 확인
            move_to_element(self.driver, self.by_type, self.locators['usage_detail_tabs'], f"월별 사용량 상세조회 탭")
            show_elements_list(self.driver, self.by_type, self.locators['usage_detail_tabs'], "text", f"월별 사용량 상세조회 탭")

            click_all_items(self.driver, self.by_type, self.locators['usage_detail_tabs'], "text", f"월별 사용량 상세조회 탭")

        except Exception as e:
            eh.exception_handler(self.driver, e, "월별 사용량 조회 테스트 실패")
            raise
