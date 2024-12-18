import os
import time

"""
    class Screenshot: 에러시 스크린샷 저장
"""
class Screenshot:
    def __init__(self, driver, directory="./screenshots"):
        self.driver = driver
        self.directory = directory

        # 스크린샷 저장 디렉토리 생성
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def capture(self, filename=None):
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.directory, filename)
        self.driver.save_screenshot(filepath)
        print(f"스크린샷 저장: {filepath}")