import random

from base.webdriver import WebDriver
from common.function import Function
from common.debug import Debug

from selenium.webdriver.common.keys import Keys


class SupportPage():
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)

    def support(self):
        self.FC.gotoHome()
        try:
            self.FC.movepage(self.FC.var['support_el']['support'],address=self.FC.var['support_el']['url'])       # 메인 > 혜택 > 바로가기

            # 자주 찾는 검색어
            result=[]
            self.FC.move_to_element(self.FC.loading_find_css_pre(self.FC.var['support_el']['고객지원_검색영역']))
            result.append(self.FC.loading_find_css(self.FC.var['support_el']['고객지원_검색_플래이스홀더']))
            result.append(5 == len(self.FC.loading_find_csss(self.FC.var['support_el']['자주찾는검색어'])))
            assert self.DBG.print_res(result), self.DBG.logger.debug("고객지원 > 서브메인 > 상단 자주찾는 검색어 정상 노출 실패")

            # 수동 검색어 검색
            keyword="테스트"
            self.FC.loading_find_css(self.FC.var['support_el']['고객지원_검색인풋창']).send_keys(keyword)
            self.FC.loading_find_css(self.FC.var['support_el']['고객지원_검색인풋창']).send_keys(Keys.ENTER)
            self.FC.wait_loading()

            # 검색어/탭 정상 출력
            text_list=['전체','모바일','인터넷','TV','전화','유독','U+스마트홈','결합 할인','해외로밍','소상공인','가입 및 변경','요금 및 납부']
            assert self.FC.text_list_in_element(self.FC.var['support_el']['자주하는질문_메뉴탭'],text_list),self.DBG.logger.debug("고객지원 > 서브메인 > 자주하는 질문 > 검색 결과 탭 콘텐츠 정상 출력 실패")
            assert keyword == self.FC.loading_find_css_pre(self.FC.var['support_el']['검색어_텍스트']).get_property('innerText'),self.DBG.logger.debug("고객지원 > 서브메인 > 자주하는 질문 > 키워드로 찾기 탭 > 테스트 키워드:'%s' 정상 노출 확인 실패", keyword)
            search_list=self.FC.loading_find_csss(self.FC.var['support_el']['검색결과_리스트'])

            search_result=[]
            for el in search_list:
                self.FC.move_to_element(el)
                if el.get_property('nextElementSibling').get_attribute('style') == 'display: none;':
                    self.FC.move_to_click(el)
                res=keyword in el.get_property('innerText') or self.FC.loading_find_csss(self.FC.var['support_el']['검색결과'])[search_list.index(el)]
                search_result.append(res)

            assert all(search_result), self.DBG.logger.debug("고객지원 > 서브메인 > 자주하는 질문 > 검색 결과 콘텐츠 정상 출력 실패")


            # 키워드 검색어 검색
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['support_el']['검색결과_전체영역']))
            keyword_list=self.FC.loading_find_csss(self.FC.var['support_el']['자주하는질문키워드'])
            random_num=random.randrange(0,len(keyword_list))
            keyword=keyword_list[random_num].get_property('innerText')
            self.FC.move_to_click(keyword_list[random_num])

            # 검색어/탭 정상 출력
            text_list=['전체','모바일','인터넷','TV','전화','유독','U+스마트홈','결합 할인','해외로밍','소상공인','가입 및 변경','요금 및 납부']
            assert self.FC.text_list_in_element(self.FC.var['support_el']['자주하는질문_메뉴탭'],text_list),self.DBG.logger.debug("고객지원 > 서브메인 > 자주하는 질문 > 검색 결과 탭 콘텐츠 정상 출력 실패")
            assert keyword == self.FC.loading_find_css_pre(self.FC.var['support_el']['검색어_텍스트']).get_property('innerText'),self.DBG.logger.debug("고객지원 > 서브메인 > 자주하는 질문 > 키워드로 찾기 탭 > 테스트 키워드:'%s' 정상 노출 확인 실패", keyword)
            search_list=self.FC.loading_find_csss(self.FC.var['support_el']['검색결과_리스트'])
            search_result.clear()
            for el in search_list:
                self.FC.move_to_element(el)
                if el.get_property('nextElementSibling').get_attribute('style') == 'display: none;':
                    self.FC.move_to_click(el)
                res=keyword in el.get_property('innerText') or self.FC.loading_find_csss(self.FC.var['support_el']['검색결과'])[search_list.index(el)]
                search_result.append(res)
            assert all(search_result), self.DBG.logger.debug("고객지원 > 서브메인 > 자주하는 질문 > 검색 결과 콘텐츠 정상 출력 실패")
            self.FC.driver.get(self.FC.var['support_el']['url'])

            # 로그인 여부에 따른 콘텐츠 출력
            result.clear()
            is_login=self.FC.is_login()
            if is_login is not True:
                self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['support_el']['도움이될내용']))
                text_list=['가까운 매장','U+','로그인']
                result.append(self.FC.text_list_in_element(self.FC.var['support_el']['도움이될내용'],text_list))
                # 로그인 버튼 클릭 시, 팝업 노출
                self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['support_el']['도움이될내용_버튼']))
                text_list=['U+ ID','비밀번호','로그인','비회원','U+ ID 로그인','임직원 로그인','아이디 저장','LG 통합 아이디']
                result.append(self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list))

            else:
                # 자주 찾는 질문(도움이 될 내용을 확인하세요)
                self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['support_el']['도움이될내용']))
                result.clear()
                self.FC.move_to_element(self.FC.loading_find_csss(self.FC.var['support_el']['도움이될내용_버튼'])[-1])
                assert 11 == len(self.FC.loading_find_csss(self.FC.var['support_el']['도움이될내용_버튼']))


            # 스스로 해결 가이드(누구나 쉽게 따라할 수 있는 영상)
            result.clear()
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['support_el']['스스로해결가이드']))
            self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['support_el']['스스로해결가이드_더보기']))
            result.append(self.FC.var['support_el']['self_guide_url'] == self.FC.loading_find_css(self.FC.var['support_el']['스스로해결가이드_상세_전체영역']).get_property('baseURI'))
            self.FC.goto_url(self.FC.var['support_el']['url'])
            self.FC.move_to_element(self.FC.loading_find_css_pre(self.FC.var['support_el']['스스로해결가이드']))
            assert self.DBG.print_res(result), self.DBG.logger.debug("혜택 > 서브메인 > 스스로 해결 가이드 콘텐츠 및 기능 정상 동작 실패")

            # 이용가이드
            result.clear()
            self.FC.move_to_element(self.FC.loading_find_css_pre(self.FC.var['support_el']['이용가이드영역']))
            text_list=['서비스 가입안내','모바일기기','인터넷/IPTV/인터넷 전화','스마트홈','가입 및 기기변경','가입제한','신규고객 안내']
            result.append(self.FC.text_list_in_element(self.FC.var['support_el']['서비스가입안내'],text_list))
            text_list=['서비스 조회','가입조회','개통내역조회']
            result.append(self.FC.text_list_in_element(self.FC.var['support_el']['서비스조회'],text_list))
            text_list=['서비스 변경/일시정지/해지','변경(명의, 번호, 유심)','일시정지/해제','복지할인 등록','발신내역 조회','납부방법 변경']
            result.append(self.FC.text_list_in_element(self.FC.var['support_el']['서비스변경_일시정지_해지'],text_list))
            text_list=['매뉴얼 다운로드','매뉴얼','프로그램']
            result.append(self.FC.text_list_in_element(self.FC.var['support_el']['매뉴얼다운로드'],text_list))
            assert self.DBG.print_res(result), self.DBG.logger.debug("혜택 > 서브메인 > 이용가이드 콘텐츠 및 기능 정상 동작 실패")

            # 찾으시는 내용이 없으신가요?
            self.FC.move_to_element(self.FC.loading_find_css_pre(self.FC.var['support_el']['안내영역']))
            text_list=['1:1 문의','고객센터/ARS 안내','홈페이지 개선제안']
            assert self.FC.text_list_in_element(self.FC.var['support_el']['안내영역'],text_list)

        except  Exception :
            self.DBG.print_dbg("고객지원 페이지 정상 노출 및 기능 동작 확인",False)
            return False

        else :
            self.DBG.print_dbg("고객지원 페이지 정상 노출 및 기능 동작 확인")
            return True


if __name__ == "__main__":
    driver = WebDriver()
    fc = Function(driver)
    support = SupportPage(driver, fc)

    if support.FC.is_login():
        support.support()
