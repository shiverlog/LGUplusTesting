from selenium.webdriver.common.action_chains import ActionChains
from utils import custom_logger
from utils import exception_handler as eh

def highlight_element(driver, element):
    """요소를 강조하기 위해 테두리와 배경색을 변경하는 함수"""
    driver.execute_script("""
        arguments[0].style.border = '3px solid red';
        arguments[0].style.backgroundColor = 'rgba(255, 255, 0, 0.5)';
    """, element)

def remove_highlight(driver, element):
    """요소의 스타일을 원래대로 되돌리는 함수"""
    driver.execute_script("""
        arguments[0].style.border = '';
        arguments[0].style.backgroundColor = '';
    """, element)

def highlight_header(driver):
    """헤더 요소를 강조하기 위해 테두리와 배경색을 변경하는 함수"""
    driver.execute_script("""
        const header = document.querySelector('div.header-inner'); // 헤더 요소 선택
        header.style.border = '3px solid red';
        header.style.backgroundColor = 'rgba(255, 255, 0, 0.5)';
    """)

def remove_highlight_header(driver):
    """헤더 요소의 스타일을 원래대로 되돌리는 함수"""
    driver.execute_script("""
        const header = document.querySelector('div.header-inner'); // 헤더 요소 선택
        header.style.border = '';
        header.style.backgroundColor = '';
    """)

def move_to_element(driver, element, text=""):
    """
    요소로 마우스를 이동하고 강조 표시하는 함수

    :param driver: WebDriver 객체
    :param element: WebElement 객체
    :param text: 로그 메시지에 추가할 텍스트 (선택 사항)
    """
    try:
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        highlight_element(driver, element)  # 강조 표시 추가
        custom_logger.info(f"{text} {element}로 마우스를 이동했습니다.")
    except Exception as e:
        eh.exception_handler(driver, e, f"{text} {element}로 마우스를 이동하지 못했습니다.")