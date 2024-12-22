from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.custom_logger import custom_logger
from element_utils import *
from custom_actionchains import *
from exception_handler import ExceptionHandler

"""
    class ModalHandler: 모달창 처리
    handle_modal: 모달 케이스에 따라 처리 if문으로 분기
    determine_modal_type: 모달 타입 결정
"""

class ModalHandler:
    """모달창 처리 클래스"""
    # determine_modal_type
    def determine_modal_type(self):
        try:
            # 모달창이 나타날 때까지 기다립니다.
            wait_for_element_to_appear(self.driver, (By.CSS_SELECTOR, ".modal-content"))

            # .modal-content 클래스를 가진 활성화된 모달 요소를 가져옵니다.
            modal_content = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-content"))
            )
            
            # modal_type을 결정합니다.
            if modal_content.find_element(By.CSS_SELECTOR, ".pop-tit-1") and modal_content.find_element(By.CSS_SELECTOR, ".pop-tit-1").text.strip() == "주소찾기":
                modal_type = "address_modal"
            
            elif modal_content.find_element(By.CSS_SELECTOR, ".h3") and modal_content.find_element(By.CSS_SELECTOR, ".h3").text.strip() == "확인" \
                    and modal_content.find_element(By.CSS_SELECTOR, ".modal-footer button") and modal_content.find_element(By.CSS_SELECTOR, ".modal-footer button").text.strip() == "확인":
                modal_type = "confirm_modal"
            
            elif modal_content.find_element(By.CSS_SELECTOR, ".pop-tit-1") and modal_content.find_element(By.CSS_SELECTOR, ".pop-tit-1").text.strip() == "4G 요금제 선택":
                modal_type = "plan_select_modal"
            
            else:
                modal_type = "unknown"

            # handle_modal 함수를 호출합니다.
            self.handle_modal(modal_type)

        except Exception as e:
            handle_exception(self.driver, e, "모달 타입 결정 중 오류 발생")# 모달창의 타입을 결정

    # handle_modal
    def handle_modal(self, modal_type):
        try: 
            match modal_type:
                case "event_modal":
                    self.handle_event_modal()
                case "confirm_modal":
                    self.handle_confirm_modal()
                case "address_modal":
                    self.handle_address_modal()
                case "market_pipup_modal":
                    self.handle_market_pipup_modal()
                case _:
                    self.logger.error(f"처리할 수 없는 모달창 타입")
        except Exception as e:
            self.logger.error(f"모달창 처리 실패: {str(e)}")

    # handle_event_modal
    # handle_confirm_modal
    def handle_confirm_modal(self):
        try:
            # 모달창의 확인 버튼이 나타날 때까지 대기
            confirm_button = find_clickable_element(self.driver, (By.CSS_SELECTOR, 'div.c-btn-group button.c-btn-solid-1-m'))
            
            click(confirm_button)

            wait_for_element_to_disappear(self.driver, (By.CSS_SELECTOR, 'div.modal-dialog'))
            self.logger.info("모달창 닫힘 감지 완료")

        except Exception as e:
            handle_exception(self.driver, e, "확인 모달 처리 실패")
            
    # handle_address_modal
    # handle_market_pipup_modal
    


