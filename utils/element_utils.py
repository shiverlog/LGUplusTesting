from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.custom_logger import custom_logger
from utils.exception_handler import handle_exception
from config.config import IMPLICIT_WAIT, EXPLICIT_WAIT

"""
    # Selenium WebDriver를 위한 요소 조작 유틸리티 모듈
    find_element: 요소 찾기
    find_elements: 요소들 찾기
    find_visible_element: 보이는 요소 찾기
    find_clickable_element: 클릭 가능한 요소 찾기
    click_element: 요소 클릭
    enter_text: 요소에 텍스트 입력
    clear_text: 요소의 텍스트 지우기
    get_text: 요소의 텍스트 가져오기
    get_attribute: 요소의 속성 값 가져오기
    select_option: 요소에서 옵션 선택
    is_element_present: 요소 존재 여부 확인
    is_element_visible: 요소 보이는 상태 확인
    is_element_enabled: 요소 활성화 여부 확인
    is_element_selected: 요소 선택 여부 확인
    wait_for_element_to_appear: 요소가 나타날때까지 대기
    wait_for_element_to_disappear: 요소가 사라질 때까지 대기
    wait_until_element_is_enabled: 요소가 활성화 될 때까지 대기
"""

# find_element
def find_element(driver, locator):
    """요소를 찾아 반환"""
    try:
        element = WebDriverWait(driver, IMPLICIT_WAIT).until(
            EC.presence_of_element_located(locator)
        )
        custom_logger.info(f"요소 찾음: {locator}")
        return element
    except Exception as e:
        handle_exception(driver, e, f"요소를 찾을 수 없음: {locator}")
        return None

# find_elements
def find_elements(driver, locator):
    """여러 요소들을 찾아 리스트로 반환"""
    try:
        elements = WebDriverWait(driver, IMPLICIT_WAIT).until(
            EC.presence_of_all_elements_located(locator)
        )
        custom_logger.info(f"요소들 찾음: {locator}")
        return elements
    except Exception as e:
        handle_exception(driver, e, f"요소들을 찾을 수 없음: {locator}")
        return []

# find_visible_element
def find_visible_element(driver, locator):
    """화면에 보이는 요소를 찾아 반환"""
    try:
        element = WebDriverWait(driver, IMPLICIT_WAIT).until(
            EC.visibility_of_element_located(locator)
        )
        custom_logger.info(f"보이는 요소 찾음: {locator}")
        return element
    except Exception as e:
        handle_exception(driver, e, f"보이는 요소를 찾을 수 없음: {locator}")
        return None

# find_clickable_element
def find_clickable_element(driver, locator):
    """클릭 가능한 요소를 찾아 반환"""
    try:
        element = WebDriverWait(driver, IMPLICIT_WAIT).until(
            EC.element_to_be_clickable(locator)
        )
        custom_logger.info(f"클릭 가능한 요소 찾음: {locator}")
        return element
    except Exception as e:
        handle_exception(driver, e, f"클릭 가능한 요소를 찾을 수 없음: {locator}")
        return None

# click_element
def click_element(driver, locator):
    """요소를 클릭"""
    try:
        element = find_clickable_element(driver, locator)
        if element:
            element.click()
            custom_logger.info(f"{locator} 요소를 클릭")
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소 클릭 실패")

# enter_text
def enter_text(driver, locator, text):
    """요소에 텍스트 입력"""
    try:
        element = find_element(driver, locator)
        if element:
            element.send_keys(text)
            custom_logger.info(f"{locator} 요소에 '{text}' 텍스트를 입력 완료")
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소에 텍스트 입력 실패")

# clear_text
def clear_text(driver, locator):
    """요소의 텍스트 삭제"""
    try:
        element = find_element(driver, locator)
        if element:
            element.clear()
            custom_logger.info(f"{locator} 요소의 텍스트 지우기 성공")
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소의 텍스트 지우기 실패")

# get_text
def get_text(driver, locator):
    """요소의 텍스트 값을 반환"""
    try:
        element = find_element(driver, locator)
        if element:
            text = element.text
            custom_logger.info(f"{locator} 요소에서 텍스트 '{text}' 가져오기 성공")
            return text
        return None
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소의 텍스트 가져오기 실패")
        return None

# get_attribute
def get_attribute(driver, locator, attribute_name):
    """요소의 속성 값을 반환"""
    try:
        element = find_element(driver, locator)
        if element:
            attribute_value = element.get_attribute(attribute_name)
            custom_logger.info(f"{locator} 요소에서 '{attribute_name}' 속성 값 '{attribute_value}' 가져오기 성공")
            return attribute_value
        return None
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소의 속성 값 가져오기 실패")
        return None

# select_option
def select_option(driver, locator, value):
    """드롭다운에서 옵션 선택"""
    try:
        from selenium.webdriver.support.ui import Select
        element = find_element(driver, locator)
        if element:
            select = Select(element)
            select.select_by_value(value)
            custom_logger.info(f"{locator} 요소에서 '{value}' 옵션을 선택 완료")
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소에서 옵션 선택 실패")

# is_element_present
def is_element_present(driver, locator):
    """요소 존재 여부 확인"""
    try:
        WebDriverWait(driver, IMPLICIT_WAIT).until(
            EC.presence_of_element_located(locator)
        )
        custom_logger.info(f"{locator} 요소가 존재")
        return True
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소를 찾을 수 없음")
        return False

# is_element_visible
def is_element_visible(driver, locator):
    """요소가 화면에 보이는지 확인"""
    try:
        WebDriverWait(driver, IMPLICIT_WAIT).until(
            EC.visibility_of_element_located(locator)
        )
        custom_logger.info(f"{locator} 요소를 보이는 상태로 찾음")
        return True
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소가 보이지 않음")
        return False

# is_element_enabled
def is_element_enabled(driver, locator):
    """요소가 활성화 상태인지 확인"""
    try:
        element = find_element(driver, locator)
        if element:
            is_enabled = element.is_enabled()
            custom_logger.info(f"{locator} 요소가 {'활성화' if is_enabled else '비활성화'}")
            return is_enabled
        return False
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소 활성화 상태 확인 실패")
        return False

# is_element_selected
def is_element_selected(driver, locator):
    """요소가 선택 상태인지 확인"""
    try:
        element = find_element(driver, locator)
        if element:
            is_selected = element.is_selected()
            custom_logger.info(f"{locator} 요소가 {'선택' if is_selected else '선택되지 않음'}")
            return is_selected
        return False
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소 선택 상태 확인 실패")
        return False

# wait_for_element_to_appear
def wait_for_element_to_appear(driver, locator, timeout=EXPLICIT_WAIT):
    """요소가 나타날 때까지 대기"""
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        custom_logger.info(f"{locator} 요소가 나타날 때까지 기다렸습니다.")
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소가 {timeout}초 후에도 나타나지 않았습니다.")

# wait_for_element_to_disappear
def wait_for_element_to_disappear(driver, locator):
    """요소가 사라질 때까지 대기"""
    try:
        WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.invisibility_of_element_located(locator)
        )
        custom_logger.info(f"{locator} 요소가 사라질 때까지 기다리기")
    except Exception as e:
        handle_exception(driver, e, f"{locator} 요소가 {EXPLICIT_WAIT}초 후에도 사라지지 않음")

# wait_until_element_is_enabled
def wait_until_element_is_enabled(driver, element):
    """요소가 활성화될 때까지 대기"""
    try:
        WebDriverWait(driver, EXPLICIT_WAIT).until(EC.element_to_be_clickable(element))
        custom_logger.info(f"{element} 활성화될때까지 대기")
    except Exception as e:
        handle_exception(driver, e, f"대기실패 ERROR")

# handle_alert
def handle_alert(driver, action="accept"):
    """알림창 처리 (확인/취소)"""
    try:
        alert = driver.switch_to.alert
        if action == "accept":
            alert.accept()
            custom_logger.info("경고창 확인 버튼을 클릭")  
        else:
            alert.dismiss()
            custom_logger.info("경고창 취소 버튼을 클릭") 
    except Exception as e:
        handle_exception(driver, e, f"경고창 처리 실패")
