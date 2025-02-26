import re
import sys
from base.webdriver import WebDriver
from common.function import Function
from common.debug import Debug
from pages.login import LoginPage

sys.path.append(r'C:\dev\lg_regression\selenium_mw')


class Search():
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)

    def searching(self,keyword:str=''):
        '''
        키워드 검색하기
        keyword: 검색할 키워드
        '''
        search_input=self.FC.loading_find_css(self.FC.var['search_el']['검색창_input'])
        search_input.click()
        self.FC.is_exists_element_click(self.FC.loading_find_css_pre(self.FC.var['search_el']['검색창_비우기']))
        search_input.send_keys(keyword)
        self.FC.bring_el_to_front_csss(self.FC.var['search_el']['검색창_검색버튼'])
        self.FC.loading_find_css(self.FC.var['search_el']['검색창_검색버튼']).click()
        self.FC.wait_loading()

    # 메인페이지 로그인 후
    def search(self):
        self.FC.gotoHome()
        try:
            self.FC.loading_find_css_pre(self.FC.var['search_el']['search_btn']).click()
            assert self.FC.loading_find_css_pre(self.FC.var['search_el']['검색_모달창_판단']).get_property('className') == "modal-open",self.DBG.logger.debug("검색 모달창 노출 실패")

            result=[]
            result.clear()
            # 검색결과 있음, 검색결과 없음, 특수문자 검색
            test_keywords = ['테스트','결과없음','~!@#$%^&*_-+=`|\\(){}[]:;\"\'<>,.?/']
            for keyword in test_keywords:
                self.searching(keyword)
                if keyword != '테스트':
                    assert self.FC.loading_find_css_pre(self.FC.var['search_el']['검색결과_검색창']) is False , self.DBG.logger.debug("검색 > 테스트 키워드:'%s' 정상 노출 확인 실패", keyword)
                else:
                    assert keyword in self.FC.loading_find_css(self.FC.var['search_el']['검색결과_검색창']).get_property("innerText") , self.DBG.logger.debug("검색 > 테스트 키워드:'%s' 정상 노출 확인 실패", keyword)
                    result= self.FC.loading_find_css(self.FC.var['search_el']['검색결과_건수']).get_property('innerText')
                    result_count = re.sub(r'[^0-9]','',result)
                    print(f"result_count -> {result_count}")
                    assert result_count in self.FC.loading_find_css(self.FC.var['search_el']['검색결과_탭']).get_property("innerText") , self.DBG.logger.debug("검색 > 테스트 키워드:'%s' 정상 노출 확인 실패", keyword)

        except  Exception :
            self.DBG.print_dbg("검색기능 정상 동작",False)
            return False

        else :
            self.DBG.print_dbg("검색기능 정상 동작")
            return True

if __name__ == "__main__":
    driver = WebDriver()
    fc = Function(driver)
    main = Search(driver,fc)
    login = LoginPage(driver,fc)

    if fc.is_login():
        login.logout()

    login.u_plus_login()


    main.search()

    driver.driver.quit()
    # driver.kill()
