from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
    class CustomActionChains: ActionChains 매소드를 사용하여 다양한 동작을 수행할 수 있는 함수들을 정의한 파일
"""
class CustomActionChains(ActionChains):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    
    # 요소클릭
    def click(self, element):
        try:
            # ActionChains.click() 메소드를 사용하여 요소를 클릭
            self.click(element).perform()
            print(f"{element}")
        except Exception as e:
            print(f"{element.text} 클릭이 실패되었습니다. Error: {e}")

    # 요소안 text 가져오기
    def get_text(self, element):
        try:
            # ActionChains.click() 메소드를 사용하여 요소를 클릭
            text = element.text
            print(f"{text}")
            return text
        except Exception as e:
            print(f"텍스트가져오기실패 Error: {e}")
    
    # 요소에 키보드 입력

    # 요소에 마우스 오버
    
    # 대기 시간 설정 
    # 요소가 활성화 될 때까지 대기
    def wait_until_element_is_enabled(self, element, timeout=10):
        try:
            # WebDriverWait를 사용하여 요소가 활성화 될 때까지 대기
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
            print(f"{element} 활성화될때까지 대기")
        except Exception as e:
            print(f"대기실패 Error: {e}")

    # Function to Scroll to a specific element
    def scroll_to_element(driver, element):
        try:
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            print(f"Scrolled to element: {element}")
        except Exception as e:
            print(f"Scroll failed - Error: {e}")


    # Function to Scroll to the bottom of the page
    def scroll_to_bottom(driver):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Scrolled to the bottom of the page.")
        except Exception as e:
            print(f"Scroll to bottom failed - Error: {e}")


    # Function to Scroll by a specific amount of pixels
    def scroll_by_amount(driver, x, y):
        try:
            driver.execute_script(f"window.scrollBy({x}, {y});")
            print(f"Scrolled by ({x}, {y}) pixels.")
        except Exception as e:
            print(f"Scroll by amount failed - Error: {e}")


    # Function to take a Screenshot
    def save_screenshot(driver, file_path):
        try:
            driver.save_screenshot(file_path)
            print(f"Screenshot saved: {file_path}")
        except Exception as e:
            print(f"Screenshot save failed - Error: {e}")


    # Function to handle Pop-up alerts
    def handle_alert(driver, action="accept"):
        try:
            alert = driver.switch_to.alert
            if action == "accept":
                alert.accept()
                print("Alert accepted.")
            else:
                alert.dismiss()
                print("Alert dismissed.")
        except Exception as e:
            print(f"Alert handling failed - Error: {e}")


    # Function to validate text of an element
    def validate_element_text(element, expected_text):
        actual_text = element.text
        if actual_text == expected_text:
            print(f"Text matches: {actual_text}")
        else:
            print(f"Text mismatch - Expected: {expected_text}, Found: {actual_text}")


    # Function to perform keyboard actions
    def send_keys_to_element(element, keys):
        try:
            element.send_keys(keys)
            print(f"Keys sent: {keys}")
        except Exception as e:
            print(f"Sending keys failed - Error: {e}")