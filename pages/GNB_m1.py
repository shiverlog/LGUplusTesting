import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils import exception_handler as eh
from base.base import Base, LocatorLoader
import random
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils.custom_actionchains import *
from utils.element_utils import *

class TestCase04(Base):
    """테마배너 항목 텍스트 정상 노출 확인"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m1')

    def execute(self):
        try:
            # 1. 모바일 메뉴 클릭
            mobile_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['mobile_menu']))
            )
            mobile_button.click()
            time.sleep(5)

            # URL 확인
            mobile_url = self.driver.current_url
            if "/mobile" in mobile_url:
                self.logger.info(f"모바일 페이지로 이동 URL: {mobile_url}")
            else:
                self.logger.info(f"모바일 페이지로 이동 실패 URL: {mobile_url}")

            # 2. 테마배너 섹션 포커싱
            kv_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['theme_banner_section']))
            )
            ActionChains(self.driver).move_to_element(kv_section).perform()
            time.sleep(2)

            # 배너 정보 수집
            banners = kv_section.find_elements(By.CSS_SELECTOR, self.locators['banner_links'])
            banner_list = kv_section.find_elements(By.CSS_SELECTOR, self.locators['banner_slides'])
            button_count = len(banner_list)
            location = kv_section.get_attribute("location")

            self.logger.info(f"배너 정보: {location}")
            self.logger.info(f"배너 슬라이드 갯수: {button_count}")

            # 3. 테마배너 정보 확인
            for index, banner in enumerate(banner_list):
                data_index = banner.get_attribute("data-index")
                slide_page = f"슬라이드 {int(data_index) + 1}페이지"
                
                banner_link = banners[index].get_attribute("data-gtm-click-url")
                visual_text = banners[index].find_element(By.CSS_SELECTOR, self.locators['banner_text']).get_attribute("alt")
                visual_bg = banners[index].find_element(By.CSS_SELECTOR, self.locators['banner_bg']).get_attribute("src")
                
                self.logger.info(f"{slide_page}_링크: {banner_link}")
                self.logger.info(f"{slide_page}_문구: {visual_text}")
                self.logger.info(f"{slide_page}_배경: {visual_bg}")

            # 재생/정지 버튼 테스트
            play_button = self.driver.find_element(By.CSS_SELECTOR, self.locators['play_button'])
            pause_button = self.driver.find_element(By.CSS_SELECTOR, self.locators['pause_button'])
            pause_button.click()
            time.sleep(2)
            
            if play_button.is_displayed():
                self.logger.info("정지버튼 > 재생버튼 변경됨")
            else:
                self.logger.info("버튼이 변경되지 않음")

            # 4. 테마배너 슬라이드 버튼 확인
            prev_button = self.driver.find_element(By.CSS_SELECTOR, self.locators['prev_button'])
            next_button = self.driver.find_element(By.CSS_SELECTOR, self.locators['next_button'])

            for direction, limit in [("next", button_count-1), ("previous", 0)]:
                while True:
                    active_slide = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['active_slide']))
                    )
                    current_index = int(active_slide.get_attribute('data-index'))
                    visual_text = active_slide.find_element(By.CSS_SELECTOR, self.locators['banner_text']).get_attribute('alt')
                    time.sleep(1)
                    
                    self.logger.info(f"슬라이드_{current_index+1} 텍스트: {visual_text}")
                    
                    if current_index == limit:
                        break
                        
                    if direction == "previous":
                        WebDriverWait(self.driver, 30).until(
                            EC.element_to_be_clickable(prev_button)
                        ).click()
                    elif direction == "next":
                        if current_index < limit:
                            WebDriverWait(self.driver, 30).until(
                                EC.element_to_be_clickable(next_button)
                            ).click()
                        else:
                            break
                time.sleep(2)

        except Exception as e:
            eh.exception_handler(self.driver, e, "테마배너 테스트 실패")
            raise

class TestCase05(Base):
    """모바일 메뉴 > 기기 섹션에서 랜덤 기기 선택 후 주문하기 클릭, 팝업 창에서 정보 확인 및 장바구니 담기"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m1')

    def execute(self):
        try:
            self.select_mobile_device()
            self.check_available_options()
            self.select_device_option()
            self.select_shipping_option()
            self.select_other_option()
            self.order_info()
            self.cart_redirection()
            self.order_delete()
        except Exception as e:
            eh.exception_handler(self.driver, e, "휴대폰 주문 및 장바구니 테스트 실패")
            raise

    def select_mobile_device(self):
        # 모바일 메뉴 클릭 및 기기 선택 로직
        mobile_menu = find_element(self.driver, (By.CSS_SELECTOR, self.locators['mobile_menu']))
        click(self.driver, mobile_menu)
        time.sleep(5)

        # 디바이스 섹션 포커싱 및 탭 선택
        device_section = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['device_section']))
        )
        ActionChains(self.driver).move_to_element(device_section).perform()

        tabs = device_section.find_elements(By.CSS_SELECTOR, '.c-tabmenu-tab.c-tab-default ul li')
        random_tab = random.choice(tabs)
        random_tab.click()
        self.logger.info(f"선택한 탭: {random_tab.text}")

        # 무작위 기기 선택 및 주문하기 클릭
        visible_devices = self.driver.find_elements(By.CSS_SELECTOR, self.locators['visible_devices'])
        random_device = random.choice(visible_devices)
        device_name = random_device.find_element(By.CSS_SELECTOR, self.locators['device_name']).text
        order_button = random_device.find_element(By.CSS_SELECTOR, self.locators['order_button'])
        order_button.click()
        self.logger.info(f"선택된 기기: {device_name}")

    def check_available_options(self):
        # 팝업창 닫기 및 옵션 확인 로직
        try:
            popup_close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['popup_close_button']))
            )
            popup_close_button.click()
        except TimeoutException:
            self.logger.info("팝업창이 나타나지 않았습니다.")

        # 옵션 섹션 설정
        self.color_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['color_section'])
        self.storage_section = self.driver.find_elements(By.CSS_SELECTOR, self.locators['storage_section'])[0]
        self.join_section = self.driver.find_elements(By.CSS_SELECTOR, self.locators['join_section'])[1]
        self.shipping_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['shipping_section'])
        self.fee_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['fee_section'])
        self.installment_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['installment_section'])
        self.card_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['card_section'])
        self.vip_benefit_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['vip_benefit_section'])

        # VIP 멤버십 혜택 확인 및 추가할인 섹션 설정
        th_texts = [th.text for th in self.driver.find_elements(By.CSS_SELECTOR, self.locators['th_texts'])]
        if "VIP 멤버십 혜택" in th_texts:
            self.sale_plus_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['sale_plus_section'])
            self.logger.info("VIP 멤버십 혜택이 존재합니다. 추가할인 셋팅")
        else:
            self.sale_plus_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['sale_plus_section_vip_none'])
        self.gift_section = self.driver.find_elements(By.CSS_SELECTOR, self.locators['gift_section'])[0]
        self.coupon_section = self.driver.find_elements(By.CSS_SELECTOR, self.locators['coupon_section'])[1]

    def select_device_option(self):
        # 1. 색상 선택
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element(By.CSS_SELECTOR, self.locators['color_section'])).perform()
        
        color_list = self.driver.find_elements(By.CSS_SELECTOR, self.locators['color_options'])
        color_list_text = [color.find_element(By.CSS_SELECTOR, self.locators['color_name']).text.strip() for color in color_list]
        self.logger.info(f"색상옵션: {len(color_list)} {color_list_text}")
        
        selected_color_button = random.choice(color_list)
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['color_button']))).click()
        selected_color = selected_color_button.find_element(By.CSS_SELECTOR, self.locators['color_name']).text.strip()
        self.logger.info(f"선택된 색상: {selected_color}")

        # 2. 저장공간 선택
        actions.move_to_element(self.driver.find_element(By.CSS_SELECTOR, self.locators['storage_section'])).perform()
        
        storage_list = self.driver.find_elements(By.CSS_SELECTOR, self.locators['storage_options'])
        storage_list_text = [storage.find_element(By.CSS_SELECTOR, self.locators['storage_name']).text.strip() for storage in storage_list]
        self.logger.info(f"저장옵션: {len(storage_list)} {storage_list_text}")
        
        selected_storage = random.choice(storage_list)
        selected_storage.find_element(By.CSS_SELECTOR, self.locators['storage_button']).click()
        selected_storage_text = selected_storage.find_element(By.CSS_SELECTOR, self.locators['storage_name']).text.strip()
        self.logger.info(f"선택된 저장공간: {selected_storage_text}")

        # 3. 가입유형 선택
        actions.move_to_element(self.driver.find_element(By.CSS_SELECTOR, self.locators['join_section'])).perform()
        
        join_type_list = self.driver.find_elements(By.CSS_SELECTOR, self.locators['join_options'])
        join_type_list_text = [join.find_element(By.CSS_SELECTOR, self.locators['join_name']).text for join in join_type_list]
        self.logger.info(f"가입유형: {len(join_type_list)} {join_type_list_text}")
        
        selected_join_type = random.choice(join_type_list)
        selected_join_type.find_element(By.CSS_SELECTOR, self.locators['join_button']).click()
        selected_join_type_text = selected_join_type.find_element(By.CSS_SELECTOR, self.locators['join_name']).text.strip()
        self.logger.info(f"선택된 가입유형: {selected_join_type_text}")

        self.driver.implicitly_wait(5)

    def select_shipping_option(self):
        # 배송방법 선택
        actions = ActionChains(self.driver)
        actions.move_to_element(self.shipping_section).perform()
        
        shipping_list = self.shipping_section.find_elements(By.CSS_SELECTOR, self.locators['shipping_options'])
        shipping_list_text = [shipping.find_element(By.CSS_SELECTOR, self.locators['shipping_name']).text.strip() for shipping in shipping_list]
        self.logger.info(f"배송유형: {len(shipping_list)} {shipping_list_text}")
        
        # 배송방법 리스트 첫 번째 옵션 선택
        selected_shipping_option = shipping_list[0]
        shipping_button = selected_shipping_option.find_element(By.CSS_SELECTOR, self.locators['shipping_button'])
        shipping_button.click()
        
        selected_shipping = selected_shipping_option.find_element(By.CSS_SELECTOR, self.locators['shipping_name']).text.strip()
        self.logger.info(f"선택된 배송방법: {selected_shipping}")


    def select_other_option(self):
        # 1. 요금제 선택
        actions = ActionChains(self.driver)
        actions.move_to_element(self.fee_section).perform()
        
        fee_list = self.fee_section.find_elements(By.CSS_SELECTOR, self.locators['fee_options'])
        fee_list_text = [fee.find_element(By.CSS_SELECTOR, self.locators['fee_name']).text.strip() for fee in fee_list]
        self.logger.info(f"요금제유형: {len(fee_list)} {fee_list_text}")
        
        selected_fee = random.choice(fee_list)
        fee_button = selected_fee.find_element(By.CSS_SELECTOR, self.locators['fee_button'])
        fee_button.click()
        selected_fee_text = selected_fee.find_element(By.CSS_SELECTOR, self.locators['fee_name']).text.strip()
        self.logger.info(f"선택된 요금제: {selected_fee_text}")

        # 2. 요금제 특별혜택 선택
        try:
            fee_special_list = self.driver.find_elements(By.CSS_SELECTOR, self.locators['fee_special_options'])
            if fee_special_list:
                selected_fee_special = random.choice(fee_special_list)
                checkbox = selected_fee_special.find_element(By.CSS_SELECTOR, self.locators['fee_special_checkbox'])
                checkbox.click()
                selected_special_fee = selected_fee_special.find_element(By.CSS_SELECTOR, self.locators['fee_special_name']).text.strip()
                self.logger.info(f"선택된 특별혜택: {selected_special_fee}")
            else:
                self.logger.info("특별 혜택이 없습니다.")
        except NoSuchElementException:
            self.logger.info("선택된 요금제에는 특별혜택이 없습니다.")

        # 3. 할부금 납부 기간 선택
        actions.move_to_element(self.installment_section).perform()
        
        try:
            discount_list = self.driver.find_elements(By.CSS_SELECTOR, self.locators['discount_options'])
            if discount_list:
                selected_discount = random.choice(discount_list)
                radio = selected_discount.find_element(By.CSS_SELECTOR, self.locators['discount_radio'])
                radio.click()
                span_elements = selected_discount.find_elements(By.CSS_SELECTOR, self.locators['discount_span'])
                span_texts = [span.text for span in span_elements]
                self.logger.info(f"선택된 할인방법: {span_texts[0]} {span_texts[1]}")
            else:
                notice = self.driver.find_elements(By.CSS_SELECTOR, self.locators['notice'])
                if notice:
                    self.logger.info(f"알림 메시지: {notice[0].text}")
        except NoSuchElementException:
            self.logger.info("선택된 요금제에는 할인방법이 없습니다.")

        # 4. 할부금 납부기간 선택
        installment_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['installment_button']))
        )
        installment_button.click()
        
        installments_list = self.installment_section.find_elements(By.CSS_SELECTOR, self.locators['installments_options'])
        installments_list_text = [installments.find_element(By.CSS_SELECTOR, self.locators['installments_name']).text.strip() for installments in installments_list]
        self.logger.info(f"할부금납부 방법: {len(installments_list)} | {installments_list_text}")
        
        selected_installment = random.choice(installments_list)
        installment_button = selected_installment.find_element(By.CSS_SELECTOR, self.locators['installment_radio'])
        installment_button.click()
        selected_installment_text = selected_installment.find_element(By.CSS_SELECTOR, self.locators['installments_name']).text
        self.logger.info(f"선택된 할부금 납부기간: {selected_installment_text}")

        # 5. 제휴카드 선택
        ActionChains(self.driver).move_to_element(self.card_section).perform()
        more_card_button = self.card_section.find_element(By.CSS_SELECTOR, self.locators['more_card_button'])
        more_card_button.click()
        
        all_card_list = self.card_section.find_elements(By.CSS_SELECTOR, self.locators['card_options'])
        card_list_text = [card.text.strip() for card in all_card_list[1:]]
        self.logger.info(f"카드 미선택 문구: {all_card_list[0].text.strip()}")
        for index, card_text in enumerate(card_list_text):
            self.logger.info(f"카드_{index + 1}: {card_text}")
        
        selected_card_list = random.choice(all_card_list)
        card_button = selected_card_list.find_element(By.CSS_SELECTOR, self.locators['card_radio'])
        card_button.click()
        selected_card_list_text = selected_card_list.find_element(By.CSS_SELECTOR, self.locators['card_name']).text
        self.logger.info(f"선택된 카드: {selected_card_list_text}")

        # 6. VIP맴버십 혜택 선택
        try:
            vip_benefits_list = self.driver.find_elements(By.CSS_SELECTOR, self.locators['vip_benefits_options'])
            if vip_benefits_list:
                ActionChains(self.driver).move_to_element(self.vip_benefilt_section).perform()
                vip_benefits_list_text = [
                    {
                        "이미지": self.vip.find_element(By.CSS_SELECTOR, self.locators['vip_image']).get_attribute('src').strip(),
                        "혜택": self.vip.find_element(By.CSS_SELECTOR, self.locators['vip_benefit']).text.strip(),
                        "가격": self.vip.find_element(By.CSS_SELECTOR, self.locators['vip_price']).text.strip()
                    }
                    for self.vip in vip_benefits_list
                ]
                self.logger.info(f"VIP맴버십 혜택: {len(vip_benefits_list)} {vip_benefits_list_text}")
                
                selected_vip_benefit = random.choice(vip_benefits_list)
                vip_benefits_button = selected_vip_benefit.find_element(By.CSS_SELECTOR, self.locators['vip_radio'])
                vip_benefits_button.click()
                selected_vip_benefit_text = selected_vip_benefit.find_element(By.CSS_SELECTOR, self.locators['vip_benefit']).text
                self.logger.info(f"선택된 VIP 혜택: {selected_vip_benefit_text}")
        except NoSuchElementException:
            self.logger.info("VIP맴버십 혜택이 없습니다.")

        # 7. 추가할인 선택
        actions.move_to_element(self.sale_plus_section).perform()
        sale_plus_list = self.sale_plus_section.find_elements(By.CSS_SELECTOR, self.locators['sale_plus_options'])
        sale_plus_list_text = [sale_plus.find_element(By.CSS_SELECTOR, self.locators['sale_plus_name']).text.strip() for sale_plus in sale_plus_list]
        self.logger.info(f"추가할인: {len(sale_plus_list)} {sale_plus_list_text}")
        
        selected_sale_plus = random.choice(sale_plus_list)
        discount_option_button = selected_sale_plus.find_element(By.CSS_SELECTOR, self.locators['sale_plus_checkbox'])
        discount_option_button.click()
        selected_sale_plus_text = selected_sale_plus.find_element(By.CSS_SELECTOR, self.locators['sale_plus_name']).text.strip()
        self.logger.info(f"선택된 추가 할인: {selected_sale_plus_text}")

        # 8. 사은품 선택
        actions.move_to_element(self.gift_section).perform()
        gift_list = [gift for gift in self.gift_section.find_elements(By.CSS_SELECTOR, self.locators['gift_options']) if not gift.find_elements(By.CSS_SELECTOR, self.locators['gift_sold_out'])]
        gift_list_text = [gift.find_element(By.CSS_SELECTOR, self.locators['gift_name']).text.strip() for gift in gift_list]
        self.logger.info(f"사은품 옵션(품절 제외): {len(gift_list)} | {gift_list_text}")
        
        selected_gift_list = random.choice(gift_list)
        gift_button = selected_gift_list.find_element(By.CSS_SELECTOR, self.locators['gift_radio'])
        gift_button.click()
        selected_gift = selected_gift_list.find_element(By.CSS_SELECTOR, self.locators['gift_name']).text.strip()
        self.logger.info(f"선택된 사은품: {selected_gift}")

        # 9. 쇼핑쿠폰백 선택
        ActionChains(self.driver).move_to_element(self.coupon_section).perform()
        coupon_list = [coupon for coupon in self.coupon_section.find_elements(By.CSS_SELECTOR, self.locators['coupon_options']) if not coupon.find_elements(By.CSS_SELECTOR, self.locators['coupon_disabled'])]
        gift_list_text = [coupon.find_element(By.CSS_SELECTOR, self.locators['coupon_name']).text.strip() for coupon in coupon_list]
        self.logger.info(f"쇼핑쿠폰팩 옵션: {len(coupon_list)} {gift_list_text}")
        
        selected_coupon_option = random.choice(coupon_list)
        coupon_option_button = selected_coupon_option.find_element(By.CSS_SELECTOR, self.locators['coupon_radio'])
        coupon_option_button.click()
        selected_coupon = selected_coupon_option.find_element(By.CSS_SELECTOR, self.locators['coupon_name']).text
        self.logger.info(f"선택된 쇼핑쿠폰백: {selected_coupon}")

    def order_info(self):
        # 주문하기 버튼 클릭 전 선택 사항 리스트 확인
        # 계산 박스 정보 포커싱
        self.calculation_section = self.driver.find_element(By.CSS_SELECTOR, self.locators['calculation_section'])
        ActionChains(self.driver).move_to_element(self.calculation_section).perform()

        # 계산 박스 정보 출력
        self.device_name = self.calculation_section.find_element(By.CSS_SELECTOR, self.locators['device_name']).text
        time.sleep(10)

        # 색상 / 기기용량 / 기기변경
        device_color = self.calculation_section.find_element(By.CSS_SELECTOR, self.locators['device_color']).text
        device_storage = self.calculation_section.find_element(By.CSS_SELECTOR, self.locators['device_storage']).text
        device_change_type = self.calculation_section.find_element(By.CSS_SELECTOR, self.locators['device_change_type']).text

        self.logger.info(f"선택된 기기명: {self.device_name}")
        self.logger.info(f"선택된 색상: {device_color}")
        self.logger.info(f"선택된 저장공간: {device_storage}")
        self.logger.info(f"선택된 가입유형: {device_change_type}")

        self.driver.implicitly_wait(5)


    def cart_redirection(self):
        # 1. 장바구니 버튼 클릭
        cart_button = self.calculation_section.find_element(By.CSS_SELECTOR, self.locators['cart_button'])
        cart_button.click()
        self.logger.info("장바구니 버튼 클릭 완료")

        # 2. 장바구니 버튼 클릭시, 모달창 확인 버튼 클릭하기
        header = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['cart_modal_header']))
        ).text.strip()
        
        if header == "장바구니담기":
            self.logger.info("장바구니담기 팝업창 오픈 완료")
            cart_link_button = self.driver.find_element(By.CSS_SELECTOR, self.locators['cart_link_button'])
            cart_link_button.click()
            self.logger.info("장바구니로 이동 버튼 클릭 완료")

            try:
                WebDriverWait(self.driver, 10).until(EC.url_contains("/cart"))
                cart_url = self.driver.current_url
                self.logger.info(f"장바구니 페이지로 이동 성공 URL: {cart_url}")
            except TimeoutException:
                cart_url = self.driver.current_url
                self.logger.error(f"장바구니 페이지로 이동 실패 URL: {cart_url}")
        else:
            self.logger.error("장바구니 팝업창이 나타나지 않았습니다.")

        # 3. 장바구니에서 기기명 확인
        self.cart_list = self.driver.find_element(By.CSS_SELECTOR, self.locators['cart_list'])
        cart_device_info = self.cart_list.find_element(By.CSS_SELECTOR, self.locators['cart_device_info'])
        cart_device_name = cart_device_info.find_element(By.CSS_SELECTOR, self.locators['cart_device_name']).text
        self.logger.info(f"장바구니 기기명: {cart_device_name}")

        self.device_name = self.device_name.strip()
        cart_device_name = cart_device_name.strip().replace('\n', ' ')
        if cart_device_name in self.device_name:
            self.logger.info(f"선택된 기기: {self.device_name}, 장바구니 기기: {cart_device_name}와 기기명이 일치합니다")
        else:
            self.logger.info(f"선택된 기기: {self.device_name}, 장바구니 기기: {cart_device_name}와 기기명이 일치하지 않습니다.")

    def order_delete(self):
        # 1. 장바구니에서 항목 삭제
        try:
            delete_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['delete_button']))
            )
            delete_button.click()
            time.sleep(1)

            confirm_delete_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['confirm_delete_button']))
            )
            confirm_delete_button.click()
            time.sleep(2)
        except TimeoutException as e:
            self.logger.error(f"Error: {e}")
            self.logger.error("장바구니에서 항목 삭제 실패")

        # 2. 장바구니에서 삭제 되었는지 리스트에서 확인
        empty_cart = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['empty_cart']))
        )
        if empty_cart:
            self.logger.info("장바구니가 비어 있습니다.")
            # 메인 페이지로 이동
            main_page_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.locators['main_page_button']))
            )
            main_page_button.click()
            self.logger.info("메인 페이지로 이동 버튼 클릭 완료")
        else:
            self.logger.info("장바구니에 항목이 남아 있습니다.")

class TestCase06(Base):
    """인터넷/IPTV 결합 영역 드롭다운 항목 무작위선택 후 할인 금액 데이터 추출 및 '가입상담신청' 클릭, 상담 신청하기 페이지 내 할인 금액 데이터 비교"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.locators = LocatorLoader.load_locators('gnb_m1')
    
    def execute(self):
        try:
            # 1. 모바일 메뉴 클릭
            mobile_button = self.driver.find_element(By.CSS_SELECTOR, self.locators['mobile_menu'])
            mobile_button.click()
            time.sleep(5)

            # 2. 인터넷/IPTV결합 섹션 포커싱
            mobile_combined_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.locators['device_section']))
            )
            ActionChains(self.driver).move_to_element(mobile_combined_section).perform()
            self.logger.info("인터넷/IPTV결합 섹션 포커싱 완료")

            # 3-1. 드롭다운 갯수 확인
            dropdowns = mobile_combined_section.find_elements(By.CSS_SELECTOR, self.locators['dropdowns'])
            select_area_txt = mobile_combined_section.find_elements(By.CSS_SELECTOR, self.locators['select_area_txt'])
            for element in select_area_txt:
                select_area_txt = element.text
                self.logger.info(f"드롭다운 영역: {select_area_txt}")
            self.logger.info(f"드롭다운 갯수: {len(dropdowns)}")

            # 3-2. 핸드폰 결합 기기 수/인터넷/IPTV 드롭다운 랜덤 선택
            for dropdown in dropdowns:
                select_button = dropdown.find_element(By.CSS_SELECTOR, self.locators['select_button'])
                select_button.click()
                time.sleep(1)
                options = dropdown.find_elements(By.CSS_SELECTOR, self.locators['options'])
                area_txt = dropdown.find_element(By.CSS_SELECTOR, self.locators['area_txt'])
                random_option = random.choice(options)
                random_option_text = random_option.text
                random_option.click()
                self.logger.info(f"{(area_txt).text}: {random_option_text}")
                time.sleep(2)

            # 4-1. 할인 금액 데이터 추출
            results = mobile_combined_section.find_elements(By.CSS_SELECTOR, self.locators['results'])
            discount_values = []
            for result in results:
                discount_text = result.text.strip()
                discount_value = int(''.join(filter(str.isdigit, discount_text)))
                discount_values.append(discount_value)
                total_discount = sum(discount_values)
                self.logger.info(f"할인금액: {discount_value}")
            self.logger.info(f"총 할인금액: {total_discount}")
           
            # 4-2. 할인 금액 데이터 추출
            discount_spans = mobile_combined_section.find_elements(By.CSS_SELECTOR, self.locators['discount_spans'])
            for discount_span in discount_spans:
                discount_text = ''.join(filter(lambda x: x.isdigit() or x == '.', discount_span.text.strip()))
                self.logger.info(f"할인금액: {discount_text}")

            # 4-3. 상담 신청하기 페이지 내 할인 금액 데이터 비교
            if total_discount == int(discount_text.replace(',', '')):
                self.logger.info(f"{total_discount}원으로 할인금액이 일치합니다.")
            else:
                self.logger.info(f"할인금액이 일치하지 않습니다. 총 할인금액: {total_discount}, 할인금액: {discount_text}")
            time.sleep(5)

            # 5. 가입상담신청 버튼 클릭
            consultation_button = find_element(self.driver , (By.CSS_SELECTOR, self.locators['consultation_button']))
            time.sleep(5)
            click(self.driver, consultation_button)

            # 6. 상위 윈도우에서 하위 윈도우로 전환
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.logger.info("상담신청 페이지로 이동")

            consultation_modal = find_element(self.driver , (By.CSS_SELECTOR, self.locators['consultation_modal']))
            if consultation_modal:
                self.logger.info("상담신청 모달창이 나타남")
            else:
                self.logger.info("상담신청 모달창이 나타나지 않음")

            # 7. 상담신청 페이지 내 할인 금액 데이터 추출
            # 할인 금액 데이터 추출
            calcutaor_value = find_element(self.driver , (By.CSS_SELECTOR, self.locators['calcutaor_value']))
            total_amt = calcutaor_value.get_attribute("data-total-amt")
            self.logger.info(f"상담신청 페이지 내 할인 금액: {total_amt}")

            if total_discount == int(total_amt.replace(',', '')):
                self.logger.info(f"{total_discount}원으로 할인금액이 일치합니다.")
            else:
                self.logger.info(f"할인금액이 일치하지 않습니다. 총 할인금액: {total_discount}, 할인금액: {total_amt}")
            
        except Exception as e:
            eh.exception_handler(self.driver, e, "인터넷/IPTV 결합 테스트 실패")
            raise
