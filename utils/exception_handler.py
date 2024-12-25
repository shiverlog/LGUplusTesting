from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.custom_logger import custom_logger
from utils.screenshot import Screenshot
import traceback

def exception_handler(driver, e, message="오류 발생"):
    """예외 처리"""
    custom_logger.error(f"{message}: {str(e)}")
    custom_logger.error(traceback.format_exc())
    
    if isinstance(e, TimeoutException):
        custom_logger.info("타임아웃 발생. 페이지를 새로고침합니다.")
        # driver.refresh()
    elif isinstance(e, NoSuchElementException):
        custom_logger.warning("요소를 찾을 수 없습니다.")
    else:
        custom_logger.error(f"예상치 못한 예외 발생: {type(e).__name__}")
    
    # 스크린샷 캡처 실행
    Screenshot(driver).capture_error(e, message)
    return False 