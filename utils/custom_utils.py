
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.custom_logger import custom_logger
from utils import exception_handler as eh
from config.config import EXPLICIT_WAIT, EXPLICIT_WAIT

# get_element_info
def get_element_info(element):
    """WebElement 객체의 정보를 딕셔너리로 반환하는 함수"""
    return {
        "tag_name": element.tag_name,
        "id": element.get_attribute('id'),
        "class": element.get_attribute('class')
}

# find_visible_section
def find_visible_sections(driver, locators, text=""):
    """각 페이지 주요 섹션 존재 확인"""
    for key, value in locators.items():
        if '_section' in key:
            find_visible_element(driver, (By.CSS_SELECTOR, value), f"{text} {key} 영역")

# find_visible_element
def find_visible_element(driver, locator, text=""):
    """보이는 요소를 찾는 함수"""
    try:
        element = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_element_located(locator)  # 요소가 존재하는지 확인
        )
        # 요소가 화면에 보이지 않으면 스크롤하여 포커싱
        if not element.is_displayed():
            move_to_element(element)
            custom_logger.info(f"{text}{locator}(이)가 화면에 보이지 않아 스크롤하여 포커싱했습니다.")

        custom_logger.info(f"{text}{locator}(이)가 화면에 보입니다.")
        return element
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}{locator}(이)가 화면에 보이지 않습니다.")
        return None

# select_random_list_one
def select_random_list_one(driver, locator, text=""):
    """요소들을 찾아 랜덤하게 선택하는 함수"""
    try:
        elements = find_elements(driver, locator, text)
        if elements:
            elements_text = []
            for element in elements:
                elements_text.append(get_text(driver, element, text)) 
            import random
            random_element = random.choice(elements)
            custom_logger.info(f"{text}{locator}(을)를 랜덤하게 선택하였습니다.")
            return random_element, elements_text  
        return None, []  
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}{locator}(을)를 랜덤하게 요소 선택하지 못했습니다.")
        return None, [] 

# find_element
def find_element(driver, locator, text=""):
    """요소를 찾는 함수"""
    try:
        element = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_element_located(locator)
        )
        custom_logger.info(f"{text}{locator}(을)를 찾았습니다.")
        return element
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}{locator}(을)를 찾지못했습니다.")
        return None

# find_elements
def find_elements(driver, locator, text=""):
    """요소들을 찾는 함수"""
    try:
        elements = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_all_elements_located(locator)
        )
        custom_logger.info(f"{text}{locator}들을 {len(elements)}개 찾았습니다.")
        return elements
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}{locator}들을 찾지못했습니다.")
        return []
    
# move_to_element
def move_to_element(driver, locator, text=""):
    """요소로 마우스를 이동"""
    try:
        actions = ActionChains(driver)
        actions.pause(1)  # 1초 멈춤
        actions.move_to_element(locator).perform()
        custom_logger.info(f"{text}{locator}로 마우스를 이동했습니다.")
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}{locator}로 마우스를 이동하지 못했습니다.")

# click
def click(driver, locator, text=""):
    """요소를 클릭하는 함수"""
    try:
        element_info = get_element_info(locator) 
        ActionChains(driver).click(locator).perform()
        custom_logger.info(f"{text}{element_info}(을)를 클릭하였습니다.")
    except Exception as e:
        custom_logger.error(f"{text}{element_info}(을)를 클릭 실패하였습니다. {e}")
        raise e

# get_text
def get_text(driver, locator, text=""):
    """요소의 텍스트를 가져오는 함수"""
    try:
        element = find_element(driver, locator, text)
        if element:
            try:
                # .text로 텍스트 가져오기 시도
                element_text = element.text.strip().replace("\n", " ")
                custom_logger.info(f"{text}{locator}에서 텍스트 '{element_text}'를 가져왔습니다.")
                return text
            except Exception as e:
                # .text로 실패 시 .get_attribute('textContent') 시도
                text = element.get_attribute('textContent').strip().replace("\n", " ")
                custom_logger.warning(f"{text}{locator}에서 .get_attribute('textContent')을 사용하여 텍스트 '{element_text}'를 가져왔습니다.")
                return text
        return None
    except Exception as e:
        eh.exception_handler(driver, e, f"{locator} 요소의 텍스트 가져오기 실패")
        return None
    
# show_elements_text
def show_elements_text(driver, locator, text=""):
    """요소안의 정보를 텍스트로 출력하는 함수"""
    try:
        elements = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_all_elements_located(locator)
        )
        custom_logger.info(f"{text}{locator}들을 {len(elements)}개 찾았습니다.")
        for index, element in enumerate(elements):
            print_info = element.get_attribute('src')
            if print_info:
                custom_logger.info(f"{text} {index + 1}번째 src: {print_info}")
            else:  # 이미지가 아닌 경우
                custom_logger.info(f"{text} {index + 1}번째 텍스트: {element.text.strip()}")
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}{locator}들을 찾지못했습니다.")
        return []

# show_element_list
def show_element_list(driver, locator, text=""):
    """요소들을 리스트로 출력하는 함수"""
    try:
        elements = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_all_elements_located(locator)
        )
        custom_logger.info(f"{text}{locator}들을 {len(elements)}개 찾았습니다.")
        print_info = []
        for element in elements:
            src = element.get_attribute('src')
            if src:
                print_info.append(src)
            else:
                print_info.append(element.text.strip())
        custom_logger.info(f"{text} src: {print_info}")
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}{locator}들을 찾지못했습니다.")
        return []
    
# # find_visible_element
# def find_visible_element(driver, locator, text=""):
#     """보이는 요소를 찾는 함수"""
#     try:
#         element = WebDriverWait(driver, EXPLICIT_WAIT).until(
#             EC.visibility_of_element_located(locator)
#         )
#         if not element.is_displayed():
#             move_to_element(driver, element)
#         custom_logger.info(f"{text}{locator}(이)가 화면에 보입니다.")
#         return element
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{text}{locator}(이)가 화면에 보이지 않습니다.")
#         return None
    
# def check_section_active(driver, locator, text=""):
#     """섹션이 활성화 상태(active 클래스 포함)인지 확인하는 함수"""
#     try:
#         element = find_visible_element(driver, locator, text)  # 요소 찾기
#         if element:
#             move_to_element(driver, element, text)
#             class_name = element.get_attribute("class")
#             if "active" in class_name:
#                 custom_logger.info(f"{text} 섹션이 활성화 상태입니다.")
#                 return True
#         else:
#             return False
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{text} 섹션 활성화 상태 확인 실패")
#         return False





# def click_and_hold(driver, element):
#     """요소를 클릭하고 누른 상태를 유지하는 함수"""
#     actions = ActionChains(driver).click_and_hold(element)
#     perform_action(driver, actions, f"{element} 요소 클릭 및 유지")

# def context_click(driver, element):
#     """요소를 마우스 오른쪽 버튼으로 클릭하는 함수"""
#     actions = ActionChains(driver).context_click(element)
#     perform_action(driver, actions, f"{element} 요소에서 마우스 오른쪽 버튼 클릭")

# def double_click(driver, element):
#     """요소를 더블 클릭하는 함수"""
#     actions = ActionChains(driver).double_click(element)
#     perform_action(driver, actions, f"{element} 요소 더블 클릭")

# def drag_and_drop(driver, source, target):
#     """source 요소를 target 요소로 드래그 앤 드롭"""
#     actions = ActionChains(driver).drag_and_drop(source, target)
#     perform_action(driver, actions, f"{source} 요소를 {target}로 드래그 앤 드롭")

# def drag_and_drop_by_offset(driver, source, xoffset, yoffset):
#     """source 요소를 offset으로 드래그 앤 드롭"""
#     actions = ActionChains(driver).drag_and_drop_by_offset(source, xoffset, yoffset)
#     perform_action(driver, actions, f"{source} 요소를 ({xoffset}, {yoffset})만큼 드래그 앤 드롭")



# def move_to_element_with_offset(driver, element, xoffset, yoffset):
#     """요소에서 특정 오프셋만큼 마우스를 이동"""
#     actions = ActionChains(driver).move_to_element_with_offset(element, xoffset, yoffset)
#     perform_action(driver, actions, f"{element} 요소에서 ({xoffset}, {yoffset}) 만큼 떨어진 곳으로 마우스 이동")

# def key_down(driver, value, element=None):
#     """키를 누르는 함수"""
#     actions = ActionChains(driver).key_down(value, element)
#     perform_action(driver, actions, f"{element} 요소에 키 누름: {value}")

# def key_up(driver, value, element=None):
#     """키를 놓는 함수"""
#     actions = ActionChains(driver).key_up(value, element)
#     perform_action(driver, actions, f"{element} 요소에 키 놓음: {value}")

# def move_by_offset(driver, xoffset, yoffset):
#     """현재 위치에서 오프셋만큼 마우스를 이동"""
#     actions = ActionChains(driver).move_by_offset(xoffset, yoffset)
#     perform_action(driver, actions, f"마우스를 ({xoffset}, {yoffset}) 만큼 이동")

# def pause(driver, seconds):
#     """지정된 시간 동안 일시중지"""
#     actions = ActionChains(driver).pause(seconds)
#     perform_action(driver, actions, f"{seconds}초 동안 일시중지")

# def release(driver, element=None):
#     """마우스 버튼 놓기"""
#     actions = ActionChains(driver).release(element)
#     perform_action(driver, actions, f"{element} 요소에서 마우스 버튼 놓기")

# def send_keys(driver, *keys_to_send):
#     """현재 포커스된 요소에 키 입력"""
#     actions = ActionChains(driver).send_keys(*keys_to_send)
#     perform_action(driver, actions, f"키 입력: {keys_to_send}")

# def send_keys_to_element(driver, element, *keys_to_send):
#     """지정된 요소에 키 입력"""
#     actions = ActionChains(driver).send_keys_to_element(element, *keys_to_send)
#     perform_action(driver, actions, f"{element} 요소에 키 입력: {keys_to_send}")


# # find_visible_elements
# def find_visible_elements(driver, locator, EXPLICIT_WAIT=10):
#     """보이는 요소들을 찾는 함수"""
#     try:
#         elements = WebDriverWait(driver, EXPLICIT_WAIT).until(
#             EC.visibility_of_all_elements_located(locator)
#         )
#         custom_logger.info(f"보이는 요소들 찾음: {locator}")
#         return elements
#     except Exception as e:
#         eh.exception_handler(driver, e, f"보이는 요소들을 찾을 수 없음: {locator}")
#         return []



# # find_clickable_element
# def find_clickable_element(driver, locator, text=""):
#     """클릭 가능한 요소를 찾는 함수"""
#     try:
#         element = WebDriverWait(driver, EXPLICIT_WAIT).until(
#             EC.element_to_be_clickable(locator)
#         )
#         custom_logger.info(f"{text}{locator}(이)가 클릭 가능한 상태입니다. ")
#         return element
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{text}{locator}(이)가 클릭 가능하지 않은 상태입니다.")
#         return None

# # enter_text
# def enter_text(driver, locator, input_text, text=""):
#     """요소에 텍스트를 입력하는 함수"""
#     try:
#         element = find_element(driver, locator, text)
#         if element:
#             element.send_keys(input_text)
#             custom_logger.info(f"{text}{locator}에 '{input_text}' 텍스트를 입력하였습니다.")
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{text}{locator} 요소에 텍스트 입력하지 못했습니다.")

# # clear_text
# def clear_text(driver, locator):
#     """요소의 텍스트를 지우는 함수"""
#     try:
#         element = find_element(driver, locator)
#         if element:
#             element.clear()
#             custom_logger.info(f"{locator} 요소의 텍스트 지우기 성공")
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{locator} 요소의 텍스트 지우기 실패")



# # get_attribute
# def get_attribute(driver, locator, attribute_name):
#     """요소의 속성 값을 가져오는 함수"""
#     try:
#         element = find_element(driver, locator)
#         if element:
#             attribute_value = element.get_attribute(attribute_name)
#             custom_logger.info(f"{locator} 요소에서 '{attribute_name}' 속성 값 '{attribute_value}' 가져오기 성공")
#             return attribute_value
#         return None
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{locator} 요소의 속성 값 가져오기 실패")
#         return None

# # select_option
# def select_option(driver, locator, value):
#     """요소에서 옵션 선택하는 함수"""
#     try:
#         from selenium.webdriver.support.ui import Select
#         element = find_element(driver, locator)
#         if element:
#             select = Select(element)
#             select.select_by_value(value)
#             custom_logger.info(f"{locator} 요소에서 '{value}' 옵션을 선택 완료")
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{locator} 요소에서 옵션 선택 실패")

# # is_element_present
# def is_element_present(driver, locator):
#     """요소 존재 여부 확인"""
#     try:
#         WebDriverWait(driver, EXPLICIT_WAIT).until(
#             EC.presence_of_element_located(locator)
#         )
#         custom_logger.info(f"{locator} 요소가 존재")
#         return True
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{locator} 요소를 찾을 수 없음")
#         return False

# # is_element_visible
# def is_element_visible(driver, locator):
#     """요소 보이는 상태 확인"""
#     try:
#         WebDriverWait(driver, EXPLICIT_WAIT).until(
#             EC.visibility_of_element_located(locator)
#         )
#         custom_logger.info(f"{locator} 요소를 보이는 상태로 찾음")
#         return True
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{locator} 요소가 보이지 않음")
#         return False

# # is_element_enabled
# def is_element_enabled(driver, locator):
#     """요소 활성화 상태 확인"""
#     try:
#         element = find_element(driver, locator)
#         if element:
#             is_enabled = element.is_enabled()
#             custom_logger.info(f"{locator} 요소가 {'활성화' if is_enabled else '비활성화'}")
#             return is_enabled
#         return False
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{locator} 요소 활성화 상태 확인 실패")
#         return False

# # is_element_selected
# def is_element_selected(driver, locator):
#     """요소 선택 상태 확인"""
#     try:
#         element = find_element(driver, locator)
#         if element:
#             is_selected = element.is_selected()
#             custom_logger.info(f"{locator} 요소가 {'선택' if is_selected else '선택되지 않음'}")
#             return is_selected
#         return False
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{locator} 요소 선택 상태 확인 실패")
#         return False

# # wait_for_element_to_appear
# def wait_for_element_to_appear(driver, locator, timeout=EXPLICIT_WAIT):
#     """요소가 나타날 때까지 대기"""
#     try:
#         WebDriverWait(driver, timeout).until(
#             EC.visibility_of_element_located(locator)
#         )
#         custom_logger.info(f"{locator} 요소가 나타날 때까지 기다렸습니다.")
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{locator} 요소가 {timeout}초 후에도 나타나지 않았습니다.")

# # wait_for_element_to_disappear
# def wait_for_element_to_disappear(driver, locator):
#     """요소가 사라질 때까지 대기"""
#     try:
#         WebDriverWait(driver, EXPLICIT_WAIT).until(
#             EC.invisibility_of_element_located(locator)
#         )
#         custom_logger.info(f"{locator} 요소가 사라질 때까지 기다리기")
#     except Exception as e:
#         eh.exception_handler(driver, e, f"{locator} 요소가 {EXPLICIT_WAIT}초 후에도 사라지지 않음")

# # wait_until_element_is_enabled
# def wait_until_element_is_enabled(driver, element):
#     """요소가 활성화될 때까지 대기"""
#     try:
#         WebDriverWait(driver, EXPLICIT_WAIT).until(EC.element_to_be_clickable(element))
#         custom_logger.info(f"{element} 활성화될 때까지 대기")
#     except Exception as e:
#         eh.exception_handler(driver, e, f"대기 실패")

# # handle_alert
# def handle_alert(driver, action="accept"):
#     """경고창 처리"""
#     try:
#         alert = WebDriverWait(driver, EXPLICIT_WAIT).until(EC.alert_is_present())
#         if action == "accept":
#             alert.accept()
#             custom_logger.info("경고창 확인 버튼을 클릭했습니다.")
#         elif action == "dismiss":
#             alert.dismiss()
#             custom_logger.info("경고창 취소 버튼을 클릭했습니다.")
#         else:
#             custom_logger.error(f"올바르지 않은 action 값: {action}. 'accept' 또는 'dismiss'만 허용됩니다.")
#     except Exception as e:
#         eh.exception_handler(driver, e, "경고창 처리 중 예외 발생")
