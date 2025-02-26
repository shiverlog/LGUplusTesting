import os
import traceback                                      # 콘솔창에 오류 메세지 출력
import sys                                            # 현재 호출하는 함수명 반환 모듈

from common.function import Function
from common.debug import Debug
from base.webdriver import WebDriver

sys.path.append('C:/lg-uplus/project/selenium_pc')


class LoginPage():
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)

    # U+ 로그인
    def u_plus_login(self):
        self.FC.gotoHome()
        try:
            uplus_id = os.environ['UPLUS_ID']
            uplus_pw = os.environ['UPLUS_PW']

            user_icon=self.FC.loading_find_css(self.FC.var['login_el']['user_icon'])
            self.FC.move_to_element(user_icon)
            user_icon_login=self.FC.loading_find_css_pre(self.FC.var['login_el']['user_icon_login'])
            self.FC.move_to_click(user_icon_login)

            if self.FC.driver.current_url in self.FC.var['common_el']['url']:
                for _ in range(3):
                    self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mainpage_el']['KV_area']))
                    self.FC.move_to_element(user_icon)
                    self.FC.move_to_click(user_icon_login)

            self.FC.loading_find_css_pre(self.FC.var['login_el']['uplus_login_img']).get_property('parentElement').click()
            self.FC.wait_loading()

            self.FC.is_exists_element_click(self.FC.loading_find_css(self.FC.var['login_el']['입력한문자삭제']))
            self.FC.loading_find_xpath(self.FC.var['login_el']['id_저장']).click()
            self.FC.wait_loading()

            self.FC.loading_find_css(self.FC.var['login_el']['id_input']).send_keys(uplus_id)
            self.FC.move_to_click(self.FC.loading_find_css('.c-ttp-inner .item:nth-of-type(1) .nm-tooltip-button'))
            for _ in range(3):
                try:
                    if self.FC.loading_find_css('.c-tooltip') is False:
                        self.FC.loading_find_css(self.FC.var['login_el']['pw_input']).send_keys(uplus_pw)
                        self.FC.loading_find_css(self.FC.var['login_el']['로그인_btn']).click()
                        break
                    else:
                        self.FC.move_to_click(self.FC.loading_find_css('.c-ttp-inner .item:nth-of-type(1) .nm-tooltip-button'))
                except:
                    raise Exception('로그인 실패 : tooltip 처리 실패')

            self.FC.wait_loading()

            # 유플러스 로그인 후 정상적으로 메인페이지로 이동했는지 확인
            assert self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['KV']).get_property('baseURI') == self.FC.var['common_el']['url'], self.DBG.logger.debug("유플러스 로그인 후 메인페이지 이동 실패")

        except  Exception :
            self.DBG.print_dbg("u+ ID 로그인 정상 동작 확인",False)
            return False

        else :
            self.DBG.print_dbg("u+ ID 로그인 정상 동작 확인")
            return True

    # 로그아웃
    def logout(self):
        self.FC.gotoHome()
        try:                   
            self.FC.movepage(self.FC.var['login_el']['logout_btn'])      # 로그아웃 버튼 선택
            assert self.FC.loading_find_css('div#KV').get_property('baseURI') == self.FC.var['common_el']['url'], self.DBG.logger.debug("로그아웃 후 메인페이지 이동 실패")

            self.FC.loading_find_css('.c-btn-menu').click()
            assert self.FC.loading_find_css(self.FC.var['login_el']['login_btn']).get_property('innerText') == "로그인", self.DBG.logger.debug("정상 로그아웃 실패")

        except  Exception:
            self.DBG.logger.debug(sys._getframe(0).f_code.co_name + " 실패")
            self.DBG.screenshot()
            print(traceback.format_exc())
            return False

        else :
            self.DBG.logger.info(sys._getframe(0).f_code.co_name + " 성공")
            return True

    # 로그인
    def do_login(self, login_type:str):
        '''
        U+ID, 카카오, 네이버 로그인
        '''
        self.FC.gotoHome()
        try:
            user_icon=self.FC.loading_find_css(self.FC.var['login_el']['user_icon'])
            self.FC.move_to_element(user_icon)
            user_icon_login=self.FC.loading_find_css_pre(self.FC.var['login_el']['user_icon_login'])
            self.FC.move_to_click(user_icon_login)

            if self.FC.driver.current_url in self.FC.var['common_el']['url']:
                for _ in range(3):
                    self.FC.move_to_element(self.FC.loading_find_css(self.FC.var['mainpage_el']['KV_area']))
                    self.FC.move_to_element(user_icon)
                    self.FC.move_to_click(user_icon_login)
            ## 위까지 동일
            dict = {
                "uplus" : [os.environ['UPLUS_ID'], os.environ['UPLUS_PW']],
                "kakao" : [],
                "naver" : [],
            }

            self.FC.loading_find_css_pre(self.FC.var['login_el'][f'{login_type}_login_img']).get_property('parentElement').click()
            self.FC.wait_loading()

            self.FC.is_exists_element_click(self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_입력한문자삭제']))
            self.FC.is_exists_element_click(self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_id_저장']))
            self.FC.wait_loading()

            self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_id_input']).send_keys(dict[login_type][0])

            if login_type == "uplus":
                self.FC.is_exists_element_click(self.FC.loading_find_css('.c-ttp-inner .item:nth-of-type(1) .nm-tooltip-button'))
                for _ in range(3):
                    try:
                        if self.FC.loading_find_css('.c-tooltip') is False:
                            self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_pw_input']).send_keys(dict[login_type][1])
                            break
                        else:
                            self.FC.move_to_click(self.FC.loading_find_css('.c-ttp-inner .item:nth-of-type(1) .nm-tooltip-button'))
                    except:
                        raise Exception('로그인 실패 : tooltip 처리 실패')

            else:
                self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_pw_input']).send_keys(dict[login_type][1])

            self.FC.again_click(self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_login_btn']))

            # 유플러스 로그인 후 정상적으로 메인페이지로 이동했는지 확인
            assert self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['KV']).get_property('baseURI') == self.FC.var['common_el']['url'], self.DBG.logger.debug("유플러스 로그인 후 메인페이지 이동 실패")

        except  Exception :
            self.DBG.print_dbg(f"{login_type} 로그인 정상 동작 확인",False)
            return False

        else :
            self.DBG.print_dbg(f"{login_type} 로그인 정상 동작 확인")
            return True
        