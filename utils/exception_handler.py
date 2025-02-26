from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, StaleElementReferenceException, WebDriverException, InvalidSelectorException, InvalidElementStateException, MoveTargetOutOfBoundsException
from utils.custom_logger import custom_logger
from utils.screenshot import Screenshot
import traceback

def exception_handler(driver, e, message = "오류 발생"):
    """
    예외 처리
    TimeoutException: 지정된 시간 내에 작업이 완료되지 않았을 때 발생
    NoSuchElementException: 요청한 요소를 페이지에서 찾을 수 없을 때 발생
    TypeError: 잘못된 타입의 인자가 함수에 전달되었거나, 객체가 예상치 못한 타입일 때 발생
    KeyError: 딕셔너리에서 존재하지 않는 키를 참조하려고 할 때 발생
    IndexError: 리스트나 튜플 등의 시퀀스에서 유효하지 않은 인덱스에 접근하려고 할 때 발생
    ElementNotInteractableException: 요소가 페이지에 존재하지만 클릭, 입력 등의 상호작용이 불가능한 상태일 때 발생
    ElementClickInterceptedException: 요소가 다른 요소에 가려져 클릭할 수 없는 경우 발생
    AttributeError: 객체에 존재하지 않는 속성이나 메서드를 호출하려고 할 때 발생
    AssertionError: assert 문이 실패했을 때 발생하며, 일반적으로 테스트나 검증 과정에서 사용
    StaleElementReferenceException: 참조하는 요소가 더 이상 DOM에 존재하지 않을 때 발생
    WebDriverException: WebDriver 관련 일반적인 문제가 발생했을 때 발생
    InvalidSelectorException: 잘못된 선택자(selector)가 사용되었을 때 발생
    InvalidElementStateException: 요소가 현재 수행하려는 작업에 적합하지 않은 상태일 때 발생
    MoveTargetOutOfBoundsException: 타겟 요소가 뷰포트 밖에 있어 이동할 수 없을 때 발생
    """
    custom_logger.error(f"{message}: {str(e)}")
    custom_logger.error(traceback.format_exc())

    if isinstance(e, TimeoutException):
        custom_logger.info("타임아웃이 발생했습니다.")
    elif isinstance(e, NoSuchElementException):
        custom_logger.warning("요소를 찾을 수 없습니다.")
    elif isinstance(e, TypeError):
        custom_logger.warning("해당 요소와 상호작용할 수 없습니다.")
    elif isinstance(e, KeyError):
        custom_logger.warning("키 값에 문제가 있습니다.")
    elif isinstance(e, IndexError):
        custom_logger.warning("인덱스 값에 문제가 있습니다.")
    elif isinstance(e, ElementNotInteractableException):
        custom_logger.warning("해당 요소와 상호작용할 수 없습니다.")
    elif isinstance(e, ElementClickInterceptedException):
        custom_logger.warning("해당 요소를 클릭할 수 없습니다.")
    elif isinstance(e, AttributeError):
        custom_logger.warning("요소를 찾을 수 없습니다.")
    elif isinstance(e, AssertionError):
        custom_logger.warning("이슈가 발생했습니다.")
    elif isinstance(e, StaleElementReferenceException):
        custom_logger.warning("요소가 더 이상 DOM에 존재하지 않습니다.")
    elif isinstance(e, WebDriverException):
        custom_logger.warning("WebDriver 관련 문제가 발생했습니다.")
    elif isinstance(e, InvalidSelectorException):
        custom_logger.warning("잘못된 선택자가 사용되었습니다.")
    elif isinstance(e, InvalidElementStateException):
        custom_logger.warning("요소가 유효하지 않은 상태입니다.")
    elif isinstance(e, MoveTargetOutOfBoundsException):
        custom_logger.warning("타겟 요소가 뷰포트 밖에 있습니다.")
    else:
        custom_logger.error(f"예상치 못한 예외가 발생했습니다: {type(e).__name__}")

    # 스크린샷 캡처 실행
    Screenshot(driver).capture_error(e, message)
    return False