import random
from base.webdriver import WebDriver
from common.function import Function
from common.debug import Debug

class MypagePage():
    bill_count='2'
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)

    # 마이페이지 서브메인
    def mypage(self):
        self.FC.gotoHome()
        try:
            self.FC.movepage(self.FC.var['mypage']['mypage'],address=self.FC.var['mypage']['mypage_url'])
            self.FC.modal_ck()

            # 마이페이지 > 상단 청구 및 납부 정보 콘텐츠 및 기능 확인
            result=[]
            mypage_datas={
                'mypage_bill_top':['청구 및 납부 정보','청구서'],
                'mypage_bill':['청구요금','요금 바로 납부'],
                'mypage_bill_membership':['등급','혜택 변경','나만의 콕'],
                # 'mypage_bill_ezpoint':['사용 가능한 ez포인트'],
                }
            text_list_result=[]
            for key,value in mypage_datas.items():
                text_list_result.append(self.FC.text_list_in_element(self.FC.var['mypage'][key],value))
                self.FC.wait_loading()
            res = self.FC.wait_datas(self.FC.var['mypage']['청구서_영역'],'li')
            result.append(not isinstance(res,str))
            assert self.DBG.print_res(result), self.DBG.logger.debug("마이페이지 > 서브메인 > 청구 및 납부 정보 콘텐츠 정상 출력 실패")

            # 청구서 팝업 기능 확인
            result.clear()
            self.bill_count=self.FC.loading_find_css(self.FC.var['mypage']['mypage_bill_more']).get_property('innerText')
            self.FC.wait_loading()
            btn=self.FC.loading_find_css(self.FC.var['mypage']['mypage_bill_more_btn'])
            self.FC.move_to_click(btn)
            result.append(self.bill_count==str(len(self.FC.loading_find_csss(self.FC.var['mypage']['mypage_bill_more_modal_data']))))
            result.append(self.bill_count in self.FC.loading_find_css(self.FC.var['mypage']['mypage_bill_more_modal_ctn']).get_property('innerText'))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 서브메인 > 청구서 기능 정상 작동 실패")
            self.FC.modal_ck()

            # ez포인트 영역 없어짐 25.01.02
            # # 사용 가능한 ez포인트 링크 이동
            # self.FC.loading_find_css(self.FC.var['mypage']['사용가능한_ez포인트']).click()
            # assert self.FC.var['mypage']['ezpoint_url'] in self.FC.loading_find_css(self.FC.var['mypage']['ez포인트_조회_페이지']).get_property('baseURI'), self.DBG.logger.debug("마이페이지 > 서브메인 > ez 포인트 링크 정상 이동 실패")
            # self.FC.goto_url(self.FC.var['mypage']['mypage_url'])

            # 마이페이지 > 서브메인 > 전체알림 영역
            self.FC.modal_ck()
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mypage']['전체알림_타이틀']))
            self.FC.wait_datas(self.FC.var['mypage']['전체알림_영역'],'h3')
            assert self.FC.text_list_in_element(self.FC.var['mypage']['전체알림_영역'],['전체알림','읽은 알림 삭제','전체 삭제']), self.DBG.logger.debug("마이페이지 > 서브메인 > 전체알림 콘텐츠 정상 출력 실패")

            # 마이페이지 > 서브메인 > 주문정보 영역
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mypage']['주문정보_영역']))
            assert self.FC.text_list_in_element(self.FC.var['mypage']['주문정보영역_xpath'],['주문정보']), self.DBG.logger.debug("마이페이지 > 서브메인 >주문정보 콘텐츠 정상 출력 실패")

            # 마이페이지 > 서브메인 > 가입서비스 영역
            self.FC.wait_datas(self.FC.var['mypage']['가입서비스_영역'],'h3')
            assert self.FC.text_list_in_element(self.FC.var['mypage']['가입서비스_영역'],['가입서비스']), self.DBG.logger.debug("마이페이지 > 서브메인 >주문정보 콘텐츠 정상 출력 실패")
            self.FC.wait_loading()
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mypage']['주문정보_영역']))

            # 탭 콘텐츠에 탭 명이 포함되어 있는지 확인(콘텐츠 정상 출력)
            tab_list_el=self.FC.loading_find_csss(self.FC.var['mypage']['가입서비스_영역_탭메뉴'])
            for tab in tab_list_el:
                tab.click()
                tab_name=tab.get_property('innerText')[0]
                tab_content=self.FC.loading_find_csss(self.FC.var['mypage']['가입서비스_영역_컨텐츠'])[tab_list_el.index(tab)].get_property('innerText')
                assert tab_name in tab_content,self.DBG.logger.debug("마이페이지 > 서브메인 > 가입서비스(%s 탭) 콘텐츠 정상 출력 실패", tab_name)

            # 마이페이지 > 서브메인 > 하단 넷플릭스/쿠폰 영역
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mypage']['넷플계정_쿠폰등록_영역']))
            assert self.FC.text_list_in_element(self.FC.var['mypage']['넷플계정_쿠폰등록_영역'],['넷플릭스','쿠폰']),self.DBG.logger.debug("마이페이지 > 서브메인 > 하단 넷플릭스/쿠폰 영역 정상 출력 실패")

        except  Exception :
            self.DBG.print_dbg("마이페이지 정상 노출 및 기능 동작 확인",False)
            return False

        else :
            self.DBG.print_dbg("마이페이지 정상 노출 및 기능 동작 확인")
            return True

    # 마이페이지 > 요금 조회/납부
    def mypage_bill(self):

        self.FC.gotoHome()
        try:
            self.FC.movepage(self.FC.var['mypage']['mypage'],self.FC.var['mypage']['payinfo'],address=self.FC.var['mypage']['pay_info_url'])
            self.FC.modal_ck()

            # 마이페이지 >  요금 조회/납부 > 상단 요금 조회/납부 영역 확인
            result=[]
            res = self.FC.wait_datas(self.FC.var['mypage']['청구서_영역'],'th','td')
            result.append(not isinstance(res,str))
            text_list=['고객명','납부방법','청구서 받는 방법','청구서 더 보기','서비스명','카드주/결제요청일','요금바로 납부','납부 방법 변경','청구서 받는 방법 변경','입금전용 계좌 발급']
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구서_영역'],text_list))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 >  요금 조회/납부 > 상단 요금 조회/납부 콘텐츠 정상 출력 실패")

            # 청구서 더 보기 기능 확인
            result.clear()
            self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['mypage']['청구서_더보기_버튼']),True)
            result.append(self.bill_count==str(len(self.FC.loading_find_csss(self.FC.var['mypage']['청구서_더보기_팝업_데이터']))))
            result.append(self.bill_count in self.FC.loading_find_css(self.FC.var['mypage']['청구서_더보기_팝업_데이터_카운트']).get_property('innerText'))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 >  요금 조회/납부 > 청구서 더 보기 기능 정상 작동 실패")
            self.FC.modal_ck()


            # 마이페이지 > 요금 조회/납부 > 요금바로 납부 기능 확인
            self.FC.loading_find_css(self.FC.var['mypage']['요금바로 납부_버튼']).click()
            self.FC.wait_loading()
            text_list=['고객명','서비스명','납부방법','카드주/결제요청일','청구서 받는 방법']
            assert self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 요금바로 납부 기능 정상 작동 실패")
            self.FC.modal_ck()

            # 마이페이지 > 요금 조회/납부 > 납부 방법 변경 기능 확인
            result.clear()
            self.FC.loading_find_css(self.FC.var['mypage']['납부방법변경_버튼']).click()
            self.FC.wait_loading()
            text_list=['납부방법','고객유형','카드번호','카드사명','카드 명의자명','카드 명의자 생년월일','성별','카드 유효기간','꼭 확인하세요','취소','인증하기','은행','카드','개인','사업자','내국인','외국인','남자','여자']
            result.append(self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 납부 방법 변경 기능 정상 작동 실패")
            self.FC.modal_ck()

            # 마이페이지 > 요금 조회/납부 > 결제일 변경 기능 확인
            result.clear()
            self.FC.loading_find_css(self.FC.var['mypage']['결제일변경_버튼']).click()
            self.FC.wait_loading()
            text_list=['결제일 변경','닫기','카드사','카드번호','결제일','선택','1차','2차','3차','4차','꼭 확인하세요','취소','인증하기']
            result.append(self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 결제일 변경 기능 정상 작동 실패")
            self.FC.modal_ck()

            # 마이페이지 > 요금 조회/납부 > 청구서 받는 방법 변경 기능 확인
            result.clear()
            self.FC.loading_find_css(self.FC.var['mypage']['청구서받는방법변경_버튼']).click()
            self.FC.wait_loading()
            text_list=['고객명','고객번호','납부방법','가입서비스 자세히 보기','납부방법 변경']
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구서받는방법변경_팝업_정보'],text_list))
            result.append(self.FC.wait_datas(self.FC.var['mypage']['청구서받는방법변경_팝업_정보'],'td'))
            text_list=['청구서 받는 방법','변경일']
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['현재청구서받는방법_영역'],text_list))
            result.append(self.FC.wait_datas(self.FC.var['mypage']['현재청구서받는방법_영역'],'td'))
            text_list=['청구서 반송내역','청구년월','청구유형','반송일','반송사유']
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구서반송내역_영역'],text_list))
            text_list=['청구서 받는 방법','이메일','휴대폰','우편']
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구서받는방법및주소변경_영역'],text_list))
            # 마이페이지 > 요금 조회/납부 > 청구서 받는 방법 및 주소 변경 기능 확인
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mypage']['청구서받는방법및주소변경_영역']))
            bill_receive_list_el=self.FC.loading_find_csss(self.FC.var['mypage']['청구서받는방법_버튼들'])
            text_list=[['보안 이메일','예','아니오','이메일 주소','선택'],['고객센터','아이폰','휴대폰 인증'],['청구서 받는 주소','연락처','주소찾기']]
            for current in bill_receive_list_el:
                current.click()
                if bill_receive_list_el.index(current) == 2:
                    result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구서받는방법_우편청구서'],text_list[bill_receive_list_el.index(current)]))
                else :
                    result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구서받는방법및주소변경_영역'],text_list[bill_receive_list_el.index(current)]))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 청구서 받는 방법 변경 기능 정상 작동 실패")

            # 마이페이지 > 요금 조회/납부 > 청구서 받는 방법 변경 > 가입서비스 자세히 보기
            result.clear()
            self.FC.move_to_click(self.FC.loading_find_xpath(self.FC.var['mypage']['가입서비스자세히보기_버튼']))
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['가입서비스자세히보기_컨텐츠'],['유형','서비스명','상품명']))
            result.append(self.FC.wait_datas(self.FC.var['mypage']['가입서비스자세히보기_컨텐츠'],'td'))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 청구서 받는 방법 변경 > 가입서비스 자세히보기 기능 정상 작동 실패")
            self.FC.modal_ck() # 이중 모달 상태 ->  가입서비스 자세히보기 모달 창 닫기

            #  마이페이지 > 요금 조회/납부 > 청구서 받는 방법 변경 > 납부방법 변경 기능 확인
            result.clear()
            self.FC.move_to_click(self.FC.loading_find_xpath(self.FC.var['mypage']['청구서_납부방법변경_버튼'])) # 납부방법 변경 모달 창으로 변경됌
            text_list=['납부방법','고객유형','카드번호','카드사명','카드 명의자명','카드 명의자 생년월일','성별','카드 유효기간','꼭 확인하세요','취소','인증하기','은행','카드','개인','사업자','내국인','외국인','남자','여자']
            result.append(self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 청구서 받는 방법 변경 > 납부방법 변경 기능 정상 작동 실패")
            self.FC.modal_ck()
            # 납부방법 변경 모달 창으로 변경
            result.clear()
            self.FC.loading_find_css(self.FC.var['mypage']['청구서받는방법변경_버튼']).click()
            text_list=['청구서 받는 방법','변경일']
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['현재청구서받는방법_영역'],text_list))
            text_list=['청구서 반송내역','청구년월','청구유형','반송일','반송사유']
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구서반송내역_영역'],text_list))
            text_list=['청구서 받는 방법','이메일','휴대폰','우편']
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구서받는방법및주소변경_영역'],text_list))
            self.FC.modal_ck()

            # 마이페이지 > 요금 조회/납부 > 입금전용 계좌 발급 기능 확인
            result.clear()
            self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['mypage']['입금전용_계좌발급_버튼']))
            text_list=['고객명','고객번호','납부방법','이용중인 입금전용계좌','이름','금융기관','계좌번호','입금전용 계좌 추가','은행명','신청','휴대폰 번호','계좌번호 받기','보안문자','인증번호 받기','인증번호 확인','문자메시지 받을 번호']
            result.append(self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list))
            result.append(self.FC.wait_datas(self.FC.var['common_el']['팝업_컨텐츠'],'tr:not([style="display: none;"]) td'))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 입금전용 계좌 발급 기능 정상 작동 실패")
            # 마이페이지 > 요금 조회/납부 > 입금전용 계좌 발급 기능 > 가입서비스 자세히보기 기능
            result.clear()
            self.FC.move_to_click(self.FC.loading_find_xpath(self.FC.var['mypage']['가입서비스자세히보기_버튼']))
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['가입서비스자세히보기_컨텐츠'],['유형','서비스명','상품명']))
            result.append(self.FC.wait_datas(self.FC.var['mypage']['가입서비스자세히보기_컨텐츠'],'td'))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 입금전용 계좌 발급 기능 > 납부방법 변경 기능 정상 작동 실패")
            self.FC.modal_ck() # 이중 모달 상태 ->  가입서비스 자세히보기 모달 창 닫기
            # 납부방법 변경 모달 창으로 변경
            result.clear()
            self.FC.loading_find_xpath(self.FC.var['mypage']['청구서_납부방법변경_버튼']).click()
            self.FC.wait_loading()
            text_list=['납부방법','고객유형','카드번호','카드사명','카드 명의자명','카드 명의자 생년월일','성별','카드 유효기간','꼭 확인하세요','취소','인증하기','은행','카드','개인','사업자','내국인','외국인','남자','여자']
            result.append(self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 입금전용 계좌 > 납부방법 변경 기능 정상 작동 실패")
            self.FC.modal_ck()

            # 마이페이지 > 요금 조회/납부 > 청구내역 영역
            result.clear()
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mypage']['청구내역_영역']))
            text_list=['청구내역','청구월','청구금액','납부상태','청구서재발행']
            result.append(self.FC.text_list_in_element(self.FC.var['mypage']['청구내역_영역'],text_list))
            result.append(self.FC.wait_datas(self.FC.var['mypage']['청구내역_영역'],'td'))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 청구내역 영역 콘텐츠 정상 출력 실패")

            # 청구내역 데이터가 있을 시, 콘텐츠 출력 및 기능 확인
            payment_data=self.FC.loading_find_csss(self.FC.var['mypage']['청구내역_청구월'])
            if len(payment_data) >=1:
                # 청구내역 클릭 시, 청구서 조회
                random_num=random.randrange(1,len(payment_data))
                month=payment_data[random_num].get_property('innerText').split('-')[-1]
                if month != '10':
                    month=month.strip('0')+'월'
                pay=payment_data[random_num].get_property('parentNode').get_property('nextElementSibling').get_property('innerText')
                self.FC.move_to_click(payment_data[random_num])
                text = self.FC.loading_find_css(self.FC.var['mypage']['청구내역_영역2']).get_property('innerText')
                assert all(keyword in text for keyword in [month,pay]),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 청구내역 영역 - 청구월/청구금액(%s, %s) 링크 정상 이동 실패", month, pay)
                self.FC.goto_url(self.FC.var['mypage']['pay_info_url'])

                payment_data_btn=self.FC.loading_find_csss(self.FC.var['mypage']['청구내역_재발행_버튼'])
                self.FC.move_to_click(payment_data_btn[random_num])
                self.FC.loading_find_css(self.FC.var['common_el']['팝업_바디'])
                text_list=['고객명','고객번호','납부방법','가입서비스 자세히 보기','납부방법 변경','현재 청구서 받는 방법','청구서 재발행 신청','신청월','신청사유','청구서 받는 방법']
                assert self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 청구내역 영역 - 재발행 기능 정상 작동 실패")
                self.FC.modal_ck()

            # 마이페이지 > 요금 조회/납부 > 납부내역 영역
            result.clear()
            self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mypage']['부가세포함금액_텍스트']))
            # 납부내역 데이터가 있을 시, 콘텐츠 출력 및 기능 확인
            payment_data=self.FC.loading_find_csss(self.FC.var['mypage']['납부내역_데이터'])
            if len(payment_data) >=1:
                text_list=['납부일','입금확인일','납부금액','납부방법','발급','납부확인서 신청','현금영수증 발행','납부내역 더보기']
                result.append(self.FC.text_list_in_element(self.FC.var['mypage']['주문정보_영역'],text_list))
                result.append(self.FC.wait_datas(self.FC.var['mypage']['주문정보_영역'],'td'))
                assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 납부내역 영역 콘텐츠 정상 출력 실패")

                # 요금 납부확인서 신청 기능 확인
                self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['mypage']['납부확인서신청_버튼']),True)
                text_list=['발급신청기간','신청방법']
                assert self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 납부내역 영역 - 납부확인서 신청 기능 정상 작동 실패")
                self.FC.modal_ck()

                # 현금영수증 발행 기능 확인
                self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['mypage']['현금영수증발행_버튼']))
                text_list=['고객명','조회기간']
                assert self.FC.text_list_in_element(self.FC.var['common_el']['팝업_컨텐츠'],text_list),self.DBG.logger.debug("마이페이지 > 요금 조회/납부 > 납부내역 영역 - 납부확인서 신청 기능 정상 작동 실패")
                self.FC.modal_ck()

                # 영수증 기능 확인
                random_num=random.randrange(0,len(payment_data))
                td=payment_data[random_num].get_property('children')
                month=td[0].get_property('innerText')
                pay=td[2].get_property('innerText')
                payment=td[3].get_property('innerText')
                self.FC.loading_find_csss(self.FC.var['mypage']['납부내역_영수증_버튼'])[random_num].click()
                self.FC.driver.switch_to.window(self.FC.driver.window_handles[-1])
                result.append(pay in self.FC.loading_find_css(self.FC.var['mypage']['납부영수증_납부한금액']).get_property('innerText'))
                result.append(month in self.FC.loading_find_css(self.FC.var['mypage']['납부영수증_납부일자']).get_property('innerText'))
                result.append(payment in self.FC.loading_find_css(self.FC.var['mypage']['납부영수증_납부방법']).get_property('innerText'))
                assert self.DBG.print_res(result),self.DBG.logger.debug("f마이페이지 > 요금 조회/납부 > 납부내역 영역 - 영수증({month}) 기능 실패")
                self.FC.close_popup(self.FC.driver.window_handles)

        except  Exception :
            self.DBG.print_dbg("마이페이지 > 요금 조회/납부내역에 대한 동작 및 정보 확인",False)
            self.FC.modal_ck()
            return False

        else :
            self.DBG.print_dbg("마이페이지 > 요금 조회/납부내역에 대한 동작 및 정보 확인")
            return True

    # 마이페이지 >  사용현황 > 사용 내역 조회 진입
    def mypage_use(self):
        self.FC.gotoHome()
        try:
            self.FC.movepage(self.FC.var['mypage']['mypage'],self.FC.var['mypage']['bilv'],address=self.FC.var['mypage']['bilv_url'])

            # 청구서 더보기 기능 확인
            result=[]
            self.FC.move_to_click(self.FC.loading_find_css(self.FC.var['mypage']['청구서더보기_버튼']))
            result.append(self.bill_count==str(len(self.FC.loading_find_csss(self.FC.var['mypage']['청구서_더보기_팝업_데이터']))))
            result.append(self.bill_count in self.FC.loading_find_css(self.FC.var['mypage']['청구서더보기_팝업_데이터_카운트']).get_property('innerText'))
            assert self.DBG.print_res(result),self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 > 청구서 더보기 기능 정상 작동 실패")
            self.FC.modal_ck()

            # 상단 탭별 콘텐츠 정상 노출 확인
            tab_list=['실시간 요금 조회','월별사용량조회','통화상세내역']
            for tab in tab_list:
                tab_list_el=self.FC.loading_find_csss(self.FC.var['mypage']['사용내역_탭메뉴_버튼'])
                self.FC.move_to_click(tab_list_el[tab_list.index(tab)],True)
                tab_result=[]
                if tab == tab_list[0]:  # 실시간 요금 조회
                    tab_result.clear()
                    left_bill_total=self.FC.loading_find_css(self.FC.var['mypage']['사용요금']).get_property('innerText')
                    right_bill_total=self.FC.loading_find_css(self.FC.var['mypage']['사용요금_합계']).get_property('innerText')
                    tab_result.append(left_bill_total == right_bill_total)
                    if left_bill_total == '0원' or right_bill_total == '0원':
                        text_list=['현재까지 사용한 요금','남은 기간','사용','사용기간','합계']
                    else:
                        text_list=['현재까지 사용한 요금','남은 기간','사용','사용기간','이동통신','월정액','미납합계','합계']
                    tab_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['사용내역_탭메뉴_컨텐츠'],text_list))
                    assert all(tab_result),self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 >  실시간 요금 조회 영역 콘텐츠 정상 출력 실패")

                if tab == tab_list[1]:  # 월별사용량조회
                    text_list=['최근 사용량 정보','메뉴','상세항목','비고']
                    assert self.FC.text_list_in_element(self.FC.var['mypage']['사용내역_탭메뉴_컨텐츠'],text_list),self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 > 월별사용량조회 영역 콘텐츠 정상 출력 실패")
                    # 금월 텍스트
                    month=self.FC.loading_find_css_pre(self.FC.var['mypage']['월별사용량조회_조회월']).get_property('innerText')
                    month = int(month.strip('0').strip('월').strip(' '))
                    check_months=[12+(month-i) if month-i<=0 else month-i for i in range(0,4)]
                    for check_month in check_months:
                        self.FC.wait_loading()
                        prev_month=self.FC.loading_find_css_pre(self.FC.var['mypage']['월별사용량조회_조회월']).get_property('innerText')
                        assert str(check_month) in prev_month,self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 > 월별사용량조회 영역 최근 4개월 사용량 조회 실패")
                        self.FC.move_to_click(self.FC.loading_find_css_pre(self.FC.var['mypage']['월별사용량조회_이전월_버튼']),True)

                    # 월별 사용량 상세조회 기능 확인
                    self.FC.move_to_click(self.FC.loading_find_css_pre(self.FC.var['mypage']['월별사용량상세조회_버튼']))
                    text_list=['월별 사용량 상세 조회','국내통화 이용내역','데이터 이용내역','메시지 이용내역','부가서비스 이용내역','휴대폰 소액결제 이용내역']
                    assert self.FC.text_list_in_element(self.FC.var['mypage']['사용내역_탭메뉴_컨텐츠'],text_list),self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 > 월별사용량조회 - 월별 사용량 상세조회 기능 정상 동작 실패")

                    tab_list2=['국내통화 이용내역','데이터 이용내역','메시지 이용내역','부가서비스 이용내역','휴대폰 소액결제 이용내역']
                    tab_list_el2=self.FC.loading_find_csss(self.FC.var['mypage']['월별사용량상세조회_탭메뉴'])
                    self.FC.wait_loading()
                    for tab2 in tab_list2:
                        self.FC.move_to_click(tab_list_el2[tab_list2.index(tab2)],True)

                        if tab2 == tab_list2[0]:  # 국내통화 이용내역
                            text_list=['서비스','시간대','사용건수','사용시간','할인전금액','할인금액','청구금액','최종사용일시','합계','무료제공 서비스','시간대','총 제공량','총 사용량','총 잔여량']
                            assert self.FC.text_list_in_element(self.FC.var['mypage']['월별사용량상세조회_탭메뉴_컨텐츠'],text_list), self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 > 월별사용량조회 - 월별 사용량 상세조회(%s 이용내역) 콘텐츠 정상 출력 실패", tab)

                        if tab2 == tab_list2[1]:  # 데이터 이용내역
                            text_list=['패킷','이용량','유료패킷','사용건수','사용량','할인 전 금액','할인금액','사용금액','최종사용일시']
                            assert self.FC.text_list_in_element(self.FC.var['mypage']['월별사용량상세조회_탭메뉴_컨텐츠'],text_list), self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 > 월별사용량조회 - 월별 사용량 상세조회(%s 이용내역) 콘텐츠 정상 출력 실패", tab)

                        if tab2 == tab_list2[2]:  # 메시지 이용내역'메시지 이용 내역',
                            text_list=['유료 서비스명','사용건수','단문메시지','장문메시지','할인전 금액','할인금액','청구금액','최종사용일']
                            assert self.FC.text_list_in_element(self.FC.var['mypage']['월별사용량상세조회_탭메뉴_컨텐츠'],text_list), self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 > 월별사용량조회 - 월별 사용량 상세조회(%s 이용내역) 콘텐츠 정상 출력 실패", tab)

                        if tab2 == tab_list2[3]:  # 부가서비스 이용내역
                            text_list=['무료서비스 사용내역','무료 부가서비스명','시간대','총 공제량','총 적용량','총 잔여량']
                            assert self.FC.text_list_in_element(self.FC.var['mypage']['월별사용량상세조회_탭메뉴_컨텐츠'],text_list), self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 > 월별사용량조회 - 월별 사용량 상세조회(%s 이용내역) 콘텐츠 정상 출력 실패", tab)

                        if tab2 == tab_list2[4]:  # 휴대폰 소액결제 이용내역
                            self.FC.driver.switch_to.frame(self.FC.loading_find_css_pre(self.FC.var['mypage']['휴대폰_소액결제_이용내역']))
                            text_list=['이용내역','이용일시','이용구분','서비스명','실판매자 상호명 전화번호','결제대행사','승인방식','이용금액']
                            self.FC.wait_loading()
                            assert self.FC.text_list_in_element('#wrap2',text_list), self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 > 월별사용량조회 - 월별 사용량 상세조회(%s 이용내역) 콘텐츠 정상 출력 실패", tab2)
                            self.FC.driver.switch_to.default_content()

                if tab == tab_list[2]:  # 통화상세내역
                    tab_result.clear()
                    text_list=['이름','서비스유형','국내통화','해외통화','전화번호','조회']
                    tab_result.append(self.FC.text_list_in_element(self.FC.var['mypage']['사용내역_탭메뉴_컨텐츠'],text_list))
                    tab_result.append(self.FC.wait_datas(self.FC.var['mypage']['사용내역_탭메뉴_컨텐츠'],'td'))
                    assert all(tab_result),self.DBG.logger.debug("마이페이지 > 사용현황 > 사용 내역 조회 > 통화상세내역 영역 콘텐츠 정상 출력 실패")

        except  Exception :
            self.DBG.print_dbg("마이페이지 > 사용현황 > 사용 내역 조회대한 내역 확인 및 페이지 정상 노출 확인",False)
            return False

        else :
            self.DBG.print_dbg("마이페이지 > 사용현황 > 사용 내역 조회대한 내역 확인 및 페이지 정상 노출 확인")
            return True
