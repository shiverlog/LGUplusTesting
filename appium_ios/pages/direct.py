
import sys
import traceback

from base.server import AppiumServer
from base.appdriver import AppDriver
from common.function import Function
from common.debug import Debug
import common.variable as var

sys.path.append('/Users/nam/dev/remotePC_batchfiles/pubsub/appium_ios')


class DirectPage():
    def __init__(self,AppDriver:AppDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(AppDriver)


    def direct(self):
        self.FC.gotoHome()

        try:
            self.FC.movepage(self.FC.var['direct_el']['direct'],self.FC.var['iptv_el']['direct'],address=self.FC.var['direct_el']['url'])   # 상단 햄버거 버튼 클릭 동작
            ## KV 콘텐츠 정상 출력 확인
            kv_list_el=self.FC.loading_find_csss(self.FC.var['direct_el']['kv_list'])
            assert (len(kv_list_el)) >= 1, self.DBG.logger.debug("다이렉트 > 서브메인 > KV 콘텐츠 정상 출력 실패")
            result=[]
            ## sec1(cont-01) 콘텐츠 확인
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['direct_el']['con_01'])) 
            text_list=['유심 가입 방법 확인']
            result.append(self.FC.text_list_in_element(self.FC.var['direct_el']['con_01'],text_list))
            assert self.DBG.print_res(result), self.DBG.logger.debug("다이렉트 > 유심 가입 컨텐츠 출력 실패")

            ## 유플닷컴 전용 요금제
            result.clear()
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['direct_el']['con_02'])) 
            direct_plan_tit = self.FC.loading_find_csss(self.FC.var['direct_el']['con_02_title'])
            direct_plan_price = self.FC.loading_find_csss(self.FC.var['direct_el']['con_02_price'])
            direct_plan_btn = self.FC.loading_find_csss(self.FC.var['direct_el']['con_02_가입하기'])
            random_num=0    # random.randrange(0,len(direct_plan_tit))
            direct_plan_tit_txt = direct_plan_tit[random_num].get_property('innerText')         # 임의의 유플닷컴 전용 요금제
            direct_plan_price_txt = direct_plan_price[random_num].get_property('innerText')
            self.FC.wait_loading()
            self.FC.move_to_click(direct_plan_btn[random_num])
            assert self.FC.var['direct_el']['전용요금제_가입하기_url'] in self.FC.driver.current_url, self.DBG.logger.debug("다이렉트 > 유플닷컴 전용 요금제 가입하기 페이지 이동 실패")
            self.FC.goto_url(self.FC.var['direct_el']['url'])
            self.FC.scroll2_v2(self.FC.loading_find_css(self.FC.var['direct_el']['con_03'])) 
            plan_list=self.FC.loading_find_csss(self.FC.var['direct_el']['con_03_li'])
            self.FC.scroll2_v2(plan_list[0]) 
            assert len(plan_list) == 4 , self.DBG.logger.debug("다이렉트 > 다이렉트 요금제 혜택 콘텐츠 노출 실패")
            #고객리뷰
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['direct_el']['con_04'])) 
            reviews = self.FC.loading_find_csss(self.FC.var['direct_el']['con_04_li'])
            assert len(reviews) >= 3 , self.DBG.logger.debug("다이렉트 > 고객리뷰 콘텐츠 노출 실패")
            #다이렉트를 가장 쉽게 만나는 방법
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['direct_el']['con_05'])) 
            li = self.FC.loading_find_csss(self.FC.var['direct_el']['con_05_li'])
            assert len(li) == 3 , self.DBG.logger.debug("다이렉트 > 다이렉트를 가장 쉽게 만나는 방법 콘텐츠 노출 실패")
            # 이번달 꿀혜택 영역
            self.FC.scroll2_v2(self.FC.loading_find_css(self.FC.var['direct_el']['con_06'])) 
            li = self.FC.loading_find_csss(self.FC.var['direct_el']['con_06_li'])
            assert len(li) == 3 , self.DBG.logger.debug("다이렉트 > 이번달 꿀혜택 콘텐츠 노출 실패")
        except  Exception :
            self.DBG.print_dbg("다이렉트페이지 정상 노출 및 기능 동작 확인",False)
            return False
        else :
            self.DBG.print_dbg("다이렉트페이지 정상 노출 및 기능 동작 확인")
            return True



    def direct2(self):

        try:

            self.FC.movepage(var.direct_el['direct'],address=var.direct_el['url'])   # 상단 햄버거 버튼 클릭 동작
    
            # # 유독 페이지 URL로 정상 이동이 이루어졌는지 확인
            assert var.direct_el['url'] in self.FC.loading_find_css('div.direct_wrap').get_property('baseURI'),self.DBG.logger.debug("다이렉트 페이지 정상 이동 실패")

            # self.FC.loading_find_css_pre('div#directDialogPopup button.ui_modal_close').click()

            # # KV 콘텐츠 정상 출력 확인
            kv_list_el=self.FC.loading_find_csss('div.swiper-container div.swiper-slide div img')
            assert len(kv_list_el)>0, self.DBG.logger.debug("다이렉트 페이지 KV 콘텐츠 정상 출력 실패")


            result=[]
            
            ## sec1(cont-01) 콘텐츠 확인
            # self.FC.scroll2_v2(self.FC.loading_find_css_pre('div.cont-01')) 
            #  
            self.FC.scroll2(self.FC.loading_find_css_pre('div.cont-01'))

            text_list=['다이렉트 요금제','24시간 365일','저렴','약정부담','유심만']
            result.append(self.FC.text_list_in_element('div.cont-01',text_list))
            result.append(len(self.FC.loading_find_csss('div.cont-01 ul>li'))==4)
            assert self.DBG.print_res(result), self.DBG.logger.debug("다이렉트 > sec1 콘텐츠 정상 출력 실패")


            ## sec2(cont-02) 콘텐츠 확인
            # self.FC.scroll2_v2(self.FC.loading_find_css_pre('div.cont-02')) 
            #  
            self.FC.scroll2(self.FC.loading_find_css_pre('div.cont-02'))

            text_list=['요금','혜택','가입하기']
            result.append(self.FC.text_list_in_element('div.cont-02',text_list))
            plan_list=self.FC.loading_find_csss('div.cont-02 div>a')
            result.append(len(plan_list) == 7)
            print(str(result))
            assert self.DBG.print_res(result), self.DBG.logger.debug("다이렉트 > sec2 콘텐츠 및 액션 정상 동작 실패")
            result.clear()
            
            # # 무작위 임의 요금제 이동 <<오류
            # random_num=random.randrange(0,len(plan_list))
            # product_json=plan_list[random_num].get_attribute('data-ec-product');   # 임의 상품 json 가져오기
            # product=json.loads(product_json)
            # print("price_select >>>>>>>>>>>>>>>>>>>>>>>> ",product['ecom_prd_price'])
            # price_txt=list(str(product['ecom_prd_price']))
            # price_txt.insert(-3,',')
            # product['ecom_prd_price']=''.join(price_txt)
            # print("다이렉트 요금제 name =>>>",product['ecom_prd_name'])
            # print("다이렉트 요금제 price =>>>",product['ecom_prd_price'])
            # self.FC.scroll2_v2(plan_list[random_num]).click() 
            #  

            # assert product['ecom_prd_name'] in self.FC.loading_find_xpath_pre('//div[contains(.,"요금제") and @class="component"]//ul/li[1]//a').get_property('innerText'),self.DBG.logger.debug("다이렉트 > sec2 콘텐츠 및 액션 정상 동작 실패")
            # assert product['ecom_prd_price'] in self.FC.loading_find_xpath_pre('//div[contains(.,"요금제") and @class="component"]//ul/li[1]//p[3]').get_property('innerText'),self.DBG.logger.debug("다이렉트 > sec2 콘텐츠 및 액션 정상 동작 실패")
           
            # if 'https://www.lguplus.com/direct' not in self.FC.driver.current_url:
            #     self.FC.driver.back()
            

            ## sec3(cont-03) 콘텐츠 확인
            # self.FC.scroll(0)
            # self.FC.swipe('div.cont-03')
            self.FC.scroll2(self.FC.loading_find_css_pre('div.cont-03'))
            btns=self.FC.loading_find_csss('div.cont-03 a')
            # self.FC.swipe(1)

            # 결합 신청하기 버튼
            self.FC.scroll2(btns[0]).re_click()
            self.FC.loading_find_css_pre('section.dr-allWrap')
            assert self.FC.text_list_in_element('section.dr-allWrap',['함께 할인','내가 초대하고 할인']),self.DBG.logger.debug("다이렉트 > sec3 콘텐츠 및 액션 정상 동작 실패")
            if var.direct_el['url'] != self.FC.driver.current_url:
                self.FC.driver.back()

            # 유쓰 더 알아보기 버튼
            # self.FC.scroll(3100)
            # self.FC.swipe('div.cont-03')
            self.FC.scroll2(self.FC.loading_find_css_pre('div.cont-03'))
            btns=self.FC.loading_find_csss('div.cont-03 a')
            # self.FC.scroll2_v2(btns[1]).click() 
            #  
            self.FC.scroll2(btns[1]).re_click()
            assert var.uth_el['url'] in self.FC.loading_find_css_pre('div.uth_allwrap').get_property('baseURI'),self.DBG.logger.debug("다이렉트 > sec3 콘텐츠 및 액션 정상 동작 실패")
            # while True:
            #     if var.direct_el['url'] != self.FC.driver.current_url:
            #         self.FC.driver.back()
            #     if 'https://m.lguplus.com/' == self.FC.driver.current_url:
            #         self.FC.movepage(var.direct_el['direct'],address=var.direct_el['url'])   # 상단 햄버거 버튼 클릭 동작
            #     else:
            #         break
            self.FC.goto_url(self.FC.var['direct_el']['url'])




            
            # sec3~4 콘텐츠는 텍스트성 콘텐츠


            ## sec5(cont-05) 콘텐츠 확인
            
            # self.FC.swipe('div.cont-05 div.slick_wrap')
            self.FC.scroll2(self.FC.loading_find_css_pre('div.cont-05 div.slick_wrap'))
            product_list=self.FC.loading_find_csss('div.cont-05 div.slick_wrap div a')
            print(f"product_list => {len(product_list)}")
            assert len(product_list) >= 3,self.DBG.logger.debug("다이렉트 > sec5 콘텐츠 및 액션 정상 동작 실패")


            # product_json=tablet_watch_list[random_num].get_attribute('data-ec-product');   # 임의 상품 json 가져오기
            # product=json.loads(product_json)    # ecom_prd_name(상품명)), ecom_prd_id(상품코드), ecom_prd_brand(브랜드(apple등)), ecom_prd_category(ex.개인/모바일기기/5G휴대폰), ecom_prd_variant
            # print(product['ecom_prd_name'])

            # # 임의 태블릿/스마트워치/노트북 링크 이동
            # self.FC.scroll2(tablet_watch_list[random_num]).re_click()
            # title_text=self.FC.loading_find_css('p.device-kv-wrap__info--title').get_property('innerText')
            # print(f"title_text => {product['ecom_prd_name']} in {title_text}")
            # assert product['ecom_prd_name'] in title_text , self.DBG.logger.debug("모바일 > 서브메인 > 선택된 태블릿/스마트워치/노트북 상품 페이지 이동 실패")

            # self.FC.find_css(var.common_el['back']).click() # 화면 뒤로 이동



            # random_num=random.randrange(1,(len(product_list)-1)/2)
            random_num=2
            product_name_text=product_list[random_num].get_attribute('data-gtm-click-text')
            index=product_name_text.find('상세보기') 
            product_name=product_name_text[:index-1] 
            product_name=product_name[0:(product_name.find(' '))] 
            print(f"random_num => {random_num}")
            print(f"product_name => {product_name}")
            product_list[random_num].click()
            # self.FC.action.scroll_to_element(product_list[random_num]).double_click() 
            #  
            self.FC.wait_loading()
            if self.FC.loading_find_css_pre('html[lang="ko"]>body').get_property('className') == "modal-open":
                self.FC.loading_find_css('div.modal-content button.c-btn-close').click()
            
            assert product_name in self.FC.loading_find_css_pre('p.device-kv-wrap__info--title').get_property('innerText'),self.DBG.logger.debug("다이렉트 > sec5 콘텐츠 및 액션 정상 동작 실패")
            while True:
                if var.direct_el['url'] != self.FC.driver.current_url:
                    self.FC.driver.back()
                    self.FC.wait_loading()
                if 'https://app.lguplus.com/' == self.FC.driver.current_url:
                    self.FC.movepage(var.direct_el['direct'],address=var.direct_el['url'])   # 상단 햄버거 버튼 클릭 동작
                if var.direct_el['url'] == self.FC.driver.current_url:
                    break


            ## 이벤트 콘텐츠 확인  
            # self.FC.scroll2_v2(self.FC.loading_find_xpath("//div[contains(.,'이벤트')and contains(@class,'cont_inner')]//div[contains(@class,'event_banner')]")) 
            #  
            self.FC.scroll2(self.FC.loading_find_xpath("//div[contains(.,'이벤트')and contains(@class,'cont_inner')]//div[contains(@class,'event_banner')]"))

            content_list=self.FC.loading_find_xpaths("//div[contains(.,'이벤트')and contains(@class,'cont_inner')]//div[contains(@class,'event_banner')]//a")
            assert len(content_list) == 6, self.DBG.logger.debug("다이렉트 > 이벤트 콘텐츠 및 액션 정상 동작 실패")



            
        except  Exception :
            self.DBG.print_dbg("다이렉트페이지 정상 노출 및 기능 동작 확인",False)
            print(traceback.format_exc())
            pass

        else :
            self.DBG.print_dbg("다이렉트페이지 정상 노출 및 기능 동작 확인")



if __name__ == "__main__":
    try:
        server = AppiumServer(4723)
        port = server.appium_service()
        if not server.waiting():
            raise Exception("서버 실행 불가")
        driver = AppDriver(port=port)
        fc = Function(driver)
        direct = DirectPage(driver,fc)

        fc.pre_script()
        
        direct.direct()
        driver.driver.quit()
        server.stop()
    except Exception as e:
        print(e)
        # os.system("lsof -P -i :4723 |awk NR==2'{print $2}'|xargs kill -9")
        # os.system(f"ios-deploy --kill --bundle_id com.lguplus.mobile.cs")

