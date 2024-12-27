from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base import Base, LocatorLoader
from utils import exception_handler as eh
from utils.custom_utils import *   

class TestCase09(Base):

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m4')
        self.by_type = self.get_by_type("css")
    
    def combine_locators(self, *locator_keys):
        return ' '.join(self.locators[key] for key in locator_keys)

    def execute(self):
        """온라인 가입 할인 혜택 영역에서 '혜택 모두 보기' 클릭 후 온라인 구매 혜택 항목 텍스트 정상 노출 확인"""
        try:
            # 혜택/맴버십 메뉴 클릭
            benefit_menu = find_element(self.driver, self.by_type, self.locators['benefit_menu'], f"혜택/멤버십 메뉴")
            click(self.driver, benefit_menu, f"혜택/멤버십 메뉴")
            
            # 혜택/맴버십 페이지로 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, benefit_menu, f"모바일")
            
            # middlearea 영역 중 스크롤하여 각 div 요소에 포커싱
            find_visible_sections(self.driver, self.by_type, self.locators, "모바일페이지")
            
            # PcSubMainBenefitEventSection 섹션으로 이동
            move_to_element(self.driver, self.by_type, self.locators['benefit_event_section'], f"혜택")
            
            # 혜택 모두 보기 링크 클릭
            benefit_link = find_element(self.driver, self.by_type, self.combine_locators('benefit_event_section', 'benefit_link'), f"혜택 모두 보기")
            click(self.driver, benefit_link, f"혜택 모두 보기")
            
            # 온라인 구매 혜택 페이지로 리다이렉션 확인 (by와 locator 전달)
            page_redirect_confirm(self.driver, self.by_type, benefit_link, f"온라인 구매 혜택") 

        except Exception as e:
            eh.exception_handler(self.driver, e, "온라인 구매 혜택 항목 텍스트 정상 노출 실패")
            raise


class TestCase10(Base):
   
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m4')
        self.by_type = self.get_by_type("css")

    def combine_locators(self, *locator_keys):
        return ' '.join(self.locators[key] for key in locator_keys)

    def execute(self):
        """이벤트 영역에서 '이벤트 모두 보기' 클릭 후 이벤트 페이지 URL 정상 이동 확인"""
        try:
            # 혜택/맴버십 메뉴 클릭
            benefit_menu = find_element(self.driver, self.by_type, self.locators['benefit_menu'], f"혜택/멤버십 메뉴")
            click(self.driver, benefit_menu, f"혜택/멤버십 메뉴")
            
            # 혜택/맴버십 페이지로 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, benefit_menu, f"모바일")

            # 이벤트 섹션으로 이동
            move_to_element(self.driver, self.by_type, self.locators['event_section'], f"이벤트")

            # 혜택 모두 보기 링크 클릭
            event_link = find_element(self.driver, self.by_type, self.combine_locators('event_section', 'event_link'), f"이벤트 모두 보기")
            click(self.driver, event_link, f"이벤트 모두 보기")
            
            # 진행 중 이벤트 페이지로 리다이렉션 확인 (by와 locator 전달)
            page_redirect_confirm(self.driver, self.by_type, event_link, f"진행 중 이벤트") 

        except Exception as e:
            eh.exception_handler(self.driver, e, "이벤트 페이지 URL 정상 이동 실패")
            raise
