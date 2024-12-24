from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from base.base import Base, LocatorLoader
from utils import exception_handler as eh
from utils.element_utils import *
from utils.custom_actionchains import *
from utils.custom_utils import *
import time
import random

class TestCase02(Base):
    """메인 페이지 KV 영역 테스트 케이스"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('main')

    def execute(self):
        try:
            # 메인 페이지 영역 활성화 확인
            find_visible_sections(self.driver, self.locators, "메인페이지")

            # KV 영역 확인 - 이미지 한줄씩
            show_elements_text(self.driver, (By.CSS_SELECTOR, self.locators['kv_section_img']), f"KV영역 이미지")

        except Exception as e:
            eh.exception_handler(self.driver, e, "KV 영역 테스트 실패")

class TestCase03(Base):
    """기기 추천 영역 테스트 케이스"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('main')
        # (By.CSS_SELECTOR, self.locators['key_name']) 튜플형식으로 locators로 넘김
    
    def get_locator(self, section, sub_locator=""):
        """ section에 맞는 기본 locator와 하위 요소를 동적으로 생성 """
        return (By.CSS_SELECTOR, self.locators[section] + sub_locator)

    def execute(self):
        try:
            device_locator = (By.CSS_SELECTOR, self.locators['device_section'])
            device_section = find_visible_element(self.driver, device_locator, f"기기 추천 영역")
            move_to_element(self.driver, device_section, f"기기 추천 영역")
            
            custom_logger.info(f"기기 추천 영역: {self.locators['device_section']}")
            device_tabs = find_elements(self.driver, (By.CSS_SELECTOR, self.locators['device_section'] + " .tab-wrap ul li"), f"기기 추천 탭")
            






            tabs = find_visible_element(device_section, (By.CSS_SELECTOR, self.locators['device_section']), f"기기 추천 영역")
            tabs = device_section.find_elements(By.CSS_SELECTOR, ".tab-wrap ul li")
            device_section.find_element(self.driver, (By.CSS_SELECTOR, ".tab-wrap ul li "), f"기기 추천 탭")
            
            # 랜덤 탭 선택
            tabs = self.driver.find_elements(By.CSS_SELECTOR, '.tab-wrap ul li')
            self.random_tab = random.choice(tabs)
            self.random_tab_text = self.random_tab.text
            self.random_tab.click()

            # 선택된 탭 확인
            active_tab = self.driver.find_element(By.CSS_SELECTOR, '.tab-wrap ul li.active a')
            self.logger.info(f"선택한 탭: {self.random_tab_text}")
            self.logger.info(f"활성화된 탭: {active_tab.text}")

            # 탭 ID 설정
            expected_id = {
                "추천": "recomm-tabcon-01",
                "삼성": "recomm-tabcon-02",
                "Apple": "recomm-tabcon-03"
            }.get(next((key for key in ["추천", "삼성", "Apple"] if key in self.random_tab_text), None))

            if expected_id:
                # 기기 목록 가져오기
                self.device_list = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'#{expected_id} ul.recomm-device-list li'))
                )
                self.logger.info(f"{self.random_tab_text} 탭의 기기 개수: {len(self.device_list)}")

                # 기기 정보 출력
                for index, device in enumerate(self.device_list):
                    device_thumbnail = device.find_element(By.CSS_SELECTOR, '.device-thumnail img').get_attribute('src')
                    device_information = device.find_element(By.CSS_SELECTOR, '.device-infomation p.device-name').text
                    self.logger.info(f"기기 {index + 1}: {device_information} 썸네일: {device_thumbnail}")

                # 랜덤 기기 선택
                self.random_device = random.choice(self.device_list)
                self.device_name = self.random_device.find_element(By.CSS_SELECTOR, '.device-name').text
                self.device_url = self.random_device.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                self.random_device.click()
                self.logger.info(f"선택된 기기: {self.device_name}")
                self.logger.info(f"기기 상세 페이지 링크: {self.device_url}")

                # 상세 페이지 이동 확인
                if "/mobile/device" in self.device_url:
                    self.logger.info(f"디바이스 상세 페이지로 이동 URL: {self.device_url}")
                
                    # 상세 페이지 로딩 대기
                    WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.device-info-area'))
                    )
                    time.sleep(10)
                    # 기기명 비교
                    device_detail_name = self.driver.find_element(By.CSS_SELECTOR, 'div.device-info-area > h2.title-main').get_attribute('textContent')
                    self.logger.info(f"상세 페이지 기기명: {device_detail_name}")
                
                    if self.device_name in device_detail_name:
                        self.logger.info(f"기기명이 일치합니다: {device_detail_name}")
                    else:
                        self.logger.info(f"기기명이 일치하지 않습니다. 선택된 기기: {self.device_name}, 상세 페이지 기기: {device_detail_name}")
            else:
                self.logger.info(f"탭 텍스트에 해당하는 클래스가 없습니다: {self.random_tab_text}")

        except Exception as e:
            eh.exception_handler(self.driver, e, "기기 추천 영역 테스트 실패")
            raise

    

