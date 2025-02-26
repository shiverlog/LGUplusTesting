import time
import json
import random

from selenium.webdriver.support.select import Select

from base.appdriver import AppDriver
from base.server import AppiumServer

from common.function import Function
from common.debug import Debug


class MobilePage():
    def __init__(self,AppDriver:AppDriver,FC:Function):
        self.driver=AppDriver.driver
        self.FC=FC
        self.DBG=Debug(AppDriver)
        
    def mobile(self):
        self.FC.gotoHome()
        try:
            # 메인 >  모바일기기 > 바로가기
            self.FC.movepage(self.FC.var['mobile_el']['mobile'], self.FC.var['mobile_el']['direct'],address=self.FC.var['mobile_el']['url'])

           # KV 콘텐츠 정상 출력 확인
            kv_list=self.FC.loading_find_csss(self.FC.var['mobile_el']['KV_링크'])
            assert len(kv_list) > 0, self.DBG.logger.debug("모바일 > 서브메인 > KV 정상 출력 실패") 
            
            # 서브메인 테마배너
            check_text_list=['휴대폰','요금제','유심','모델별 지원금','해외로밍']
            assert self.FC.text_list_in_element(self.FC.var['mobile_el']['테마배너'],check_text_list),self.DBG.logger.debug("모바일 > 서브메인 > 테마베너 정상 출력 실패") 
            # 노답 구간 ----------------------------------------
            time.sleep(3)
            theme_list_link=self.FC.loading_find_csss(self.FC.var['mobile_el']['테마배너_링크'])
            random_num= random.randrange(0,len(theme_list_link))
            check_link=theme_list_link[random_num].get_attribute('href')
            check_link=check_link[check_link.rfind('/'):]
            tab_name= theme_list_link[random_num].get_attribute('data-gtm-click-text')
            self.FC.move_to_click(theme_list_link[random_num])
            time.sleep(3)
            # 노답 구간 ----------------------------------------
            assert check_link in self.FC.driver.current_url,self.DBG.logger.debug(f"모바일 > 서브메인 > 테마베너 > {tab_name}탭 정상 동작 실패")
            self.FC.goto_url(self.FC.var['mobile_el']['url'])
            
            # 이벤트 영역에서 콘텐츠 정상 출력 및 클릭 시, 정상 이동 확인
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['이벤트_title']))
            self.FC.click_until_go_page(self.FC.loading_find_css(self.FC.var['mobile_el']['이벤트_title']))
            assert self.FC.var['benefit_el']['진행 중인 이벤트_url'] in self.FC.driver.current_url,self.DBG.logger.debug("모바일 > 서브메인 > 이벤트 타이틀 기능 정상 동작 실패 ")
            self.FC.goto_url(self.FC.var['mobile_el']['url'])
            
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['이벤트'])) 
            event_list = self.FC.loading_find_csss(self.FC.var['mobile_el']['이벤트_콘텐츠'])
            assert len(event_list) == 4, self.DBG.logger.debug("모바일 > 서브메인 > 이벤트 콘텐츠 4개 노출 실패 ")


            # 휴대폰 영역 기능 및 콘텐츠 정상 노출 확인
            # 휴대폰 타이틀 링크 이동 확인
            self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['mobile_el']['휴대폰_title']))
            assert self.FC.var['mobile_el']['모바일기기_휴대폰_url'] in self.FC.driver.current_url,self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 > 타이틀 클릭 시, 정상 이동 실패")
            self.FC.goto_url(self.FC.var['mobile_el']['url'])

            # # 휴대폰 탭 메뉴 정상 노출
            tab_list_el=self.FC.loading_find_csss(self.FC.var['mobile_el']['휴대폰_탭_링크'])
            tab_list=['추천','삼성','Apple','가성비폰']
            for tab in tab_list_el:
                num=tab_list_el.index(tab)
                assert tab_list[num] in tab.get_property('innerText'),self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 > 탭 정상 노출 실패")

                self.FC.move_to_click(tab)
                self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['휴대폰_panel'])) 
                 
                self.FC.wait_datas(self.FC.var['mobile_el']['휴대폰_panel'],'p.big-title')
                list=self.FC.loading_find_csss(self.FC.var['mobile_el']['휴대폰_panel_주문하기'])
                assert len(list) > 0,self.DBG.logger.debug(f"모바일 > 서브메인 > 휴대폰 > {tab_list[num]}탭 콘텐츠 정상 노출 실패")
                
            # 임의 상품 이동
            self.FC.move_to_click(tab_list_el[0])
            # time.sleep(1) # 애니메이션 대기
            carousel=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['휴대폰_panel'])
            list=self.FC.loading_find_csss(self.FC.var['mobile_el']['휴대폰_panel_상품명'])
            random_num=random.randrange(0,len(list))
            for n in range(random_num):                                           
                x=int(round(self.FC.driver.get_screen_size().get('width')/2))
                y=carousel.location.get('y') + 100
                self.FC.driver.swipe(x+100,y,x-100,y,300)
                 
            titles=self.FC.loading_find_csss(self.FC.var['mobile_el']['휴대폰_panel_상품명'])
            title=titles[random_num].get_property('innerText')
            if 'Z Flip5' in title:
                title ='갤럭시 Z Flip 5'
            self.FC.click_until_go_page(self.FC.var['mobile_el']['휴대폰_panel_주문하기'])
            title_text=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['기기상품상세_title']).get_property('innerText')
            assert title in title_text, self.DBG.logger.debug(f"모바일 > 서브메인 > 휴대폰 > {title} 상품 정상 이동 실패")
            self.FC.goto_url(self.FC.var['mobile_el']['url'])

            # 추천 요금제
            # 추천 요금제 타이틀 링크
            self.FC.scroll(2)
            self.FC.scroll2_v2(self.FC.var['mobile_el']['추천 요금제'])
            self.FC.click_until_go_page(self.FC.loading_find_css(self.FC.var['mobile_el']['추천 요금제_title']))
            assert self.FC.var['mobile_el']['모바일요금제_요금제_url'] in self.FC.driver.current_url,self.DBG.logger.debug(f"모바일 > 서브메인 > 요금제 > 타이틀 정상 이동 실패")
            self.FC.goto_url(self.FC.var['mobile_el']['url'])
            
            # 추천요금제 임의 상품 링크 이동
            self.FC.scroll2_v2(self.FC.var['mobile_el']['추천 요금제'])
            list=self.FC.loading_find_csss(self.FC.var['mobile_el']['추천 요금제_링크'])
            random_num=random.randrange(0,len(list)-1)# 요금제 더보기 제외  
            carousel=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['추천 요금졔_panel'])
            self.FC.wait_datas(self.FC.var['mobile_el']['추천 요금제_링크'],'p')
            self.FC.scroll_x(list[random_num])
            for n in range(random_num):                                          
                x=int(round(self.FC.driver.get_screen_size().get('width')/2))
                y=carousel.location.get('y') + 100
                self.FC.driver.swipe(x+100,y,x-100,y,300)
                 

            json_data=list[random_num].get_attribute('data-ec-product')
            data=json.loads(json_data)
            title=data['ecom_prd_name']
            # price=str(data['ecom_prd_price'])[:-3]+','+str(data['ecom_prd_price'])[-3:-1]

            list=self.FC.loading_find_csss(self.FC.var['mobile_el']['추천 요금제_링크'])
            self.FC.click_until_go_page(list[random_num])
                    
            title_text=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['요금제상품상세_title']).get_property('innerText')
            # price_text=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['요금제상품상세_price']).get_property('innerText')
            # assert title in title_text and price in price_text,self.DBG.logger.debug(f"모바일 > 서브메인 > 요금제 > {title} 상품 정상 이동 실패")
            assert title in title_text ,self.DBG.logger.debug(f"모바일 > 서브메인 > 요금제 > {title} 상품 정상 이동 실패")
            self.FC.goto_url(self.FC.var['mobile_el']['url'])

            # 결합할인 영역 없어짐 25.01.02
        #     # 휴대폰 결합 할인 계산 영역 콘텐츠 노출 확인
        #     # Select.select_by_index()가 ElementNotInteractableException: Message: element not interactable: Element is not currently visible and may not be manipulated 오류로 Keys.Down으로 대체
        #     # 가입 상담 신청 버튼 노출 확인
        #     self.FC.swipe(self.FC.var['mobile_el']['휴대폰결합상품'],'true')
        #     self.FC.wait_loading()
        #     # time.sleep(1.5) # 애니메이션 대기
        #     button=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['가입상담신청_btn'])
        #     self.FC.scroll2_v2(button) 
             
        #     assert button !=None ,self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 결합 할인 계산 영역의 가입상담 신청 버튼 노출 실패 ")

        #     # 휴대폰/인터넷/IPTV 드롭다운 선택 후 가입 상담 신청 시, 임의 선택한 데이터 정상 노출 확인(선택한 데이터:check_list)
        #     self.FC.loading_find_css(self.FC.var['mobile_el']['휴대폰결합상품_select'])
        #     select_list=self.FC.loading_find_csss(self.FC.var['mobile_el']['휴대폰결합상품_select'])
        #     for select in select_list:      # 무작위로 option 선택
        #         current_select=Select(select)
        #         random_num=random.randrange(0,len(current_select.options))
        #         print(f"random num => {random_num}")
        #         if random_num !=0:
        #             # self.FC.redefinition_v2(select).re_click()
        #             select.click()
        #             self.FC.switch_view('NATIVE_APP')
        #             self.FC.loading_find_chains('**/XCUIElementTypeCell/XCUIElementTypeButton')[random_num].click()
        #             self.FC.switch_view()
        #             # time.sleep(.5)
        #             self.FC.wait_loading()

        #         else:
        #             pass
        #     price_value=self.FC.loading_find_csss(self.FC.var['mobile_el']['휴대폰결합상품_value'])
        #     check_value=[]
        #     for n in range(0,len(price_value)):
        #         check_value.append(price_value[n].get_property('innerText').replace('원',''))            
        #     print(f"check_value => {str(check_value)}")

        #     count=0
        #     while True:
        #         self.FC.scroll2_v2(self.FC.var['mobile_el']['가입상담신청_btn']).re_click()
        #         # self.FC.wait_loading()
        #         time.sleep(1)
        #         count+=1
        #         print(f"현재 페이지 views -> {str(self.driver.contexts)}")
        #         if len(self.driver.contexts) >2:
        #             break
        #         assert count <= 4, print('while 무한 반복 오류')
            
        #    # 가입상담 신청 팝업창으로 들어옮 (팝업창 핸들러 실행)
           
        #     time.sleep(3)
        #     if len(self.driver.contexts) ==2:
        #         print(f"컨텍스트 두개")
        #         for context in self.driver.contexts:
        #             if context != 'NATIVE_APP':
        #                 self.FC.switch_view(context)
        #                 print(f"current_url -> {self.driver.current_url}")
        #                 break
        #     elif len(self.driver.contexts) >2:
        #         print(f"컨텍스트 두개 이상")
        #         for context in self.driver.contexts:
        #             if context != 'NATIVE_APP' and context != self.FC.default_webview : 
        #                 self.FC.driver.activate_app('com.apple.mobilesafari')
        #                 self.FC.switch_view(context)
        #                 print(f"current_url -> {self.driver.current_url}")
        #                 if 'shopevent.uplus.co.kr' in self.FC.driver.current_url :
        #                     break
        #                 else: continue
        #     # for context in self.driver.contexts:
        #     #     if context != 'NATIVE_APP' and context != self.FC.default_webview : 
        #     #         self.FC.switch_view(context)
        #     #         print(f"current_url -> {self.FC.driver.current_url}")
        #     print('---------------------------')
        #     print(f"{self.FC.driver.contexts} -> {self.FC.driver.current_context}")
        #     print(self.FC.driver.current_url)
        #     print('---------------------------')
        #     self.FC.wait_loading()
        #     title= self.FC.loading_find_css(self.FC.var['mobile_el']['가입상담신청_팝업_타이틀']).get_property('innerText')  #상담 신청
        #     assert "상담 신청" in title and self.FC.loading_find_css_pre(self.FC.var['mobile_el']['가입상담신청_팝업_고객명']) and self.FC.loading_find_css_pre(self.FC.var['mobile_el']['가입상담신청_팝업_휴대폰번호']) and self.FC.loading_find_css_pre(self.FC.var['mobile_el']['가입상담신청_팝업_개인정보_동의']), self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 결합 할인 계산 영역의 가입상담 신청 팝업 > 콘텐츠 정상 노출 실패 ")

        #     self.FC.loading_find_css(self.FC.var['mobile_el']['가입상담신청_팝업_data_load'])   # 로딩
        #     price_list=self.FC.loading_find_csss(self.FC.var['mobile_el']['가입상담신청_팝업_data'])
        #     print(f"price_list ========================================>")
        #     print(price_list)
        #     for num in range(0,len(check_value)):
        #         # 홀수
        #         print(f"{check_value[num]} in {price_list[num].get_property('innerText')}")
        #         assert check_value[num] in price_list[num].get_property('innerText'),self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 결합 할인 계산 영역의 가입상담 신청 팝업 > select data 정상 노출 실패 ")
            
        #     self.FC.driver.activate_app(self.FC.var['common_el']['app'])
        #     time.sleep(3)# context 대기
        #     self.FC.switch_view()
        #     time.sleep(3)# context 대기

            # 태블릿/스마트워치
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['태블릿'])) 
            self.FC.click_until_go_page(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['태블릿_title']))
             
            assert self.FC.var['mobile_el']['모바일기기_태블릿_url'] in self.FC.driver.current_url,self.DBG.logger.debug("모바일 > 서브메인 > 태블릿/스마트워치 > 타이틀 정상 이동 실패")
            self.FC.goto_url(self.FC.var['mobile_el']['url'])

            # self.FC.swipe(4)
            # 태블릿/스마트워치 탭 메뉴 정상 노출
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['태블릿']))
            tab_list_el=self.FC.loading_find_csss(self.FC.var['mobile_el']['태블릿_탭_링크'])
            tab_list=['추천','삼성','Apple']
            for tab in tab_list_el:
                num=tab_list_el.index(tab)
                assert tab_list[num] in tab.get_property('innerText'),self.DBG.logger.debug("모바일 > 서브메인 > 태블릿/스마트워치 > 탭 정상 노출 실패")
                tab.re_double_click() 
                 
                # self.FC.wait_datas(self.FC.var['mobile_el']['태블릿_panel'],'p.big-title')
                list=self.FC.loading_find_csss(self.FC.var['mobile_el']['태블릿_panel_상품명'])
                assert len(list) > 0,self.DBG.logger.debug(f"모바일 > 서브메인 > 태블릿/스마트워치 > {tab_list[num]}탭 콘텐츠 정상 노출 실패")

            # 임의 상품 이동
            self.FC.scroll2_v2(tab_list_el[0]).re_click()
            self.FC.wait_loading()
            # time.sleep(1) # 애니메이션 대기
            carousel=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['태블릿_panel'])
            list=self.FC.loading_find_csss(self.FC.var['mobile_el']['태블릿_panel_상품명'])
            random_num=random.randrange(0,len(list))
            for n in range(random_num):
                x=int(round(self.FC.driver.get_screen_size().get('width')/2))
                y=carousel.location.get('y') + 100
                self.FC.driver.swipe(x+100,y,x-100,y,300)

            titles=self.FC.loading_find_csss(self.FC.var['mobile_el']['태블릿_panel_상품명'])
            title=titles[random_num].get_property('innerText')
            self.FC.click_until_go_page(self.FC.loading_find_css(self.FC.var['mobile_el']['태블릿_panel_주문하기']))
            title_text=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['기기상품상세_title']).get_property('innerText')
            assert title in title_text, self.DBG.logger.debug(f"모바일 > 서브메인 > 태블릿/스마트워치 > {title} 상품 정상 이동 실패")
            self.FC.goto_url(self.FC.var['mobile_el']['url'])

            # 하위메뉴
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['하위메뉴_panel_콘텐츠'])) 
            self.FC.wait_loading()
            self.FC.scroll_x(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['하위메뉴_panel_콘텐츠']))# 제휴팩 체크에서 챗봇 상담 UI와 겹침으로 인한 클릭 오류 발생 방지

            check_text_tab_list=['매장에서 받기','7% 추가요금 할인','다이렉트 요금제','유심 가입','결합 할인','제휴카드 할인','제휴팩']
            for num in range(0,len(check_text_tab_list)):
                # 1트
                tab_list=self.FC.loading_find_csss(self.FC.var['mobile_el']['하위메뉴_탭_링크'])
                tab_list[num].re_double_click() 
                self.FC.wait_loading()
                # 2트
                tab_list=self.FC.loading_find_csss(self.FC.var['mobile_el']['하위메뉴_탭_링크'])
                tab_list[num].re_double_click() 
                self.FC.wait_loading()

                tab_panel_con=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['하위메뉴_panel_콘텐츠']).get_attribute('alt')
                assert check_text_tab_list[num] in tab_panel_con, self.DBG.logger.debug("모바일 > 서브메인 > 하위메뉴 > 탭 콘텐츠 정상 출력 실패 ")

            # 구매후기 영역 출력 및 링크 이동 정상 확인
            review_section=self.FC.loading_find_css(self.FC.var['mobile_el']['구매후기'])
            self.FC.scroll2_v2(review_section) 
             
            review_tap=self.FC.loading_find_csss(self.FC.var['mobile_el']['구매후기_tab_list'])
            # check_text=['일반 구매 후기','전문가 리뷰'] #TODO DCBGQA-557 이슈로 인해 일시 주석처리
            check_text=['일반 구매 후기']
            for num in range(0,len(check_text)):
                self.FC.scroll2_v2(review_tap[num]).re_click() 
                 
                text= review_tap[num].get_property('innerText')
                assert check_text[num] in text, self.DBG.logger.debug("모바일 > 서브메인 > 구매 후기 영역 탭 정상 출력 실패 ")
                views=self.FC.loading_find_csss(self.FC.var['mobile_el']['구매후기_콘텐츠'])
                assert len(views) >= 1, self.DBG.logger.debug(f"모바일 > 서브메인 > 구매 후기({check_text[num]}) 정상 출력 실패 ")
                # for item in views:
                #     item_children=self.driver.execute_script("return arguments[0].children;", item)
                #     assert len(item_children) >0 and item.get_property('innerText') != "", self.DBG.logger.debug(f"모바일 > 서브메인 > 구매 후기({check_text[num]}) > 정상 출력 실패  ")
        

        except  Exception :
            self.DBG.print_dbg("모바일기기 페이지 정상 노출 및 이벤트 링크 이동 및 상품 페이지 정상 이동 동작 확인",False)
            if self.driver.current_context != 'NATIVE_APP' or self.driver.current_context != self.FC.default_webview : 
                self.FC.driver.activate_app(self.FC.var['common_el']['app'])
                self.FC.switch_view()
            return False

        else :
            self.DBG.print_dbg("모바일기기 페이지 정상 노출 및 이벤트 링크 이동 및 상품 페이지 정상 이동 동작 확인")
            return True


      # 모바일 > 모바일 요금제
    def mobile_plan(self):
        self.FC.gotoHome()
        try:
            self.FC.movepage(self.FC.var['mobile_el']['mobile'],self.FC.var['mobile_el']['모바일요금제_5g'],address=self.FC.var['mobile_el']['5g_url'])

            # 상단 사용중인 요금제 정보 정상 확인 
            result=[]
            self.FC.move_to_click(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['사용중인_요금제_정보_btn']))
            text_list=['월정액','데이터']
            result.append(self.FC.text_list_in_element(self.FC.var['mobile_el']['사용중인_요금제_정보'],text_list))
            result.append(self.FC.wait_datas(self.FC.var['mobile_el']['사용중인_요금제_정보'],'p','strong'))
            my_plan_name = self.FC.loading_find_css_pre(self.FC.var['mobile_el']['사용중인_요금제명']).get_property('innerText')
            assert self.DBG.print_res(result),self.DBG.logger.debug("모바일 > 모바일 요금제 > 5G > 상단 사용중인 요금제 정보 정상 출력 실패")

            # 탭 페이지 이동 확인
            result.clear()
            tab_keys = ['lte','태블릿/스마트워치','듀얼넘버','5g']
            for key in tab_keys:
                self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['mobile_el'][f'{key}_tab']))
                result.append(self.FC.var['mobile_el'][f'{key}_url'] in self.FC.driver.current_url)
            assert self.DBG.print_res(result),self.DBG.logger.debug(f"모바일 > 모바일 요금제 > 5G > {key}탭 정상 이동 및 콘텐츠 확인 실패")
            
             # 임의 요금제 비교하기
            result.clear()
            btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['요금제_비교하기'])
            random_num = random.randrange(0,len(btns))
            # 요금제 정보
            datas ={
                '요금제명': None,
                '가격': None,
                '할인가격': None,
            }
            compare_plan_name = self.FC.loading_find_csss(self.FC.var['mobile_el'][f'요금제_list_요금제명'])[random_num].get_property('innerText')
            if my_plan_name in compare_plan_name and random_num == (len(btns) - 1):
                random_num -= 1
            elif my_plan_name in compare_plan_name and random_num < len(btns):
                random_num += 1

            for key in datas.keys():
                datas[key] = self.FC.loading_find_csss(self.FC.var['mobile_el'][f'요금제_list_{key}'])[random_num].get_property('innerText').strip().replace(' 원','').split('월')[-1].lstrip()
            # self.FC.move_to_click(btns[random_num])
            # if self.FC.loading_find_css(self.FC.var['mobile_el']['요금제_비교하기_팝업_확인']):
            #     self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['mobile_el']['요금제_비교하기_팝업_확인']))
            #     random_num-=1
            #     datas ={
            #     '요금제명': None,
            #     '가격': None,
            #     '할인가격': None,
            #     }
            #     for key in datas.keys():
            #         print(self.FC.loading_find_csss(self.FC.var['mobile_el'][f'요금제_list_{key}'])[random_num].get_property('innerText'))
            #         datas[key] = self.FC.loading_find_csss(self.FC.var['mobile_el'][f'요금제_list_{key}'])[random_num].get_property('innerText').strip().replace(' 원','').split('월')[-1].lstrip()
            self.FC.move_to_click(btns[random_num])
            for key in datas.keys():
                print(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['요금제비교함_신청하기_버튼']).get_attribute('disabled'))
                if self.FC.loading_find_css_pre(self.FC.var['mobile_el']['요금제비교함_신청하기_버튼']).get_attribute('disabled') == 'disabled':
                    self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['common_el']['이전화면']))
                    self.FC.move_to_click(btns[random_num])
                else:
                    pass

                result.append(datas[key] in self.FC.loading_find_css_pre(self.FC.var['mobile_el'][f'요금제비교함_{key}']).get_property('innerText'))
                
            result.append(self.FC.wait_datas(self.FC.var['mobile_el']['요금제비교함'],'p:not(.small)','strong'))
            assert self.DBG.print_res(result),self.DBG.logger.debug(f"모바일 > 모바일 요금제 > 5G > 요금제 비교하기 > 비교함 {datas['요금제명']} 정상 노출 확인 실패")
            # 요금제 비교함 > 비교 요금제 드롭다운 변경
            self.FC.loading_find_css(self.FC.var['mobile_el']['요금제비교함_드롭다운']).re_click()
            dropdown_list =self.FC.loading_find_csss(self.FC.var['mobile_el']['요금제비교함_드롭다운_list'])
            random_num = random.randrange(0,len(dropdown_list))
            check_title = dropdown_list[random_num].get_property('innerText')
            self.FC.scroll_x(dropdown_list[random_num]).re_click()
            self.FC.loading_find_css(self.FC.var['mobile_el']['요금제비교함_드롭다운_추가하기']).re_click()
            assert check_title in self.FC.loading_find_css_pre(self.FC.var['mobile_el']['요금제비교함_요금제명']).get_property('innerText'),self.DBG.logger.debug(f"모바일 > 모바일 요금제 > 5G > 요금제 비교하기 > 비교함 {check_title} 드롭다운 변경 기능 정상 동작 실패")
            self.FC.goto_url(self.FC.var['mobile_el']['5g_url'])

            # 모바일 > 모바일 요금제 > 요금제 변경
            result.clear()
            btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['요금제_변경하기'])
            random_num = 0
            # 요금제 정보
            datas ={
                '요금제명': None,
                '가격': None,
                '할인가격': None,
            }
            compare_plan_name = self.FC.loading_find_csss(self.FC.var['mobile_el'][f'요금제_list_요금제명'])[random_num].get_property('innerText')
            if my_plan_name in compare_plan_name and random_num == (len(btns) - 1):
                random_num -= 1
            elif my_plan_name in compare_plan_name and random_num < len(btns):
                random_num += 1
            for key in datas.keys():
                datas[key] = self.FC.loading_find_csss(self.FC.var['mobile_el'][f'요금제_list_{key}'])[random_num].get_property('innerText').strip().replace(' 원','').split('월')[-1].lstrip()
            self.FC.move_to_click(btns[random_num])
            
            if self.FC.loading_find_css(self.FC.var['mobile_el']['다음_버튼']):
                if self.FC.loading_find_csss(self.FC.var['mobile_el']['혜택_선택_list']) == False:
                    pass
                # 프리미엄 혜택
                elif '프리미엄' in self.FC.loading_find_css_pre(self.FC.var['mobile_el']['혜택_title']).get_property('innerText'):
                    btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['혜택_선택_list'])
                    self.FC.wait_loading()
                    for i in range(0, len(btns)):
                        if btns[i].get_attribute('alt') == '일리커피구독':
                            btns[i].re_click()
                            break
                    self.FC.loading_find_css(self.FC.var['mobile_el']['다음_버튼']).re_click()
                # 미디어 혜택
                elif '미디어' in self.FC.loading_find_css_pre(self.FC.var['mobile_el']['혜택_title']).get_property('innerText'):
                    btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['혜택_선택_list'])
                    self.FC.wait_loading()
                    time.sleep(1)
                    # btns[random.randrange(0, len(btns))].re_click()
                    btns[0].re_click()
                    if self.FC.loading_find_css_pre(self.FC.var['mobile_el']['다음_버튼']).get_attribute('disabled') == "disabled":
                        btns[random.randrange(0, len(btns))].re_click()
                    self.FC.loading_find_css_pre(self.FC.var['mobile_el']['다음_버튼']).re_click()

            check_datas=self.FC.loading_find_csss(self.FC.var['mobile_el']['요금제_변경_data'])
            result.append(datas['요금제명'] in check_datas[0].get_property('innerText'))
            result.append(datas['가격'] in check_datas[2].get_property('innerText'))
            result.append(self.FC.var['mobile_el']['요금제조회변경_url'] in self.FC.driver.current_url)

            assert self.DBG.print_res(result) ,self.DBG.logger.debug(f"모바일 > 모바일 요금제 > 5G > 요금제 변경하기 > 요금제 조회/변경 페이지 정상 이동 실패")
            
        except  Exception:
            self.DBG.print_dbg("모바일 > 모바일 요금제 > 5G > 페이지 정상 노출 및 기능 확인",False)
            self.FC.close_popup(self.FC.driver.window_handles)
            return False

        else :
            self.DBG.print_dbg("모바일 > 모바일 요금제 > 5G 페이지 정상 노출 및 이벤트 링크 이동 및 상품 페이지 정상 이동 동작 확인") 
            return True
        

    # 모바일 > 모바일 기기 > 휴대폰
    def mobile_device(self):
        self.FC.gotoHome()
        try:
            self.FC.movepage(self.FC.var['mobile_el']['mobile'],self.FC.var['mobile_el']['mobile_device_phone'],address= self.FC.var['mobile_el']['phone_url'])
            self.FC.modal_ck()

            # 임의 랜덤 기기 신청하기 이동
            random_num =  random.randrange(0,10)
            select_btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['신청하기_btn'])
            self.FC.scroll_center(select_btns[random_num])
            select_btns[random_num].re_click()
            self.FC.wait_loading()
            self.FC.modal_ck()
            self.FC.wait_datas(self.FC.var['mobile_el']['phone_info'],self.FC.var['mobile_el']['phone_name'],self.FC.var['mobile_el']['phone_info2'])

            phone_name = self.FC.loading_find_css(self.FC.var['mobile_el']['phone_name']).get_property('innerText')

            # # 가입유형 클릭
            self.FC.move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_가입유형'])[0])

            phone_plan_btn = self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_요금제'])[0]
            self.FC.move_to_click(phone_plan_btn)
            phone_plan = phone_plan_btn.get_attribute('data-gtm-click-text')
            self.FC.is_exists_move_to_click(self.FC.loading_find_css(self.FC.var['mobile_el']['장바구니_요금제_특별혜택'])) # 요금제 추가 혜택

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_할인방법'])[0]) # 할인 방법

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_납부기간'])[0]) # 기기 할부

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_배송방법'])[0]) # 우체국 택배

            if self.FC.loading_find_csss(self.FC.var['mobile_el']['장바구니_멤버십혜택']) is True:
                self.FC.is_exists_move_to_click(self.FC.loading_find_csss(self.FC.var['mobile_el']['장바구니_멤버십혜택'])[1]) # VIP 멤버십 혜택
                
            if self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_사은품']):
                btns = self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_사은품'])
                for btn in btns:
                    if btn.get_attribute('disabled'):
                        pass
                    else:
                        self.FC.move_to_click(btn)
                        break

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_추가혜택'])[0]) # 혜택

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_제휴카드'])[0]) # 제휴카드

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_추가할인'])[0]) # 추가 할인 혜택


            phone_price = self.FC.loading_find_css(self.FC.var['mobile_el']['phone_price']).get_property('innerText')

            # 장바구니 바로가기
            self.FC.loading_find_css(self.FC.var['mobile_el']['장바구니_btn']).re_click()
            self.FC.loading_find_css(self.FC.var['mobile_el']['장바구니로_이동_btn']).re_click()
            self.FC.wait_loading()
            assert self.FC.driver.current_url in self.FC.var['mobile_el']['장바구니_url'], self.DBG.logger.debug("모바일 > 모바일 기기 > 휴대폰 > 장바구니 이동 실패")
            
            cart_list = self.FC.loading_find_csss(self.FC.var['mobile_el']['장바구니_상품_영역'])
            is_text_in_cart=[]
            for cart in cart_list:
                res = all([True if text in cart.get_property('innerText') else False for text in [phone_name,phone_plan,phone_price]])
                is_text_in_cart.append(res)

            assert any(is_text_in_cart),self.DBG.logger.debug("모바일 > 모바일 기기 > 휴대폰 > 장바구니 기능 정상 동작 실패")
            idx = is_text_in_cart.index(True)
            del_btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['장바구니_삭제_버튼'])
            self.FC.move_to_click(del_btns[idx])
            del_confirm = self.FC.loading_find_css_pre(self.FC.var['mobile_el']['삭제_확인_버튼'])
            self.FC.move_to_click(del_confirm)
            self.FC.modal_ck2()


        except  Exception :

            self.DBG.print_dbg("모바일 > 모바일 기기 > 휴대폰 > 장바구니 기능",False)
            self.FC.modal_ck()
            return False

        else :
            self.DBG.print_dbg("모바일 > 모바일 기기 > 휴대폰 > 장바구니 기능")
            return True

if __name__ == "__main__":
    try:
        server = AppiumServer(4723)
        port = server.appium_service()
        if not server.waiting():
            raise Exception("서버 실행 불가")
        driver = AppDriver(port=port)
        fc = Function(driver)
        direct = MobilePage(driver,fc)

        fc.pre_script()
        
        direct.direct()
        driver.driver.quit()
        server.stop()
    except Exception as e:
        print(e)
        # os.system("lsof -P -i :4723 |awk NR==2'{print $2}'|xargs kill -9")
        # os.system(f"ios-deploy --kill --bundle_id com.lguplus.mobile.cs")
