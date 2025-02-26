import random

from base.server import AppiumServer
from base.appdriver import AppDriver
from common.function import Function
from common.debug import Debug
from pages.login import LoginPage


class MainPage():
    def __init__(self,AppDriver:AppDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(AppDriver)


    def mainpage_myinfo_new(self):
        self.FC.gotoHome()
        try:
            # 상단 개인 정보 영역
            result=[]
            self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['개인화'])
            text_list=['데이터','잔여량','청구요금','부가서비스 / 약정 / 할부 보기']
            self.FC.wait_datas(self.FC.var['mainpage_el']['개인화'],'span')
            result.append(self.FC.text_list_in_element(self.FC.var['mainpage_el']['개인화'],text_list))
            
            # self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['개인화_상품 조회 변경']).re_click()
            # self.FC.wait_loading()
            # if self.FC.loading_find_csss(self.FC.var['mainpage_el']['개인화_모달_상품']) == None:
            #     self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['개인화_상품 조회 변경']).re_click()
            # self.FC.wait_loading()
            # result.append(len(self.FC.loading_find_csss(self.FC.var['mainpage_el']['개인화_모달_상품'])) > 0)
            # self.FC.loading_find_css(self.FC.var['common_el']['modal_close']).re_click()

            assert self.DBG.print_res(result), self.DBG.logger.debug("메인(로그인 후) > 상단 유저 정보 카드 > 콘텐츠 및 기능 정상 노출 실패")

            result.clear()
            self.FC.click_until_not_displayed(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['부가서비스_약정_할부 버튼']))
            self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['부가서비스_약정_할부 콘텐츠'])
            result.append(self.FC.wait_datas(self.FC.var['mainpage_el']['부가서비스_약정_할부 콘텐츠'],'p','dt','dd') != str)
            text_list=['부가서비스']
            result.append(self.FC.text_list_in_element(self.FC.var['mainpage_el']['부가서비스_약정_할부 콘텐츠'],text_list))

            links=[self.FC.var['mainpage_el']['부가서비스 조회/변경_url']]
            extra_content=self.FC.loading_find_csss(self.FC.var['mainpage_el']['부가서비스_약정_할부 링크'])
            for link in links:
                # time.sleep(1.5)
                index=links.index(link)
                extra_content=self.FC.loading_find_csss(self.FC.var['mainpage_el']['부가서비스_약정_할부 링크'])
                self.FC.click_until_go_page(extra_content[index])
                result.append(link in self.FC.driver.current_url)
                self.FC.gotoHome()
                if self.FC.var['common_el']['url'] in self.FC.driver.current_url:
                    self.FC.move_to_click(self.FC.var['mainpage_el']['부가서비스_약정_할부 버튼'])
                    self.FC.wait_datas(self.FC.var['mainpage_el']['부가서비스_약정_할부 콘텐츠'],'p','dt','dd')

            assert self.DBG.print_res(result),self.DBG.logger.debug("메인(로그인 후) > 상단 유저 정보 카드 > 콘텐츠 및 기능 정상 노출 실패")

            #  퀵메뉴 탭
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['퀵메뉴']))
            # text_list=['내 가입정보','해외로밍','데이터 선물','휴대폰 구매','인터넷/IPTV','홈 설치변경']
            text_list=['내 가입정보','해외로밍','데이터 선물','휴대폰 구매','인터넷/IPTV','일시정지/해제']
            assert self.FC.text_list_in_element(self.FC.var['mainpage_el']['퀵메뉴'],text_list), self.DBG.logger.debug("메인(로그인 후) > 퀵메뉴 콘텐츠 정상 노출 실패")

            # 혜택
            # 내가 받은 혜택/멤버십
            result.clear()
            self.FC.wait_datas(self.FC.var['mainpage_el']['내가 받은 혜택'],'strong')
            self.FC.click_until_go_page(self.FC.var['mainpage_el']['내가 받은 혜택'])
            result.append(self.FC.var['mainpage_el']['report_url'] in self.FC.driver.current_url)
            self.FC.gotoHome()

            self.FC.click_until_modal_displayed(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['멤버십']))
            result.append(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['멤버십_바코드']).is_displayed())
            self.FC.wait_datas(self.FC.var['common_el']['modal_하단버튼'],'span')
            self.FC.click_until_go_page(self.FC.loading_find_css_pre(self.FC.var['common_el']['modal_하단버튼']),False)
            result.append(self.FC.var['benefit_el']['membership_url'] in self.FC.loading_find_css_pre(self.FC.var['benefit_el']['membership']).get_property('baseURI'))
            self.FC.gotoHome()

            # 나의 멤버십
            tag_el=self.FC.loading_find_csss(self.FC.var['mainpage_el']['나의 멤버십_태그명'])
            tags=[]
            for i in range(len(tag_el)):
                tags.append(tag_el[i].get_property('innerText'))

            self.FC.click_until_go_page(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['나의 멤버십_링크']))
            # self.FC.scroll2_v2(self.FC.var['mainpage_el']['나의 멤버십_링크']).re_click()
            self.FC.wait_loading()
            assert self.FC.var['mainpage_el']['나의 멤버십_url'] in self.FC.driver.current_url, self.DBG.logger.debug("메인(로그인 후) > 나의 멤버십 정상 이동 실패")
            assert all(tag in self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['나의 멤버십_등급']).get_property('innerText') for tag in tags) , self.DBG.logger.debug("메인(로그인 후) > 나의 멤버십 등급 정상 노출 실패")
            self.FC.gotoHome()

            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['혜택_list']))
            result.append(3 == len(self.FC.loading_find_csss(self.FC.var['mainpage_el']['혜택_list_링크'])))

            # 더보기
            self.FC.click_until_go_page(self.FC.loading_find_css(self.FC.var['mainpage_el']['혜택_더보기']))
            result.append(self.FC.var['mainpage_el']['나의 혜택 모아보기_url'] in self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['나의 혜택 모아보기']).get_property('baseURI'))
            assert self.DBG.print_res(result), self.DBG.logger.debug("메인(로그인 후) > 나의 혜택 모아보기 콘텐츠 및 기능 정상 노출 실패")


        except  Exception :
            self.DBG.print_dbg("메인 페이지(로그인 후) > 개인화 영역 정상 노출 확인",False)
            return False

        else :
            self.DBG.print_dbg("메인 페이지(로그인 후) > 개인화 영역 정상 노출 확인")
            return True


    def mainpage_new(self):
        self.FC.gotoHome()
        try:
            #KV
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['KV']))
            assert len(self.FC.loading_find_csss(self.FC.var['mainpage_el']['KV_링크'])) > 0,  self.DBG.logger.debug("메인(로그인 후) > KV 콘텐츠 정상 노출 실패")


            # 이벤트
            result =[]
            self.FC.click_until_go_page(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['이벤트_title']))
            result.append(self.FC.var['benefit_el']['진행 중인 이벤트_url'] in self.FC.driver.current_url)
            self.FC.gotoHome()
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['이벤트_title']))
            contents=self.FC.loading_find_csss(self.FC.var['mainpage_el']['이벤트_콘텐츠'])
            result.append(len(contents) >= 1)
            assert self.DBG.print_res(result), self.DBG.logger.debug("메인(로그인 후) > 이벤트 타이틀 및 콘텐츠 정상 노출 실패")
            
            
            # 추천 지금 인기모바일
            # 타이틀 
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['추천모바일']))
            self.FC.wait_loading()
            self.FC.click_until_go_page(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['추천모바일_title']))
            assert self.FC.var['mobile_el']['모바일기기_휴대폰_url'] in self.FC.driver.current_url,self.DBG.logger.debug("메인(로그인 후) > 추천 기기 타이틀 링크 정상 이동 실패")
            self.FC.gotoHome()

            # 무작위 랜덤 기기 이동
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['추천모바일']))
            product_list=self.FC.loading_find_csss(self.FC.var['mainpage_el']['추천모바일_콘텐츠'])
            random_num=random.randrange(0,len(product_list)-1) # 모바일 더보기 링크 박스 제외
            product_title=self.FC.loading_find_csss(self.FC.var['mainpage_el']['추천모바일_콘텐츠_title'])[random_num].get_property('innerText')
            self.FC.scroll_x(product_list[random_num])
            self.FC.click_until_go_page(product_list[random_num])
            text=self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['상품상세_title']).get_property('innerText')
            assert product_title == text, self.DBG.logger.debug("메인(로그인 후) > 추천 기기 상세 링크 정상 이동 실패")
            self.FC.gotoHome()

            # 더보기
            self.FC.click_until_go_page(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['추천모바일_콘텐츠_더보기']))
            assert self.FC.var['mobile_el']['모바일기기_휴대폰_url'] in self.FC.driver.current_url,  self.DBG.logger.debug("메인(로그인 후) > 추천 기기 더보기 링크 정상 이동 실패")
            self.FC.gotoHome()

            # 추천 요금제
            # 타이틀 
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['추천요금제_title'])).re_click()
            self.FC.wait_loading()
            result.append(self.FC.var['mobile_el']['모바일요금제_요금제_url'] in self.FC.driver.current_url)
            self.FC.gotoHome()
            
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['추천요금제']))
            self.FC.wait_datas(self.FC.var['mainpage_el']['추천요금제'],'p')
            items=self.FC.loading_find_csss(self.FC.var['mainpage_el']['추천요금제_콘텐츠'])
            items_titles=self.FC.loading_find_csss(self.FC.var['mainpage_el']['추천요금제_콘텐츠_title'])
            random_num=random.randrange(0,len(items)-1)
            title=items_titles[random_num].get_property('innerText')
            self.FC.scroll_x(items[random_num])
            items=self.FC.loading_find_csss(self.FC.var['mainpage_el']['추천요금제_콘텐츠'])
            self.FC.click_until_go_page(items[random_num])
            assert title in self.FC.loading_find_css_pre(self.FC.var['mobile_el']['요금제상품상세_title']).get_property('innerText'), self.DBG.logger.debug("메인(로그인 후) > 추천 요금제 임의 상품 링크 정상 이동 실패")
            self.FC.gotoHome()

            # 더보기
            self.FC.wait_datas(self.FC.var['mainpage_el']['추천요금제_콘텐츠'],'p')
            btn = self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['추천요금제_콘텐츠_더보기'])
            self.FC.scroll2_v2(btn)
            self.FC.scroll_x(btn)
            self.FC.click_until_go_page(btn)
            assert self.FC.var['mobile_el']['모바일요금제_요금제_url'] in self.FC.driver.current_url,  self.DBG.logger.debug("메인(로그인 후) > 추천 요금제 더보기 링크 정상 이동 실패")
            self.FC.gotoHome()

            # 추천 홈상품 가입
            self.FC.scroll2_v2(self.FC.loading_find_css_pre(self.FC.var['mainpage_el']['추천홈상품_title']))
            self.FC.click_until_go_page(self.FC.var['mainpage_el']['추천홈상품_title'])
            assert self.FC.var['mainpage_el']['인터넷iptv_url'] in self.FC.driver.current_url, self.DBG.logger.debug("메인(로그인 후) > 추천 홈상품 가입 타이틀 링크 정상 이동 실패")
            self.FC.gotoHome()


            self.FC.wait_datas(self.FC.var['mainpage_el']['추천홈상품'],'p')
            items=self.FC.loading_find_csss(self.FC.var['mainpage_el']['추천홈상품_콘텐츠'])
            items_titles=self.FC.loading_find_csss(self.FC.var['mainpage_el']['추천홈상품_콘텐츠_title'])
            random_num=random.randrange(0,len(items))
            title=items_titles[random_num].get_property('innerText')
            self.FC.click_until_go_page(items[random_num])
            titles=title.split(' + ')
            text_el=self.FC.loading_find_csss(self.FC.var['mainpage_el']['iptv상품상세_title'])
            assert self.FC.var['mainpage_el']['iptv상품상세_url'] in self.FC.driver.current_url and titles[0] in text_el[0].get_property('innerText') and titles[1] in text_el[1].get_property('innerText') ,self.DBG.logger.debug("메인(로그인 후) > 추천 홈상품 가입 임의 상품 링크 정상 이동 실패")
            self.FC.gotoHome()

        except  Exception :
            self.DBG.print_dbg("메인 페이지(로그인 후) 정상 노출 확인",False)
            return False
        else :
            self.DBG.print_dbg("메인 페이지(로그인 후) 정상 노출 확인")
            return True



if __name__ == "__main__":
    try:
        server = AppiumServer(4723)
        port = server.appium_service()
        if not server.waiting():
            raise Exception("서버 실행 불가")
        driver = AppDriver(port=port)
        fc = Function(driver)
        main = MainPage(driver,fc)
        login = LoginPage(driver,fc)

        fc.pre_script()
        
        if fc.is_login():
            login.logout()
        login.u_plus_login()
        main.mainpage_new()
        driver.driver.quit()
        server.stop()
    except Exception as e:
        print(e)
        # os.system("lsof -P -i :4723 |awk NR==2'{print $2}'|xargs kill -9")
        # os.system(f"ios-deploy --kill --bundle_id com.lguplus.mobile.cs")