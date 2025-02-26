from datetime import datetime, timedelta 
import json
import os, getpass
import signal
import time
import traceback
# from PIL import Image
# import pytesseract

# import pyperclip
import requests
from base.appdriver import AppDriver
from base.server import AppiumServer
from selenium.webdriver.support.ui import WebDriverWait
from common.function import Function
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.login import LoginPage
import math
import ssl
print(ssl.OPENSSL_VERSION)

class AppDriver속도측정(AppDriver):
    count=0 # 디버그 스크린샷 파일명 연번 static
    def __init__(self,port:int|str=4723,device_name:str='갤럭시_S24_PLUS'):
        self.path = super().path_split()
        # super().download_chromedriver()
        self.option = self.set_options(device_name)
        self.driver = super().remote_aos(port,self.option)
        self.udid=self.option['appium:options']['udid']
        # self.timeout = 10
        self.timeout = 5
        self.wait = WebDriverWait(self.driver, timeout=self.timeout)
        self.action = ActionChains(self.driver)
        
    def set_options(self,device_name:str,devices_path="base\\devices.json"):
        '''
        ['chromedriverExecutable'] 옵션 추가
        '''
        path = os.path.join(self.path, devices_path)

        option = {}
        with open (path,encoding='UTF8') as f:
            data =json.load(f)
            common = data["common"]
            device_opt = data[device_name]['appium:options']
            # chrome_path = self.exit_chrome_driver(common['chromedriverExecutable_appium_mw'])
            chrome_path = self.exit_chrome_driver(common['chromedriverExecutable'])
            if 'chromedriverExecutable' not in device_opt:
                device_opt['chromedriverExecutable']=""
            device_opt['chromedriverExecutable']=chrome_path

            option = data[device_name]
            f.close()
        return option
    
class AppiumServer속도측정(AppiumServer):
    def __init__(self,PORT:int|str=4723):
        super().__init__(PORT)
    
    def stop(self) -> bool:
        """
        appium 서버가 정상적으로 멈추면 True 반환
        """
        is_terminated = False
        if self.is_running:
            assert self.server_process
            self.server_process.send_signal(signal.CTRL_BREAK_EVENT)
            os.kill(self.server_process.pid,signal.SIGTERM)
            # os.system('adb shell pm clear com.lguplus.mobile.cs')
            # os.system('adb shell am force-stop com.sec.android.app.sbrowser.beta')
            print("----------- appium server stop -----------")
            is_terminated = True
        self.server_process = None
        return is_terminated

class Function속도측정(Function):
    def __init__(self,Driver:AppDriver):
        super().__init__(Driver)

    # def __call__(self, *args, **kwargs):
    #     start_time = time.time()
    #     print(f"{self.func.__name__} 실행 시작 시간: {datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")

    #     self.func(*args, **kwargs)  # 함수 실행

    #     end_time = time.time()
    #     print(f"{self.func.__name__} 실행 종료 시간: {datetime.datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")

    #     elapsed_time = end_time - start_time
    #     print(f"{self.func.__name__} 총 실행 시간: {elapsed_time:.2f}초")
        
    def find_csss(self,css):
        try:
            el=self.driver.find_elements(By.CSS_SELECTOR,css)[0]
        except:
            el=False
        return el

    def find_xpaths(self,xpath):
        try:
            el =self.driver.find_elements(By.XPATH,xpath)[0]
        except:
            el=False
        return el
    
    def wait_loading(self):
        loading_elem_css='div.c-loading-1'
        loading_elem_css1='*.b-skeleton'

        self.loading(loading_elem_css)
        self.loading(loading_elem_css1)
    
    def loading(self,css):
        max_count=10
        count=0
        self.driver.implicitly_wait(0.1)
        while True:
            try:
                loading_elem=self.driver.find_element(By.CSS_SELECTOR,css)
                count+=1
                if count>max_count:
                    raise UserWarning("무한 로딩")
            except UserWarning :
                print(f"{max_count} 무한 로딩 ")
                self.driver.implicitly_wait(10)
                break
            except Exception:
                break

    def wait_loading_속도체크(self):
        loading_elem_css='div.c-loading-1'
        loading_elem_css1='*.b-skeleton'

        self.loading_속도체크(loading_elem_css)
        self.loading_속도체크(loading_elem_css1)
    
    def loading_속도체크(self,css):
        max_count=100
        count=0
        # self.driver.implicitly_wait(0.1)
        while True:
            try:
                loading_elem=self.driver.find_element(By.CSS_SELECTOR,css)
                count+=1
                if count>max_count:
                    raise UserWarning("무한 로딩")
            except UserWarning :
                print(f"{max_count} 무한 로딩 ")
                # self.driver.implicitly_wait(10)
                break
            except Exception:
                break
    
    def is_exists_element_click(self,el):
        '''
        현재 페이지에 el이 존재하면 클릭
        '''
        self.wait = WebDriverWait(self.driver, timeout=1)    
        if el:
            el.click()
        self.wait = WebDriverWait(self.driver, timeout=self.timeout)    

class Tests():
    def __init__(self,AppDriver:AppDriver속도측정):
        self.Driver=AppDriver
        self.driver=AppDriver.driver
        self.driver.implicitly_wait(0.1)
        self.FC=Function속도측정(AppDriver)
        self.LoginPage=LoginPage(AppDriver,self.FC)
        self.속도측정데이터가져오기()

    def 속도측정데이터가져오기(self):
        file = os.getenv('SPEEDCHECK')
        with open(file,'r') as f:
            data = json.load(f)

        self.kt=data['kt']
        self.skt=data['skt']

    def 삼성브라우저_테스트(self):
        print(str(self.driver.contexts))
        self.driver.switch_to.context('NATIVE_APP')
        print("current => "+ str(self.driver.context))
        if self.FC.loading_find_id('com.sec.android.app.sbrowser.beta:id/help_intro_legal_agree_button'):
            self.FC.loading_find_id('com.sec.android.app.sbrowser.beta:id/help_intro_legal_agree_button').click()
            self.FC.loading_find_id('com.sec.android.app.sbrowser.beta:id/help_intro_legal_agree_button').click()
        self.driver.switch_to.context('WEBVIEW_Terrace')
        print("current => "+ str(self.driver.context))
        # self.FC.loading_find_id('com.sec.android.app.sbrowser.beta:id/location_bar_edit_text').send_keys("https://m.lguplus.com")
        # self.FC.loading_find_id('com.sec.android.app.sbrowser.beta:id/location_bar_edit_text').send_keys(Keys.ENTER)
        self.driver.get("https://www.google.com/")
        # self.LoginPage.u_plus_login()

        print(str(self.driver.contexts))

    def test(self,url,lcp:str):
        self.driver.implicitly_wait(0)
        self.driver.get(url)
        start = time.time()
        math.factorial(100000)
        if lcp.startswith('//'):
            self.Driver.wait.until(EC.visibility_of_element_located((By.XPATH, lcp)))
        else:
            self.Driver.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, lcp)))
        end = time.time()
        print(f"{end - start:.2f} sec",end='\t')

    def DCL_기준(self,url=''):
        self.driver.implicitly_wait(0)
        self.driver.get(url)
        start = time.time()
        math.factorial(100000)
        # self.FC.wait_loading_속도체크() # 로딩("고객님의 소중한 정보를 확인하고 있어요" 아님), 스켈레톤 완료
      
        self.Driver.wait.until(lambda d:self.driver.execute_script('return document.readyState;') == 'complete')
        end = time.time()
        print(f"{end - start:.2f} sec",end='\t')
    
    def LCP_기준(self,url='',lcp=''):
        self.driver.implicitly_wait(0)
        self.driver.get(url)
        start = time.time()
        math.factorial(100000)
        if lcp.startswith('//'):
            count =0
            while True:
                count+=1
                try:
                    el=self.FC.find_xpaths(lcp)
                    if el == False:
                        continue
                    visibility=self.FC.driver.execute_script("return arguments[0].checkVisibility({opacityProperty: true,visibilityProperty: true,contentVisibilityAuto: true});",el)
                    # print(visibility)
                    # print(count)
                    if visibility or count > 30:
                        break
                except:
                    pass
            # el=self.Driver.wait.until(EC.presence_of_all_elements_located((By.XPATH, lcp)))
            # print(el[0].get_property('outerHTML'))

            # self.Driver.wait.until(EC.visibility_of_any_elements_located((By.XPATH, lcp)))
        else:
            count =0
            while True:
                count+=1
                try:
                    el=self.FC.find_csss(lcp)
                    if el == False:
                        continue
                    visibility=self.FC.driver.execute_script("return arguments[0].checkVisibility({opacityProperty: true,visibilityProperty: true,contentVisibilityAuto: true});",el)
                    # print(visibility)
                    # print(count)
                    if visibility or count > 30:
                        break
                except:
                    pass
            # el=self.Driver.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tab-panel')))
            # print(el[0].get_property('outerHTML'))

            # self.Driver.wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, lcp)))
        end = time.time()
        print(f"{end - start:.2f} sec",end='\t')

    def LOAD_기준(self,url=''):
        self.driver.implicitly_wait(0)
        self.driver.get(url)
        math.factorial(100000)
        # self.FC.wait_loading_속도체크() # 로딩 아이콘 사라지고, 페이지 이동이 확실
        self.Driver.wait.until(lambda d:self.driver.execute_script('return performance.timing.loadEventEnd - performance.timing.navigationStart;') > 0)
        print(f"{self.driver.execute_script('return performance.timing.loadEventEnd - performance.timing.navigationStart;')/1000:.2f}",end='\t')

    def 로딩아이콘_제거_기준(self,url=''):
        self.driver.implicitly_wait(0)
        self.driver.get(url)
        start = time.time()
        math.factorial(100000)
        self.Driver.wait.until(lambda d:self.driver.execute_script('return document.readyState;') == 'complete')
        self.FC.wait_loading_속도체크()
        end = time.time()
        print(f"{end - start:.2f} sec",end='\t')

    def LCP_기준_v2(self,url=''):
        self.driver.implicitly_wait(0)
        if url != '':
            self.driver.get(url)
        # time.sleep(7)
        # self.Driver.wait.until(lambda d:self.driver.execute_script("new PerformanceObserver((entryList) => {console.dirxml(entryList.getEntries())}).observe({type:'largest-contentful-paint', buffered: true});") != None)
        # print(self.driver.execute_script("new PerformanceObserver((entryList) => {return entryList.getEntries() }).observe({type:'largest-contentful-paint', buffered: true});"))
        self.FC.driver.set_script_timeout(60)
        self.Driver.wait.until(lambda d:self.driver.execute_script('return document.readyState;') == 'complete')
        self.FC.wait_loading_속도체크() # 로딩 아이콘 사라지고, 페이지 이동이 확실
        time.sleep(5)
        # script = "var callback = arguments[arguments.length - 1]; "\
        #             "function getLCPEntries() {"\
        #             "return new Promise((resolve, reject) => {"\
        #             "const entries = [];"\
        #             "try {"\
        #             "const observer = new PerformanceObserver((entryList) => {"\
        #             "for(const entry of entryList.getEntries()){"\
        #             "entries.push(entry);}"\
        #             "if (entries.length > 0) {"\
        #             "resolve(entries);}"\
        #             "});"\
        #             "observer.observe({ type: 'largest-contentful-paint', buffered: true });"\
        #             "setTimeout(() => {"\
        #             "observer.disconnect();"\
        #             "resolve(entries);"\
        #             "}, 5000);"\
        #             "} catch (error) {"\
        #             "reject(error);}"\
        #             "});}"\
        #             "getLCPEntries().then((entries) => {"\
        #             "callback(entries)"\
        #             "}).catch((error) => {"\
        #             "callback(error)});"
                    
        script= "var callback = arguments[arguments.length - 1]; "\
                "const entries = [];"\
                "new PerformanceObserver((entryList) => {"\
                "for (const entry of entryList.getEntries()){"\
                "entries.push(entry);"\
                "}"\
                "callback(entries);"\
                "}).observe({type: 'largest-contentful-paint', buffered: true});"
        datas =self.driver.execute_async_script(script)
        data=datas[-1]
        # for data in datas:
        #     for key, val in data.items():
        #         if key == 'element' and val != None:
        #             print(f"{key}: {val.get_property('outerHTML')}")
        #         else:
        #             print(f"{key}: {val}")

        print(f"element: {data.get('element').get_property('outerHTML') if data.get('element',None) !=None else None }")
        print(f"startTime: {data['startTime']/1000:.2f}")

        print("전==========================================================")
        time.sleep(10)
        script= "var callback = arguments[arguments.length - 1]; "\
                "const entries = [];"\
                "new PerformanceObserver((entryList) => {"\
                "for (const entry of entryList.getEntries()){"\
                "entries.push(entry);"\
                "}"\
                "callback(entries);"\
                "}).observe({type: 'largest-contentful-paint', buffered: true});"
        datas =self.driver.execute_async_script(script)
        data=datas[-1]
        print(f"element: {data.get('element').get_property('outerHTML') if data.get('element',None) !=None else None }")
        print(f"startTime: {data['startTime']/1000:.2f}")

        print("후==========================================================")

    def LCP_기준_v3(self,url=''):
        self.driver.implicitly_wait(0)
        if url != '':
            self.driver.get(url)
        self.FC.driver.set_script_timeout(60)
        self.Driver.wait.until(lambda d:self.driver.execute_script('return document.readyState;') == 'complete')
        self.FC.wait_loading_속도체크()
        time.sleep(10)
        script= "var callback = arguments[arguments.length - 1]; "\
                "const entries = [];"\
                "new PerformanceObserver((entryList) => {"\
                "for (const entry of entryList.getEntries()){"\
                "entries.push(entry);"\
                "}"\
                "callback(entries);"\
                "}).observe({type: 'largest-contentful-paint', buffered: true});"
        datas =self.driver.execute_async_script(script)
        data=datas[-1]
        if type(data['element']) != type(None):
            print(f" {data['startTime']/1000:.2f}",end="\n")
            # print(data['element'].get_property('outerHTML'))

        else:
            time.sleep(10)
            # print(datas)
            # print(data)
            # print(datas[0]['element'].get_property('outerHTML'))
            script= "var callback = arguments[arguments.length - 1]; "\
                "const entries = [];"\
                "new PerformanceObserver((entryList) => {"\
                "for (const entry of entryList.getEntries()){"\
                "entries.push(entry);"\
                "}"\
                "callback(entries);"\
                "}).observe({type: 'largest-contentful-paint', buffered: true});"
            datas =self.driver.execute_async_script(script)
            data=datas[-1]
            print(f" {data['startTime']/1000:.2f}",end="\n")
            # print(datas[-1])
        return data['startTime']/1000

    def get_현재_시간(self,switch=True):
        '''
        switch(True) : %Y-%m-%d %H:%M:%S
        switch(False) : %Y-%m-%d

        '''
        now = datetime.now()
        if switch:
            return now.strftime('%Y-%m-%d %H:%M:%S')  
        else:
            return now.strftime('%Y-%m-%d')  

    def kt_login(self):
        try:
            self.driver.get('https://m.kt.com/')
            # time.sleep(5)
            # print('go go')
            # 팝업
            self.FC.is_exists_element_click(self.FC.loading_find_css_pre('div#mainpop02 button.layer-stop'))
            self.FC.is_exists_element_click(self.FC.loading_find_css_pre('div#mainpop02 button[title*="닫"]'))

            
            self.FC.loading_find_css('a.btn_blk').click()

            print(self.FC.loading_find_css_pre('input[name="userId"]').get_property('value'))

            self.FC.is_exists_element_click(self.FC.loading_find_css_pre('div:not([style="visibility: hidden;"]) div#mainpop02 button[title*="닫"]'))

            if self.kt['id'] not in self.FC.loading_find_css_pre('input[name="userId"]').get_property('value'):
                for word in self.kt['id']:
                    print(word)
                    self.FC.loading_find_css_pre('input[name="userId"]').send_keys(word)
                    time.sleep(.2)
            
            for word in self.kt['pw']:
                print(word)
                self.FC.loading_find_css_pre('input[name="password"]').send_keys(word)
                time.sleep(.2)

            # pyperclip.copy(self.kt['id'])
            # if self.kt['id'] not in self.FC.loading_find_css_pre('input[name="userId"]').get_property('value'):
            #     self.FC.loading_find_css_pre('input[name="userId"]').click()
            #     self.FC.loading_find_css_pre('input[name="userId"]').send_keys(Keys.CONTROL,'v')

            # time.sleep(1)
            # pyperclip.copy(self.kt['pw'])
            # self.FC.loading_find_css_pre('input[name="password"]').click()
            # self.FC.loading_find_css_pre('input[name="password"]').send_keys(Keys.CONTROL,'v')
            # time.sleep(1)

            # self.FC.is_exists_element_click(self.FC.loading_find_css_pre('div#mainpop02 button.layer-stop'))
            # self.FC.is_exists_element_click(self.FC.loading_find_css_pre('div:not([style="visibility: hidden;"]) div#mainpop02 button[title*="닫"]'))
            self.FC.loading_find_css_pre('button#loginSubmit').click()

            self.Driver.wait.until(lambda d:self.driver.execute_script('return document.readyState;') == 'complete')
            time.sleep(15)

            assert self.FC.loading_find_css_pre('div.homeMain').get_property('baseURI') == 'https://m.kt.com/',print('kt 로그인 실패')
            print("kt 로그인 성공")
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    # def 리캡챠_테스트(self):
    #     img = Image.open(r"result/recapcha.png")
    #     # pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
    #     pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\유닉솔루션(주)\\AppData\\Local\\tesseract.exe'
    #     try:
    #         # print(pytesseract.image_to_string('test.jpg', timeout=2)) # Timeout after 2 seconds
    #         print(pytesseract.image_to_string('test.jpg', timeout=0.5)) # Timeout after half a second
    #         print(pytesseract.image_to_string('result/recapcha.png')) # Timeout after half a second
    #         print(pytesseract.image_to_string(img)) # Timeout after half a second
    #     except RuntimeError as timeout_error:
    #         print(traceback.format_exc())
    #         print(timeout_error)
    #     # captcha_text = pytesseract.image_to_string(img)
    #     # print(captcha_text)

    def skt_login(self):
        try:
            self.driver.get('https://m.tworld.co.kr/v6/main')
            time.sleep(5)
            # 팝업
            self.FC.is_exists_element_click(self.FC.loading_find_css_pre('div.modal-content-transition button.check-btn'))

            self.FC.loading_find_css('div.g-line-user a[href*="login"]').click()

            # 자동 로그인(저장된 아이디)
            if self.FC.loading_find_css('.account-list a.account-info'):
                self.FC.is_exists_element_click(self.FC.loading_find_css('.account-list a.account-info'))
            else:
                self.FC.loading_find_css_pre('input#userId').send_keys(self.skt['id'])
                self.FC.loading_find_css_pre('input#password').send_keys(self.skt['pw'])
                self.FC.loading_find_css_pre('button#authLogin').click()
                self.Driver.wait.until(lambda d:self.driver.execute_script('return document.readyState;') == 'complete')
            assert self.FC.loading_find_css('main.main').get_property('baseURI') == 'https://m.tworld.co.kr/v6/main',print('skt 로그인 실패')
            print("skt 로그인 성공")
        except Exception as e:
            print(e)

if __name__ == '__main__' :

    cwd = os.getcwd()
    if 'test' not in cwd:
        cwd += '\\test'

    print(f">>>{cwd}")
    # 자동 속도 측정 시, 따로 저장할 json
    자동_속도측정_결과_경로 =f'{cwd}\\output\\속도측정_결과.json' 
    # 수동,자동 속도측정 결과를 작성랑 로그 파일
    수동자동_결과_로그_경로 =f'{cwd}\\output\\결과.json'
    # 자동 속도측정 기본 포맷
    자동_속도측정_결과_포맷_경로 =f'{cwd}\\output\\속도측정_포맷.json'

    # def 리캡챠_테스트():
    #     img = Image.open(r"result/recapcha2.png")
    #     # pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
        # pytesseract.pytesseract.tesseract_cmd = f'C:\\Users\\{getpass.getuser}\\AppData\\Local\\tesseract.exe'
    #     try:
    #         # print(pytesseract.image_to_string('test.jpg', timeout=2)) # Timeout after 2 seconds
    #         print(pytesseract.image_to_string('result/recapcha2.png',config=('--oem 3 --psm 6'))) # Timeout after half a second
    #         print(pytesseract.image_to_string(img,config=('--oem 3 --psm 6'))) # Timeout after half a second
    #     except RuntimeError as timeout_error:
    #         print(traceback.format_exc())
    #         print(timeout_error)
    #     # captcha_text = pytesseract.image_to_string(img)
    #     # print(captcha_text)
    
    def 자동_속도측정(): # 33~11
        try:
            속도측정_포맷 = {}
            with open(자동_속도측정_결과_경로,encoding='utf-8') as f:
                속도측정_포맷=json.load(f)
                f.close()


            server=AppiumServer속도측정(4723)
            port=server.appium_service()
            if not server.waiting():
                raise Exception("서버 실행 불가")
            

            # driver = AppDriver속도측정(port=port,device_name="Z_FLIP4_삼성인터넷")
            driver = AppDriver속도측정(port=port)
            test=Tests(driver)

            test.삼성브라우저_테스트()

        
            속도측정_결과 = 속도측정_포맷.copy()
            통신사s = ["kt","lg","skt"]
            # 통신사s = ["kt"]
            # 통신사s = ["skt"]

            for 통신사 in 통신사s:
                if 통신사 == "kt":
                    test.kt_login()
                elif 통신사 == "lg":
                    test.LoginPage.u_plus_login()
                elif 통신사 == "skt":
                    test.skt_login()
                    

                for count in range(0,5):
                    for 페이지명,값 in 속도측정_결과[통신사].items():
                        print(f" {통신사} - {페이지명} ",end="\t")
                        if 통신사 == "kt" and 페이지명 =="gnb": 
                            측정속도 = -1 # kt gnb는 페이지가 아닌 UI라 측정X
                        else:
                            측정속도 = test.LCP_기준_v3(값["url"])
                        if 측정속도 == -1:
                            값['측정'].append({"date":test.get_현재_시간(),"value":0.0}) 
                        else:
                            값['측정'].append({"date":test.get_현재_시간(),"value":round(측정속도,2)}) 
                    with open(자동_속도측정_결과_경로,'w',encoding='utf-8') as f:
                        json.dump(속도측정_결과,f,ensure_ascii=False,indent=4)
                        f.close()
            print(속도측정_결과)
            server.stop()
            
        except BaseException as e:
            raise RuntimeError(e)
        
    def 로그_저장():

        # 속도측정 결과 가져오기
        속도측정_결과={}
        with open(자동_속도측정_결과_경로,encoding='utf-8') as f:
            속도측정_결과=json.load(f)
            f.close()
        
        # 속도측정 결과 저장
        result=[]
        with open(수동자동_결과_로그_경로,'w',encoding='utf-8') as f:
            for 통신사,통신사값 in 속도측정_결과.items():
                for 페이지명,페이지값 in 통신사값.items():
                    평균값=0.0
                    for 측정 in 페이지값["측정"]:
                        평균값 +=측정["value"]
                    print(len(페이지값["측정"]))
                    평균값 = round(평균값/len(페이지값["측정"]),2)
                    result.append({"code":페이지값["page_id"],"value":평균값,"tested_at":페이지값["측정"][-1]["date"]})

            json.dump(result,f,ensure_ascii=False,indent=4)
            # f.write(result)
            f.close()

    def 현재_날짜():
        now = datetime.now()
        # now = datetime.now() - timedelta(days=1)
        return now.strftime('%Y%m%d')


    def 전송(url:str="https://dcms.uhdcsre.com/dcms/qa"):
        date = 현재_날짜()
        # print(date)
        _data={}
        
        with open(수동자동_결과_로그_경로,encoding='utf-8') as f:
            _data=json.load(f)
            
            try:
                # 정상 데이터 검증 ------------------------------
                now = datetime.now()
                now.strftime('%Y-%m-%d')
                if True in [True for i in _data if "APP" in str(list(i.values()))]: 
                    raise Exception("APP 측정값이 존재합니다.")
                elif True in [True for i in _data if "MW" in str(list(i.values()))] and True in [True for i in _data if now.strftime('%Y-%m-%d') in str(list(i.values()))]:
                    pass
                else:
                    raise Exception("데이터를 다시 확인해주세요")
                # 정상 데이터 검증 ------------------------------

                # 자동: A / 수동: M
                res = requests.post(url,json=_data,params={"date":date,"div":"A"}) # 500 error
                print(res)
                if res.status_code == 200:
                    print(f"{date} 전송 완료")
                else:
                    print("전송 실패")
            except Exception as e:
                print("전송 실패")
                print(e)
            
            f.close()




    # 리캡챠_테스트()
    자동_속도측정() # 자동화 속도측정 수행
    로그_저장() # 속도측정_결과.json -> 결과.json 내보내기
    # 전송() # 결과.json 전송