from config import IMPLICIT_WAIT
from utils.exception_handler import handle_exception
from utils.custom_logger import custom_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.custom_actionchains import click

class PageRedirectionHandler:
    """
        페이지 리다이렉션 확인 
        :param a_element: 링크 요소
        :param click_url: 클릭 시 이동할 URL
        :param current_url: 리다이렉션한 페이지 URL
        :param timeout: 대기 시간
        :return: 리다이렉션 성공 여부
    """
    def page_redirection(self, a_element, click_url, current_url, timeout=IMPLICIT_WAIT):
        redirection_handler = PageRedirectionHandler(self, custom_logger)
        try:
            # URL을 가져오기 위해 a_element를 클릭합니다.
            click(a_element)

            # url_contains(url): 현재 URL에 지정된 URL이 포함되어 있는지 확인
            # url_to_be(url): 현재 URL이 지정된 URL과 정확히 일치하는지 확인
            # url_changes(url): 현재 URL이 지정된 URL과 다른지 확인

            # click_url이 현재 URL에 포함될 때까지 대기
            WebDriverWait(self.driver, timeout).until(EC.url_contains(click_url))
            current_url = self.driver.current_url

            # 현재 URL이 click_url을 포함하는지 확인합니다.
            if click_url in current_url:
                custom_logger.info(f"페이지가 정상적으로 리다이렉션되었습니다. URL: {current_url}")
                return True
            else:
                custom_logger.warning(f"페이지 리다이렉션에 문제가 있습니다.")
                custom_logger.warning(f"현재 URL: {current_url}")
                return False

        except Exception as e:
            handle_exception(self, e, redirection_handler, "expected_url_part", a_element, click_url, current_url)