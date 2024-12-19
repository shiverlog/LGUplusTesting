import os
import time
import utils.custom_logger as custom_logger
from config import SCREENSHOT_DIR

"""
    class Screenshot: 에러시 스크린샷 저장
"""
class Screenshot:
    def __init__(self, driver, directory=SCREENSHOT_DIR):
        self.driver = driver
        self.directory = directory

        # 스크린샷 저장 디렉토리 생성
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def capture(self, filename=None):
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}_{time.time_ns()}.png"
        filepath = os.path.join(self.directory, filename)
        try:
            self.driver.save_screenshot(filepath)
            custom_logger.info(f"스크린샷 저장: {filepath}")
        except Exception as e:
            custom_logger.error(f"스크린샷 저장 실패: {e}")