import json
import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base import Base, LocatorLoader

class TestCase09(Base):
    """온라인 가입 할인 혜택 영역에서 '혜택 모두 보기' 클릭 후 온라인 구매 혜택 항목 텍스트 정상 노출 확인"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m4')

    def execute(self):
        try:
            # 1. 혜택/맴버십 메뉴 클릭
            m4_menu_item = self.driver.find_element(By.CSS_SELECTOR, self.locators["gnb_m4_menu_item"])
            m4_menu_item.click()
            time.sleep(5)

            # 2. 혜택/맴버십 페이지로 리다이렉션 확인
            benefit_url = self.driver.current_url
            if "/benefit" in benefit_url:
                self.logger.info(f"혜택/맴버십 페이지로 이동 URL: {benefit_url}")
            else:
                self.logger.info(f"혜택/맴버십 페이지로 이동 실패 URL: {benefit_url}")

            # 3. middlearea 영역 중 스크롤하여 각 div 요소에 포커싱
            contents_section = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, self.locators["middlearea_contents_class"]))
            )
            div_elements = contents_section.find_elements(By.TAG_NAME, "div")

            div_section = [
                div for div in div_elements
                if div.get_attribute("module-index")
                and div.get_attribute("class")
                and div.get_attribute("class").startswith("bo-modules")
            ]
            div_section_count = len(div_section)
            self.logger.info(f"섹션 수: {div_section_count}")

            for div in div_section:
                location = div.get_attribute("location")
                ActionChains(self.driver).move_to_element(div).perform()
                self.logger.info(f"섹션: {location} 정보 찾기 성공")

            # 4. PcSubMainBenefitEventSection 섹션 안에 있는 event_link 찾기
            benefit_event_section = self.driver.find_element(By.CSS_SELECTOR, self.locators["benefit_event_section"])
            benefit_link = benefit_event_section.find_element(By.CSS_SELECTOR, self.locators["benefit_link"])
            actions = ActionChains(self.driver)
            actions.move_to_element(benefit_link).click().perform()
            time.sleep(5)

            # 5. 혜택 페이지 URL 확인
            current_url = self.driver.current_url
            expected_url = self.locators["benefit_page_url"]
            if current_url == expected_url:
                self.logger.info("혜택 페이지 URL로 이동하였습니다.")
            else:
                self.logger.info("혜택 페이지 URL이 일치하지 않습니다.")
            time.sleep(5)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            traceback.print_stack()


class TestCase10(Base):
    """이벤트 영역에서 '이벤트 모두 보기' 클릭 후 이벤트 페이지 URL 정상 이동 확인"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m4')

    def execute(self):
        try:
            # 1. 혜택/맴버십 메뉴 클릭
            m4_menu_item = self.driver.find_element(By.CSS_SELECTOR, self.locators["gnb_m4_menu_item"])
            m4_menu_item.click()
            time.sleep(2)

            # 2. 혜택/맴버십 페이지로 리다이렉션 확인
            benefit_url = self.driver.current_url
            if "/benefit" in benefit_url:
                self.logger.info(f"혜택/맴버십 페이지로 이동 URL: {benefit_url}")
            else:
                self.logger.info(f"혜택/맴버십 페이지로 이동 실패 URL: {benefit_url}")

            # 3. middlearea 영역 중 스크롤하여 각 div 요소에 포커싱
            contents_section = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, self.locators["middlearea_contents_class"]))
            )
            div_elements = contents_section.find_elements(By.TAG_NAME, "div")

            div_section = [
                div for div in div_elements
                if div.get_attribute("module-index")
                and div.get_attribute("class")
                and div.get_attribute("class").startswith("bo-modules")
            ]
            div_section_count = len(div_section)
            self.logger.info(f"섹션 수: {div_section_count}")

            for div in div_section:
                location = div.get_attribute("location")
                ActionChains(self.driver).move_to_element(div).perform()
                self.logger.info(f"섹션: {location} 정보 찾기 성공")

            # 4. 이벤트 섹션 안에 있는 event_link 찾기
            benefit_event_section = self.driver.find_element(By.CSS_SELECTOR, self.locators["event_section"])
            event_link = benefit_event_section.find_element(By.CSS_SELECTOR, self.locators["event_link"])
            event_link.click()
            time.sleep(2)

            # 5. 이벤트 페이지 URL 확인
            current_url = self.driver.current_url
            expected_url = self.locators["event_page_url"]
            if current_url == expected_url:
                self.logger.info("이벤트 페이지 URL로 이동하였습니다.")
            else:
                self.logger.info("이벤트 페이지 URL이 일치하지 않습니다.")
            time.sleep(5)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            traceback.print_stack()
