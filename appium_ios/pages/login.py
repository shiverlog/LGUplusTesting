import os
import sys
import traceback

from base.server import AppiumServer
from base.appdriver import AppDriver
import common.variable as var
from common.function import Function
from common.debug import Debug
from common.slack import Slack

sys.path.append('/Users/nam/dev/remotePC_batchfiles/pubsub/appium_ios')


class LoginPage():
    def __init__(self,AppDriver:AppDriver,FC:Function):
        self.driver=AppDriver.driver
        self.FC=FC
        self.DBG=Debug(AppDriver)
        

    # U+ 로그인
    def u_plus_login(self):
        self.FC.gotoHome()
        try:
            uplus_id = os.environ['UPLUS_ID']
            uplus_pw = os.environ['UPLUS_PW']
            
        # 햄버거 메뉴로 진입
            if self.driver.current_url != self.FC.var['login_el']['url']:
                self.FC.movepage(var.login_el['login_btn'],address=self.FC.var['login_el']['url'])
            self.FC.is_exists_element_click(self.FC.loading_find_css(self.FC.var['login_el']['ID로그인_btn'])) # 간편 로그인 화면 처리
            self.FC.is_exists_element_click(self.FC.loading_find_css(self.FC.var['login_el']['uplus_login_img']))

            self.FC.modal_ck2() # 결함 DCBGQA-4368
            self.FC.is_exists_element_click(self.FC.loading_find_css(self.FC.var['login_el']['uplus_입력한문자삭제']))

            self.FC.loading_find_css(self.FC.var['login_el']['uplus_id_input']).send_keys(uplus_id)   # ID 입력
            self.FC.is_exists_element_click(self.FC.loading_find_css('.c-ttp-inner .item:nth-of-type(1) .nm-tooltip-button'))
            for _ in range(3):
                try:
                    if self.FC.loading_find_css('.c-tooltip') == False:
                        self.FC.loading_find_css(self.FC.var['login_el']['uplus_pw_input']).send_keys(uplus_pw)   # PW 입력
                        self.FC.loading_find_css(self.FC.var['login_el']['uplus_login_btn']).re_click()  # 로그인 버튼 선택
                        break
                    else:
                        self.FC.is_exists_element_click(self.FC.loading_find_css('.c-ttp-inner .item:nth-of-type(1) .nm-tooltip-button'))
                except:
                    raise Exception('로그인 실패 : tooltip 안사라짐')
            self.FC.wait_loading()
            
            # 유플러스 로그인 후 정상적으로 메인페이지로 이동했는지 확인
            assert var.common_el['url'] in self.FC.loading_find_css(var.mainpage_el['개인화']).get_property('baseURI') , self.DBG.logger.debug("u+ID 로그인 후 메인페이지 이동 실패")

        except  Exception as e :
            self.DBG.print_dbg("u+ ID 로그인 정상 동작 확인",False)
            return False
        else :
            self.DBG.print_dbg("u+ ID 로그인 정상 동작 확인")
            return True


    def u_plus_login_retry(self,count):
        try:
            while 0 < count:
                res = self.u_plus_login()
                if res:
                    self.DBG.print_dbg("u+ ID 로그인 정상 동작 확인")
                    return True
                else:
                    count-=1
                    if count <= 0:
                        self.DBG.print_dbg("u+ ID 로그인 정상 동작 확인",False)
                        return False
                    else:
                        Slack.send_slack_text(log=f"u+ ID 로그인 {count}회 재실행중...",test_result=None)
            return False
        except Exception:
            print(traceback.format_exc())


        # 로그아웃
    def logout(self):
        self.FC.gotoHome()
        try:                
            self.FC.loading_find_css('.c-btn-menu').re_click()
            self.FC.wait_loading()
            count=1
            max_count=5
            while True:
                if self.FC.var['common_el']['gnb_url'] in self.driver.current_url or count>max_count:
                    break
                self.FC.loading_find_css_pre(self.FC.var['common_el']['메인_메뉴']).re_click()
                self.FC.loading_find_css_pre(self.FC.var['login_el']['로그인 여부'])
                count+=1
            self.FC.loading_find_css_pre(var.login_el['logout_btn']).re_click()
            self.FC.wait_loading()
            assert self.FC.loading_find_css_pre(var.mainpage_el['KV']).get_property('baseURI') in self.FC.var['common_el']['url'], self.DBG.logger.debug("로그아웃 후 메인페이지 이동 실패")

            assert self.FC.is_login()==False , self.DBG.logger.debug("정상 로그아웃 실패")
            self.driver.back()
    
        except  Exception as e :
            self.DBG.print_dbg("로그아웃 정상 동작 확인",False)
            return False

        else :
            self.DBG.print_dbg("로그아웃 정상 동작 확인")
            return True
        
    def do_login(self, login_type:str):
        '''
        U+ID, 카카오, 네이버 로그인
        '''
        self.FC.gotoHome()
        try:
            if self.driver.current_url != self.FC.var['login_el']['url']:
                self.FC.movepage(self.FC.var['login_el']['login_btn'],address=self.FC.var['login_el']['url'])

            self.FC.is_exists_element_click(self.FC.loading_find_css(self.FC.var['login_el']['ID로그인_btn'])) # 간편 로그인 화면 처리
            self.FC.is_exists_element_click(self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_login_img']))
            self.FC.wait_loading()
            self.FC.modal_ck2() # 결함 DCBGQA-4368
            
            dict = {
                "uplus" : [os.environ['UPLUS_ID'], os.environ['UPLUS_PW']],
                "kakao" : [],
                "naver" : [],
            }    

            self.FC.is_exists_element_click(self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_입력한문자삭제']))
            # self.FC.is_exists_element_click(self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_id_저장']))
            self.FC.wait_loading()
            
            self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_id_input']).send_keys(dict[login_type][0])

            if login_type == "uplus":
                self.FC.is_exists_element_click(self.FC.loading_find_css('.c-ttp-inner .item:nth-of-type(1) .nm-tooltip-button'))
                for _ in range(3):
                    try:
                        if self.FC.loading_find_css('.c-tooltip') == False:
                            self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_pw_input']).send_keys(dict[login_type][1])
                            break
                        else:
                            self.FC.is_exists_element_click(self.FC.loading_find_css('.c-ttp-inner .item:nth-of-type(1) .nm-tooltip-button'))

                    except:
                        raise Exception('로그인 실패 : tooltip 처리 실패')
            
            else:
                self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_pw_input']).send_keys(dict[login_type][1])
                
            self.FC.click_until_go_page(self.FC.loading_find_css(self.FC.var['login_el'][f'{login_type}_login_btn']))

            # # # 유플러스 로그인 후 정상적으로 메인페이지로 이동했는지 확인
            assert self.FC.var['common_el']['url'] in self.FC.loading_find_css(self.FC.var['mainpage_el']['개인화']).get_property('baseURI'), self.DBG.logger.debug("u+ ID 로그인 후 메인페이지 이동 실패")


        except Exception as e:
            self.DBG.print_dbg(f"{login_type} 로그인 정상 동작",False)
            return False

        else :
            self.DBG.print_dbg(f"{login_type} 로그인 정상 동작")
            return True
            
    # # 리캡차로 수동 조작 필요
    # def naver_login(self):


    # # 리캡차로 수동 조작 필요
    # def kakao_login(self):


    # def usim_login(self):
        

    # def my_lg_login(self) -> bool:


if __name__ == "__main__":
    try:
        server = AppiumServer(4723)
        port = server.appium_service()
        if not server.waiting():
            raise Exception("서버 실행 불가")
        driver = AppDriver(port=port)
        FC = Function(driver)
        login = LoginPage(driver,FC)

        FC.pre_script()
        
        if FC.is_login():
            login.logout()
        login.u_plus_login()
        login.logout()
        # login.my_lg_login()
        # login.logout()

        driver.driver.quit()
        server.stop()
    except Exception as e:
        print(e)
        # os.system("lsof -P -i :4723 |awk NR==2'{print $2}'|xargs kill -9")
        # os.system(f"ios-deploy --kill --bundle_id com.lguplus.mobile.cs")