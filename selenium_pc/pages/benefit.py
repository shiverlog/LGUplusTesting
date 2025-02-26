import random

from base.webdriver import WebDriver
import common.json.variable as var
from common.function import Function
from common.debug import Debug
from pages.login import LoginPage


class BenefitPage():
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)

    # 혜택테스트 부분
    def benefit(self):
        try:
            self.FC.movepage(self.FC.var['benefit_el']['benefit'], address=self.FC.var['benefit_el']['url'])

            # 서브메인 테마배너 혜택
            check_text_list=['멤버십','이벤트','장기고객 혜택','결합할인 혜택','선택약정 할인']
            assert self.FC.text_list_in_element(self.FC.var['mobile_el']['테마배너'],check_text_list),self.DBG.logger.debug("모바일 > 서브메인 > 테마베너 정상 출력 실패")
            theme_list_link=self.FC.loading_find_csss(self.FC.var['mobile_el']['테마배너_링크'])
            random_num= random.randrange(0,len(theme_list_link))
            check_link=theme_list_link[random_num].get_attribute('href')
            check_link=check_link[check_link.rfind('/'):]
            tab_name= theme_list_link[random_num].get_attribute('data-gtm-click-text')
            self.FC.move_to_element(self.FC.loading_find_css_pre(self.FC.var['common_el']['KV']))
            self.FC.scroll(2,False)
            self.FC.wait_loading()
            theme_list_link[random_num].click()
            self.FC.wait_loading()
            assert check_link in self.FC.driver.current_url,self.DBG.logger.debug(f"모바일 > 서브메인 > 테마베너 > {tab_name}탭 정상 동작 실패")
            self.FC.goto_url(self.FC.var['benefit_el']['url'])

            result=[]
            # # 멤버십 혜택
            result.clear()
            self.FC.move_to_element(self.FC.loading_find_css_pre(self.FC.var['benefit_el']['멤버십혜택_영역']))
            text_list=['APP/기기','엑티비티','뷰티/건강','쇼핑','생활/편의','푸드','문화/여가','교육','여행/교통']
            result.append(self.FC.text_list_in_element(self.FC.var['benefit_el']['멤버십혜택_탭메뉴'],text_list))
            self.FC.loading_find_css_pre(self.FC.var['benefit_el']['제휴사전체보기_버튼']).click()
            result.append(self.FC.var['benefit_el']['url'] in self.FC.loading_find_css(self.FC.var['benefit_el']['제휴사전체보기_전체영역']).get_property('baseURI'))
            if self.FC.var['benefit_el']['url'] != self.FC.driver.current_url:
                self.FC.goto_url(self.FC.var['benefit_el']['url'])
            self.FC.move_to_element(self.FC.loading_find_css_pre(self.FC.var['benefit_el']['멤버십혜택_영역']))
            assert self.DBG.print_res(result), self.DBG.logger.debug("혜택/멤버십 > 서브메인 > sec-2 영역 콘텐츠 정상 출력 실패")

            self.FC.con_check_full_view(var.benefit_el, '온라인_가입할인_혜택','온라인_가입할인_혜택_컨텐츠','혜택모두보기_버튼','online','혜택모두보기_상세')
            assert self.DBG.print_res(result), self.DBG.logger.debug("혜택/멤버십 > 서브메인 > sec-3 영역 콘텐츠 정상 출력 실패")

        except  Exception :
            self.DBG.print_dbg("혜택/멤버십 페이지 정상 노출 및 기능 동작 확인",False)
            self.FC.gotoHome()
            self.FC.modal_ck4()
            return False

        else :
            self.DBG.print_dbg("혜택/멤버십 페이지 정상 노출 및 기능 동작 확인")
            return True

    # 혜택/멤버십 > 멤버십 > 멤버십 이용내역/변경내역
    def membership(self):
        self.FC.gotoHome()

        try:
            self.FC.movepage(self.FC.var['benefit_el']['benefit'],self.FC.var['benefit_el']['멤버십_이용내역'] ,address=self.FC.var['benefit_el']['membership_url'])

            result=[]
            text_list=['멤버십 카드 번호','멤버십 카드 신청 및 재발급','이번 달 나의 등급','올해 누적 할인']
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['멤버십_영역'],text_list))
            result.append(self.FC.wait_datas(self.FC.var['mypage']['멤버십_영역'],'div.text','div.card-num'))
            assert self.DBG.print_res(result), self.DBG.logger.debug("혜택/멤버십 > 멤버십 > 서브메인 > 상단 영역 콘텐츠 정상 출력 실패")

            # 안내 문자메시지 수신 설정
            self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['mypage']['멤버십_안내문자메시지수신설정_버튼']))
            text_list=['휴대폰 번호','문자메시지 수신 여부','문자메시지 수신 설정']
            assert self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list),self.DBG.logger.debug("혜택/멤버십 > 멤버십 > 서브메인 > 상단 영역 - 안내 메시지 수신 설정 기능 정상 작동 실패")
            self.FC.modal_ck()

            # 멤버십 카드 신청 및 재발급
            self.FC.loading_find_xpath(self.FC.var['mypage']['카드신청_및_재발급_버튼']).click()
            self.FC.wait_loading()
            text_list=['멤버십 카드 재발급','취소','재발급 신청']
            assert self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list),self.DBG.logger.debug("혜택/멤버십 > 멤버십 > 서브메인 > 상단 영역 - 멤버십 카드 신청 및 재발급 기능 정상 작동 실패")
            self.FC.modal_ck()

            # 멤버십 등급 안내
            self.FC.loading_find_xpath(self.FC.var['mypage']['등급안내_버튼']).click()
            self.FC.wait_loading()
            text_list=['VVIP','VIP','우수']
            assert self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list),self.DBG.logger.debug("혜택/멤버십 > 멤버십 > 서브메인 > 상단 영역 - 멤버십 등급 안내 기능 정상 작동 실패")
            self.FC.modal_ck()

            # 멤버십 이용내역/멤버십 변경 내역 콘텐츠 정상 출력 확인
            tab_list_el=self.FC.loading_find_csss(self.FC.var['mypage']['멤버십_탭메뉴'])
            tab_list=['멤버십 이용내역','멤버십 변경내역']
            for tab in tab_list:
                self.FC.move_to_click(tab_list_el[tab_list.index(tab)],True)

                if tab == tab_list[0]: # 멤버십 이용내역
                    text_list=['멤버십 월별 정보','연월','멤버십 등급','할인 혜택','올해 누적 할인']
                    result.append(self.FC.text_list_in_element(self.FC.var['mypage']['멤버십_월별정보'],text_list))
                    text_list=['기간별 이용내역 조회','조회기간','기간설정','검색']
                    result.append(self.FC.text_list_in_element(self.FC.var['mypage']['멤버십_기간별이용내역조회'],text_list))
                    self.FC.loading_find_css(self.FC.var['mypage']['멤버십_기간별이용내역조회_검색버튼']).click()
                    self.FC.wait_loading()
                    text_list=['누적 할인혜택','사용일','사용처','누적 할인 혜택','한도','승인']
                    result.append(self.FC.text_list_in_element(self.FC.var['mypage']['멤버십_기간별이용내역조회_검색버튼영역'],text_list))
                    assert self.DBG.print_res(result),self.DBG.logger.debug("혜택/멤버십 > 멤버십 > 서브메인 > 멤버십 이용내역 탭 콘텐츠 정상 출력 실패")

                if tab == tab_list[1]:  # 멤버십 변경 내역
                    result.clear()
                    text_list=['멤버십 등급 변경내역','변경일','멤버십 등급','이용 요금제','등급산정기준']
                    result.append(self.FC.text_list_in_element(self.FC.var['mypage']['멤버십_월별정보'],text_list))
                    result.append(self.FC.wait_datas(self.FC.var['mypage']['멤버십_월별정보'],'td'))
                    text_list=['멤버십 카드 발급내역','신청일','멤버십 카드번호','발급일','사용 중지일','상태']
                    result.append(self.FC.text_list_in_element(self.FC.var['mypage']['멤버십_기간별이용내역조회'],text_list))
                    assert self.DBG.print_res(result),self.DBG.logger.debug("혜택/멤버십 > 멤버십 > 서브메인 > 멤버십 변경 내역 탭 콘텐츠 정상 출력 실패")

        except  Exception :
            self.DBG.print_dbg("혜택/멤버십 > 멤버십 > 멤버십 관련 정보 및 멤버십 이용/변경 내역 정상 동작 확인",False)
            return False

        else :
            self.DBG.print_dbg("혜택/멤버십 > 멤버십 > 멤버십 관련 정보 및 멤버십 이용/변경 내역 정상 동작 확인")
            return True


if __name__ == "__main__":
    driver = WebDriver()
    fc = Function(driver)
    benefit = BenefitPage(driver,fc)
    login = LoginPage(driver,fc)

    # 공통모듈로 분리?
    if fc.is_login():
        login.logout()

    login.u_plus_login()

    benefit.benefit()
    driver.driver.quit()
   