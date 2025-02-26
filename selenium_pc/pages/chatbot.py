import common.json.variable as var               # 지정한 변수 모듈
import traceback        # 콘솔창에 오류 메세지 출력
from common.function import Function
from base.webdriver import WebDriver
from common.debug import Debug
import random
import time



class ChatbotPage():
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)

####################### 챗봇 #################################
    def chatbot(self):
        self.FC.gotoHome()
        try:
            self.FC.loading_find_css(self.FC.var['chatbot_el']['챗봇']).click()

            # 빠른 가입 챗봇
            self.FC.loading_find_css(self.FC.var['chatbot_el']['빠른가입']).click()
            print(str(self.FC.driver.window_handles))
            self.FC.driver.switch_to.window(self.FC.driver.window_handles[1])
            
            # 핸드폰 구매 > 기기 검색 > 스마트 워치
            result=[]
            result.clear()
            # self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['창_처음으로']).click()
            self.FC.loading_find_xpath_pre(self.FC.var['chatbot_el']['창_핸드폰 구매']).click()
            result.append(self.FC.text_list_in_element(self.FC.var['chatbot_el']['창_마지막 대화 내용'],['기기 검색','빠른 구매','추천 받기','휴대폰/스마트기기']))
            self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['아래로']).click()
            time.sleep(.5) # 스크롤 애니메이션 대기
            self.FC.loading_find_xpath_pre(self.FC.var['chatbot_el']['창_핸드폰 구매_기기 검색']).click()
            time.sleep(.5) # 스크롤 애니메이션 대기
            result.append(len(self.FC.loading_find_csss(self.FC.var['chatbot_el']['창_핸드폰 구매_기기 검색_btns']))>0)
            self.FC.scroll_center(self.FC.loading_find_xpath_pre(self.FC.var['chatbot_el']['창_핸드폰 구매_기기 검색_스마트워치']))
            
            self.FC.loading_find_xpath_pre(self.FC.var['chatbot_el']['창_핸드폰 구매_기기 검색_스마트워치']).click()
            result.append(self.FC.text_list_in_element(self.FC.var['chatbot_el']['창_마지막 대화 내용'],['스마트 워치','월 예상 납부금액']))
            
            print(str(result))
            assert self.DBG.print_res(result), self.DBG.logger.debug("챗봇 > 빠른 가입 챗봇 > 핸드폰 구매 > 기기 검색 > 스마트워치 > 결과 노출 실패")


            # 하단 메뉴 정상 노출
            self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['하단메뉴']).click()
            assert len(self.FC.loading_find_csss(self.FC.var['chatbot_el']['하단메뉴_btns'])) > 0,self.DBG.logger.debug("챗봇 > 빠른 가입 챗봇 > 하단 메뉴 정상 노출 실패")
            self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['하단메뉴']).click()

            # 입력창 정상 노출 및 기능
            self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['입력창']).click()
            self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['입력창']).send_keys('최신 핸드폰')
            self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['전송버튼']).click()
            assert self.FC.text_list_in_element(self.FC.var['chatbot_el']['창_마지막 대화 내용'],['최신 핸드폰','월 예상 납부금액']), self.DBG.logger.debug("챗봇 > 빠른 가입 챗봇 > 입력창 기능 정상 동작 실패")

            # 전문 상담사 연결/대화내용 전송 정상 노출 및 기능
            result.clear()
            self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['창_전문 상담사 연결']).click()
            result.append(self.FC.text_list_in_element(self.FC.var['chatbot_el']['창_마지막 대화 내용'],['전문 상담사','상담사와 채팅하기']))
            self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['창_대화내용 전송']).click()
            result.append(self.FC.text_list_in_element(self.FC.var['chatbot_el']['창_팝업'],['SMS','카카오톡','전송하기']))
            self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['창_팝업_닫기']).click()
            print(str(result))
            assert self.DBG.print_res(result),self.DBG.logger.debug("챗봇 > 빠른 가입 챗봇 > 전문 상담사 연결/대화내용 전송 정상 노출 및 기능 실패")
            
            
            # 창 닫기 시, 만족도 조사
            self.FC.loading_find_css_pre(self.FC.var['chatbot_el']['창닫기']).click()
            self.FC.text_list_in_element(self.FC.var['chatbot_el']['창_팝업'],['만족도 조사','상담 내용','연령대','평가 보내기'])
            star=self.FC.loading_find_csss(self.FC.var['chatbot_el']['창_팝업_만족도 조사_별'])
            star[4].click()
            age=self.FC.loading_find_csss(self.FC.var['chatbot_el']['창_팝업_만족도 조사_나이'])
            age[1].click()
            self.FC.loading_find_css(self.FC.var['chatbot_el']['창_팝업_만족도 조사_평가 보내기']).click()
            assert len(self.FC.driver.window_handles) == 1,self.DBG.logger.debug("챗봇 > 빠른 가입 챗봇 > 창닫기 정상 동작 실패")


        
        except  Exception :
            
            self.DBG.logger.debug("챗봇 상담 기능 정상 동작 확인 실패")
            self.DBG.screenshot()
            self.DBG.send_slack("챗봇 상담 기능 정상 동작 확인 실패",False)
            print(traceback.format_exc())
            self.FC.modal_ck()
            pass

        else :
            self.DBG.logger.PASS("챗봇 상담 기능 정상 동작 확인 실패 성공")
            self.DBG.send_slack("챗봇 상담 기능 정상 동작 확인 실패 성공")