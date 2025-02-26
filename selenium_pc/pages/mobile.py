import random
import json
from base.webdriver import WebDriver
from common.function import Function
from common.debug import Debug


class MobilePage():

    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)

    # 모바일 > 서브메인
    def mobile(self):
        self.FC.gotoHome()
        try:
            self.FC.movepage(self.FC.var['mobile_el']['mobile'],address= self.FC.var['mobile_el']['url'])
            self.FC.modal_ck4()

            # KV 콘텐츠 정상 출력 확인
            kv_list=self.FC.loading_find_csss(self.FC.var['mobile_el']['KV'])
            assert len(kv_list) >=1, self.DBG.logger.debug("모바일 > 서브메인 > KV 정상 출력 실패")

            # 서브메인 테마배너
            check_text_list=['휴대폰','요금제','유심','모델별 지원금','해외로밍']
            assert self.FC.text_list_in_element(self.FC.var['mobile_el']['테마배너'],check_text_list),self.DBG.logger.debug("모바일 > 서브메인 > 테마베너 정상 출력 실패")
            theme_list_link=self.FC.loading_find_csss(self.FC.var['mobile_el']['테마배너_링크'])
            random_num= random.randrange(0,len(theme_list_link))
            check_link=theme_list_link[random_num].get_attribute('href')
            check_link=check_link[check_link.rfind('/'):]
            tab_name= theme_list_link[random_num].get_attribute('data-gtm-click-text')
            self.FC.move_to_click(theme_list_link[random_num],True)
            assert check_link in self.FC.driver.current_url,self.DBG.logger.debug("모바일 > 서브메인 > 테마베너 > %s탭 정상 동작 실패", tab_name)
            self.FC.goto_url(self.FC.var['mobile_el']['url'])

            # 이벤트 영역에서 콘텐츠 정상 출력 및 클릭 시, 정상 이동 확인
            self.FC.con_check(self.FC.var['mobile_el'],'이벤트list','모바일')

            # 이벤트 전체보기
            self.FC.full_view(self.FC.var['mobile_el'],'이벤트_전체보기','이벤트상세_전체영역','진행중인 이벤트_url','url')

            # # 휴대폰 영역
            self.FC.scroll(4)
            tab_list_el=self.FC.loading_find_csss(self.FC.var['mobile_el']['휴대폰_tab'])
            tab_list=['추천','삼성','Apple','가성비폰']
            for tab in tab_list_el:
                num=tab_list_el.index(tab)
                assert tab_list[num] in tab.get_property('innerText'),self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 > 탭 정상 노출 실패")
                self.FC.move_to_click(tab)

            # 휴대폰 영역(추천 탭)에서 임의 상품 정상 이동 확인
            tab_list_el[0].click()
            self.FC.wait_loading()
            phone_list=self.FC.loading_find_csss(self.FC.var['mobile_el']['휴대폰_panel_주문하기'])
            random_num=random.randrange(4,8)
            titles=self.FC.loading_find_csss(self.FC.var['mobile_el']['휴대폰_panel_상품명'])
            title=titles[random_num].get_property('innerText').replace(" ", "")

            self.FC.move_to_click(phone_list[random_num])
            title_text=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['휴대폰_상세_상품명']).get_property('innerText').replace(" ", "")

            assert title in title_text, self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 > %s 상품 정상 이동 실패", title)
            self.FC.goto_url(self.FC.var['mobile_el']['url'])

            # 추천요금제 더보기 이동
            plan_list = self.FC.loading_find_csss(self.FC.var['mobile_el']['추천요금제_리스트'])
            self.FC.move_to_element(plan_list[0])
            all_btn = self.FC.loading_find_css(self.FC.var['mobile_el']['추천요금제_더보기'])
            self.FC.move_to_click(all_btn)
            assert self.FC.driver.current_url in self.FC.var['mobile_el']['5g_url'], self.DBG.logger.debug("모바일 > 서브메인 > 추천요금제 > 타이틀 정상 이동 실패")
            self.FC.goto_url(self.FC.var['mobile_el']['url'])

            # 추천요금제 임의 상품 링크 이동
            plan_list=self.FC.loading_find_csss(self.FC.var['mobile_el']['추천요금제_리스트'])
            self.FC.move_to_element(plan_list[0])
            random_num=random.randrange(0,len(plan_list))

            json_data=plan_list[random_num].get_attribute('data-ec-product')
            data=json.loads(json_data)
            title=data['ecom_prd_name']

            self.FC.move_to_click(plan_list[random_num])
            title_text=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['요금제상품상세_title']).get_property('innerText')

            assert title in title_text, self.DBG.logger.debug("모바일 > 서브메인 > 요금제 > %s 상품 정상 이동 실패", title)
            self.FC.goto_url(self.FC.var['mobile_el']['url'])

            # 결합할인 영역 없어짐 25.01.02
            # # 휴대폰 결합 할인 계산 영역 콘텐츠 노출 확인
            # # Select.select_by_index()가 ElementNotInteractableException: Message: element not interactable: Element is not currently visible and may not be manipulated 오류로 Keys.Down으로 대체
            # self.FC.scroll(4)
            # button=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['결합 할인_상담 신청 버튼'])
            # self.FC.move_to_element(button)
            # assert button is not None, self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 결합 할인 계산 > 가입상담 신청 버튼 노출 실패 ")

            # # 휴대폰/인터넷/IPTV 드롭다운 선택 후 가입 상담 신청 시, 임의 선택한 데이터 정상 노출 확인(선택한 데이터:check_list)
            # select_list_el = self.FC.loading_find_csss(self.FC.var['mobile_el']['결합 할인_드롭다운'])
            # for select in select_list_el:
            #     self.FC.move_to_click(select)
            #     select_ul_el = self.FC.loading_find_csss(self.FC.var['mobile_el']['결합 할인_드롭다운_data'])
            #     random_num=random.randrange(0,len(select_ul_el))
            #     self.FC.move_to_click(select_ul_el[random_num])

            # price_value=self.FC.loading_find_csss(self.FC.var['mobile_el']['결합 할인_드롭다운_결과'])
            # check_value=[]
            # check_total_value=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['결합 할인_드롭다운_결과_total']).get_property('innerText')
            # for n in range(0,len(price_value)):
            #     check_value.append(price_value[n].get_property('innerText').split('\n')[-1])

            # while True:
            #     self.FC.move_to_click(button)
            #     if len(self.FC.driver.window_handles) >=2:
            #         break


            # # 가입상담 신청 팝업창으로 들어옮 (팝업창 핸들러 실행)
            # self.FC.driver.switch_to.window(self.FC.driver.window_handles[1])
            # title= self.FC.loading_find_css(self.FC.var['mobile_el']['가입상담신청_팝업_타이틀']).get_property('innerText')
            # # 입력창 정상 출력 확인
            # assert "상담 신청" in title and self.FC.loading_find_css(self.FC.var['mobile_el']['가입상담신청_팝업_이름입력창']) and self.FC.loading_find_css(self.FC.var['mobile_el']['가입상담신청_팝업_휴대폰번호']) and self.FC.loading_find_css(self.FC.var['mobile_el']['가입상담신청_팝업_개인정보동의']).is_displayed(), self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 결합 할인 계산 영역의 가입상담 신청 팝업 > 콘텐츠 정상 노출 실패 ")

            # self.FC.loading_find_css(self.FC.var['mobile_el']['가입상담신청_팝업_금액_로딩'])   # 로딩
            # price_list=self.FC.loading_find_csss(self.FC.var['mobile_el']['가입상담신청_팝업_금액'])
            # print("check_value : ", str(check_value), "\n", "price_list : ", str(price_list[0].get_property('innerText')), str(price_list[1].get_property('innerText')), str(price_list[2].get_property('innerText')))
            # for num in range(0,len(check_value)):
            #     assert check_value[num] in price_list[num].get_property('innerText'),self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 결합 할인 계산 영역의 가입상담 신청 팝업 > select data 정상 노출 실패 ")

            # assert check_total_value in self.FC.loading_find_css(self.FC.var['mobile_el']['가입상담신청_팝업_결합할인']).get_property('innerText'),self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 결합 할인 계산 영역의 가입상담 신청 팝업 > select data 정상 노출 실패 ")
            # self.FC.loading_find_css(self.FC.var['mobile_el']['가입상담신청_팝업_닫기버튼']).click()     # 창닫기
            # self.FC.driver.switch_to.window(self.FC.driver.window_handles[0])

            # # 탭 변경 시, 데이터 변동
            # self.FC.scroll(3)

            # 임의 태블릿/스마트워치/노트북 링크 이동
            tab_list_el=self.FC.loading_find_csss(self.FC.var['mobile_el']['태블릿_tab'])
            tab_list=['추천','삼성','Apple']
            for tab in tab_list_el:
                num=tab_list_el.index(tab)
                assert tab_list[num] in tab.get_property('innerText'),self.DBG.logger.debug("모바일 > 서브메인 > 태블릿/스마트워치 > 탭 정상 노출 실패")
                self.FC.move_to_click(tab)

            # 태블릿/스마트워치 영역(추천 탭)에서 임의 상품 정상 이동 확인
            tab_list_el[0].click()
            self.FC.wait_loading()
            tab_order_list=self.FC.loading_find_csss(self.FC.var['mobile_el']['태블릿_panel_주문하기'])
            random_num=random.randrange(0,3)
            titles=self.FC.loading_find_csss(self.FC.var['mobile_el']['태블릿_panel_상품명'])
            title=titles[random_num].get_property('innerText')
            self.FC.move_to_click(tab_order_list[random_num])
            title_text=self.FC.loading_find_css_pre(self.FC.var['mobile_el']['휴대폰_상세_상품명']).get_property('innerText')
            assert title in title_text, self.DBG.logger.debug("모바일 > 서브메인 > 휴대폰 > %s 상품 정상 이동 실패", title)
            self.FC.goto_url(self.FC.var['mobile_el']['url'])

            # 하위메뉴
            tab_list_el=self.FC.loading_find_csss(self.FC.var['mobile_el']['모바일이벤트_탭메뉴'])
            tab_list=['매장에서 받기','7% 추가요금 할인','다이렉트 요금제','유심 가입','결합할인','제휴카드할인','제휴팩']

            for tab in tab_list_el:
                num=tab_list_el.index(tab)
                assert tab_list[num] in tab.get_property('innerText'),self.DBG.logger.debug("모바일 > 서브메인 > 이벤트탭 > 탭 정상 노출 실패")
                self.FC.move_to_click(tab)
                self.FC.scroll(1) # 오류 시, 이미지를 정확하게 찍기 위함

            # 구매후기 영역 출력 및 링크 이동 정상 확인
            review_section=self.FC.loading_find_css(self.FC.var['mobile_el']['구매후기'])
            self.FC.move_to_element(review_section)
            review_tap=self.FC.loading_find_csss(self.FC.var['mobile_el']['구매후기_컨텐츠'])
            assert len(review_tap) >= 1, self.DBG.logger.debug("모바일 > 서브메인 > 구매 후기 정상 출력 실패 ")

        except  Exception :
            self.DBG.print_dbg("모바일 > 서브메인  페이지 정상 노출 및 이벤트 링크 이동 및 상품 페이지 정상 이동 동작 확인",False)
            self.FC.close_popup(self.FC.driver.window_handles)
            self.FC.modal_ck4()
            return False

        else :
            self.DBG.print_dbg("모바일 > 서브메인 페이지 정상 노출 및 이벤트 링크 이동 및 상품 페이지 정상 이동 동작 확인")
            return True

    # 모바일 > 모바일 요금제 > 5G
    def mobile_plan(self):
        self.FC.gotoHome()
        try:
            self.FC.movepage(self.FC.var['mobile_el']['mobile'],self.FC.var['mobile_el']['mobile_plan'],address= self.FC.var['mobile_el']['5g_url'])
            self.FC.modal_ck4()


            # 상단 사용중인 요금제 정보 정상 확인
            result=[]
            text_list=['이용중인 요금제','월정액','데이터']
            result.append(self.FC.text_list_in_element(self.FC.var['mobile_el']['사용중인_요금제_정보'],text_list))
            result.append(self.FC.wait_datas(self.FC.var['mobile_el']['사용중인_요금제_정보'],'dd'))
            my_plan_name = self.FC.loading_find_css(self.FC.var['mobile_el']['사용중인_요금제명']).get_property('innerText')
            assert self.DBG.print_res(result),self.DBG.logger.debug("모바일 > 모바일 요금제 > 5G > 상단 사용중인 요금제 정보 정상 출력 실패")

            # 탭 페이지 이동 확인
            result.clear()

            tab_keys = ['lte','태블릿/스마트워치','듀얼넘버','5g']
            for key in tab_keys:
                self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['mobile_el'][f'{key}_tab']))
                result.append(self.FC.var['mobile_el'][f'{key}_url'] in self.FC.driver.current_url)
            assert self.DBG.print_res(result),self.DBG.logger.debug("모바일 > 모바일 요금제 > 5G > %s탭 정상 이동 및 콘텐츠 확인 실패", key)

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

            compare_plan_name = self.FC.loading_find_csss(self.FC.var['mobile_el']['요금제_list_요금제명'])[random_num].get_property('innerText')
            if my_plan_name in compare_plan_name and random_num == (len(btns) - 1):
                random_num -= 1
            elif my_plan_name in compare_plan_name and random_num < len(btns):
                random_num += 1

            for key in datas:
                datas[key] = self.FC.loading_find_csss(self.FC.var['mobile_el'][f'요금제_list_{key}'])[random_num].get_property('innerText').strip().split('월')[-1]
            self.FC.move_to_click(btns[random_num])
            for key in datas:
                result.append(datas[key] in self.FC.loading_find_css_pre(self.FC.var['mobile_el'][f'요금제비교함_{key}']).get_property('innerText'))
            result.append(self.FC.wait_datas(self.FC.var['mobile_el']['요금제비교함'],'p:not(.small)','span:not(.small,.blind)'))
            assert self.DBG.print_res(result),self.DBG.logger.debug("모바일 > 모바일 요금제 > 5G > 요금제 비교하기 > 비교함 %s 정상 노출 확인 실패", datas['요금제명'])
            # 요금제 비교함 > 비교 요금제 드롭다운 변경
            self.FC.loading_find_css(self.FC.var['mobile_el']['요금제비교함_드롭다운']).click()
            dropdown_list =self.FC.loading_find_csss(self.FC.var['mobile_el']['요금제비교함_드롭다운_list'])
            # random_num = random.randrange(0,len(dropdown_list)) # FIXME 이슈로 차후 수정 필요 DCBGQA-3311
            random_num = random.randrange(0,5)
            check_title = dropdown_list[random_num].get_property('innerText')
            dropdown_list[random_num].click()
            self.FC.wait_loading()
            assert check_title in self.FC.loading_find_css_pre(self.FC.var['mobile_el']['요금제비교함_요금제명']).get_property('innerText'),self.DBG.logger.debug("모바일 > 모바일 요금제 > 5G > 요금제 비교하기 > 비교함 %s 드롭다운 변경 기능 정상 동작 실패", check_title)
            self.FC.goto_url(self.FC.var['mobile_el']['5g_url'])

            # 모바일 > 모바일 요금제 > 요금제 변경
            result.clear()
            self.FC.bring_el_to_front_csss(self.FC.var['mobile_el']['요금제_변경하기'])
            btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['요금제_변경하기'])
            random_num = random.randrange(0, len(btns))
            # 요금제 정보
            datas ={
                '요금제명': None,
                '가격': None,
                '할인가격': None,
            }

            compare_plan_name = self.FC.loading_find_csss(self.FC.var['mobile_el']['요금제_list_요금제명'])[random_num].get_property('innerText')
            if my_plan_name in compare_plan_name and random_num == (len(btns) - 1):
                random_num -= 1
            elif my_plan_name in compare_plan_name and random_num < len(btns):
                random_num += 1

            for key in datas:
                datas[key] = self.FC.loading_find_csss(self.FC.var['mobile_el'][f'요금제_list_{key}'])[random_num].get_property('innerText').strip().replace(' 원','').split('월')[-1].lstrip()
            self.FC.again_click(btns[random_num])

            if self.FC.loading_find_csss(self.FC.var['mobile_el']['혜택_선택_list']) == [False]:
                pass
            # 프리미엄 혜택
            elif '프리미엄' in self.FC.loading_find_css_pre(self.FC.var['mobile_el']['혜택_title']).get_property('innerText'):
                btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['혜택_선택_list'])
                for i in range(0, len(btns)):
                    if btns[i].get_attribute('alt') == '일리커피구독':
                        self.FC.move_to_click(btns[i])
                self.FC.move_to_click(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['다음_버튼']))
            # 미디어 혜택
            elif '미디어' in self.FC.loading_find_css_pre(self.FC.var['mobile_el']['혜택_title']).get_property('innerText'):
                btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['혜택_선택_list'])
                self.FC.move_to_click(btns[random.randrange(0, len(btns))])
                self.FC.move_to_click(self.FC.loading_find_css_pre(self.FC.var['mobile_el']['다음_버튼']))
            check_datas=self.FC.loading_find_csss(self.FC.var['mobile_el']['요금제_변경_data'])
            result.append(datas['요금제명'] in check_datas[0].get_property('innerText'))
            result.append(datas['가격'] in check_datas[2].get_property('innerText'))
            result.append(self.FC.var['mobile_el']['요금제조회변경_url'] in self.FC.driver.current_url)

            assert self.DBG.print_res(result) ,self.DBG.logger.debug("모바일 > 모바일 요금제 > 5G > 요금제 변경하기 > 요금제 조회/변경 페이지 정상 이동 실패")


        except  Exception :
            self.DBG.print_dbg("모바일 > 모바일 요금제 > 5G > 페이지 정상 노출 및 기능 확인",False)
            self.FC.close_popup(self.FC.driver.window_handles)
            self.FC.modal_ck4()
            return False

        else :
            self.DBG.print_dbg("모바일 > 모바일 요금제 > 5G 페이지 정상 노출 및 이벤트 링크 이동 및 상품 페이지 정상 이동 동작 확인")
            return True

    # 모바일 > 모바일 기기 > 휴대폰
    def mobile_device(self):
        self.FC.gotoHome()
        try:
            self.FC.movepage(self.FC.var['mobile_el']['mobile'],self.FC.var['mobile_el']['mobile_device'],address= self.FC.var['mobile_el']['phone_url'])
            self.FC.modal_ck4()

            # 임의 랜덤 기기 신청하기 이동
            random_num = random.randrange(0,10)
            select_btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['신청하기_btn'])
            self.FC.move_to_click(select_btns[random_num])
            self.FC.modal_ck()
            self.FC.wait_datas(self.FC.var['mobile_el']['phone_info'],self.FC.var['mobile_el']['phone_name'])

            result = []
            phone_name = self.FC.loading_find_css_pre(self.FC.var['mobile_el']['phone_name']).get_property('innerText').split('(')[0]

            self.FC.move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_가입유형'])[0],True)

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_요금제'])[0],True)

            phone_plan_btn = self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_요금제명'])[0]
            self.FC.move_to_click(phone_plan_btn,True)
            phone_plan = phone_plan_btn.get_property('innerText')

            self.FC.is_exists_move_to_click(self.FC.loading_find_css(self.FC.var['mobile_el']['장바구니_요금제_특별혜택'])) # 요금제 특별 혜택

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_할인방법'])[0],True) # 할인 방법

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_납부기간'])[0],True) # 할부금 납부 기간

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_제휴카드'])[0],True) # 제휴카드

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_추가할인'])[0],True) # 추가 할인 혜택

            if self.FC.loading_find_csss(self.FC.var['mobile_el']['장바구니_멤버십혜택']) is True:
                self.FC.is_exists_move_to_click(self.FC.loading_find_csss(self.FC.var['mobile_el']['장바구니_멤버십혜택'])[1]) # VIP 멤버십 혜택

            if self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_사은품']):
                btns = self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_사은품'])
                for btn in btns:
                    if btn.get_attribute('disabled'):
                        pass
                    else:
                        self.FC.move_to_click(btn, True)
                        break

            self.FC.is_exists_move_to_click(self.FC.loading_find_xpaths(self.FC.var['mobile_el']['장바구니_쇼핑쿠폰팩'])[0],True) # 쇼핑쿠폰팩

            phone_price = self.FC.loading_find_css(self.FC.var['mobile_el']['phone_price']).get_property('innerText')

            # 장바구니 바로가기
            self.FC.loading_find_csss(self.FC.var['mobile_el']['장바구니_btn'])[1].click()
            self.FC.loading_find_xpath(self.FC.var['mobile_el']['장바구니로_이동_btn']).click()
            self.FC.wait_loading()

            assert self.FC.driver.current_url in self.FC.var['mobile_el']['장바구니_url'], self.DBG.logger.debug("모바일 > 모바일 기기 > 휴대폰 > 장바구니 이동 실패")
            is_text_in_cart=[]
            cart_list = self.FC.loading_find_csss(self.FC.var['mobile_el']['장바구니_상품_영역'])
            is_text_in_cart=[]
            for cart in cart_list:
                res = all([True if text in cart.get_property('innerText') else False for text in [phone_name,phone_plan,phone_price]])
                is_text_in_cart.append(res)

            assert self.DBG.print_res(result),self.DBG.logger.debug("모바일 > 모바일 기기 > 휴대폰 > 장바구니 기능 정상 동작 실패")

            del_btns = self.FC.loading_find_csss(self.FC.var['mobile_el']['장바구니_삭제_버튼'])
            idx = is_text_in_cart.index(True)
            self.FC.move_to_click(del_btns[idx])
            del_confirm = self.FC.loading_find_css_pre(self.FC.var['mobile_el']['삭제_확인_버튼'])
            self.FC.move_to_click(del_confirm)
            self.FC.modal_ck4()

        except  Exception :
            self.DBG.print_dbg("모바일 > 모바일 기기 > 휴대폰 > 장바구니 기능 정상 동작",False)
            self.FC.close_popup(self.FC.driver.window_handles)
            self.FC.modal_ck4()
            return False

        else :
            self.DBG.print_dbg("모바일 > 모바일 기기 > 휴대폰 > 장바구니 기능 정상 동작")
            return True



if __name__ == "__main__":
    driver = WebDriver()
    fc = Function(driver)
    mobile = MobilePage(driver, fc)

    mobile.mobile()
