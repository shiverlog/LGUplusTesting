import utils.custom_logger as custom_logger

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

# actions.click
def click(self, element):
    try:
        self.click(element).perform()
        custom_logger.info(f"{element} 요소를 클릭")
    except Exception as e:
        custom_logger.error(f"{element.text} 요소 클릭 실패 Error: {e}")

# actions.click_and_hold
def click_and_hold(self, element):
    try:
        super().click_and_hold(element).perform()
        custom_logger.info(f"{element} 요소를 클릭하고 누른 상태를 유지")
    except Exception as e:
        custom_logger.error(f"클릭 및 유지 실패: {e}")

# actions.context_click
def context_click(self, element):
    try:
        super().context_click(element).perform()
        custom_logger.info(f"{element} 요소를 마우스 오른쪽 버튼으로 클릭")
    except Exception as e:
        custom_logger.error(f"마우스 오른쪽 버튼 클릭 실패: {e}")

# actions.double_click
def double_click(self, element):
    try:
        super().double_click(element).perform()
        custom_logger.info(f"{element} 요소를 더블 클릭")
    except Exception as e:
        custom_logger.error(f"더블 클릭 실패: {e}")

# actions.drag_and_drop
def drag_and_drop(self, source, target):
    try:
        super().drag_and_drop(source, target).perform()
        custom_logger.info(f"{source} 요소를 {target} 요소로 드래그 앤 드롭")
    except Exception as e:
        custom_logger.error(f"드래그 앤 드롭 실패: {e}")

# actions.drag_and_drop_by_offset
def drag_and_drop_by_offset(self, source, xoffset, yoffset):
    try:
        super().drag_and_drop_by_offset(source, xoffset, yoffset).perform()
        custom_logger.info(f"{source} 요소를 ({xoffset}, {yoffset}) 만큼 드래그 앤 드롭")
    except Exception as e:
        custom_logger.error(f"드래그 앤 드롭 실패: {e}")

# actions.key_down
def key_down(self, value, element=None):
    try:
        super().key_down(value, element).perform()
        custom_logger.info(f"{element} 요소에 키 누름: {value}")
    except Exception as e:
        custom_logger.error(f"키 누름 실패: {e}")

# actions.key_up
def key_up(self, value, element=None):
    try:
        super().key_up(value, element).perform()
        custom_logger.info(f"{element} 요소에 키 놓음: {value}")
    except Exception as e:
        custom_logger.error(f"키 놓음 실패: {e}")

# actions.move_by_offset
def move_by_offset(self, xoffset, yoffset):
    try:
        super().move_by_offset(xoffset, yoffset).perform()
        custom_logger.info(f"마우스를 ({xoffset}, {yoffset}) 만큼 이동")
    except Exception as e:
        custom_logger.error(f"마우스 이동 실패: {e}")

# actions.move_to_element
def move_to_element(self, element):
    try:
        super().move_to_element(element).perform()
        custom_logger.info(f"{element} 요소로 마우스를 이동")
    except Exception as e:
        custom_logger.error(f"마우스 이동 실패: {e}")

# actions.move_to_element_with_offset
def move_to_element_with_offset(self, to_element, xoffset, yoffset):
    try:
        super().move_to_element_with_offset(to_element, xoffset, yoffset).perform()
        custom_logger.info(f"{to_element} 요소에서 ({xoffset}, {yoffset}) 만큼 떨어진 곳으로 마우스를 이동")
    except Exception as e:
        custom_logger.error(f"마우스 이동 실패: {e}")

# actions.pause
def pause(self, seconds):
    try:
        super().pause(seconds).perform()
        custom_logger.info(f"{seconds}초 동안 일시중지")
    except Exception as e:
        custom_logger.error(f"일시중지 실패: {e}")

# actions.perform
def perform(self):
    try:
        super().perform()
        custom_logger.info("액션 체인을 실행")
    except Exception as e:
        custom_logger.error(f"액션 체인 실행 실패: {e}")

# actions.release
def release(self, on_element=None):
    try:
        super().release(on_element).perform()
        custom_logger.info(f"{on_element} 요소에서 마우스 버튼 놓기")
    except Exception as e:
        custom_logger.error(f"마우스 버튼 놓기 실패: {e}")

# actions.reset_actions
def reset_actions(self):
    try:
        super().reset_actions()
        custom_logger.info("액션 체인을 초기화")
    except Exception as e:
        custom_logger.error(f"액션 체인 초기화 실패: {e}")

# actions.send_keys
def send_keys(self, *keys_to_send):
    try:
        super().send_keys(*keys_to_send).perform()
        custom_logger.info(f"키 입력: {keys_to_send}")
    except Exception as e:
        custom_logger.error(f"키 입력 실패: {e}")

# actions.send_keys_to_element
def send_keys_to_element(self, element, *keys_to_send):
    try:
        super().send_keys_to_element(element, *keys_to_send).perform()
        custom_logger.info(f"{element} 요소에 키 입력: {keys_to_send}")
    except Exception as e:
        custom_logger.error(f"키 입력 실패: {e}")
