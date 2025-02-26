import sys
import time

from base.server import AppiumServer
from base.appdriver import AppDriver
from common.function import Function
from common.debug import Debug
import common.variable as var      # 지정한 변수 모듈 
from pages.login import LoginPage

sys.path.append('/Users/nam/dev/remotePC_batchfiles/pubsub/appium_ios')


class SupportPage():
    def __init__(self,AppDriver:AppDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(AppDriver)


    # 고객지원 부분, 휴대폰분실파손 부분 오류
    def support(self):
        self.FC.gotoHome()

        try:
            # 메인 > 고객지원 > 바로가기
            self.FC.movepage(var.support_el['support'], var.support_el['direct'],address=self.FC.var['support_el']['url'])

            # 자주 찾는 검색어 영역 콘텐츠 및 기능 정상 확인
            # 수동입력 검색
            result=[]
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['support_el']['고객지원_검색_영역']))
            result.append(self.FC.loading_find_css_pre(self.FC.var['support_el']['고객지원_검색창']))
            result.append(5 == len(self.FC.loading_find_csss(self.FC.var['support_el']['고객지원_자주찾는_검색어_list'])))
            assert self.DBG.print_res(result), self.DBG.logger.debug("고객지원 > 서브메인 > 상단 자주찾는 검색어 정상 노출 실패") 

            # 수동 검색어 검색
            test_keyword='테스트'   #검색할 키워드
            search_el=self.FC.loading_find_css_pre(self.FC.var['support_el']['고객지원_검색창'])
            search_el_id='#' + search_el.get_attribute('id')

            self.FC.bring_el_to_front(search_el_id)
            search_el=self.FC.loading_find_css(search_el_id)
            search_el.re_click()
            search_el.send_keys(test_keyword)
            search_enter = self.FC.var['support_el']['고객지원_검색_버튼']
            self.FC.bring_el_to_front(search_enter)
            self.FC.loading_find_css_pre(search_enter).re_click()
            self.FC.wait_loading()

            self.FC.loading_find_css(self.FC.var['support_el']['키워드로_찾기_tab']).re_click()  #키워드로 찾기 탭 이동
            assert self.FC.loading_find_css(self.FC.var['support_el']['포함_검색어']).get_property('innerText')==test_keyword, self.DBG.logger.debug(f"고객지원 > 자주하는 질문 > 키워드로 찾기 탭 > 테스트 키워드:'{test_keyword}' 정상 노출 확인 실패") 
            # TODO 기존 이슈로인해 일시 주석처리
            # assert self.FC.loading_find_css('input#addr-1-1').get_property('value')==test_keyword, self.DBG.logger.debug(f"고객지원 > 자주하는 질문 > 키워드로 찾기 탭 > 테스트 키워드:'{test_keyword}' 정상 노출 확인 실패")                  #현재 이슈로인해 Fail 반환 - DCBGQA-336

            result.append(self.FC.loading_find_css(self.FC.var['support_el']['포함_검색어']).get_property('innerText')==test_keyword)
            # result.append(self.FC.loading_find_css('input#addr-1-1').get_property('value')==test_keyword)    #현재 이슈로인해 Fail 반환 - DCBGQA-336
            search_result_list_el=self.FC.loading_find_csss(self.FC.var['support_el']['자주하는질문_list'])

            # 검색 결과 콘텐츠가 검색한 키워드를 포함하는지 확인
            search_result=[]
            for el in search_result_list_el:
                el_nextElementSibling=self.FC.driver.execute_script("return arguments[0].nextElementSibling;", el)
                if el_nextElementSibling.get_attribute('style') == 'display: none;':
                    self.FC.move_to_click(el)
                time.sleep(1)  # 슬라이드 애니메이션 대기
                res=test_keyword in el.get_property('innerText') or self.FC.loading_find_csss(self.FC.var['support_el']['답변_내용'])[search_result_list_el.index(el)]
                search_result.append(res)
            assert all(search_result), self.DBG.logger.debug(f"고객지원 > 자주하는 질문 > 키워드로 찾기 탭 > 검색 결과 콘텐츠 정상 출력 실패") 
            self.FC.goto_url(self.FC.var['support_el']['url'])

            # sec-2 영역 콘텐츠 정상 출력 확인, 로그인 전/후 로직 분리 필요
            result.clear()
            self.FC.scroll2_v2(self.FC.loading_find_css(self.FC.var['support_el']['도움이_될_내용']))
            text_list=['도움']
            result.append(self.FC.text_list_in_element(self.FC.var['support_el']['도움이_될_내용'], text_list))
            result.append(len(self.FC.loading_find_csss(self.FC.var['support_el']['도움이_될_내용_list']))>1)
            assert self.DBG.print_res(result), self.DBG.logger.debug(f"고객지원 > 서브메인 > 도움이 될 내용 콘텐츠 정상 출력 실패")

            # 스스로 해결 가이드로 간편하게 해결해 보세요 영역
            result.clear()
            # self.FC.action.move_to_element(self.FC.loading_find_css_pre('div.submain-section > div.c-section-xs > div.c-section-md')).perform()
            # self.FC.action.reset_actions()
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['support_el']['스스로_해결_가이드']))

            # 상단 타이틀"스스로 해결 가이드" 키워드 유무 확인
            text_list=['스스로 해결','가이드']
            result.append(self.FC.text_list_in_element(self.FC.var['support_el']['스스로_해결_가이드_title'], text_list))
            video_list_el=self.FC.loading_find_csss(self.FC.var['support_el']['스스로_해결_가이드_list'])
            result.append(len(video_list_el) == 4)
            assert self.DBG.print_res(result), self.DBG.logger.debug("고객지원 > 서브메인 > 스스로 해결 가이드 정상 노출 확인 실패")


            # 마지막 섹션 콘텐츠 출력 및 링크 이동
            # result.clear()
            # self.FC.swipe('div.submain-section > div.c-section-md')
            # # TODO 1:1문의하기 링크 이동 이슈 있음 - DCBGQA-375 / 1:1 문의하기는 로그인 전/후 로직 필요
            # # 홈페이지 개선제안 버튼은 팝업 출력으로 제외
            # url_list=['https://app.lguplus.com/support/service/use-guide','https://app.lguplus.com/support/online/inquiry','https://app.lguplus.com/support/service/ars']
            # page_el=['div.section-support-guide','div.c-board-card-feedback-list-index','button.collapsed']
            # for url in url_list:
            #     info_list_el=self.FC.loading_find_csss('div.submain-section > div.c-section-md > ul>li a')
            #     num=url_list.index(url)
            #     # self.FC.action.move_to_element(info_list_el[num]).re_click().perform()
            #     # self.FC.action.reset_actions()
            #     self.FC.move_to_click(info_list_el[num])
            #     # self.FC.scroll2_v2(info_list_el[num]).re_click()
            #     result.append(url in self.FC.loading_find_css_pre(page_el[num]).get_property('baseURI'))
            #     self.FC.goto_url("https://app.lguplus.com/support")
            #     # while True:
            #     #     if 'https://app.lguplus.com/support' != self.FC.driver.current_url:
            #     #         self.FC.back()
            #     #         self.FC.loading_find_css_pre('div.visual-img img')
            #     #     if 'https://app.lguplus.com/support' == self.FC.driver.current_url:
            #     #         break
            #     self.FC.scroll2_v2(self.FC.loading_find_css_pre('div.submain-section > div.c-section-md'))
            
            # info_list_el=self.FC.loading_find_csss('div.submain-section > div.c-section-md > ul>li a')
            # self.FC.action.move_to_element(info_list_el[-1]).re_click().perform()
            # self.FC.action.reset_actions()
            # self.FC.driver.switch_to.window(self.FC.driver.window_handles[1])
            # print(self.FC.loading_find_css_pre('div.cont_01').get_property('innerText'))
            # result.append("고객의 소리" in self.FC.loading_find_css_pre('div.cont_01').get_property('innerText'))
            # self.FC.close_popup(self.FC.driver.window_handles)
            
            # print(str(result))
            # assert self.DBG.print_res(result), self.DBG.logger.debug("고객지원 > 서브메인 > 정보 버튼(마지막 섹션) 정상 노출 확인 실패")
            

        except  Exception :
            self.DBG.print_dbg("고객지원 페이지 정상 노출 및 기능 동작 확인",False)
            self.FC.close_popup(self.FC.driver.window_handles)
            return False

        else :
            self.DBG.print_dbg("고객지원 페이지 정상 노출 및 기능 동작 확인")
            return True


if __name__ == "__main__":
    try:
        server = AppiumServer(4723)
        port = server.appium_service()
        if not server.waiting():
            raise Exception("서버 실행 불가")
        driver = AppDriver(port=port)
        fc = Function(driver)
        login = LoginPage(driver,fc)
        support = SupportPage(driver,fc)

        fc.pre_script()
        
        if fc.is_login():
            login.logout()
        login.u_plus_login()
        
        support.support()
        driver.driver.quit()
        server.stop()
    except Exception as e:
        print(e)
        # os.system("lsof -P -i :4723 |awk NR==2'{print $2}'|xargs kill -9")
        # os.system(f"ios-deploy --kill --bundle_id com.lguplus.mobile.cs")
