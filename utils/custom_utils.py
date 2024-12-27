
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.custom_logger import custom_logger
from selenium.webdriver.remote.webelement import WebElement
from utils import exception_handler as eh
from config.config import EXPLICIT_WAIT, EXPLICIT_WAIT
from selenium.common.exceptions import StaleElementReferenceException
import random, time


# unpack_by_locator
def _unpack_by_locator(*args):
    """by와 locator를 unpacking하는 함수 *args: by, locator 또는 (by, locator) 형태의 인자"""
    if len(args) == 1:
        return args[0] if isinstance(args[0], tuple) else (args[0], None)
    elif len(args) == 2:
        return args
    else:
        raise TypeError("_unpack_by_locator() 함수는 1개 또는 2개의 인자를 받습니다.")
    

# get_element_info
def get_element_info(element):
    """WebElement 객체의 정보를 딕셔너리로 반환하는 함수"""
    return {
        "tag_name": element.tag_name,
        "id": element.get_attribute('id'),
        "class": element.get_attribute('class')
}


# find_element
def find_element(driver, by, locator, text=""):
    """요소를 찾는 단일함수"""
    try:
        element = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_element_located((by, locator))  # by와 locator를 튜플로 묶어서 전달
        )
        custom_logger.info(f"{text} {by}: {locator}(을)를 찾았습니다.")  # by 정보 추가
        return element
    except Exception as e:
        eh.exception_handler(driver, e, f"{text} {by}: {locator}(을)를 찾지못했습니다.")  # by 정보 추가
        return None


# find_elements
def find_elements(driver, by, locator, text=""):
    """요소들을 찾는 단일함수"""
    try:
        elements = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_all_elements_located((by, locator))
        )
        custom_logger.info(f"{text} {locator}들을 {len(elements)}개 찾았습니다.")
        return elements
    except Exception as e:
        eh.exception_handler(driver, e, f"{text} {locator}들을 찾지못했습니다.")
        return []


# find_visible_element
def find_visible_element(driver, by, locator, text=""):
    """
    1. visibility_of_element_located로 화면에 보이는 요소 찾기
    2. 요소가 화면에 보이지 않으면 move_to_element을 사용하여 포커싱
    """
    try:
        element = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.visibility_of_element_located((by, locator))  # 요소가 존재하는지 확인
        )
        # 요소가 화면에 보이지 않으면 스크롤하여 포커싱
        if not element.is_displayed():
            move_to_element(driver, locator, text)
            custom_logger.info(f"{text}{locator}(이)가 화면에 보이지 않아 스크롤하여 포커싱했습니다.")

        custom_logger.info(f"{text}{locator}(이)가 화면에 보입니다.")
        return element
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}{locator}(이)가 화면에 보이지 않습니다.")
        return None


# find_clickable_element
def find_clickable_element(driver, by, locator, text=""):
    """클릭 가능한 요소를 찾는 단일함수"""
    try:
        element = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.element_to_be_clickable((by, locator))
        )
        custom_logger.info(f"{text} {locator}(이)가 클릭가능한 상태입니다. ")
        return element
    except Exception as e:
        eh.exception_handler(driver, e, f"{text} {locator}(이)가 클릭가능하지 않은 상태입니다.")
        return None
   

# move_to_element
def move_to_element(driver, by, locator, text=""):
    """
    1. find_element 함수로 요소찾기
    2. move_to_element 함수로 요소로 마우스 이동
    """
    try:
        element = find_element(driver, by, locator, text)
        if element:
            actions = ActionChains(driver)
            actions.pause(1)  # 1초 멈춤
            actions.move_to_element(element).perform()  # WebElement 객체 전달
            custom_logger.info(f"{text} {locator}로 마우스를 이동했습니다.")
        else:
            custom_logger.error(f"{text} {locator}를 찾을 수 없어 마우스를 이동하지 못했습니다.")
    except Exception as e:
        eh.exception_handler(driver, e, f"{text} {locator}로 마우스를 이동하지 못했습니다.")


# clickable_link_click
def clickable_link_click(driver, by, locator, text=""):
    """
    1. find_clickable_element 함수로 클릭가능한 요소찾기
    2. click.perform 을 사용하여 요소를 클릭
    """
    try:
        element = find_clickable_element(driver, by, locator, text)
        if element:
            element_info = get_element_info(element)
            actions = ActionChains(driver)
            actions.move_to_element(element).click().perform() 
            custom_logger.info(f"{text} {element_info}(을)를 클릭하였습니다.")
    except Exception as e:
        custom_logger.error(f"{text} {element_info}(을)를 클릭 실패하였습니다. {e}")
        raise e


def page_redirect_confirm(driver, by, locator, text=""):
    """
    1. find_element 함수로 요소찾기 또는 element 직접 전달
    2. 요소에 href, src, data-gtm-click-url 속성 값이 있을 경우, 아닌 경우 분기
    3. 특정 요소 클릭 후 리다이렉션 확인
    4. 리다이렉션 후 요소가 사라지는 경우 StaleElementReferenceException 처리
    """
    try:
        # element 직접 전달
        if isinstance(locator, WebElement):
            element = locator
        # by, locator 전달
        else:
            element = find_element(driver, by, locator, text)

        if element:
            expected_url = None
            try:
                # data-gtm-click-url, src, href 순으로 속성 존재 여부 확인
                if "data-gtm-click-url" in element.get_property("attributes"):
                    expected_url = element.get_attribute("data-gtm-click-url")
                elif "src" in element.get_property("attributes"):
                    expected_url = element.get_attribute("src")
                elif "href" in element.get_property("attributes"):
                    expected_url = element.get_attribute("href")

            except StaleElementReferenceException:
                custom_logger.warning(f"{text} 요소가 리다이렉션 후 사라졌습니다. URL 변경 확인을 계속합니다.")

                # 현재 URL 가져오기
                current_url = driver.current_url
                custom_logger.info(f"{text} 페이지 리다이렉션 확인 URL: {current_url}")
                return True  # 리다이렉션 확인 후 함수 종료

            if expected_url:
                # 예상 URL이 있을 경우 로그 출력
                custom_logger.info(f"클릭한 요소 안의 URL: {expected_url}")

                try:
                    # expected_url이 있을 경우 URL 변경이 일어날 때까지 대기
                    WebDriverWait(driver, EXPLICIT_WAIT).until(EC.url_to_be(expected_url))

                    # 현재 URL 가져오기
                    current_url = driver.current_url

                    # URL 비교
                    if current_url == expected_url:
                        custom_logger.info(f"{text} 페이지 리다이렉션 성공하였습니다. URL: {current_url}")
                        return True
                    else:
                        custom_logger.warning(f"{text} 페이지 리다이렉션 실패하였습니다. 예상 URL({expected_url})와 현재 URL({current_url}) 불일치 발생")
                        return False

                except StaleElementReferenceException:
                    # StaleElementReferenceException 발생 시 예외 처리
                    custom_logger.warning(f"{text} 요소가 리다이렉션 후 사라졌습니다. URL 변경 확인을 계속합니다.")

        # 클릭한 요소의 expected_url이 없거나 element를 찾지 못한 경우 URL 변경이 일어날 때까지 대기
        WebDriverWait(driver, EXPLICIT_WAIT).until(EC.url_changes(driver.current_url))

        current_url = driver.current_url
        custom_logger.info(f"{text} 페이지 리다이렉션 확인 URL: {current_url}")
        return True

    except Exception as e:
        eh.exception_handler(driver, e, "리다이렉션 시간초과")
        raise e


# get_attribute 속성 값 가져오기
def get_attribute(driver, by, locator, attribute_name, text=""):
    """요소의 속성 값을 가져오는 함수"""
    try:
        element = find_element(driver, by, locator, text) 
        if element:
            value = element.get_attribute(attribute_name) 
            if value:
                return value
            else:
                custom_logger.info(f"{element} 요소에 '{attribute_name}' 속성이 없습니다.")
                return None
        else:
            custom_logger.error(f"{locator} 요소를 찾을 수 없습니다.")
            return None
    except Exception as e:
        eh.exception_handler(driver, e, f"{locator} 요소의 '{attribute_name}' 속성 가져오기 실패")
        return None


# enter_text
def enter_text(driver, by, locator, input_text, text=""):
    """요소에 텍스트를 입력하는 함수"""
    try:
        element = find_element(driver, by, locator, text)
        if element:
            # tag_name은 input 또는 textarea인 경우에만 텍스트 입력
            if element.tag_name in ["input", "textarea"]:  
                element.send_keys(input_text)
                custom_logger.info(f"{text} {locator}에 '{input_text}' 텍스트를 입력하였습니다.")
            else:
                custom_logger.error(f"{text} {locator}는 텍스트를 입력할 수 있는 요소가 아닙니다.")
    except Exception as e:
        eh.exception_handler(driver, e, f"{text} {locator} 요소에 텍스트 입력하지 못했습니다.")


# find_visible_section
def find_visible_sections(driver, by, locators, text=""):
    """각 페이지 주요 섹션 존재 확인"""
    for key, value in locators.items():
        if '_section' in key:
            find_visible_element(driver, by, value, f"{text} {key} 영역")


def show_elements_text(driver, by, locator, attribute, text=""):
    """요소들의 속성 값 또는 텍스트를 출력하는 함수"""
    try:
        elements = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_all_elements_located((by, locator))
        )
        custom_logger.info(f"{text} {locator}들을 {len(elements)}개 찾았습니다.")

        for index, element in enumerate(elements):
            if attribute:
                print_info = element.get_attribute(attribute)
                custom_logger.info(f"{text} {index + 1}번째 {attribute}: {print_info}")
            else:
                custom_logger.info(f"{text} {index + 1}번째 {attribute}: {element.text.strip()}")

    except Exception as e:
        eh.exception_handler(driver, e, f"{text} {locator}들을 찾지못했습니다.")
        return []


# show_elements_list
def show_elements_list(driver, by, locator, attribute, text=""):
    """요소들을 리스트로 출력하는 함수"""
    try:
        elements = find_elements(driver, by, locator, text)
        print_info = []
        for element in elements:
            if attribute.lower() == "text":
                # .text로 텍스트 가져오기 시도
                element_text = element.text.strip().replace("\n", " ")
                if not element_text:
                    # .text로 가져온 텍스트가 비어 있으면 .get_attribute('textContent')로 시도
                    element_text = element.get_attribute('textContent').strip().replace("\n", " ")
                    if not element_text:
                        # textContent도 비어 있으면 innerHTML로 시도
                        element_text = element.get_attribute('innerHTML').strip().replace("\n", " ")
                        custom_logger.info(f"{text} {element.tag_name} 요소에서 .get_attribute('innerHTML')을 사용하여 텍스트 '{element_text}'를 가져왔습니다.")
                    else:
                        custom_logger.info(f"{text} {element.tag_name} 요소에서 .get_attribute('textContent')을 사용하여 텍스트 '{element_text}'를 가져왔습니다.")
                else:
                    custom_logger.info(f"{text} {element.tag_name} 요소에서 .text를 사용하여 텍스트 '{element_text}'를 가져왔습니다.")
                info = element_text
            elif attribute:
                info = element.get_attribute(attribute)
            else:
                info = element.text.strip()
            if info:
                print_info.append(info)
        custom_logger.info(f"{text}: {print_info}")
        return print_info
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}를 찾지 못했습니다.")
        return []
    

# 요소들을 찾아 랜덤하게 선택하는 함수
def select_random_item(driver, by, locator, attribute, text=""):
    """
    1. show_elements_list로 요소들 찾기
    2. 요소 text 정보 가져와서 리스트로 출력
    3. 요소들 중 하나를 랜덤하게 선택
    4. return 선택된 요소
    """
    try:
        # show_elements_list를 호출하여 요소 리스트와 텍스트 가져오기
        elements_text = show_elements_list(driver, by, locator, attribute, text)

        if elements_text:
            custom_logger.info(f"리스트 목록 {elements_text}")

            # 랜덤하게 요소 한 개 선택
            random_element_text = random.choice(elements_text)

            custom_logger.info(f"{text} {random_element_text}(을)를 선택하였습니다.")
            
            # 선택된 텍스트에 해당하는 요소 찾기
            elements = find_elements(driver, by, locator, text)
            for element in elements:
                if element.text.strip() == random_element_text or element.get_attribute('textContent').strip() == random_element_text:
                    return element, random_element_text

        return None, None
    except Exception as e:
        eh.exception_handler(driver, e, f"{text} {locator}(을)를 랜덤하게 요소 선택하지 못했습니다.")
        return None, None


# click
def click(driver, element, text=""):
    """요소를 클릭하는 단일함수"""
    try:
        # 요소가 클릭 가능할 때까지 기다린 후 클릭
        WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(element)
            ).click()

        custom_logger.info(f"{text}(을)를 클릭하였습니다.")
        return True
    except Exception as e:
        eh.exception_handler(driver, e, f"{text}(을)를 클릭 실패하였습니다.")
        return False


# get_text
def get_text(driver, by, locator, text=""):
    """요소의 텍스트를 가져오는 함수"""
    try:
        element = find_element(driver, by, locator, text)  # find_element를 사용하여 element 찾기
        if element:
            if element.tag_name == 'input':
                # input 요소인 경우 value 속성 값을 가져옵니다.
                element_text = element.get_attribute('value')
                custom_logger.info(f"{text} {element.tag_name} 요소에서 value 속성값 '{element_text}' 가져오기 성공")
            elif element.tag_name == 'img':
                # 이미지인 경우 alt 속성 값을 가져옵니다.
                element_text = element.get_attribute('alt')
                custom_logger.info(f"{text} {element.tag_name} 요소에서 alt 속성값 '{element_text}' 가져오기 성공")
            elif element.tag_name == 'a':
                # a 요소인 경우 data-gtm-click-text 속성 값을 가져옵니다.
                element_text = element.get_attribute('data-gtm-click-text')
                custom_logger.info(f"{text} {element.tag_name} 요소에서 data-gtm-click-text 속성값 '{element_text}' 가져오기 성공")
            else:
                # .text로 텍스트 가져오기 시도
                element_text = element.text.strip().replace("\n", " ")
                if not element_text:
                    # .text로 가져온 텍스트가 비어 있으면 .get_attribute('textContent')로 시도
                    element_text = element.get_attribute('textContent').strip().replace("\n", " ")
                    if not element_text:
                        # textContent도 비어 있으면 innerHTML로 시도
                        element_text = element.get_attribute('innerHTML').strip().replace("\n", " ")
                        custom_logger.info(f"{text} {element.tag_name} 요소에서 .get_attribute('innerHTML')을 사용하여 텍스트 '{element_text}'를 가져왔습니다.")
                    else:
                        custom_logger.info(f"{text} {element.tag_name} 요소에서 .get_attribute('textContent')을 사용하여 텍스트 '{element_text}'를 가져왔습니다.")
                else:
                    custom_logger.info(f"{text} {element.tag_name} 요소에서 .text를 사용하여 텍스트 '{element_text}'를 가져왔습니다.")
            return element_text
        return None
    except Exception as e:
        eh.exception_handler(driver, e, f"{locator} 요소의 텍스트 가져오기 실패하였습니다.")
        return None


# check_active
def check_active(driver, by, locator, condition, text=""):
    """활성화 상태(active, show, collapse 클래스 등)인지 확인하는 함수"""
    try:
        element = find_visible_element(driver, by, locator, text)
        if element:
            move_to_element(driver, element, text)  # by, locator 제거
            class_name = element.get_attribute("class")

            # 조건에 맞는 클래스가 포함되어 있는지 확인
            if condition in class_name:
                custom_logger.info(f"{text}(이)가 활성화 상태입니다.")
                return True
            else:
                return False
        else:
            return False  # 요소를 찾지 못한 경우

    except Exception as e:
        eh.exception_handler(driver, e, f"{text}(이)가 활성화 상태인지 확인하지 못했습니다.")
        return False
    

# compare_values
def compare_values(*values):
    """여러 값을 비교하여 일치 여부를 확인하고 결과를 로그로 출력하는 함수"""
    if len(values) < 3:  # 최소 2개의 비교값과 1개의 text가 필요
        custom_logger.warning("비교할 값이 충분하지 않습니다. 최소 2개의 값과 1개의 텍스트가 필요합니다.")
        return False

    *comparison_values, text = values  # 마지막 값을 text로 분리
    
    if len(comparison_values) < 2:
        custom_logger.warning(f"{text} 비교할 값이 충분하지 않습니다. 최소 2개의 값이 필요합니다.")
        return False

    reference_value = comparison_values[0]
    all_match = True

    for i, value in enumerate(comparison_values[1:], 1):
        if reference_value in value:
            custom_logger.info(f"{text} 기준값: {reference_value}(와)과 비교값{i}: {value}(이)가 일치합니다.")
        else:
            custom_logger.info(f"{text} 기준값: {reference_value}(와)과 비교값{i}: {value}(이)가 일치하지 않습니다.")
            all_match = False
    
    if all_match:
        custom_logger.info(f"{text} 모든 데이터가 일치합니다.")
    else:
        custom_logger.info(f"{text} 일부 또는 모든 데이터가 불일치합니다.")
    
    return all_match


# navigate_slides
def navigate_slides(driver, by_type, locators, text=""):
    def find_and_click(button_locator):
        button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((by_type, locators[button_locator]))
        )
        custom_logger.info(f"{text} {button_locator} 클릭")
        button.click()

    button_count = len(WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((by_type, locators['slide']))
    ))
    
    # 버튼 클릭 방향 설정
    for direction, limit in [("next", button_count-1), ("previous", 0)]:
        while True:
            active_slide = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by_type, locators['active_slide']))
            )
            current_index = int(active_slide.get_attribute('data-index'))
            visual_text = active_slide.find_element(by_type, locators['banner_text']).get_attribute('alt')
            
            if current_index == 0:
                custom_logger.info(f"{text} 첫 슬라이드입니다. alt: {visual_text}")
            elif current_index == button_count - 1:
                custom_logger.info(f"{text} 마지막 슬라이드입니다. alt: {visual_text}")
            else:
                custom_logger.info(f"{text} 슬라이드_{current_index+1} alt: {visual_text}")
            
            if current_index == limit:
                break
            
            if direction == "previous":
                find_and_click('prev_button')
            elif direction == "next":
                find_and_click('next_button')
            
            time.sleep(2)
        time.sleep(2)


# release
def release(driver, element, text=""):
    """마우스 버튼 놓기"""
    try:
        actions = ActionChains(driver)
        actions.release(element)
        actions.perform()
        custom_logger.info(f"{text} 요소에서 마우스 버튼을 놓았습니다.")
    except Exception as e:
        custom_logger.error(f"{text} 요소에서 마우스 버튼 놓기 실패: {str(e)}")


# select_random_option
def select_random_option(driver, by, area_txt_locator, dropdowns_locator, text=""):
    """
    dropbox 요소에서 랜덤하게 옵션 선택
    """
    try:
        # 영역명/ 드롭박스 요소들 찾기
        area_txts = find_elements(driver, by, area_txt_locator, f"{text} 영역명")
        dropdowns = find_elements(driver, by, dropdowns_locator, f"{text} 드롭박스")
        for area_txt, dropdown in zip(area_txts, dropdowns):
            try:
                # 드롭박스 열기 <- 나중에 공통변수로 빼기
                select_button = dropdown.find_element(By.CSS_SELECTOR, "a.select-btn")
                select_button.click()
                time.sleep(1)

                # 옵션 목록 찾기 <- 나중에 공통변수로 빼기
                options = dropdown.find_elements(By.CSS_SELECTOR, "ul li a")

                # 랜덤 옵션 선택
                random_option = random.choice(options)
                random_option_text = random_option.text
                random_option.click()

                custom_logger.info(f"{text} {area_txt.text}: {random_option_text} 드롭박스 옵션 선택을 하였습니다.")
                time.sleep(2)

            except Exception as e:
                eh.exception_handler(driver, e, f"{text} {area_txt.text} 드롭박스 옵션 선택을 실패하였습니다.")

    except Exception as e:
        eh.exception_handler(driver, e, f"{text} 드롭박스 요소 찾기에 실패하였습니다.")


# total price calculation
def total_price_calculation(driver, by, locator, text=""):
    """총 금액 요소에서 할인 금액을 추출하고 합계를 계산하는 함수"""
    total_sum = 0
    try:
        for total_price_txt in find_elements(driver, by, locator, text):
            for discount_span in total_price_txt.find_elements(By.CSS_SELECTOR, "span.discount-price"):
                discount_text = ''.join(filter(str.isdigit, discount_span.text))
                try:
                    total_sum += int(discount_text)  # int로 변환
                except ValueError:
                    custom_logger.warning(f"할인 금액을 숫자로 변환할 수 없습니다: {discount_text}")
        custom_logger.info(f"{text} 할인 금액 합계: {total_sum}")
        return total_sum
    except Exception as e:
        eh.exception_handler(driver, e, f"{text} 요소에서 할인 금액 추출 실패")
        return 0


# switch_to_new_window
def switch_to_new_window(driver):
  """새로운 윈도우로 전환하는 함수"""
  try:
    # 현재 윈도우 핸들 저장
    current_window = driver.current_window_handle

    # 모든 윈도우 핸들 가져오기
    all_windows = driver.window_handles

    # 새로운 윈도우 핸들 찾기
    new_window = next((window for window in all_windows if window != current_window), None)
    if new_window is None:
      raise ValueError("새로운 윈도우를 찾을 수 없습니다.")

    # 새로운 윈도우로 전환
    driver.switch_to.window(new_window)
    custom_logger.info("새로운 윈도우로 전환했습니다.")

  except Exception as e:
    eh.exception_handler(driver, e, "윈도우 전환 실패")


# 임시 한번에 처리하도록 변경하기
def click_element(driver, by, locator, text=""):
    """
    요소를 클릭하는 함수(임시)
    """
    try:
        element = driver.find_element(by, locator)
        # ActionChains로 마우스 이동 후 클릭
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()

        # 클릭 후 로그
        custom_logger.info(f"{text} {locator} 클릭 성공")

    except Exception as e:
        custom_logger.error(f"{text} {locator} 클릭 실패. 오류: {e}")
        raise e
    

# 헤더 정보 출력
def print_sidebar_menu_info(driver, cards_locator, text=""):
    """
    사이드바 메뉴 정보를 출력하는 함수

    Args:
        driver: WebDriver 객체
        cards_locator: 카드 요소를 찾기 위한 locator
        text: 로그 메시지에 추가할 텍스트
    """
    try:
        cards = driver.find_elements(By.CSS_SELECTOR, cards_locator)

        tab_items = {}
        for card in cards:
            header_link = card.find_element(By.CSS_SELECTOR, "header.card-header a")
            tab_name = header_link.get_attribute("data-gtm-click-text")
            custom_logger.info(f"{text} 사이드바 메뉴: {tab_name}")  # 헤더 정보 출력
            tab_items[tab_name] = []

            tabpanels = card.find_elements(By.CSS_SELECTOR, 'div[role="tabpanel"]')
            if tabpanels:
                for tabpanel in tabpanels:
                    list_items = tabpanel.find_elements(By.CSS_SELECTOR, 'div.card-body ul li a')
                    for item in list_items:
                        item_text = item.get_attribute('innerText').strip()
                        tab_items[tab_name].append(item_text)
                        custom_logger.info(f"{text} {tab_name} | {item_text}")  # 사이드바 내 세부 메뉴 정보 출력
            else:
                custom_logger.info(f"{text} 세부메뉴 없음")

        for tab_name, items in tab_items.items():
            custom_logger.info(f"{text} {tab_name} {items}")

    except Exception as e:
        eh.exception_handler(driver, e, f"{text} 사이드바 메뉴 정보 출력 실패")            


# click_specific_side_menu
def click_specific_side_menu(driver, by, locator, target_text):
    """사이드 메뉴에서 특정 텍스트를 가진 메뉴를 클릭하는 함수"""
    try:
        # 사이드 메뉴 제목 요소들 찾기
        side_title_menus = find_elements(driver, by, locator, "사이드 메뉴 제목")  # 네 번째 인자 수정

        # 각 메뉴의 텍스트 확인 후 클릭
        for menu in side_title_menus:
            menu_text = menu.get_attribute("data-gtm-click-text")
            if menu_text == target_text:
                menu.click()
                custom_logger.info(f"사이드 메뉴 '{target_text}' 클릭")
                return

        # 찾지 못한 경우
        custom_logger.warning(f"사이드 메뉴 '{target_text}'를 찾을 수 없습니다.")

    except Exception as e:
        eh.exception_handler(driver, e, "사이드 메뉴 클릭 실패")

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