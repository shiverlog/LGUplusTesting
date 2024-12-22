from selenium.webdriver.common.action_chains import ActionChains
from utils import custom_logger as cl

"""
    # 커스텀 함수 목록
    actions.click: 요소 클릭
    actions.click_and_hold: 요소 클릭 후 누른 상태 유지
    actions.context_click: 요소에서 마우스 오른쪽 버튼 클릭
    actions.double_click: 요소 더블 클릭
    actions.drag_and_drop(source, target): source에서 target으로 드래그 앤 드롭
    actions.drag_and_drop_by_offset(source, xoffset, yoffset): source에서 x, y offset만큼 드래그 앤 드롭
    actions.key_down: 키 누름
    actions.key_up: 키 놓음
    actions.move_by_offset(xoffset, yoffset): 현재 위치에서 x, y offset만큼 마우스 이동
    actions.move_to_element(to_element): 요소로 마우스 이동
    actions.move_to_element_with_offset(to_element, xoffset, yoffset): 요소에서 x, y offset만큼 떨어진 곳으로 마우스 이동
    actions.pause(seconds): 지정된 시간 동안 일시 중지
    actions.perform(): 액션 체인 실행
    actions.release: 마우스 버튼 놓음
    actions.reset_actions(): 액션 체인 초기화
    actions.send_keys(*keys_to_send): 현재 포커스된 요소에 키 입력
    actions.send_keys_to_element(element, *keys_to_send): 지정된 요소에 키 입력
"""
custom_logger = cl.custom_logger

def perform_action(driver, action_chain, description):
    """액션 체인을 실행하는 함수"""
    try:
        action_chain.perform()
        custom_logger.info(f"{description} 성공")
    except Exception as e:
        custom_logger.error(f"{description} 실패: {e}")

def click(driver, element):
    """요소를 클릭하는 함수"""
    actions = ActionChains(driver).click(element)
    perform_action(driver, actions, f"{element} 요소 클릭")

def click_and_hold(driver, element):
    """요소를 클릭하고 누른 상태를 유지하는 함수"""
    actions = ActionChains(driver).click_and_hold(element)
    perform_action(driver, actions, f"{element} 요소 클릭 및 유지")

def context_click(driver, element):
    """요소를 마우스 오른쪽 버튼으로 클릭하는 함수"""
    actions = ActionChains(driver).context_click(element)
    perform_action(driver, actions, f"{element} 요소에서 마우스 오른쪽 버튼 클릭")

def double_click(driver, element):
    """요소를 더블 클릭하는 함수"""
    actions = ActionChains(driver).double_click(element)
    perform_action(driver, actions, f"{element} 요소 더블 클릭")

def drag_and_drop(driver, source, target):
    """source 요소를 target 요소로 드래그 앤 드롭"""
    actions = ActionChains(driver).drag_and_drop(source, target)
    perform_action(driver, actions, f"{source} 요소를 {target}로 드래그 앤 드롭")

def drag_and_drop_by_offset(driver, source, xoffset, yoffset):
    """source 요소를 offset으로 드래그 앤 드롭"""
    actions = ActionChains(driver).drag_and_drop_by_offset(source, xoffset, yoffset)
    perform_action(driver, actions, f"{source} 요소를 ({xoffset}, {yoffset})만큼 드래그 앤 드롭")

def move_to_element(driver, element):
    """요소로 마우스를 이동"""
    actions = ActionChains(driver).move_to_element(element)
    perform_action(driver, actions, f"{element} 요소로 마우스 이동")

def move_to_element_with_offset(driver, element, xoffset, yoffset):
    """요소에서 특정 오프셋만큼 마우스를 이동"""
    actions = ActionChains(driver).move_to_element_with_offset(element, xoffset, yoffset)
    perform_action(driver, actions, f"{element} 요소에서 ({xoffset}, {yoffset}) 만큼 떨어진 곳으로 마우스 이동")

def key_down(driver, value, element=None):
    """키를 누르는 함수"""
    actions = ActionChains(driver).key_down(value, element)
    perform_action(driver, actions, f"{element} 요소에 키 누름: {value}")

def key_up(driver, value, element=None):
    """키를 놓는 함수"""
    actions = ActionChains(driver).key_up(value, element)
    perform_action(driver, actions, f"{element} 요소에 키 놓음: {value}")

def move_by_offset(driver, xoffset, yoffset):
    """현재 위치에서 오프셋만큼 마우스를 이동"""
    actions = ActionChains(driver).move_by_offset(xoffset, yoffset)
    perform_action(driver, actions, f"마우스를 ({xoffset}, {yoffset}) 만큼 이동")

def pause(driver, seconds):
    """지정된 시간 동안 일시중지"""
    actions = ActionChains(driver).pause(seconds)
    perform_action(driver, actions, f"{seconds}초 동안 일시중지")

def release(driver, element=None):
    """마우스 버튼 놓기"""
    actions = ActionChains(driver).release(element)
    perform_action(driver, actions, f"{element} 요소에서 마우스 버튼 놓기")

def send_keys(driver, *keys_to_send):
    """현재 포커스된 요소에 키 입력"""
    actions = ActionChains(driver).send_keys(*keys_to_send)
    perform_action(driver, actions, f"키 입력: {keys_to_send}")

def send_keys_to_element(driver, element, *keys_to_send):
    """지정된 요소에 키 입력"""
    actions = ActionChains(driver).send_keys_to_element(element, *keys_to_send)
    perform_action(driver, actions, f"{element} 요소에 키 입력: {keys_to_send}")
