import random
import sys  # 현재 호출하는 함수명 반환 모듈

from base.webdriver import WebDriver
from common.function import Function
from common.debug import Debug

sys.path.append(r'C:\lg-uplus\project\selenium_pc')



class DirectPage():
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)


    def direct(self):
        self.FC.gotoHome()

        try:

            self.FC.movepage(self.FC.var['direct_el']['direct'],address=self.FC.var['direct_el']['url'])
            self.FC.modal_ck4()

            # KV 콘텐츠 정상 출력 확인
            kv_list_el=self.FC.loading_find_csss(self.FC.var['direct_el']['배너_이미지'])
            assert (len(kv_list_el)) > 0, self.DBG.logger.debug("다이렉트 페이지 KV 콘텐츠 정상 출력 실패")

            ## sec1(cont-01) 콘텐츠 확인
            result=[]
            self.FC.move_to_element(self.FC.loading_find_css_pre(self.FC.var['direct_el']['con_01']))
            text_list=['유심 가입 방법 확인']
            result.append(self.FC.text_list_in_element(self.FC.var['direct_el']['다이렉트_컨텐츠1'],text_list))
            assert self.DBG.print_res(result), self.DBG.logger.debug("다이렉트 > 유심 가입 컨텐츠 출력 실패")

            # 유플닷컴 전용 요금제
            result.clear()
            self.FC.move_to_element(self.FC.loading_find_css_pre(self.FC.var['direct_el']['con_02']))
            direct_plan_tit = self.FC.loading_find_csss(self.FC.var['direct_el']['다이렉트_컨텐츠2_tit'])
            direct_plan_price = self.FC.loading_find_csss(self.FC.var['direct_el']['다이렉트_컨텐츠2_price'])
            direct_plan_btn = self.FC.loading_find_csss(self.FC.var['direct_el']['다이렉트_컨텐츠2_가입버튼'])
            # random_num=random.randrange(0,len(direct_plan_tit)) # DCBGQA-3975 결함으로 인한 주석 처리
            random_num=0
            direct_plan_tit_txt = direct_plan_tit[random_num].get_property('innerText')     # 임의의 유플닷컴 전용 요금제
            direct_plan_price_txt = direct_plan_price[random_num].get_property('innerText')
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['direct_el']['다이렉트_컨텐츠2_전체보기']))
            direct_plan_btn[random_num].click()
            self.FC.wait_loading()
            text_list = [direct_plan_tit_txt, direct_plan_price_txt]
            assert self.FC.var['direct_el']['전용요금제_가입하기_url'] in self.FC.loading_find_css(self.FC.var['direct_el']['전용요금제_가입하기_전체영역']).get_property('baseURI'), self.DBG.logger.debug("다이렉트 > 유플닷컴 전용 요금제 가입하기 > 페이지 이동 실패")
            assert direct_plan_tit_txt in self.FC.loading_find_css(self.FC.var['direct_el']['다이렉트_컨텐츠2_계산영역']).get_property('innerText')  , self.DBG.logger.debug("다이렉트 > 유플닷컴 전용 요금제 가입하기 > 페이지 데이터 상이함")

            self.FC.goto_url(self.FC.var['direct_el']['url'])
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['direct_el']['다이렉트_컨텐츠2_전체보기']))
            plan_list=self.FC.loading_find_csss(self.FC.var['direct_el']['다이렉트_컨텐츠3'])
            self.FC.move_to_element(plan_list[0])
            assert len(plan_list) == 4 , self.DBG.logger.debug("다이렉트 > 다이렉트 요금제 혜택 콘텐츠 노출 실패")

            #고객리뷰
            reviews = self.FC.loading_find_csss(self.FC.var['direct_el']['다이렉트_컨텐츠4'])
            self.FC.move_to_element(reviews[4])
            assert len(reviews) >= 3 , self.DBG.logger.debug("다이렉트 > 고객리뷰 콘텐츠 노출 실패")

            #다이렉트를 가장 쉽게 만나는 방법
            direct_con5 = self.FC.loading_find_csss(self.FC.var['direct_el']['다이렉트_컨텐츠5'])
            self.FC.move_to_element(direct_con5[0])
            random_num = random.randrange(0,len(direct_con5))
            assert len(direct_con5) == 3 , self.DBG.logger.debug("다이렉트 > 다이렉트를 가장 쉽게 만나는 방법 콘텐츠 노출 실패")

            self.FC.move_to_click(direct_con5[random_num])
            assert self.FC.var['ujam_el']['url'] in self.FC.loading_find_css(self.FC.var['ujam_el']['ujam_con_all']).get_property('baseURI'), self.DBG.logger.debug("다이렉트 > 다이렉트를 가장 쉽게 만나는 방법 > 페이지 이동 실패")


        except  Exception :
            self.DBG.print_dbg("다이렉트페이지 정상 노출 및 기능 동작 확인",False)
            return False

        else :
            self.DBG.print_dbg("다이렉트페이지 정상 노출 및 기능 동작 확인")
            self.FC.modal_ck4()
            return True




if __name__ == "__main__":
    driver = WebDriver()
    fc = Function(driver)
    direct = DirectPage(driver, fc)

    direct.direct()
