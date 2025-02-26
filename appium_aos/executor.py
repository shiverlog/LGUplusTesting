import os
import time
import threading

from base.appdriver import AppDriver
from base.server import AppiumServer

from common.function import Function
from common.debug import Debug
from common.slack import Slack

from pages.login import LoginPage
from pages.mainpage import MainPage
from pages.search import Search
from pages.mypage import MypagePage
from pages.mobile import MobilePage
from pages.iptv import InternetIptvPage
from pages.benefit import BenefitPage
from pages.support import SupportPage
from pages.direct import DirectPage
from pages.ujam import UjamPage
from pages.udoc import UdocPage


class Tests():
    def __init__(self,AppDriver:AppDriver):
        self.driver=AppDriver.driver
        self.FC=Function(AppDriver)
        self.DBG=Debug(AppDriver)

        self.LoginPage=LoginPage(AppDriver,self.FC)
        self.MainPage=MainPage(AppDriver,self.FC)
        self.Search=Search(AppDriver,self.FC)
        self.MypagePage=MypagePage(AppDriver,self.FC)
        self.MobilePage=MobilePage(AppDriver,self.FC)
        self.InternetIptvPage=InternetIptvPage(AppDriver,self.FC)
        self.BenefitPage=BenefitPage(AppDriver,self.FC)
        self.SupportPage=SupportPage(AppDriver,self.FC)
        self.DirectPage=DirectPage(AppDriver,self.FC)
        self.UjamPage=UjamPage(AppDriver,self.FC)
        self.UdocPage=UdocPage(AppDriver,self.FC)

    # 테스트 케이스 작성
    
    # 임시 주석
    def TestCase_Z_FLIP3(self):
        test_result = [] # 기능 수행 결과
        Slack.send_slack_title('And 실행 시작')
        print(str(self.driver.contexts))
        print("current => "+ str(self.driver.context))
        
        time.sleep(5)
        self.FC.pre_script()
        self.DBG.screenshot_del()
        

        self.FC.chrome_clear(version='beta')
        
        # # 로그인 통신 오류 발생 시, 1번까지 재실행
        self.FC.gotoHome()
        if self.FC.is_login():
            print("로그인 상태")
            self.LoginPage.logout()
            test_result.append(self.LoginPage.u_plus_login_retry(2,"uplus"))
            if all(test_result) is not True:
                return False

        else:
            print("비로그인 상태")
            test_result.append(self.LoginPage.u_plus_login_retry(2,"uplus"))
            self.LoginPage.logout()
            test_result.append(self.LoginPage.u_plus_login_retry(2,"uplus"))
            if all(test_result) is not True:
                return False

        
        self.FC.chrome_clear(version='beta')
        test_result.append(self.MainPage.mainpage_new())
        test_result.append(self.MainPage.mainpage_myinfo_new())
        
        test_result.append(self.Search.search())
        test_result.append(self.MypagePage.mypage())
        test_result.append(self.MypagePage.mypage_bill())
        test_result.append(self.MypagePage.mypage_use()) 

        test_result.append(self.MobilePage.mobile())
        test_result.append(self.MobilePage.mobile_plan())
        test_result.append(self.MobilePage.mobile_device())
        self.FC.chrome_clear(version='beta')

        test_result.append(self.InternetIptvPage.iptv())
        test_result.append(self.BenefitPage.benefit())
        test_result.append(self.BenefitPage.membership())
        test_result.append(self.SupportPage.support())
        test_result.append(self.DirectPage.direct())
        test_result.append(self.UjamPage.ujam())
        test_result.append(self.UdocPage.udoc())

        Slack.send_slack_title('And 실행 완료')

        self.driver.quit()
        self.FC.chrome_clear(version='beta')
        print(str(test_result))
        return all(test_result)

if __name__ == '__main__' :

    def Z_FLIP4_TEST_CASE():
        try:
            os.system("for /f \"tokens=1\" %t in (\'adb devices\') do ( adb -s %t shell am force-stop com.lguplus.mobile.cs)") # 앱 강제종료
            server=AppiumServer(4723)
            port=server.appium_service()
            if not server.waiting():
                print("Appium Server 재실행")
                server=AppiumServer(4723)
                port=server.appium_service()
                if not server.waiting():
                    raise BaseException("Appium Server 재실행 실패")


            driver = AppDriver(port=port)
            test=Tests(driver)
            result = test.TestCase_Z_FLIP3()
            print(f"result:{result}")
            server.stop(result)
            
        except BaseException as e:
            print(server.stop(False))
            # os.system('adb shell pm clear com.lguplus.mobile.cs')
            os.system(r'taskkill /f /t /im node.exe')
            raise RuntimeError(e)
            

    thread1=threading.Thread(target=Z_FLIP4_TEST_CASE)
    print("===== test thread start =====")
    thread1.start()
    thread1.join()
    # thread2.start()
    # thread2.join()
    
    print("===== test thread end =====")


