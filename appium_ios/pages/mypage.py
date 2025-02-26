from base.server import AppiumServer
from base.appdriver import AppDriver
from common.function import Function
from common.debug import Debug
import common.variable as var
from pages.login import LoginPage

class MypagePage():
    def __init__(self,AppDriver:AppDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(AppDriver)

    # 마이페이지 바로가기
    def mypage(self):           
        self.FC.gotoHome()
        try:
            # 상단 메뉴 진입
            # 메인 > 마이페이지 > 바로가기
            self.FC.movepage(var.mypage['mypage'],var.mypage['direct'],address=var.mypage['mypage_url'])

            # 액션 정상 동작 확인은 상단 청구서 더보기 버튼으로 모바일에서 인터넷으로 전환되는지 동작 확인
            payment_list=['모바일','인터넷','결합']
            for payment in payment_list:
                self.FC.wait_loading()
                # time.sleep(3)
                dropdown = self.FC.loading_find_css_pre(self.FC.var['mypage']['청구서_드롭다운'])
                self.FC.scroll2_v2(dropdown)
                self.FC.driver.execute_script("arguments[0].click();", dropdown)
                self.FC.wait_loading()
                dropdown_list=self.FC.loading_find_csss(self.FC.var['mypage']['청구서_list'])

                is_continue=False
                for list in dropdown_list:
                    # 드롭다운 리스트에 모바일/인터넷/결합 상품이 존재하는지 확인 후, 드롭다운 기능 확인
                    if payment in list.get_property('innerText'):
                        index=dropdown_list.index(list)
                        radio_button=self.FC.loading_find_csss(self.FC.var['mypage']['청구서_radio_btn'])
                        radio_button[index].re_click()
                        self.FC.loading_find_css_pre(self.FC.var['mypage']['청구서_하단_확인_버튼']).re_click()
                        self.FC.wait_loading()
                        mypage_info_text = self.FC.loading_find_css_pre(self.FC.var['mypage']['청구서_text']).get_property('innerText')      # 상단에 표시된 영역이 모바일인지 인터넷인지 확인
                        assert payment == mypage_info_text, self.DBG.logger.debug("마이페이지 > 서브메인 > 드롭다운 액션 오류(청구서 드롭다운 변경 실패)")
                        break
                    else:
                        # 드롭다운 리스트 마지막 요소에도 payment가 존재하지 않을 떄, 
                        if list == dropdown_list[-1] :
                            self.FC.loading_find_css_pre(self.FC.var['mypage']['청구서_하단_확인_버튼']).re_click()
                            is_continue=True
                            break
                        else:
                            pass
                    
                # 모바일/인터넷/결합 상품 정보가 없다면, 다음 로직은 무시
                if is_continue is True:
                    continue  

                text_list_result=[]

                # 콘텐츠 정상 출력 및 액션 정상 동작 확인 부분
                if "모바일" in mypage_info_text :
                    self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mypage']['모바일_정보']))
                    text_list=['총 제공량','사용량','잔여량']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['모바일_정보'], text_list))

                    self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mypage']['청구_및_납부_정보']))
                    text_list=['청구 및 납부정보','청구요금','모바일']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구_및_납부_정보'], text_list))

                    self.FC.scroll2_v2(self.FC.loading_find_xpath_pre(self.FC.var['mypage']['주문정보']))
                    text_list_result.append(self.FC.loading_find_xpath_pre(self.FC.var['mypage']['주문정보']).is_displayed())

                    self.FC.scroll2_v2(self.FC.loading_find_xpath_pre(self.FC.var['mypage']['가입서비스']))
                    text_list=['모바일']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['가입서비스'], text_list))

                    assert all(text_list_result) is True, self.DBG.logger.debug(f"마이페이지 > 서브메인 > {mypage_info_text} 컨텐츠 정상 노출 확인 실패")
                
                # TODO '인터넷' 청구서 정보를 가지고있는 계정 필요
                #...

                # 콘텐츠 정상 출력 및 액션 정상 동작 확인 부분
                text_list_result.clear()
                if "결합" in mypage_info_text :
                    self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mypage']['청구_및_납부_정보']))
                    text_list=['청구 및 납부정보','청구요금','결합']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구_및_납부_정보'], text_list))

                    self.FC.scroll2_v2(self.FC.loading_find_xpath_pre(self.FC.var['mypage']['주문정보']))
                    text_list_result.append(self.FC.loading_find_xpath_pre(self.FC.var['mypage']['주문정보']).is_displayed())

                    self.FC.scroll2_v2(self.FC.loading_find_xpath_pre(self.FC.var['mypage']['가입서비스']))
                    text_list=['모바일','인터넷','IPTV','인터넷전화','스마트홈','결합상품']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['가입서비스'], text_list))

                    text_list=['멤버십','사용 가능한 ez포인트' ]
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['멤버십_정보'], text_list))
                
                    assert all(text_list_result), self.DBG.logger.debug(f"마이페이지 > 서브메인 > {mypage_info_text} 컨텐츠 정상 노출 확인 실패")
            
        except  Exception :
            self.DBG.print_dbg("마이페이지 정상 노출 및 기능 동작 확인",False)
            return False

        else :
            self.DBG.print_dbg("마이페이지 정상 노출 및 기능 동작 확인")
            return True

    # 마이페이지 > 요금 조회/납부 > 요금 조회/납부 홈
    def mypage_bill(self):
        self.FC.gotoHome()
        try:
            self.FC.movepage(var.mypage['mypage'],var.mypage['bill_direct'],address=var.mypage['bill_url'])
            self.FC.move_to_click(self.FC.loading_find_css_pre(self.FC.var['mypage']['요금/납부_이동']))
            ## 마이페이지 > 요금 조회/납부 > 요금 조회/납부 홈 > 드롭다운 액션(청구서 변경)
            payment_list=['모바일','인터넷','결합']
            for payment in payment_list:
                dropdown = self.FC.loading_find_css(self.FC.var['mypage']['청구서_드롭다운'])
                self.FC.scroll2_v2(dropdown)
                self.FC.driver.execute_script("arguments[0].click();", dropdown)
                self.FC.wait_loading()
                dropdown_list=self.FC.loading_find_csss(self.FC.var['mypage']['청구서_list'])

                # 이중 for문 탈출 변수
                is_continue=False
                for list in dropdown_list:
                    # 드롭다운 리스트에 모바일/인터넷/결합 상품이 존재하는지 확인 후, 드롭다운 기능 확인
                    if payment == list.get_property('innerText'):
                        index=dropdown_list.index(list)
                        radio_button=self.FC.loading_find_csss(self.FC.var['mypage']['청구서_radio_btn'])
                        radio_button[index].re_click()
                        self.FC.loading_find_css_pre(self.FC.var['mypage']['청구서_하단_확인_버튼']).re_click()
                        self.FC.wait_loading()
                        # time.sleep(2)      #드롭다운 변경 후 반영 대기시간
                        mypage_info_text = self.FC.loading_find_css_pre(self.FC.var['mypage']['청구서_text']).get_property('innerText')      # 상단에 표시된 영역이 모바일인지 인터넷인지 확인
                        assert payment == mypage_info_text, self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 요금 조회/납부 홈 > 드롭다운 액션 오류(청구서 드롭다운 변경 실패)")
                        break
                    else:
                        # 드롭다운 리스트 마지막 요소에도 payment가 존재하지 않을 떄, 
                        if list == dropdown_list[-1] :
                            self.FC.loading_find_css_pre(self.FC.var['mypage']['청구서_하단_확인_버튼']).re_click()
                            is_continue=True
                            break
                        else:
                            pass
                    
                # 모바일/인터넷/결합 상품 정보가 없다면, 다음 로직은 무시
                if is_continue is True:
                    continue  

                # 콘텐츠 정상 출력 및 액션 정상 동작 확인 부분 
                text_list_result=[]
                
                # 상단 섹션 정보(납부방법/예금주/결제일/청구받는방법) 출력 확인
                text_list=['납부방법','예금주','결제일','청구 받는 방법']
                text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['납부_정보'], text_list))

                # 청구내역/납부내역 데이터 출력 여부 확인
                tab_list=self.FC.loading_find_csss(self.FC.var['mypage']['청구_납부내역_tab'])
                for tab in tab_list:
                    self.FC.move_to_click(tab)
                    bill=self.FC.loading_find_csss(self.FC.var['mypage']['내역_list'])
                    if len(bill) == 0 :
                        self.DBG.logger.debug(f"마이페이지 > 요금 조회/납부 > 요금 조회/납부 홈 > {mypage_info_text} {tab.get_property('innerText')} 정보 없음")
                        raise Exception()
                    else:
                        text_list_result.append(True)

                assert all(text_list_result) is True, self.DBG.logger.debug(f"마이페이지 > 청구요금 및 납부 > {mypage_info_text} 컨텐츠 정상 노출 확인 실패")

        except  Exception :
            self.DBG.print_dbg("마이페이지 > 요금 조회/납부 > 요금 조회/납부 홈 > 청구요금 및 납부내역에 대한 동작 및 정보 확인",False)
            return False

        else :
            self.DBG.print_dbg("마이페이지 > 요금 조회/납부 > 요금 조회/납부 홈 > 청구요금 및 납부내역에 대한 동작 및 정보 확인")
            return True

    # 마이페이지 > 사용현황 > 사용내역 조회
    def mypage_use(self):
        self.FC.gotoHome()
        try:
            self.FC.movepage(var.mypage['mypage'], var.mypage['use_direct'],address=var.mypage['use_url'])      # 메인 > 마이페이지 > 사용현황 > 바로가기
            
            payment_list=[['결합','이동통신'],['결합','인터넷']]
            for payment in payment_list:
                dropdown = self.FC.loading_find_css_pre(self.FC.var['mypage']['청구서_드롭다운'])
                self.FC.scroll2_v2(dropdown)
                self.FC.driver.execute_script("arguments[0].click();", dropdown)
                self.FC.wait_loading()
                dropdown_list=self.FC.loading_find_csss(self.FC.var['mypage']['사용현황_청구서_list'])

                # 이중 for문 탈출 변수
                is_continue=False
                for list in dropdown_list:
                    # 드롭다운 리스트에 모바일/인터넷/결합 상품이 존재하는지 확인 후, 드롭다운 기능 확인
                    if all(key in list.get_property('innerText') for key in payment ):
                        index=dropdown_list.index(list)
                        radio_button=self.FC.loading_find_csss(self.FC.var['mypage']['청구서_radio_btn'])
                        radio_button[index].re_click()
                        self.FC.loading_find_css_pre(self.FC.var['mypage']['청구서_하단_확인_버튼']).re_click()
                        self.FC.wait_loading()

                        mypage_info_text = self.FC.loading_find_css_pre(self.FC.var['mypage']['청구서_text2']).get_property('innerText') # 상단에 표시된 영역이 모바일인지 인터넷인지 확인
                        assert all(key in mypage_info_text for key in payment ), self.DBG.logger.debug("마이페이지 > 사용현황 > 사용내역 조회 > 드롭다운 액션 오류(청구서 드롭다운 변경 실패)")
                        break
                    else:
                        # 드롭다운 리스트 마지막 요소에도 payment가 존재하지 않을 떄, 
                        if list == dropdown_list[-1] :
                            is_continue=True
                            break
                        else:
                            pass
                    
                # 모바일/인터넷/결합 상품 정보가 없다면, 다음 로직은 무시
                if is_continue is True:
                    continue  

                # 각 콘텐츠 출력 확인 결과 배열
                text_list_result=[]

                if '모바일' in mypage_info_text or all(key in mypage_info_text for key in ['결합','이동통신']):
                    
                    ##### 실시간 요금 조회 #####
                    tab=self.FC.loading_find_css(self.FC.var['mypage']['실시간요금조회'])
                    self.FC.move_to_click(tab)

                    # 실시간 요금 조회 콘텐츠 출력 확인
                    top_bill_total = self.FC.loading_find_xpath_pre(var.mypage['top_bill']).text     # 상단 실시간 요금
                    if top_bill_total == '0원':
                        bottom_bill_total=self.FC.loading_find_xpath_pre(self.FC.var['mypage']['실시간이용요금_정보']).text
                    else:    
                        bottom_bill_total = self.FC.loading_find_xpath_pre(var.mypage['bottom_bill']).text   # 하단 합계
                    text_list_result.append(top_bill_total == bottom_bill_total)
                    text_list=['현재까지 사용한 요금','조회기간','남은기간','사용기간']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['내역_정보'], text_list))
                    if top_bill_total == '0원':
                        text_list=['실시간 이용요금','합계']
                    else:
                        text_list=['실시간 이용요금','이동통신','월정액','미납합계','합계']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['사용내역_정보_상세'],text_list))
                    
                    assert all(text_list_result), self.DBG.logger.debug(f"마이페이지 > 사용현황 > 사용내역 조회 > {payment} 상품 실시간 요금조회 컨텐츠 정상 노출 확인 실패")
                    
                    ##### 월별사용량 조회 #####
                    text_list_result.clear()
                    tab=self.FC.loading_find_css_pre(self.FC.var['mypage']['월별사용량조회'])
                    self.FC.move_to_click(tab)

                    text_list=['메뉴','상세항목','비고']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['월별사용량조회_data_col'], text_list))

                    # 금월 텍스트
                    month=self.FC.loading_find_csss(self.FC.var['mypage']['월_정보']).get_property('innerText')
                    month=month[:-1]
                    if month.startswith('0'):
                        month=month[1:]
                    month=int(month)

                    for i in range(0,4):
                        self.FC.wait_loading()
                        prev_month=self.FC.loading_find_css_pre(self.FC.var['mypage']['월_정보']).get_property('innerText')
                        if month-i <= 0:
                            gab=month-i
                            monthly=12+gab
                        else:
                            monthly=month-i
                        assert str(monthly) in prev_month,self.DBG.logger.debug(f"마이페이지 > 사용현황 > 사용내역 조회 > {payment} 상품 월별사용량조회 최근 4개월 사용량 조회 실패")
                        self.FC.scroll2_v2(self.FC.loading_find_css(self.FC.var['mypage']['이전_월_버튼']))
                        self.FC.driver.execute_script("arguments[0].click();", self.FC.loading_find_css(self.FC.var['mypage']['이전_월_버튼'])) 

                    # 월별 사용량 상세 조회
                    self.FC.wait_loading()
                    self.FC.move_to_click(self.FC.loading_find_css_pre(self.FC.var['mypage']['월별사용량_상세조회_버튼']))
                    text_list=['국내통화','데이터', '메시지', '부가서비스']
                    self.FC.wait_loading()
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['월별사용량_상세조회_tab'], text_list))
                    text_list_result.append(str(monthly) in self.FC.loading_find_css(self.FC.var['mypage']['월별사용량_상세_날짜']).get_property('innerText'))
                    # TODO 가끔 확인 버튼이 클릭이 안됄 때가 있어서 스크립트로 실행
                    self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mypage']['월별사용량_상세_확인_버튼']))
                    self.FC.driver.execute_script("arguments[0].click();", self.FC.loading_find_css_pre(self.FC.var['mypage']['월별사용량_상세_확인_버튼']))    
                    
                    assert all(text_list_result), self.DBG.logger.debug(f"마이페이지 > 사용현황 > 사용내역 조회 > {payment} 상품 월별사용량조회 컨텐츠 정상 노출 확인 실패")

                    ##### 통화 상세 내역 조회 #####
                    text_list_result.clear()
                    tab=self.FC.loading_find_css_pre(self.FC.var['mypage']['통화상세내역'])
                    self.FC.move_to_click(tab)
                    text_list=['이름','서비스 유형','국내통화','해외통화','전화번호']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['내역_정보'],text_list))

                    self.FC.loading_find_css(self.FC.var['mypage']['조회_버튼']).re_click()
                    text_list=['가까운 매장찾기','서비스 신청방법 보기']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['통화상세내역_조회'], text_list))
                    self.FC.loading_find_css(self.FC.var['mypage']['통화상세내역_조회_확인_버튼']).re_click()

                    assert all(text_list_result), self.DBG.logger.debug(f"마이페이지 > 사용현황 > 사용내역 조회 > {payment} 상품 월별사용량조회 컨텐츠 정상 노출 확인 실패")

                # TODO '인터넷' 출력 확인 필요
                # ...

                if all(key in mypage_info_text for key in ['결합','인터넷']):

                    ##### 통화 상세 내역 조회 #####
                    tab=self.FC.loading_find_xpath(self.FC.var['mypage']['인터넷_통화상세내역_조회'])
                    self.FC.move_to_click(tab)

                    # TODO DCBGQA-343 이슈로 수정 및 추가 필요<<<
                    text_list=['이름','서비스 유형','전화번호']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['인터넷_통화상세내역'], text_list))

                    if all(text_list_result) is False:
                        self.DBG.logger.debug(f"마이페이지 > 사용현황 > 사용내역 조회 > {payment} 상품 월별사용량조회 컨텐츠 정상 노출 확인 실패")
                        raise Exception() 

                    ##### 기가 인터넷 사용량 #####
                    tab=self.FC.loading_find_xpath(self.FC.var['mypage']['기가인터넷사용량'])
                    self.FC.move_to_click(tab)

                    text_list=['고객정보','이름','요금제','설치장소']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['기가인터넷_사용_정보'], text_list))

                    if all(text_list_result) is False:
                        self.DBG.logger.debug(f"마이페이지 > 사용현황 > 사용내역 조회 > {payment} 상품 월별사용량조회 컨텐츠 정상 노출 확인 실패")
                        raise Exception() 


                    ##### IPTV컨텐츠 사용내역 #####
                    tab=self.FC.loading_find_xpath_pre(self.FC.var['mypage']['IPTV사용내역'])
                    self.FC.scroll_x(tab)
                    self.FC.move_to_click(tab)

                    text_list=['고객정보','이름','가입상품','설치장소','인증']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['IPTV사용_정보'], text_list))

                    text_list=['본인인증','휴대폰','바이오','PASS','TOSS','카카오','네이버','아이핀']
                    text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['IPTV_본인인증'], text_list))

                    # 본인인증 인증하기 버튼 정상 출력 확인
                    button_list=self.FC.loading_find_csss(self.FC.var['mypage']['IPTV_본인인증_버튼'])
                    text_list_result.append(len(button_list) == 7)

                    assert all(text_list_result), self.DBG.logger.debug(f"마이페이지 > 사용현황 > 사용내역 조회 > {payment} 상품 월별사용량조회 컨텐츠 정상 노출 확인 실패")

        except  Exception :
            self.DBG.print_dbg("마이페이지 > 사용현황 > 사용내역 조회 대한 내역 확인 및 페이지 정상 노출 확인",False)
            return False

        else :
            self.DBG.print_dbg("마이페이지 > 사용현황 > 사용내역 조회 대한 내역 확인 및 페이지 정상 노출 확인")
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
        mypage = MypagePage(driver,fc)

        fc.pre_script()
        
        if fc.is_login():
            login.logout()
        login.u_plus_login()
        
        mypage.mypage()
        mypage.mypage_bill()
        mypage.mypage_use()
        mypage.mypage_membership()
        driver.driver.quit()
        server.stop()
    except Exception as e:
        print(e)
        # os.system("lsof -P -i :4723 |awk NR==2'{print $2}'|xargs kill -9")
        # os.system(f"ios-deploy --kill --bundle_id com.lguplus.mobile.cs")



