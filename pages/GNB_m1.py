from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils import exception_handler as eh
from base.base import Base, LocatorLoader
import random, time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.custom_utils import *   

class TestCase04(Base):
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m1')
        self.by_type = self.get_by_type("css")
    
    def combine_locators(self, *locator_keys):
        return ' '.join(self.locators[key] for key in locator_keys)

    def execute(self):
        """테마배너 항목 텍스트 정상 노출 확인"""
        try:
            # 모바일 메뉴 찾고 클릭
            mobile_menu = find_element(self.driver, self.by_type, self.locators['mobile_menu'], f"모바일 메뉴")
            click(self.driver, mobile_menu, f"모바일 메뉴")
            
            # 모바일 페이지로 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, mobile_menu, f"모바일")

            # 모바일 페이지 섹션 확인
            find_visible_sections(self.driver, self.by_type, self.locators, "모바일")

            # 테마배너 섹션 포커싱
            move_to_element(self.driver, self.by_type, self.locators['theme_banner_section'], f"테마배너 섹션")
            
            # 배너 정보 수집
            show_elements_text(self.driver, self.by_type, self.combine_locators('theme_banner_section', 'banner_texts'), "alt", f"배너")
            show_elements_text(self.driver, self.by_type, self.combine_locators('theme_banner_section', 'banner_bgs'), "src", f"배너")
            
            # 재생/정지 | 이전/다음 버튼 테스트
            navigate_locators = {
                "slide": self.combine_locators('theme_banner_section', 'banner_texts'),
                'active_slide': self.combine_locators('theme_banner_section', 'active_slide'),
                'play_button': self.combine_locators('theme_banner_section', 'play_button'),
                'pause_button': self.combine_locators('theme_banner_section', 'pause_button'),
                'prev_button': self.combine_locators('theme_banner_section', 'prev_button'),
                'next_button': self.combine_locators('theme_banner_section', 'next_button'),
                'banner_text': self.combine_locators('theme_banner_section', 'banner_texts')
            }
            navigate_slides(self.driver, self.by_type, navigate_locators, f"배너")

        except Exception as e:
            eh.exception_handler(self.driver, e, "테마배너 테스트 실패")
            raise

class TestCase05(Base):
    """모바일 메뉴 > 기기 섹션에서 랜덤 기기 선택 후 주문하기 클릭, 팝업 창에서 정보 확인 및 장바구니 담기"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m1')
        self.by_type = self.get_by_type("css")
    
    def combine_locators(self, *locator_keys):
        return ' '.join(self.locators[key] for key in locator_keys)

    def execute(self):
        try:
            # 모바일 메뉴 찾고 클릭
            mobile_menu = find_element(self.driver, self.by_type, self.locators['mobile_menu'], f"모바일 메뉴")
            click(self.driver, mobile_menu, f"모바일 메뉴")
            
            # 모바일 페이지로 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, mobile_menu, f"모바일")

            # 디바이스 섹션 포커싱
            move_to_element(self.driver, self.by_type, self.locators['mobile_device_section'], f"디바이스 섹션")

            # 랜덤 탭(링크) 선택
            select_random_item(self.driver, self.by_type, self.combine_locators('phone_device_section','') + " .tab-wrap ul li a", f"디바이스")


            # self.check_available_options()
            # self.select_device_option()
            # self.select_shipping_option()
            # self.select_other_option()
            # self.order_info()
            # self.cart_redirection()
            # self.order_delete()
        except Exception as e:
            eh.exception_handler(self.driver, e, "휴대폰 주문 및 장바구니 테스트 실패")
            raise

    def select_mobile_device(self):
        """모바일 디바이스 랜덤으로 선택"""
        
        # 모바일 메뉴 찾고 클릭
        
        
        # 랜덤 탭(링크) 선택
        select_random_item(self.driver, self.by_type, self.combine_locators('phone_device_section','') + " .tab-wrap ul li a", f"디바이스")

        # # 4. 무작위 탭 선택
        # if phone_device_section:
        #     device_tabs = find_elements
        #     if device_tabs:
        #         random_tab = random.choice(device_tabs)
        #         random_tab_text = random_tab.text
        #         click(self.driver, random_tab)
        #         self.logger.info(f"선택한 탭: {random_tab_text}")
        #         time.sleep(2)

        #     device_list = find_visible_elements(self.driver, (By.CSS_SELECTOR, f"{self.locators['phone_device_section']} div.slick-list div.slick-track div.slick-slide"))
        #     self.logger.info(f"{random_tab_text} 보여지는 기기 갯수: {len(device_list)}")

        #     for index, device in enumerate(device_list):
        #         device_name = device.find_element(By.CSS_SELECTOR, '.big-title').text
        #         device_price = device.find_element(By.CSS_SELECTOR, '.total-price').text
        #         device_colors = [
        #             color.text for color in device.find_elements(By.CSS_SELECTOR, 'p.color-chip span.is-blind')
        #         ]
        #         device_url = device.find_element(By.CSS_SELECTOR, 'button[data-gtm-click-url]').get_attribute('data-gtm-click-url')
        #         custom_logger.info(f"기기_{index + 1}: {device_name} 가격: {device_price} 색상: {device_colors} URL: {device_url}")

        #     # 6. 무작위 기기 선택
        #     random_device = random.choice(device_list)
        #     device_name = random_device.find_element(By.CSS_SELECTOR, '.big-title').text
        #     order_button = random_device.find_element(By.CSS_SELECTOR, 'button[data-gtm-click-url]')
        #     order_button_url = order_button.get_attribute('data-gtm-click-url')
        #     self.logger.info(f"주문하기 버튼 URL: {order_button_url}")
        #     order_button.click()
        #     self.logger.info(f"선택된 기기: {device_name}")
        #     time.sleep(2)

        # 4. 무작위 탭 선택

        # 5. 무작위 기기 선택
        

        # 5. 무작위 탭의 기기 리스트 확인
        

        # 7. 주문하기 버튼 클릭 후 장바구니 페이지로 리다이렉션 확인
    #     order_url = self.driver.current_url
    #     if "/mobile/device" in order_url:
    #         self.logger.info(f"주문하기 페이지로 이동 URL: {order_url}")
    #     else:
    #         self.logger.info(f"주문하기 페이지로 이동 실패 URL: {order_url}")

    #     # 8. 주문하기 페이지에서 기기명 확인
    #     device_detail_name_element = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.title-main'))
    #     )
    #     device_detail_name = device_detail_name_element.get_attribute('textContent').split('(')[0].strip()
    #     custom_logger.info(f"주문하는 기기명: {device_detail_name}")
    #     if device_name in device_detail_name:
    #         self.logger.info(f"선택한 기기명: {device_name} 상세페이지 기기명: {device_detail_name}로 기기명이 일치합니다.")
    #     else:
    #         self.logger.info(f"기기명이 일치하지 않습니다. 선택된 기기: {device_name}, 상세 페이지 기기: {device_detail_name}")
    #     self.driver.implicitly_wait(10)
    
    # def check_available_options(self):
    #     # 팝업창 닫기(따로 빼기 일단 하드코딩)
    #     try:
    #         popup_close_button = WebDriverWait(self.driver, 10).until(
    #             EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.c-btn-close'))
    #         )
    #         popup_close_button.click()
    #         self.logger.info("팝업창 닫기 버튼 클릭 완료")
    #         self.driver.implicitly_wait(10)
    #     except TimeoutException:
    #         self.logger.info("팝업창이 나타나지 않았습니다.")
        
    #     # 1. 선택해야 할 옵션들 확인
    #     strong_texts = []
    #     option_text = self.driver.find_elements(By.CSS_SELECTOR, 'div.device-info-area div.color, div.device-info-area div.option-box')

    #     for option in option_text:
    #         strong_elements = option.find_elements(By.TAG_NAME, 'strong')
    #         texts = [strong.get_attribute('textContent').strip() for strong in strong_elements]
    #         strong_texts.extend(texts)
    #     self.logger.info(f"기기 옵션: {strong_texts}")

    #     # 2. 탭 리스트 확인
    #     tab_lists = self.driver.find_elements(By.CSS_SELECTOR, 'div.c-tab-slidemenu ul li a')
    #     tab_texts = [
    #         tab.get_attribute('data-gtm-click-text') for tab in tab_lists
    #     ]
    #     self.logger.info(f"탭 리스트 갯수: {len(tab_lists)} {tab_texts}")

    #     # 3. 탭 예상 납부금액 탭에서 선택해야 할 옵션들 확인
    #     th_texts = []
    #     th_option_text = self.driver.find_elements(By.CSS_SELECTOR, 'div.c-table table tr[role="row"] th')
        
    #     for th in th_option_text:
    #         span_elements = th.find_elements(By.TAG_NAME, 'span')
    #         texts = [span.get_attribute('textContent').strip() for span in span_elements]
    #         th_texts.extend(texts)
    #     self.logger.info(f"탭 선택옵션: {th_texts}")

    #     # 4. 옵션 선택: 색상, 저장공간, 가입유형, 배송방법, 요금제&&할인혜택, 제휴카드, VIP멤버쉽, 추가할인, 사은품, 쿠폰
    #     self.color_section = find_element(self.driver, (By.CSS_SELECTOR, 'div > div.middlearea > div > div.device-info-area > div.color'))
    #     self.storage_section = find_elements(self.driver, (By.CSS_SELECTOR, 'div > div.middlearea > div > div.device-info-area > div.option-box'))[0]
    #     self.join_section = find_elements(self.driver, (By.CSS_SELECTOR,'div > div.middlearea > div > div.device-info-area > div.option-box'))[1]
    #     self.shipping_section = find_element(self.driver, (By.CSS_SELECTOR,'tbody > tr:nth-child(1)'))
    #     self.fee_section = find_element(self.driver, (By.CSS_SELECTOR,'tbody > tr:nth-child(2) > td'))
    #     self.installment_section = find_element(self.driver, (By.CSS_SELECTOR,'tbody > tr:nth-child(3) > td'))
    #     self.card_section = find_element(self.driver, (By.CSS_SELECTOR, 'tbody > tr[name="co-card"]'))
    #     self.vip_benefilt_section = find_element(self.driver, (By.CSS_SELECTOR,'tbody > tr:nth-child(5)'))
    #     if "VIP 멤버십 혜택" in th_texts:
    #         self.sale_plus_section = find_element(self.driver, (By.CSS_SELECTOR, 'tbody > tr:nth-child(6)'))
    #         self.logger.info("VIP 멤버십 혜택이 존재합니다. 추가할인 셋팅")
    #     else:
    #         self.sale_plus_section = self.driver.find_element(By.CSS_SELECTOR, 'tbody > tr:nth-child(5)')
    #     self.gift_section = self.driver.find_elements(By.CSS_SELECTOR,'tbody > tr.gift-list')[0]
    #     self.coupon_section = self.driver.find_elements(By.CSS_SELECTOR,'tbody > tr.gift-list')[1]
    #     self.driver.implicitly_wait(5)


    # def select_device_option(self):
    #     # 1. 색상 선택
    #     # color_section에 포커싱
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(self.color_section).perform()

    #     # 색상 옵션 리스트
    #     color_list = self.color_section.find_elements(By.CSS_SELECTOR, 'div.color div.btns button.btn-color')
    #     color_list_text = [
    #         color.find_element(By.CSS_SELECTOR, 'em.is-blind').get_attribute('textContent').strip()
    #         for color in color_list
    #     ]
    #     self.logger.info(f"색상옵션: {len(color_list)} {color_list_text}")

    #     # 색상 랜덤 선택 후 리스트 내 버튼 클릭
    #     selected_color_button = random.choice(color_list)
    #     click(self.driver, selected_color_button)
    #     time.sleep(2)
    #     selected_color = selected_color_button.find_element(By.TAG_NAME, 'em').get_attribute('textContent').strip()
    #     self.logger.info(f"선택된 색상: {selected_color}")

    #     # 2. 저장공간 선택
    #     # storage_section에 포커싱
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(self.storage_section).perform()
        
    #     # 저장 옵션 리스트
    #     storage_list = self.storage_section.find_elements(By.CSS_SELECTOR, 'ul.c-card-list-icon.check-type-3-1 li')
    #     storage_list_text = [
    #         storage.find_element(By.CSS_SELECTOR, 'span.info-tit').get_attribute('textContent').strip()
    #         for storage in storage_list
    #     ]
    #     self.logger.info(f"저장옵션: {len(storage_list)} {storage_list_text}")

    #     # 저장공간 리스트 랜덤 선택 후 리스트 내 버튼 클릭
    #     selected_storage = random.choice(storage_list)
    #     storage_button = selected_storage.find_element(By.CSS_SELECTOR, '.c-radio input[type="radio"]')
    #     click(self.driver, storage_button)
    #     selected_storage_text = selected_storage.find_element(By.CSS_SELECTOR, '.info-tit').get_attribute('textContent').strip()
    #     self.logger.info(f"선택된 저장공간: {selected_storage_text}")
        
    #     # 저장 옵션 리스트
    #     storage_list = self.storage_section.find_elements(By.CSS_SELECTOR, 'ul.c-card-list-icon.check-type-3-1 li')
    #     storage_list_text = [
    #         storage.find_element(By.CSS_SELECTOR, 'span.info-tit').get_attribute('textContent').strip()
    #         for storage in storage_list
    #     ]
    #     self.logger.info(f"저장옵션: {len(storage_list)} {storage_list_text}")

    #     # 3. 가입유형 선택
    #     # join_section에 포커싱
    #     ActionChains(self.driver).move_to_element(self.join_section).perform()

    #     # 가입유형 리스트
    #     join_type_list = self.join_section.find_elements(By.CSS_SELECTOR, 'ul li')
    #     join_type_list_text = [
    #         join.find_element(By.CSS_SELECTOR, 'span.info-tit').get_attribute('textContent')
    #         for join in join_type_list
    #     ]
    #     custom_logger.info(f"가입유형: {len(join_type_list)} {join_type_list_text}")
        
    #     # 가입유형 리스트 랜덤 선택 후 리스트 내 버튼 클릭
    #     selected_join_type = random.choice(join_type_list)
    #     join_option_button = selected_join_type.find_element(By.CSS_SELECTOR, '.c-radio input[type="radio"]')
    #     click(self.driver, join_option_button)
    #     selected_join_type = selected_join_type.find_element(By.CSS_SELECTOR, 'span.info-tit').get_attribute('textContent').strip()
    #     self.logger.info(f"선택된 가입유형: {selected_join_type}")

    # def select_shipping_option(self):       
    #     # 9-4. 배송방법 선택
    #     # shipping_section에 포커싱
    #     ActionChains(self.driver).move_to_element(self.shipping_section).perform()

    #     # 배송방법 리스트
    #     shipping_list = self.shipping_section.find_elements(By.CSS_SELECTOR, 'ul.c-card-list-icon.check-type-3-1 li')
    #     shipping_list_text = [
    #         shipping.find_element(By.CSS_SELECTOR, 'span').get_attribute('textContent').strip()
    #         for shipping in shipping_list
    #     ]
    #     self.logger.info(f"배송유형: {len(shipping_list)} {shipping_list_text}")

    #     # 배송방법 리스트 랜덤 선택 후 리스트 내 버튼 클릭   
    #     # selected_shipping_option = random.choice(shipping_list) 
    #     selected_shipping_option = shipping_list[0]
    #     shipping_button = selected_shipping_option.find_element(By.CSS_SELECTOR, 'div.c-card-box div.c-radio input[type="radio"]')
    #     click(self.driver, shipping_button)
    #     selected_shipping = selected_shipping_option.find_element(By.CSS_SELECTOR, '.text-radio').get_attribute('textContent').strip()
    #     self.logger.info(f"선택된 배송방법: {selected_shipping}")

    # def select_other_option(self):    
    #     # 1. 요금제 선택
    #     # fee_section에 포커싱
    #     ActionChains(self.driver).move_to_element(self.fee_section).perform()

    #     # 요금제 리스트
    #     fee_list = self.fee_section.find_elements(By.CSS_SELECTOR, 'div.fee-select-box')
    #     fee_list_text = [
    #         fee.find_element(By.CSS_SELECTOR, 'label.text-radio div.name').get_attribute('textContent').strip()
    #         for fee in fee_list
    #     ]
    #     custom_logger.info(f"요금제유형: {len(fee_list)} {fee_list_text}")

    #     # 요금제 리스트 랜덤 선택 후 리스트 내 버튼 클릭
    #     selected_fee = random.choice(fee_list)
    #     fee_button = selected_fee.find_element(By.CSS_SELECTOR, 'span.c-radio input[type="radio"]')
    #     click(self.driver, fee_button)
    #     time.sleep(5)
    #     selected_fee_text = selected_fee.find_element(By.CSS_SELECTOR, 'label.text-radio div.name').get_attribute('textContent').strip()
    #     custom_logger.info(f"선택된 요금제: {selected_fee_text}")
        
    #     # 2. 요금제 특별혜택 선택 
    #     try:
    #         fee_special_list = self.driver.find_elements(By.CSS_SELECTOR, 'div.check-line-box')
    #         if fee_special_list:
    #             # 하나의 요소를 선택하고 그 안의 체크박스를 선택
    #             selected_fee_special = random.choice(fee_special_list)
    #             # 체크박스 요소 클릭
    #             checkbox = selected_fee_special.find_element(By.CSS_SELECTOR, 'div.c-inpfield span.c-chk input[type="checkbox"]')
    #             click(self.driver, checkbox)
    #             # 선택된 특별 혜택의 텍스트 가져오기
    #             selected_special_fee = selected_fee_special.find_element(By.CSS_SELECTOR, 'label.txt').get_attribute('textContent').strip()
    #             custom_logger.info(f"선택된 특별혜택: {selected_special_fee}")
    #         else:
    #             custom_logger.info("특별 혜택이 없습니다.")
    #     except NoSuchElementException:
    #         custom_logger.info("선택된 요금제에는 특별혜택이 없습니다.")
    #     self.driver.implicitly_wait(5)

    #     # 3. 할부금 납부 기간 포커싱
    #     # 할부금 납부기간 포커싱
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(self.installment_section).perform()

    #     # 할인방법 선택
    #     try:
    #         discount_list = self.driver.find_elements(By.CSS_SELECTOR, 'ul.sale-type-box.sale-type-box--type2 li')
    #         notice = self.driver.find_element(By.CSS_SELECTOR, 'ul.c-noticebox-h4 li')
    #         if discount_list:
    #             selected_discount = random.choice(discount_list)
    #             # 내부 라디오 요소 클릭
    #             radio = selected_discount.find_element(By.CSS_SELECTOR, 'div.c-inpfield span.c-radio input[type="radio"]')
    #             click(self.driver, radio)
    #             # 선택된 특별 혜택의 텍스트 가져오기
    #             span_elements = selected_discount.find_elements(By.CSS_SELECTOR, 'label.text-radio div.txt span')
    #             span_texts = [
    #                 span.text for span in span_elements
    #             ]
    #             first_span_text = span_texts[0]
    #             second_span_text = span_texts[1]
    #             custom_logger.info(f"선택된 할인방법: {first_span_text} {second_span_text}")
    #         else:
    #             if notice:
    #                 custom_logger.info(f"알림 메시지: {notice.get_attribute('textContent')}")
    #     except NoSuchElementException:
    #         custom_logger.info("선택된 요금제에는 할인방법이 없습니다.")

    #     # 4. 할부금 납부기간 더보기 버튼 클릭
    #     installment_button = find_clickable_element(self.driver, (By.CSS_SELECTOR, '.month-credit-box .btn-chk.is-add'))
    #     click(self.driver, installment_button)

    #     # 할부금 납부기간 선택
    #     installments_list = self.driver.find_elements(By.CSS_SELECTOR, 'div.month-credit-box div.chk-wrap ul li')
    #     installments_list_text = [
    #         installments.find_element(By.CSS_SELECTOR, 'label.text-radio span.info-tit').get_attribute('textContent').strip()
    #         for installments in installments_list
    #     ]
    #     custom_logger.info(f"할부금납부 방법: {len(installments_list)} | {installments_list_text}")
    #     selected_installment = random.choice(installments_list)
    #     installment_button = selected_installment.find_element(By.CSS_SELECTOR, 'div.c-radio input[type="radio"]')
    #     click(self.driver, installment_button)

    #     selected_installment = self.driver.find_element(By.CSS_SELECTOR, 'label span.font-m.info-tit').get_attribute('textContent')
    #     custom_logger.info(f"선택된 할부금 납부기간: {selected_installment}")
    #     self.driver.implicitly_wait(5)

    #     # 5. 제휴카드 선택
    #     # 제휴카드 포커싱
    #     move_to_element(self.driver, self.card_section)
    #     # 제휴카드 더보기 버튼 클릭
    #     more_card_button = find_element(self.driver, (By.CSS_SELECTOR, 'tbody > tr[name="co-card"] .more-view.toggle a'))
    #     if more_card_button:
    #         click(self.driver, more_card_button)
        
    #     # 제휴카드 선택
    #     all_card_list = find_elements(self.driver, (By.CSS_SELECTOR, 'tbody > tr[name="co-card"] ul.c-card-list-icon.check-type-2 li'))
    #     card_not_select = all_card_list[0]
    #     card_list = all_card_list[1:]
    #     card_not_select_text = card_not_select.get_attribute('textContent').strip()
    #     card_list_text = [
    #         card.get_attribute('textContent').strip() for card in card_list
    #     ]
    #     custom_logger.info(f"카드 미선택 문구: {card_not_select_text}") 
    #     for index, card_text in enumerate(card_list_text):
    #         custom_logger.info(f"카드_{index + 1}: {card_text}")

    #     # 제휴카드 랜덤 선택 후 리스트 내 버튼 클릭
    #     selected_card_list = random.choice(all_card_list)
    #     card_button = selected_card_list.find_element(By.CSS_SELECTOR, 'div.c-radio input[type="radio"]')
    #     click(self.driver, card_button)
    #     time.sleep(2)
    #     selected_card_list_text = find_element(selected_card_list, (By.CSS_SELECTOR, 'div.info-tit')).text
    #     custom_logger.info(f"선택된 카드: {selected_card_list_text}")
        
    #     # 6. VIP맴버십 혜택 선택
    #     try:
    #         # JavaScript로 check-line-box가 존재하는지 확인
    #         vip_benefits_list = self.driver.find_elements(By.CSS_SELECTOR, "ul.VipBenefit li")
    #         if vip_benefits_list:
    #             # VIP 혜택 포커싱
    #             move_to_element(self.driver, self.vip_benefilt_section)
    #             vip_benefits_list_text = [
    #                 {
    #                     "이미지": self.vip.find_element(By.CSS_SELECTOR, '.img img').get_attribute('src').strip(),
    #                     "혜택": self.vip.find_element(By.CSS_SELECTOR, 'strong').get_attribute('textContent').strip(),
    #                     "가격": self.vip.find_element(By.CSS_SELECTOR, 'span:last-child').get_attribute('textContent').strip()
    #                 }
    #                 for self.vip in vip_benefits_list
    #             ]
    #             custom_logger.info(f"VIP맴버십 혜택: {len(vip_benefits_list)} {vip_benefits_list_text}")
    #             # VIP 혜택 랜덤 선택 후 리스트 내 버튼 클릭
    #             selected_vip_benefit = random.choice(vip_benefits_list)
    #             vip_benefits_button = selected_vip_benefit.find_element(By.CSS_SELECTOR, 'div.c-radio input[type="radio"]')
    #             click(self.driver, vip_benefits_button)
    #             selected_vip_benefit = self.driver.find_element(By.CSS_SELECTOR, 'div.itemBenefit strong').get_attribute('textContent')
    #             custom_logger.info(f"선택된 VIP 혜택: {selected_vip_benefit}")
    #     except NoSuchElementException:
    #         custom_logger.info("VIP맴버십 혜택이 없습니다.")

    #     # 7. 추가할인
    #     # 추가할인 포커싱
    #     move_to_element(self.driver, self.sale_plus_section)
    #     sale_plus_list = self.driver.find_elements(By.CSS_SELECTOR, 'ul.sale-plus-list li')
    #     sale_plus_list_text = [
    #         sale_plus.find_element(By.CSS_SELECTOR, 'label.text-chkbox span.txt').get_attribute('textContent').strip()
    #         for sale_plus in sale_plus_list
    #     ]
    #     custom_logger.info(f"추가할인: {len(sale_plus_list)} {sale_plus_list_text}")
        
    #     # 추가할인 선택
    #     selected_sale_plus = random.choice(sale_plus_list)
    #     discount_option_button = selected_sale_plus.find_element(By.CSS_SELECTOR, 'span.c-checkbox input[type="checkbox"]')
    #     click(self.driver, discount_option_button)
    #     selected_sale_plus_text = selected_sale_plus.find_element(By.CSS_SELECTOR, 'span.txt').get_attribute('textContent').strip()
    #     custom_logger.info(f"선택된 추가 할인: {selected_sale_plus_text}")

    #     # 8. 사은품
    #     # 사은품 포커싱
    #     move_to_element(self.driver, self.gift_section)
    #     gift_list = [gift for gift in self.gift_section.find_elements(By.CSS_SELECTOR, 'div.radio-image-type ul li') if not gift.find_elements(By.CSS_SELECTOR, 'span.text-sold-out')]
    #     gift_list_text = [
    #         gift.find_element(By.CSS_SELECTOR, 'label.text-radio span.info-tit').get_attribute('textContent').strip()
    #         for gift in gift_list
    #     ]
    #     available_gift_list = [
    #         gift for gift in gift_list if not gift.find_elements(By.CSS_SELECTOR, 'span.text-sold-out')
    #     ]
    #     custom_logger.info(f"사은품 옵션(품절 제외): {len(available_gift_list)} | {gift_list_text}")

    #     # 사은품 선택
    #     selected_gift_list = random.choice(gift_list)
    #     gift_button = selected_gift_list.find_element(By.CSS_SELECTOR, 'div.c-radio input[type="radio"]')
    #     click(self.driver, gift_button)
    #     selected_gift = selected_gift_list.find_element(By.CSS_SELECTOR, '.font-m.info-tit').get_attribute('textContent').strip()
    #     custom_logger.info(f"선택된 사은품: {selected_gift}")


    #     # 9. 쇼핑쿠폰백 선택
    #     # 쇼핑쿠폰백 포커싱
    #     ActionChains(self.driver).move_to_element(self.coupon_section).perform()

    #     coupon_list = [
    #         coupon for coupon in self.coupon_section.find_elements(By.CSS_SELECTOR, 'div.coupon-gifts-list ul li') 
    #         if not coupon.find_elements(By.CSS_SELECTOR, 'input[type="radio"][disabled="disabled"]')
    #     ]
    #     gift_list_text = [
    #         coupon.find_element(By.CSS_SELECTOR, 'label.text-radio span.txt2').get_attribute('textContent').strip()
    #         for coupon in coupon_list
    #     ]
        
    #     custom_logger.info(f"쇼핑쿠폰팩 옵션: {len(gift_list)} {gift_list_text}")
    #     selected_coupon_option = random.choice(coupon_list)
    #     coupon_option_button = selected_coupon_option.find_element(By.CSS_SELECTOR, 'div.c-radio input[type="radio"]:not([disabled="disabled"])')
    #     click(self.driver, coupon_option_button)

    #     selected_coupon = selected_coupon_option.find_element(By.CSS_SELECTOR, '.txt2').get_attribute('textContent')
    #     custom_logger.info(f"선택된 쇼핑쿠폰백: {selected_coupon}")
    #     self.driver.implicitly_wait(5)

    # def order_info(self):
    #     # 주문하기 버튼 클릭 전 선택 사항 리스트 확인
    #     # 계산 박스 정보 포커싱
    #     self.calculation_section = self.driver.find_element(By.CSS_SELECTOR, 'div.calculation-box')
    #     ActionChains(self.driver).move_to_element(self.calculation_section).perform()

    #     # 계산 박스 정보 출력
    #     self.device_name = self.calculation_section.find_element(By.CSS_SELECTOR, '.name').get_attribute('textContent')
    #     time.sleep(10)
    #     # 색상 / 기기용량 / 기기변경
    #     device_color = self.calculation_section.find_element(By.CSS_SELECTOR, '.c-vline-info-type-1 .info-text:nth-child(1)').get_attribute('textContent')
    #     device_storage = self.calculation_section.find_element(By.CSS_SELECTOR, '.c-vline-info-type-1 .info-text:nth-child(2)').get_attribute('textContent')
    #     device_change_type = self.calculation_section.find_element(By.CSS_SELECTOR, '.c-vline-info-type-1 .info-text:nth-child(3)').get_attribute('textContent')

    #     custom_logger.info(f"선택된 기기명: {self.device_name}")
    #     custom_logger.info(f"선택된 색상: {device_color}")
    #     custom_logger.info(f"선택된 저장공간: {device_storage}")
    #     custom_logger.info(f"선택된 가입유형: {device_change_type}")
    #     self.driver.implicitly_wait(5)


    # def cart_redirection(self):
    #     # 1. 장바구니 버튼 클릭
    #     cart_button = self.calculation_section.find_element(By.CSS_SELECTOR, '.btn-area.btn-small button:nth-of-type(2)')
    #     click(self.driver, cart_button)
    #     custom_logger.info("장바구니 버튼 클릭 완료")
        
    #     # 2. 장바구니 버튼 클릭시, 모달창 확인 버튼 클릭하기
    #     header = self.driver.find_element(By.CSS_SELECTOR, 'div.modal-content header.modal-header h1').get_attribute('textContent').strip()
    #     if header == "장바구니담기":
    #         custom_logger.info("장바구니담기 팝업창 오픈 완료")
    #         cart_link_button = self.driver.find_element(By.CSS_SELECTOR, '.modal-footer button:nth-of-type(2)')
    #         click(self.driver, cart_link_button)
    #         custom_logger.info("장바구니로 이동 버튼 클릭 완료")
    #         try:
    #             WebDriverWait(self.driver, 10).until(EC.url_contains("/cart")) 
    #             cart_url = self.driver.current_url
    #             custom_logger.info(f"장바구니 페이지로 이동 성공 URL: {cart_url}")
    #         except Exception as e:
    #             cart_url = self.driver.current_url
    #             custom_logger.error(f"장바구니 페이지로 이동 실패 URL: {cart_url} Error: {e}")
    #     else: 
    #         custom_logger.error("장바구니 팝업창이 나타나지 않았습니다.")
    #     self.driver.implicitly_wait(5)
 
    #     # 3. 장바구니에서 기기명 확인
    #     self.cart_list = self.driver.find_element(By.CSS_SELECTOR, 'div.products-tbl ul.products-tbl-list li')
    #     cart_device_info = self.cart_list.find_element(By.CSS_SELECTOR, 'div.p-product div')
    #     cart_device_name = cart_device_info.find_element(By.CSS_SELECTOR, 'p.tit').get_attribute('textContent')
    #     custom_logger.info(f"장바구니 기기명: {cart_device_name}")
    #     self.device_name = self.device_name.strip()
    #     cart_device_name = cart_device_name.strip().replace('\n', ' ')
    #     if  cart_device_name in self.device_name:
    #         custom_logger.info(f"선택된 기기: {self.device_name}, 장바구니 기기: {cart_device_name}와 기기명이 일치합니다")
    #     else:
    #         custom_logger.info(f"선택된 기기: {self.device_name}, 장바구니 기기: {cart_device_name}와 기기명이 일치하지 않습니다. ")
    #     self.driver.implicitly_wait(5)


    # def order_delete(self):
    #     # 1. 장바구니에서 항목 삭제
    #     try: 
    #         selectors = ['button.btn-del', 'div.c-btn-group button.c-btn-solid-1-m','div.c-btn-group button.c-btn-solid-1-m']
    #         for selector in selectors:
    #             element = WebDriverWait(self.driver, 10).until(
    #                 EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    #             )
    #             time.sleep(1)
    #             element.click()
    #     except TimeoutException as e :
    #         custom_logger.error(f"Error: {e}")
    #         custom_logger.error("장바구니에서 항목 삭제 실패")
        

    #     # 2. 장바구니에서 삭제 되었는지 리스트에서 확인
    #     empty_cart_list = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cart-empty-wrap')))
    #     if empty_cart_list:
    #         custom_logger.info("장바구니가 비어 있습니다.")
            
    #         # 메인 페이지로 이동
    #         main_page_button = WebDriverWait(self.driver, 10).until(
    #            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.c-btn-outline-2'))
    #         )
    #         click(self.driver, main_page_button)

    #         custom_logger.info("메인 페이지로 이동 버튼 클릭 완료")
    #     else:
    #         custom_logger.info("장바구니에 항목이 남아 있습니다.")

class TestCase06(Base):
    
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m1')
        self.by_type = self.get_by_type("css")
    
    def combine_locators(self, *locator_keys):
        return ' '.join(self.locators[key] for key in locator_keys)
    
    def execute(self):
        """인터넷/IPTV 결합 영역 드롭다운 항목 무작위선택 후 할인 금액 데이터 추출 및 '가입상담신청' 클릭, 상담 신청하기 페이지 내 할인 금액 데이터 비교"""
        try:
            # 모바일 메뉴 찾고 클릭
            mobile_menu = find_element(self.driver, self.by_type, self.locators['mobile_menu'], f"모바일 메뉴")
            click(self.driver, mobile_menu, f"모바일 메뉴")
            
            # 모바일 페이지로 리다이렉션 확인
            page_redirect_confirm(self.driver, self.by_type, mobile_menu, f"모바일")

            # 결합할인 섹션 포커싱
            move_to_element(self.driver, self.by_type, self.locators['mobile_conbine_section'], f"결합할인 섹션")
            
            # 드롭다운 갯수 확인
            combine_area_txt = self.combine_locators('mobile_conbine_section', 'combine_txt')
            combile_dropdowns = self.combine_locators('mobile_conbine_section', 'combine_dropbox')
            
            # 드롭다운 랜덤 선택
            select_random_option(self.driver, self.by_type, combine_area_txt, combile_dropdowns, f"모바일 결합 섹션")
            
            # 할인 금액 데이터 추출
            discount_price = get_text(self.driver, self.by_type, self.locators['discount_spans'], f"할인 총 금액")
            total_price_txt = total_price_calculation(self.driver, self.by_type, self.locators['results'], f"할인 결과")
            
            # 가입상담신청 버튼 클릭
            clickable_link_click(self.driver, self.by_type, self.locators['consultation_button'], f"가입상담신청 버튼")
            
            # modal_total_price_txt = 

            # 상위 윈도우에서 하위 윈도우로 전환
            switch_to_new_window()

            # 할인 금액 데이터 비교
            # compare_values(discount_price, total_price_txt, modal_total_price_txt)
           

            

            # consultation_modal = find_element(self.driver , (By.CSS_SELECTOR, self.locators['consultation_modal']))
            # if consultation_modal:
            #     self.logger.info("상담신청 모달창이 나타남")
            # else:
            #     self.logger.info("상담신청 모달창이 나타나지 않음")

            # # 7. 상담신청 페이지 내 할인 금액 데이터 추출
            # # 할인 금액 데이터 추출
            # calcutaor_value = find_element(self.driver , (By.CSS_SELECTOR, self.locators['calcutaor_value']))
            # total_amt = calcutaor_value.get_attribute("data-total-amt")
            # self.logger.info(f"상담신청 페이지 내 할인 금액: {total_amt}")

            # close_button = find_element(self.driver , (By.CSS_SELECTOR, self.locators['modal_close_button']))
            # click(self.driver, close_button)
            
            # # 8. 자식 윈도우창 닫기 버튼 클릭 후 부모 윈도우로 전환
            # self.driver.switch_to.window(self.driver.window_handles[0])
            # self.logger.info("부모 윈도우로 전환 완료")

        except Exception as e:
            eh.exception_handler(self.driver, e, "인터넷/IPTV 결합 테스트 실패")
            raise
