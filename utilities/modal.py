from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

"""
    class ModalHandler: 모달창 처리
"""

class ModalHandler:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def click_buttons(self):
        try:
            while True:
                # 모달창의 확인 버튼이 나타날 때까지 대기
                confirm_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.c-btn-group button.c-btn-solid-1-m'))
                )
                confirm_button.click()  # 확인 버튼 클릭
                self.logger.info("확인 버튼 클릭 완료")

                # 모달창이 닫히기를 기다림
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.modal-dialog'))
                )
                self.logger.info("모달창 닫힘 감지 완료")

        except Exception as e:
            self.logger.info(f"더 이상 모달창이 없음: {str(e)}")