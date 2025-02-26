import random

from base.webdriver import WebDriver
import common.json.variable as var
from common.function import Function
from common.debug import Debug


class InternetIptvPage():
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)
    def iptv(self):
        self.FC.gotoHome()
        try :
            self.FC.movepage(self.FC.var['iptv_el']['iptv'],address=self.FC.var['iptv_el']['iptv_url'])
            self.FC.modal_ck4()

            # KVRTB 영역
            KVRTB_list=self.FC.loading_find_csss(self.FC.var['iptv_el']['KVRTB'])
            self.FC.move_to_element(KVRTB_list[0])
            assert len(KVRTB_list) >= 4,self.DBG.logger.debug("인터넷/IPTV > 서브메인 > KVRTB 콘텐츠 정상 노출 실패")

            # 서브메인 테마배너 IPTV
            check_text_list=['맞춤상품찾기','인터넷','IPTV','스마트홈','가입 사은품']
            assert self.FC.text_list_in_element(self.FC.var['mobile_el']['테마배너'],check_text_list),self.DBG.logger.debug("모바일 > 서브메인 > 테마베너 정상 출력 실패")
            theme_list_link=self.FC.loading_find_csss(self.FC.var['mobile_el']['테마배너_링크'])
            random_num= random.randrange(0,len(theme_list_link))
            check_link=theme_list_link[random_num].get_attribute('href')
            check_link=check_link[check_link.rfind('/'):]
            tab_name= theme_list_link[random_num].get_attribute('data-gtm-click-text')
            self.FC.move_to_element(self.FC.loading_find_css_pre(self.FC.var['common_el']['KV']))
            self.FC.scroll(1,False)
            self.FC.wait_loading()
            theme_list_link[random_num].click()
            self.FC.wait_loading()
            assert check_link in self.FC.driver.current_url,self.DBG.logger.debug("모바일 > 서브메인 > 테마베너 > %s탭 정상 동작 실패", tab_name)
            self.FC.goto_url(self.FC.var['iptv_el']['iptv_url'])

            # 혜택(다양한 혜택) 영역 콘텐츠 출력 및 링크 정상 이동
            self.FC.con_check(var.mobile_el,'혜택_list','인터넷/IPTV')

            # 유플러스닷컴만의 다양한 혜택을 받고 가입하세요 영역
            iptv_benefit_list=self.FC.loading_find_csss(self.FC.var['iptv_el']['유플러스혜택받고_가입_이벤트영역'])
            self.FC.move_to_element(iptv_benefit_list[0])
            assert len(iptv_benefit_list) >= 4,self.DBG.logger.debug("인터넷/IPTV > 유플러스닷컴만의 다양한 혜택 받고 가입하세요 이벤트영역")

            # 인터넷+IPTV 추천 결합 상품 영역 콘텐츠 출력 및 링크 이동 확인
            carousel=self.FC.loading_find_css_pre(self.FC.var['iptv_el']['결합상품_영역'])
            self.FC.move_to_element(carousel)

            # 무작위로 임의 결합 상품 선택
            iptv_item_list=self.FC.loading_find_csss(self.FC.var['iptv_el']['결합 상품_list'])
            assert 3 <= len(iptv_item_list),self.DBG.logger.debug("인터넷/IPTV > 서브메인 > 인터넷+IPTV 추천 결합 상품 영역 콘텐츠 정상 출력 실패")
            random_num = random.randrange(len(iptv_item_list))   #임의 상품

            # 온라인 가입 이동 후, 데이터 정상 출력 확인
            button=self.FC.loading_find_csss(self.FC.var['iptv_el']['온라인1분가입_버튼'])[random_num]
            self.FC.move_to_click(button)
            assert self.FC.var['iptv_el']['online_url'] in self.FC.loading_find_css(self.FC.var['iptv_el']['온라인1분가입_상세']).get_property('baseURI'), self.DBG.logger.debug("인터넷/IPTV > 서브메인 > 인터넷+IPTV 추천 결합 상품 영역 - 온라인 가입 페이지 정상 노출 실패")

            if self.FC.var['iptv_el']['iptv_url'] != self.FC.driver.current_url:
                self.FC.goto_url(self.FC.var['iptv_el']['iptv_url'])

            # 더 나은 일상을 위한 다양한 소식을 전해드려요 영역
            iptv_daily_list=self.FC.loading_find_csss(self.FC.var['iptv_el']['더나은일상_소식영역'])
            self.FC.move_to_click(iptv_daily_list[0])
            assert len(iptv_daily_list) >= 4,self.DBG.logger.debug("인터넷/IPTV > 더 나은 일상을 위한 다양한 소식을 전해드려요 이벤트영역 출력 실패")

        except  Exception :
            self.DBG.print_dbg("인터넷/IPTV 페이지 정상 노출 및 기능 동작 확인",False)
            self.FC.gotoHome()
            self.FC.modal_ck4()
            return False

        else :
            self.DBG.print_dbg("인터넷/IPTV 페이지 정상 노출 및 기능 동작 확인")
            return True

if __name__ == "__main__":
    driver = WebDriver()
    fc = Function(driver)
    iptv = InternetIptvPage(driver, fc)

    iptv.iptv()
