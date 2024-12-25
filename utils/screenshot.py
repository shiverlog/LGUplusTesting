import os, time
from utils.custom_logger import Logger
from config.config import SCREENSHOT_DIR

# screenshot.py
class Screenshot:
    """스크린샷 캡처 클래스"""
    def __init__(self, driver, directory=SCREENSHOT_DIR):
        self.driver = driver
        self.directory = directory
        self.logger = Logger().get_logger()

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def capture_error(self, e, message):
        """예외 발생 시 스크린샷 캡처"""
        try:
            # 현재 실행 중인 클래스 이름 가져오기
            test_class = e.__traceback__.tb_frame.f_locals.get('self').__class__.__name__
            
            # 에러 메시지에서 공백 제거
            error_msg = message.replace(" ", "")
            
            # 스크린샷 캡처
            filepath = self.capture(test_class, error_msg)
            if filepath:
                self.logger.info(f"스크린샷 저장 완료: {filepath}")
                
        except Exception as screenshot_error:
            self.logger.error(f"스크린샷 저장 실패: {str(screenshot_error)}")

    def capture(self, test_name=None, error_msg=None):
        """스크린샷 캡처 및 저장"""
        try:
            timestamp = time.strftime("%Y%m%d%H%M%S")
            filename = f"{test_name}_{error_msg}_{timestamp}.png"
            filepath = os.path.join(self.directory, filename)
            
            self.driver.save_screenshot(filepath)
            return filepath
            
        except Exception:
            return None
