import random

from base.webdriver import WebDriver
from common.function import Function
from common.debug import Debug

class MainPage():
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)

    # 로그인 후 메인페이지 내정보 출력 확인
    def mainpage_myinfo(self):
        self.FC.gotoHome()
        try:

            self.FC.loading_find_css(self.FC.var['mainpage_el']['my_data_toggle']).click()
            self.FC.wait_loading()
            assert "is-open" in self.FC.loading_find_css(self.FC.var['mainpage_el']['my_data_layer']).get_property('className'), self.DBG.logger.debug("메인 > 내정보 영역 기능 정상 작동 실패")

            my_datas={
                'my_data_phon_plan':['요금제','변경하기'],
                'my_data_add_services':['부가서비스','바로가기'],
                'my_data_data':['데이터','변경하기'],
                'my_data_combi_prod':['이번 달 청구요금','바로가기'],
                'my_data_month_pay':['나의 혜택 리포트','바로가기'],
                'my_data_benefit':['휴대폰결제 이용금액','바로가기'],
                }
            text_list_result=[]
            for key,value in my_datas.items():
                text_list_result.append(self.FC.text_list_in_element(self.FC.var['mainpage_el'][key],value))
            res = self.FC.wait_datas(self.FC.var['mainpage_el']['my_data_layer'],'p.data-info','p.data-info span','span.use-data span','div.txt-price')
            text_list_result.append(not isinstance(res,str))
            assert all(text_list_result),self.DBG.logger.debug("메인 > 내정보 영역 기능 및 콘텐츠 정상 노출 확인 실패")
            self.FC.loading_find_css(self.FC.var['mainpage_el']['my_data_toggle']).click()

        except Exception:
            self.DBG.print_dbg("메인 페이지(로그인 후) > 개인화 영역 정상 노출 확인",False)
            return False

        else :
            self.DBG.print_dbg("메인 페이지(로그인 후) > 개인화 영역 정상 노출 확인")
            return True

    # PC는 로그인 여부 상관없이 메인 페이지 출력 동일
    def mainpage(self):
        self.FC.gotoHome()

        try:
            # KV 영역 콘텐츠 정상 출력 확인
            kv_list=self.FC.loading_find_csss(self.FC.var['mainpage_el']['KV'])
            assert len(kv_list) >=1,  self.DBG.logger.debug("메인 > KV 컨텐츠 정상 노출 확인 실패")

            # 이벤트 영역 콘텐츠 정상 출력 확인
            self.FC.scroll(4)
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mainpage_el']['RTB']))
            rtb_list=self.FC.loading_find_csss(self.FC.var['mainpage_el']['RTB_event'])
            if len(kv_list) == 1:
                assert len(rtb_list) == 5, self.DBG.logger.debug("메인 > RTB 컨텐츠 정상 노출 확인 실패")
            else :
                assert len(rtb_list) == 4, self.DBG.logger.debug("메인 > RTB 컨텐츠 정상 노출 확인 실패")

            # 기기 추천 영역 콘텐츠 정상 출력 확인
            self.FC.scroll(5)
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mainpage_el']['RCMD']))
            rcmd_tab_list = self.FC.loading_find_csss(self.FC.var['mainpage_el']['RCMD_tab'])
            num = random.randrange(0, len(rcmd_tab_list))
            self.FC.move_to_click(rcmd_tab_list[num])
            
            rcmd_device = self.FC.loading_find_csss(self.FC.var['mainpage_el']['RCMD_device'])
            num = random.randrange(1, len(rcmd_device)) # 키즈폰 무너에디션 예외처리
            rcmd_device_info = rcmd_device[num].get_property('outerHTML').replace(" ", "")
            self.FC.move_to_click(rcmd_device[num])
            phone_name = self.FC.loading_find_csss(self.FC.var['mobile_el']['휴대폰_상세_상품명'])[0].get_property('innerText').split('(')[0].replace(" ", "")

            assert phone_name in rcmd_device_info, self.DBG.logger.debug("메인 > 기기 추천 컨텐츠 정상 노출 확인 실패")

            self.FC.gotoHome()

            # 유독 영역 콘텐츠 정상 출력 확인
            result = []
            self.FC.scroll(6)
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mainpage_el']['RSVC']))

            logo_img = self.FC.loading_find_css(self.FC.var['mainpage_el']['RSVC_logo'])
            result.append(logo_img.is_displayed())

            bg_img = self.FC.loading_find_css(self.FC.var['mainpage_el']['RSVC_bg'])
            result.append(bg_img.is_displayed())

            img_el_list=self.FC.loading_find_csss(self.FC.var['mainpage_el']['RSVC_content'])
            result.append([img.is_displayed() for img in img_el_list])

            assert self.DBG.print_res(result), self.DBG.logger.debug("메인 > 유독 컨텐츠 정상 노출 확인 실패")

            # 요금제 영역 콘텐츠 정상 출력 확인
            self.FC.scroll(7)
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mainpage_el']['plan']))
            plan_list=self.FC.loading_find_csss(self.FC.var['mainpage_el']['plan_content'])
            if len(kv_list) == 1:
                assert len(plan_list) == 3, self.DBG.logger.debug("메인 > 요금제 컨텐츠 정상 노출 확인 실패")
            else:
                assert len(plan_list) == 4,self.DBG.logger.debug("메인 > 요금제 컨텐츠 정상 노출 확인 실패")

            # 유잼 영역 콘텐츠 정상 출력 확인
            self.FC.scroll(8)
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mainpage_el']['company']))
            contents_list=self.FC.loading_find_csss(self.FC.var['mainpage_el']['company_content'])
            assert len(contents_list) == 3,self.DBG.logger.debug("메인 > 유잼 콘텐츠 정상 노출 확인 실패")

        

        except Exception:
            self.DBG.print_dbg("메인 페이지 정상 노출 확인",False)
            return False

        else :
            self.DBG.print_dbg("메인 페이지 정상 노출 확인")
            return True
