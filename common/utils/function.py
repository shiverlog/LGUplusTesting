from asyncio.windows_events import NULL
import traceback
from types import NoneType
import time
import os       #스크린샷 삭제시 사용
from typing import List
from openpyxl import load_workbook
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # 시간대기 모듈
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import InvalidSelectorException


# *** 주석 정리 ***
# 1. loading_find_* 해당 함수 내에서 동작하는 반복문은 간헐적으로 selenium.common.exceptions.TimeoutException이 발생하는 이슈에 대한 방안

class Function():
    # wait 반복 횟수
    retry_count= 3 
    def __init__(self,Driver:WebDriver):
        self.driver = Driver.driver 
        self.os = Driver.os 
        self.wait = Driver.wait
        self.action = Driver.action
        self.var=self.set_variables()


    def set_variables(self):
        '''
        variables.xlsx 파일에 저장된 요소 변수값을 가져와 dict 타입 파싱
        '''
        # data_only=True로 해줘야 수식이 아닌 값으로 받아온다. 
        load_wb = load_workbook(f"{os.getcwd()}\\variables.xlsx", data_only=True)
        # 시트 이름으로 불러오기 
        load_ws = load_wb['Sheet']
        
        
        all_values = {}
        for row in load_ws.rows:
            # A1 셀은 공백으로 패스
            if row[0] == load_ws['A1']:
                # print(f"{row[0]} == {load_ws['A1']}")
                continue

            # 데이터 유무(count number)
            if row[0].value:

                page_name =  row[1].value # B1
                key = row[2].value # C1
                value = row[3].value # D1
                assert page_name or key or value, print("일부 데이터 None")
                
                # {} 초기화
                try:
                    all_values[page_name] 
                except:
                    all_values[page_name] = {}

                all_values[page_name][key] = value
            elif row[0].value == row[1].value == row[2].value == row[3].value is None:
                return all_values
            else:
                # print(f"{row[0].value}  {row[1].value}  {row[2].value} {row[3].value}")
                assert row[0] or row[1] or row[2] or row[3], print("일부 데이터 비어있음")
        load_wb.close()
        return all_values

    # def find_css(self,loc):
    #     self.find = self.driver.find_element(By.CSS_SELECTOR, loc)
    #     return self.find

    # def find_csss(self,loc):
    #     self.find = self.driver.find_elements(By.CSS_SELECTOR, loc)
    #     return self.find

    # def find_xpath(self,loc):
    #     self.find = self.driver.find_element(By.XPATH, loc)
    #     return self.find

    # def find_xpaths(self,loc):
    #     self.find = self.driver.find_elements(By.XPATH, loc)
    #     return self.find

    def modal_ck(self):
        try:
            self.wait_loading()
            self.driver.implicitly_wait(1)
            self.modal_ck1()
            # print(self.loading_find_css_pre(self.var['common_el']['body']).get_property('className'))
            self.modal_ck2()
            # print(self.loading_find_css_pre(self.var['common_el']['body']).get_property('className'))
            # self.modal_ck3()
            # print(self.loading_find_css_pre(self.var['common_el']['body']).get_property('className'))
            self.driver.implicitly_wait(7)
            self.wait_loading()
        except Exception:
            self.driver.implicitly_wait(7)
            self.wait_loading()
            pass

    def modal_ck1(self):
        try:
            if self.loading_find_css_pre(self.var['common_el']['body']).get_property('className') == "modal-open":
                self.driver.find_element(By.CSS_SELECTOR,self.var['common_el']['모달창_체크박스']).click()
            else:
                return
        except Exception:
            pass

    def modal_ck2(self):
        try:
            if self.loading_find_css_pre(self.var['common_el']['body']).get_property('className') == "modal-open":
                self.driver.find_element(By.CSS_SELECTOR,self.var['common_el']['모달창_닫기']).click()
            else:
                return
        except Exception:
            pass

    def modal_ck3(self):
        try:
            if self.loading_find_css_pre(self.var['common_el']['body']).get_property('className') == "modal-open":
                self.loading_find_css_pre(self.var['common_el']['모달창_버튼']).click()
            else:
                return
        except Exception:
            pass

    def modal_ck_ins(self):
        try:
            if self.loading_find_css_pre(self.var['common_el']['딤드']):
                self.loading_find_css_pre(self.var['common_el']['모달창_버튼_ins']).click()
            else:
                return
        except Exception:
            pass

    def movepage(self,*btns:str,address:str=''):
        '''
        GNB 메뉴 이동
        *kwarg에 address 인자가 있을 시, 햄버거 메뉴 이동 후 현재 url에 address 값이 포함될 때까지 반복

        :Usage:
            ::
                FC.movepage(btn1,btn2,btn3,address="https://www.lguplus.com")
        '''
        hamburger_main = self.var['common_el']['메뉴_버튼']
        for i in range(self.retry_count):
            try:
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, hamburger_main)))
                self.driver.find_element(By.CSS_SELECTOR, hamburger_main).click()
                self.wait_loading()
                for btn in btns:
                    # Xpath
                    if btn.startswith('//'):
                        self.wait.until(EC.presence_of_element_located((By.XPATH,btn)))
                        el=self.driver.find_element(By.XPATH, btn)
                    # CSS Selector
                    else:
                        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, btn)))
                        el=self.driver.find_element(By.CSS_SELECTOR, btn)
                    # 메뉴 전체 펼침 버튼 클릭 
                    if "전체 펼침" in self.driver.find_element(By.CSS_SELECTOR,self.var['common_el']['전체_펼침']).get_property('innerText'):
                        open_list=self.driver.find_element(By.CSS_SELECTOR,self.var['common_el']['전체_펼침'])
                        self.driver.execute_script("arguments[0].scrollIntoView(false);", open_list)
                        open_list.click()
                        time.sleep(0.5)

                    self.driver.execute_script("arguments[0].scrollIntoView(false);", el)
                    el.click()
                    self.wait_loading()

                self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.var['common_el']['메뉴_버튼'])))

                # 현재 url이 address 인자값과 같으면 return(멈춤)
                if address in self.driver.current_url:
                    return

            except Exception:
                
                # 만약 햄버거 사이드바가 열린 상태일 때, 닫기
                if var.common_el['gnb_url'] in self.driver.current_url :
                    self.driver.find_element(By.CSS_SELECTOR,self.var['common_el']['뒤로가기_버튼']).click()
                    time.sleep(0.5)

                # self.retry_count번 반복해서 요소를 찾아도 없으면 False 반환
                if i == self.retry_count-1:
                    print(f"movepage({address}) 실패했습니다.")
                    return False
                else:
                    continue

    def close_popup(self,num):
        '''
        새로운 창을 모두 가져와 하나씩 닫기

        :Usage:
            ::
                FC.closw_popup(driver.window_handles)
        '''
        size  = len (num)

        for i in range(size):
            if num[i]  != num[0]:
                self.driver.switch_to.window(num[i])
                self.driver.close()

        self.driver.switch_to.window(num[0])
        
    def loading_find_css(self,elem) -> (WebElement):
        '''
        페이지 로드 후, css 요소 찾기
        '''
        for i in range(self.retry_count):
            try:
                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,elem)))
                self.find=self.driver.find_element(By.CSS_SELECTOR,elem)
                if self.find != NoneType:
                    return self.find

            except Exception:
                if i == self.retry_count-1:
                    print("해당 페이지에서 요소를 찾을 수 없습니다.")
                    return False
                
    def loading_find_csss(self,elem) -> (List[WebElement]):
        '''
        페이지 로드 후, css 요소 List 찾기
        '''
        for i in range(self.retry_count):
            try:
                self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,elem)))
                self.find=self.driver.find_elements(By.CSS_SELECTOR,elem)
                if self.find != NoneType:
                    return self.find

            except Exception:
                if i == self.retry_count-1:
                    print("해당 페이지에서 요소를 찾을 수 없습니다.")
                    return [False]

    def loading_find_css_pre(self,elem) -> (WebElement):
        '''
        페이지 로드 후, 페이지의 DOM에서 css 요소 찾기
        '''
        for i in range(self.retry_count):
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,elem)))
                self.find=self.driver.find_element(By.CSS_SELECTOR,elem)
                if self.find != NoneType:
                    return self.find

            except Exception:
                if i == self.retry_count-1:
                    print("해당 페이지에서 요소를 찾을 수 없습니다.")
                    return False

    def loading_find_xpath(self,elem) -> (WebElement):
        '''
        페이지 로드 후, xpath 요소 찾기
        '''
        for i in range(self.retry_count):
            try: 
                self.wait.until(EC.visibility_of_element_located((By.XPATH,elem)))
                self.find=self.driver.find_element(By.XPATH,elem)
                if self.find != NoneType:
                    return self.find

            except Exception:
                if i == self.retry_count-1:
                    print(f"해당 페이지에서 요소를 찾을 수 없습니다.")
                    return False

    def loading_find_xpath_pre(self,elem) -> (WebElement):
        '''
        페이지 로드 후, 페이지의 DOM에서 xpath 요소 찾기
        '''
        for i in range(self.retry_count):
            try: 
                self.wait.until(EC.presence_of_element_located((By.XPATH,elem)))
                self.find=self.driver.find_element(By.XPATH,elem)
                if self.find != NoneType:
                    return self.find

            except Exception:
                if i == self.retry_count-1:
                    print(f"해당 페이지에서 요소를 찾을 수 없습니다.")
                    return False

    def loading_find_xpaths(self,elem) -> (List[WebElement]):
        '''
        페이지 로드 후, xpath 요소 List 찾기
        '''
        for i in range(self.retry_count):
            try: 
                self.wait.until(EC.presence_of_all_elements_located((By.XPATH,elem)))
                self.find=self.driver.find_elements(By.XPATH,elem)
                if self.find != NoneType:
                    return self.find
            except Exception:
                if i == self.retry_count-1:
                    print(f"해당 페이지에서 요소를 찾을 수 없습니다.")
                    return [False]
             
    def loading(self,css):
        max_count=10
        count=0
        self.driver.implicitly_wait(1)
        
        while True:
            try:
                time.sleep(0.5)
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

    def wait_loading(self):
        '''
        해당 페이지 렌더링이 끝날 때 까지 대기
        '''
        loading_elem_css='div.c-loading-1'
        loading_elem_css1='*.b-skeleton'
        
        self.loading(loading_elem_css)
        self.loading(loading_elem_css1)
        max_count=10
        count=0
        while True:
            page_loading = self.driver.execute_script('return document.readyState;')
            if page_loading == 'complete':
                break
            count +=1
            time.sleep(0.5)
            if count >= max_count:
                raise Exception("무한로딩")

    def text_list_in_element(self,parent:str,list: list):
        '''
        요소에 text가 존재하는 확인
        parent: text 존재를 확인할 요소
        list: 확인할 text list
        :Usage:
            ::
                FC.text_list_in_element(element,['text1','text2','text3 ...])
        '''
        for i in range(self.retry_count):
            try:
                if parent.startswith('//'):
                    parent_el=self.wait.until(EC.presence_of_element_located((By.XPATH,parent)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", parent_el)
                    parent_text=parent_el.get_property('innerText')                
                else:
                    parent_el=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,parent)))
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", parent_el)
                    parent_text=parent_el.get_property('innerText')                
                        
                if parent_text is not None:
                    pass
            except Exception:
                if i == self.retry_count-1:
                    print("해당 페이지에 부모 요소를 찾을 수 없습니다. ")
                    return False
                else:
                    pass

        for t in list:
            if t not in parent_text:
                print("'"+ t + "' 텍스트를 찾을 수 없습니다.")
                return False                
        else:
            pass
        return True    
        
    def scroll_center(self,el):
        '''
        JS Execute; el요소를 중간으로 scroll
        '''
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        return

    def scroll(self,height):
        '''
        JS Execute; height까지 scroll 
        '''
        while True:
            self.driver.execute_script(f"window.scrollTo(0,{height});")
            current_scrollTop=self.driver.execute_script("return document.scrollingElement.scrollTop")
            time.sleep(0.5)
            if current_scrollTop >= height:
                break
    
    def scroll_el(self,loc:str|WebElement|int,view='true'):
        '''
        JS Execute; el을 view(true:상위/false:하위) 위치 까지 scroll
        '''
        try:
            if type(loc) == str:
                if loc.startswith('/'):
                    self.wait.until(EC.presence_of_element_located((By.XPATH, loc)))
                    el=self.driver.find_element(By.XPATH, loc)
                    self.driver.execute_script("arguments[0].scrollIntoView("+view+");", el)
                else:
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, loc)))
                    el=self.driver.find_element(By.CSS_SELECTOR, loc)
                    self.driver.execute_script("arguments[0].scrollIntoView("+view+");", el)
            elif type(loc) == WebElement:
                self.driver.execute_script("arguments[0].scrollIntoView("+view+");", loc)
            elif type(loc) == int:
                for i in range(0,loc):
                    self.driver.swipe(75,500,75,0,800)
                    print(f"swipping {i}")
            else:
                raise Exception('scroll_el() type error')
        except BaseException as e:
            el=None
            print(e)
            raise Exception('swipe error')

    def gotoHome(self):
        '''
        메인페이지로 이동
        '''
        self.driver.get(var.common_el['home_url'])
        self.modal_ck()
        self.modal_ck3()
    
    def goto_url(self,url:str):
        self.driver.get(url)
        self.wait_loading()
    
    def is_login(self):
        '''
        로그인 상태 확인
        '''
        hamburger_main = self.var['common_el']['메뉴_버튼'] 
        for i in range(self.retry_count):
            try:
                obj=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, hamburger_main)))
                self.driver.find_element(By.CSS_SELECTOR, hamburger_main).click()
                self.wait_loading()
                logout_text=self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.var['common_el']['로그인_box']))).get_property('innerText')
                self.driver.find_element(By.CSS_SELECTOR, self.var['common_el']['뒤로가기_버튼']).click()
                if obj is not None and obj !=NoneType and logout_text is not None and logout_text !=NoneType and logout_text != '' and logout_text != NULL:
                    break
            except:
                # self.retry_count번 반복해서 요소를 찾아도 없으면 False 반환
                if i == self.retry_count-1:
                    return False 

        if "로그아웃" in logout_text or "반갑습니다" in logout_text:
            return True
        elif "로그인" in logout_text:
            return False
        else:
            try:
                raise Exception(f'is_login() return error => {logout_text}')
            except Exception as e:
                return print(e)

    def bring_el_to_front_css(self,css):
        '''
        JS Execute; css로 요소를 찾아 앞으로 가져오기
        '''
        self.driver.execute_script(f"document.querySelector('{css}').style.cssText='display: block!important; visibility: visible!important; position: relative !important; z-index: 1000000000000000000000000000000000000000000000000!important;'") 
        el=self.loading_find_css_pre(css)
        if el.is_displayed() is True:
            return
        else:        
            self.driver.execute_script(f"document.querySelector('{css}').style.cssText='display: block!important; visibility: visible!important; position: fixed!important; z-index: 1000000000000000000000000000000000000000000000000!important;'") 
            el=self.loading_find_css_pre(css)
            if el.is_displayed() is True:
                return
            else:
                try:
                    raise Exception()
                except Exception as e:
                    print("bring_el_to_front_css() is failed => " +e)

    def wait_datas(self,parent_loc:str,*tag_names:str):
        '''
        태그의 innerText 출력 확인(공백X,빈란X)
        parent_loc:태그를 검색할 상위 부모(조상)요소
        tag_names: 가장 하위(자식) 태그여야 함
        '''
        self.driver.implicitly_wait(1) # 1초동안 요소 대기
        # 태그 Selector 전처리
        if parent_loc.startswith('//'):
            by=By.XPATH
            tags=[]
            for tag_name in tag_names:
                tags.append('//'+tag_name)
            tag_names=tags
        else:
            by=By.CSS_SELECTOR
            tags=[]
            for tag_name in tag_names:
                tags.append(' '+tag_name)
            tag_names=tags
        # print(f"{parent_loc}{tag_names[0]}")
        try:
            for tag_name in tag_names:
                count=0
                # print(f"검색 : {parent_loc}{tag_name} ")
                while True:
                    datas=self.driver.find_elements(by, f"{parent_loc}{tag_name}")
                    # print(f"datas => {len(datas)}")
                    for data in datas:
                        if data.get_property('childElementCount') >0:
                            if [child for child in data.get_property('children') if child.get_property('tag_name') in tag_names] == []: 
                                #자식요소가 있지만, 자식 요소 중 동일한 태그명이 존재하지 않으면 내가 확인을 원하는 데이터일 확률이 높으므로 이어서 실행 
                                pass
                            else:
                                if len(datas)-1 == datas.index(data): # 마지막 요소면 True 반환
                                    datas = True
                                    break
                                # 아니면 실행X
                                continue
                        data_txt=data.get_property('innerText')
                        # print(f"data_txt => {data_txt}")
                        # if data_txt == '' or data_txt..startswith(' ') : # data 미출력 시, max_count까지 반복
                        if data_txt.strip(' ') == ''  : # data 미출력 시, max_count까지 반복
                            break
                        elif len(datas)-1 == datas.index(data): # 특정 태그의 데이터가 모두 정상 출력 시, 다음 태그 체크를 위해 datas = True 할당
                            # print(f"{tag_name}의 datas 정상 출력 확인1")
                            datas = True
                            break
                    count+=1              
                    if count >=self.retry_count: # max_count 이상일 경우, 해당 tag_name return
                        # print(f"{tag_name} 미출력")
                        return tag_name
                    if datas is True: # datas 모두 정상출력 확인
                        break
                    time.sleep(0.5)
            # print(f"{str(tag_names)}의 datas 모두 정상 출력 확인2")
            self.driver.implicitly_wait(20)
            return True
        except BaseException as e:
            print(e)
            print(traceback.format_exc())
            self.driver.implicitly_wait(20)
                    
    def animation_none(self,parent_loc):
        '''
        애니메이션 제거(현재 미사용중이지만 업데이트 가능성 있음)
        '''
        self.driver.execute_script("li =document.querySelectorAll('"+parent_loc+" *'); function test(){ for(let i =0; i<  li.length; i++){li[i].style.cssText='animation: none !important; transition: none !important; trasnform: none !important; transition-delay: 0s; opacity: 1;'}}")

    def move_to_element(self,el):
        '''
        action chain으로 el까지 이동
        '''
        self.action.move_to_element(el).perform()
        self.action.reset_actions()

    def move_to_click(self,el,JS_switch=False):
        '''
        action chain으로 el까지 이동 후 클릭
        '''
        if JS_switch is False:
            self.action.move_to_element(el).click().perform()
            self.action.reset_actions()
            self.wait_loading()
        else:
            self.scroll_center(el)
            self.action.move_to_element(el).click().perform()
            self.action.reset_actions()
            self.wait_loading()

    def is_exists_element_click(self,el:WebElement):
        '''
        현재 페이지에 el이 존재하면 클릭
        '''
        if el:
            el.click()

    def is_exists_move_to_click(self,el:WebElement,JS_switch=False):
        '''
        현재 페이지에 el이 존재하면 이동 후 클릭
        '''
        if el:
            if JS_switch:
                self.move_to_click(el,True)
            else:
                self.move_to_click(el)

    def redefinition_v2(self,el:WebElement) -> WebElement:
        '''
        요소 재정의 함수 version 2
        iOS Hybrid App element 상호작용 오류(StaleElementReferenceException)로 인한 해결방안으로 사용
        '''
        try:
                return self.driver.execute_script("return arguments[0];", el)
        except InvalidSelectorException as e:
            print(e)
            return self.driver.execute_script("return arguments[0];", el)
        except BaseException as e:
            print(e)
            print(traceback.format_exc())

    def click_until_go_page(self,el:WebElement|str,scroll_switch:bool=True):
        '''
        다른 페이지로 이동할 때 까지 클릭 반복
        el: WebElement or location
        scroll_switch: move_to_click() 사용여부(default: 사용)
        '''
        current_url = self.driver.current_url
        re_el = el
        for _ in range(self.retry_count):
            try:
                if scroll_switch:
                    re_el = self.move_to_click(re_el)
                else:
                    re_el.click()
                    self.wait_loading()

                # time.sleep(1)
                print(f"{current_url} != {self.driver.current_url}")
                if current_url != self.driver.current_url:
                    break
                else:
                    re_el = self.redefinition_v2(re_el)
            except Exception as e:
                print(traceback.format_exc())
                print(e)
                re_el = self.redefinition_v2(re_el)
                pass
    
    def again_click(self,click_el:WebElement,display_el_selector:str=''):
        '''
        해당 요소 정상 클릭까지 반복
        click_el: 클릭을 반복할 요소
        display_el_selecto: 클릭 정상여부 확인
        '''
        current_url = self.driver.current_url
        for _ in range(self.retry_count):
            self.move_to_click(click_el)
            # click_el.click()
            self.wait_loading()
            if display_el_selector == '':
                if current_url != self.driver.current_url:
                    return
            elif display_el_selector.startswith('//'):
                if self.loading_find_xpath_pre(display_el_selector):
                    return
            else:
                if self.loading_find_css_pre(display_el_selector):
                    return
        return False

    def back(self):
        '''
        뒤로가기
        '''
        self.driver.back()
        self.wait_loading()
