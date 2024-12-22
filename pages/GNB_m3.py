import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import exception_handler as eh
from base.base import Base, LocatorLoader
from pages.login import TestCase01 as UPlusLogin

class TestCase07(Base):
    """청구내역 영역 청구월 무작위 월, 청구금액 데이터 추출 후 클릭, 페이지 이동 후 해당 월, 청구금액 일치 여부 확인"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m3')

    def execute(self):
        try:
            # 마이페이지 메뉴 클릭
            mypage_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['mypage_button']))
            )
            mypage_button.click()
            time.sleep(5)

            # 로그인 확인 및 처리
            if "/login" in self.driver.current_url:
                self.logger.info("로그인 페이지로 리다이렉션되었습니다.")
                UPlusLogin(self.driver, self.logger).login()
            else:
                self.logger.info("현재 로그인 상태입니다.")
            time.sleep(2)

            # 청구 및 납부 정보 확인
            mypage_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['mypage_list']))
            )
            billing_info = mypage_list.find_element(By.CSS_SELECTOR, self.locators['billing_info'])
            usage_period = billing_info.find_element(By.CLASS_NAME, self.locators['usage_period']).text.strip()
            usage_month = ''.join(filter(str.isdigit, billing_info.find_element(By.CLASS_NAME, self.locators['usage_month']).text.strip()))
            current_year = time.strftime("%Y")
            formatted_date = f"{current_year}-{usage_month.zfill(2)}"
            billing_amount = ''.join(filter(str.isdigit, billing_info.find_element(By.CLASS_NAME, self.locators['billing_amount']).text.strip()))

            self.logger.info(f"마이페이지내 사용기간: {usage_period}")
            self.logger.info(f"마이페이지내 사용년월: {formatted_date}")
            self.logger.info(f"마이페이지내 청구요금: {billing_amount}원")

            # 요금/납부 메뉴 클릭
            billing_header = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['billing_header']))
            )
            billing_header.click()
            time.sleep(5)

            # 요금/납부 페이지 확인
            payinfo_url = self.driver.current_url
            if "/mypage/payinfo" in payinfo_url:
                self.logger.info(f"요금/납부 메뉴로 이동 URL: {payinfo_url}")
            else:
                self.logger.info(f"요금/납부 메뉴로 이동 실패 URL: {payinfo_url}")

            # 청구내역 정보 확인
            billing_table = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['billing_table']))
            )
            billing_rows = billing_table.find_elements(By.CSS_SELECTOR, self.locators['billing_rows'])
            self.logger.info(f"보여지는 테이블 열 갯수: {len(billing_rows)}")

            first_row = self.driver.find_elements(By.CSS_SELECTOR, self.locators['first_row'])
            if first_row:
                billing_1 = first_row[0].find_element(By.CSS_SELECTOR, self.locators['billing_1']).text.strip()
                billing_2 = first_row[0].find_element(By.CSS_SELECTOR, self.locators['billing_2']).text.strip()
                billing_3 = ''.join(filter(str.isdigit, first_row[0].find_element(By.CSS_SELECTOR, self.locators['billing_3']).text.strip()))
                self.logger.info(f"요금/납부 사용년월: {billing_1}")
                self.logger.info(f"요금/납부 사용기간: {billing_2}")
                self.logger.info(f"요금/납부 청구금액: {billing_3}원")

                if formatted_date in billing_1 and billing_amount == billing_3:
                    self.logger.info(f"마이페이지 내 사용년월: {formatted_date}와 요금/납부 최근 청구월: {billing_1}으로 일치합니다.")
                    self.logger.info(f"마이페이지 내 청구요금: {billing_amount}원과 요금/납부 최근 청구금액: {billing_3}원으로 일치합니다.")
                else:
                    self.logger.info(f"데이터 불일치")
            else:
                self.logger.info("첫번째 행을 찾을 수 없습니다.")

        except Exception as e:
            eh.exception_handler(self.driver, e, "청구내역 확인 테스트 실패")
            raise

class TestCase08(Base):
    """'월별사용량조회' 탭 클릭 후 하단 '월별 사용량 상세조회' 클릭, 탭 리스트(국내통화 이용내역, 데이터 이용내역 등) 정상 노출 확인"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m3')

    def execute(self):
        try:
            # 마이페이지 메뉴 클릭
            mypage_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['mypage_button']))
            )
            mypage_button.click()
            time.sleep(5)

            # 로그인 확인 및 처리
            if "/login" in self.driver.current_url:
                self.logger.info("로그인 페이지로 리다이렉션되었습니다.")
                UPlusLogin(self.driver, self.logger).login()
            else:
                self.logger.info("현재 로그인 상태입니다.")
            time.sleep(2)

            # 마이페이지 리다이렉션 확인
            mypage_url = self.driver.current_url 
            if "/mypage" in mypage_url:
                self.logger.info(f"마이페이지로 이동 URL: {mypage_url}")
            else:
                self.logger.info(f"마이페이지로 이동 실패 URL: {mypage_url}")
            time.sleep(2)

            # 마이페이지 사이드 메뉴 정보 출력
            cards = self.driver.find_elements(By.CSS_SELECTOR, self.locators['cards'])
            tab_items = {}
            for card in cards:
                header_link = card.find_element(By.CSS_SELECTOR, self.locators['header_link'])
                tab_name = header_link.get_attribute("data-gtm-click-text")
                tab_items[tab_name] = []

                tabpanels = card.find_elements(By.CSS_SELECTOR, self.locators['tabpanels'])
                if tabpanels:
                    for tabpanel in tabpanels:
                        list_items = tabpanel.find_elements(By.CSS_SELECTOR, self.locators['list_items'])
                        for item in list_items:
                            item_text = item.get_attribute('innerText').strip()
                            tab_items[tab_name].append(item_text)

            for tab_name, items in tab_items.items():
                self.logger.info(f"{tab_name} {items}")

            # 사이드바 '가입/사용 현황' 헤더 클릭 후 아코디언 세부메뉴 '사용내역 조회' 클릭
            usage_menu = cards[1].find_element(By.CSS_SELECTOR, self.locators['usage_menu'])
            usage_menu.click()
            time.sleep(2) 

            usage_accordion = cards[1].find_element(By.CSS_SELECTOR, self.locators['usage_accordion'])
            if "collapse show" in usage_accordion.get_attribute("class"):
                self.logger.info("아코디언이 활성화 상태")
            else:
                self.logger.info("아코디언이 비활성화 상태")
            
            usage_details_li = cards[1].find_element(By.CSS_SELECTOR, self.locators['usage_details_li'])
            usage_details_li.click()
            time.sleep(10)

            # 사용내역 조회 페이지로 리다이렉션 확인
            usage_details_url = self.driver.current_url
            if "/mypage/bilv" in usage_details_url:
                self.logger.info(f"사용내역 조회 페이지로 이동 URL: {usage_details_url}")
            else:
                self.logger.info(f"사용내역 조회 페이지로 이동 실패 URL: {usage_details_url}")

            # 가입/사용 현황 탭 종류
            tab_lists = self.driver.find_elements(By.CSS_SELECTOR, self.locators['tab_lists'])
            tabs = self.driver.find_elements(By.CSS_SELECTOR, self.locators['tabs'])
            self.logger.info(f"탭 리스트 수: {len(tab_lists)}")
            for tab in tabs:
                self.logger.info(f"탭 텍스트: {tab.text}")
            
            # 탭 리스트 중 월별사용량 조회 클릭
            usage_tab = tabs[1]
            usage_tab.click()
            
            self.logger.info("월별 사용량 조회 탭 클릭 완료")
            time.sleep(2)
            detail_button = self.driver.find_element(By.CSS_SELECTOR, self.locators['detail_button'])
            detail_button.click()
            self.logger.info("월별 사용량 상세조회 클릭 완료")
            time.sleep(2)

            # 탭 리스트(국내통화 이용내역, 데이터 이용내역 등) 정상 노출 확인
            usage_details = self.driver.find_element(By.CSS_SELECTOR, self.locators['usage_details'])
            usage_detail_tabs = usage_details.find_elements(By.CSS_SELECTOR, self.locators['usage_detail_tabs'])

            for tab in usage_detail_tabs:
                tab_text = tab.find_element(By.TAG_NAME, 'a').text
                self.logger.info(f"탭 클릭: {tab_text}")
                tab.click()
                time.sleep(2)

        except Exception as e:
            eh.exception_handler(self.driver, e, "월별 사용량 조회 테스트 실패")
            raise
