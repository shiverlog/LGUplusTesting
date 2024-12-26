from selenium.webdriver.common.by import By
from base.base import Base, LocatorLoader
from utils import exception_handler as eh
from utils.custom_utils import *

class TestCase02(Base):

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('main')
        self.by_type = self.get_by_type("css")
    
    """메인 페이지 KV 영역 테스트 케이스"""
    def execute(self):
        try:
            # 메인 페이지 영역 활성화 확인
            find_visible_sections(self.driver, self.by_type, self.locators, "메인페이지")

            # KV 영역 확인 - 이미지 한줄씩
            show_elements_text(self.driver, self.by_type, self.locators['kv_section_img'], "src", f"KV영역 이미지")

        except Exception as e:
            eh.exception_handler(self.driver, e, "KV 영역 테스트 실패")


class TestCase03(Base):
    
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('main')
        self.by_type = self.get_by_type("css")
        
    """기기 추천 영역 테스트 케이스"""
    def execute(self):
        try:
            # device_section으로 포커싱
            move_to_element(self.driver, self.by_type, self.locators['device_section'], f"기기추천 영역")
            
            # 랜덤 탭(링크) 선택
            select_tab, select_tab_text = select_random_item(self.driver, self.by_type, self.locators['device_section'] + " .tab-wrap ul li a", f"기기추천")
            click(self.driver, select_tab, f"기기추천 {select_tab_text}")
            
            # 선택된 탭 텍스트
            active_list = " div.recomm-tabcon[style*=\"display: block;\"] ul li a"
                    
            # 선택된 리스트 
            select_device, select_device_text = select_random_item(self.driver, self.by_type, self.locators['device_section'] + active_list, f"기기추천 {select_tab_text}")
            click(self.driver, select_device, f"기기추천 {select_tab_text} {select_device_text}")

            # 선택된 리스트 상세페이지로 이동
            page_redirect_confirm(self.driver, self.by_type, select_device, f"{select_device_text} 상세")
            
            # 상세페이지 기기명 확인
            detail_device_name  = get_text(self.driver, self.by_type, " div.device-info-area > h2.title-main", f"기기명")
            
            # 기기명 비교
            compare_values(select_device_text, detail_device_name, "기기명")

        except Exception as e:
            eh.exception_handler(self.driver, e, "기기 추천 영역 테스트 실패")
            raise

    

