from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import os
import re
import urllib.parse
import random
import inspect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import traceback
import sys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import string
import html


# WebDriver 설정 및 웹 페이지 열기
# driver = webdriver.Firefox()
driver = webdriver.Chrome()
driver.get("https://www.lguplus.com")
driver.implicitly_wait(10)
driver.maximize_window()
driver.execute_script("document.body.style.zoom='90%'")

""" 
    automation.json: JSON 파일에 로그 기록
    class JSONFormatter(logging.Formatter): 로그 레코드를 JSON 형식으로 변환
    class ColoredFormatter(logging.Formatter): 로그 메시지에 색상 추가
    class Logger: 사용자 정의 로거 클래스 
    class NoStacktraceFormatter(logging.Formatter): 예외 스택 트레이스를 로그에 기록하지 않음
"""
class JSONFormatter(logging.Formatter):
    def format(self, record):
        # ANSI 이스케이프 시퀀스 제거
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        message = ansi_escape.sub('', record.msg)

        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": message,
            "pathname": record.pathname,
            "lineno": record.lineno
        }
        return json.dumps(log_record, ensure_ascii=False)

class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[92m",    # 초록색
        "INFO": "\033[94m",     # 파란색
        "WARNING": "\033[93m",  # 노란색
        "ERROR": "\033[91m",    # 빨간색
        "CRITICAL": "\033[1;91m" # 굵은 빨간색
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.msg = f"{color}{record.msg}{self.RESET}"
        return super().format(record)

class NoStacktraceFormatter(logging.Formatter):
    def formatException(self):
        return ''

    def format(self, record):
        record.exc_text = None
        return super().format(record)

class Logger:
    def __init__(self, logger_name="Logger", log_level=logging.DEBUG, log_to_console=True, 
                 log_file='automation.log', json_file='automation.json',
                 max_bytes=5*1024*1024, backup_count=3, when='midnight',
                 fmt='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        self.log_to_console = log_to_console
        self.log_file = log_file
        self.json_file = json_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.when = when
        self.fmt = fmt
        self.datefmt = datefmt
        self._setup_handlers()

    def _setup_handlers(self):
        # 기존 핸들러 제거
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 로그 파일 설정
        log_file = os.path.join(os.getcwd(), self.log_file)
        if self.when:
            file_handler = TimedRotatingFileHandler(log_file, when=self.when, backupCount=self.backup_count, encoding='utf-8')
        else:
            file_handler = RotatingFileHandler(log_file, mode='a', maxBytes=self.max_bytes, backupCount=self.backup_count, encoding='utf-8')
        file_handler.setLevel(self.logger.level)
        file_formatter = NoStacktraceFormatter(self.fmt, datefmt=self.datefmt)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # 콘솔 핸들러 설정
        if self.log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.logger.level)
            console_formatter = ColoredFormatter('%(name)s - %(levelname)s: %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

        # JSON 핸들러 추가
        json_file = os.path.join(os.getcwd(), self.json_file)
        json_handler = logging.FileHandler(json_file, mode='a', encoding='utf-8')
        json_handler.setLevel(self.logger.level)
        json_formatter = JSONFormatter()
        json_handler.setFormatter(json_formatter)
        self.logger.addHandler(json_handler)

    def get_logger(self):
        return self.logger
    
    def log_execution_status(self, func):
        def wrapper(*args, **kwargs):
            self.logger.info(f"{func.__name__} 실행 시작")
            try:
                result = func(*args, **kwargs)
                self.logger.info(f"{func.__name__} 실행 성공")
                return result
            except Exception as e:
                self.logger.error(f"{func.__name__} 실행 중 오류 발생: {str(e)}")
                raise
        return wrapper

# Logger 인스턴스 생성
custom_logger = Logger().get_logger()

"""
    class PageNavigationHandler: 페이지 리다이렉션 확인
        bool: 리다이렉션 성공 여부
"""
class PageNavigationHandler:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def page_redirection(self, expected_url_part, button_element=None, button_url_attribute=None, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(expected_url_part))
            current_url = self.driver.current_url
           
            if button_element and button_url_attribute:
                button_url = button_element.get_attribute(button_url_attribute)
                if button_url == expected_url_part and expected_url_part in current_url:
                    self.logger.info(f"페이지가 정상적으로 리다이렉션되었습니다. URL: {current_url}")
                    return True
                else:
                    self.logger.warning(f"페이지 리다이렉션에 문제가 있습니다.")
                    self.logger.warning(f"현재 URL: {current_url}")
                    self.logger.warning(f"버튼 URL: {button_url}")
                    return False
            else:
                if expected_url_part in current_url:
                    self.logger.info(f"페이지가 정상적으로 리다이렉션되었습니다. URL: {current_url}")
                    return True
                else:
                    self.logger.warning(f"페이지 리다이렉션에 문제가 있습니다.")
                    self.logger.warning(f"현재 URL: {current_url}")
                    return False
        except TimeoutException:
            self.logger.error(f"페이지가 {expected_url_part}로 리다이렉션되지 않았습니다.")
            return False

"""
    class Wait : 페이지 로딩 대기
"""
class CustomWait:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def wait_until(self, condition, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(condition)
            self.logger.info("조건이 충족되었습니다.")
            return True
        except TimeoutException:
            self.logger.error("조건이 충족되지 않았습니다.")
            return False

"""
    class Screenshot: 에러시 스크린샷 저장
"""
class Screenshot:
    def __init__(self, driver, directory="./screenshots"):
        self.driver = driver
        self.directory = directory

        # 스크린샷 저장 디렉토리 생성
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def capture(self, filename=None):
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.directory, filename)
        self.driver.save_screenshot(filepath)
        print(f"스크린샷 저장: {filepath}")


"""
    class ModalHandler: 모달창 처리
"""
class ModalHandler:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def click_buttons(self):
        try:
            while True:
                # 모달창의 확인 버튼이 나타날 때까지 대기
                confirm_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.c-btn-group button.c-btn-solid-1-m'))
                )
                confirm_button.click()  # 확인 버튼 클릭
                self.logger.info("확인 버튼 클릭 완료")

                # 모달창이 닫히기를 기다림
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div.modal-dialog'))
                )
                self.logger.info("모달창 닫힘 감지 완료")

        except Exception as e:
            self.logger.info(f"더 이상 모달창이 없음: {str(e)}")

"""
    class Wait: 
"""
class CustomWait:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def wait_until(self, condition, timeout = 30):
        try:
            WebDriverWait(self.driver, timeout).until(condition)
            self.logger.info("조건이 충족됨")
            return True
        except TimeoutException:
            self.logger.error("조건이 충족되지 않음")
            return False
"""
    class click: 요소 클릭
"""
class Click:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def click(self, element):
        try:
            element.click()
            self.logger.info("요소 클릭 완료")
        except Exception as e:
            self.logger.error(f"요소 클릭 실패: {str(e)}")
            self.logger.error(traceback.format_exc())

"""
    class UPlusLogin: 로그인 되지 않아, https://www.lguplus.com/login 페이지로 리다이렉션 될 시
"""
class UPlusLogin:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def login(self):
        try:
            # 1. "U+ID" 버튼 클릭
            uplus_id_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'section.new-mem-section ul.iconLoginList li:nth-of-type(4) button'))
            )
            uplus_id_button.click()
            time.sleep(2)

            # 2. 버튼 클릭 후 /login/onid-login 페이지로 리다이렉션 확인
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/login/onid-login")
            )
            Uplus_login_url = self.driver.current_url

            # /login/onid-login 해당 url로 이동하는지 확인
            if "/login/onid-login" in Uplus_login_url:
                self.logger.info(f"U+ 로그인 페이지로 이동 URL: {Uplus_login_url}")
            else:
                self.logger.info(f"U+ 로그인 페이지로 이동 실패 URL: {Uplus_login_url}")

            # 3. ID 및 비밀번호 입력 (sysdm.cpl 환경변수 사용)
            uplus_id = os.getenv('UPLUS_ID')
            uplus_pw = os.getenv('UPLUS_PW')

            id_input = self.driver.find_element(By.ID, "username-1-6")
            id_input.send_keys(uplus_id)
            pw_input = self.driver.find_element(By.ID, "password-1")
            pw_input.send_keys(uplus_pw)
            time.sleep(5)

            # 4. U+ID 로그인 버튼 클릭
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'button.c-btn-solid-1.nm-login-btn')
            login_button.click()
            time.sleep(2)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            self.logger.error(traceback.format_exc())
            traceback.print_stack()

"""
    class TestCase01: ID 및 PW 입력 후 로그인 버튼 클릭
"""
class TestCase01:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.page_navigation = PageNavigationHandler(self.driver, self.logger)

    def execute(self):
        try:
            # 마이메뉴 마우스오버 및 드롭메뉴 활성화 확인
            myinfo = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.header-menu-list-1 > li:last-child"))
            )
            ActionChains(self.driver).move_to_element(myinfo).perform()
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.icon-myInfo-1.is-active, div.myInfo-list.is-show"))
            )
            if self.driver.find_element(By.CSS_SELECTOR, "a.icon-myInfo-1.is-active") and self.driver.find_element(By.CSS_SELECTOR, "div.myInfo-list.is-show"):
                self.logger.info("마이메뉴 마우스오버시 드롭메뉴 활성화 성공")
            else:
                self.logger.info("마이메뉴 드롭메뉴 활성화 실패")

            # 로그인 버튼 클릭 및 페이지 리다이렉션 확인
            login_button = self.driver.find_element(By.CSS_SELECTOR, 'a.btn-my.c-btn-solid-1-m[data-gtm-click-text="로그인"]')
            login_button.click()
            time.sleep(2)

            WebDriverWait(self.driver, 10).until(EC.url_contains("/login"))
            login_url = self.driver.current_url
            login_button_url = login_button.get_attribute("data-gtm-click-url")
            if "login" in login_button_url:
                self.logger.info(f"로그인 페이지로 이동 URL: {login_url}")
            else:
                self.logger.info(f"로그인 페이지로 이동 실패 URL: {login_button_url}")

            # U+ID 버튼 클릭 및 리다이렉션 확인
            uplus_id_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'section.new-mem-section ul.iconLoginList li:nth-of-type(4) button'))
            )
            uplus_id_button.click()
            time.sleep(2)

            WebDriverWait(self.driver, 10).until(EC.url_contains("/login/onid-login"))
            Uplus_login_url = self.driver.current_url
            self.logger.info(f"U+ 로그인 페이지로 이동 URL: {Uplus_login_url}")
            
            # 로그인 정보 입력 및 로그인 버튼 클릭
            uplus_id = os.getenv('UPLUS_ID')
            uplus_pw = os.getenv('UPLUS_PW')
            self.driver.find_element(By.ID, "username-1-6").send_keys(uplus_id)
            self.driver.find_element(By.ID, "password-1").send_keys(uplus_pw)
            time.sleep(2)
            self.logger.info(f"입력한 ID: {uplus_id} 입력한 PW: {uplus_pw}")

            self.driver.find_element(By.CSS_SELECTOR, 'button.c-btn-solid-1.nm-login-btn').click()
            time.sleep(2)

            # 로그인 성공 여부 확인
            self.page_navigation.page_redirection("www.lguplus.com", timeout=10)
            time.sleep(2)
            
            # 사용자 정보 확인
            myinfo = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "header > div.header-gnb-wrap > div.header-inner > ul > li:nth-child(5)"))
            )
            ActionChains(self.driver).move_to_element(myinfo).pause(1).perform()
            login_info_text = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.myInfo-top p.login-info-txt"))
            ).text
            self.logger.info(f"로그인 정보: {login_info_text}")

            # 쿠키 정보 출력
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'LGU_PLUS_PERSISTED_STATE':
                    decoded_value = urllib.parse.unquote(cookie['value'])
                    self.logger.info(f"LGU_PLUS_PERSISTED_STATE 세션 정보: {decoded_value}")
                    break
            time.sleep(2)
        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            self.logger.error(traceback.format_exc())
            traceback.print_stack()

   
'''
    testcase_02: KV 영역 img 개수 확인 및 정상 노출 확인
'''
class TestCase02:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def execute(self):
        try:
            self.check_kv_images()
            self.test_carousel_play_pause()
            self.test_slide_buttons()
            self.test_carousel_navigation()
        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            self.logger.error(traceback.format_exc())
            traceback.print_stack()

    def check_kv_images(self):
        kv_images = self.driver.find_elements(By.CSS_SELECTOR, 'div.swiper-wrapper .swiper-slide img')
        image_count = len(kv_images)
        self.logger.info(f"KV 영역 이미지 개수: {image_count}")
        
        for index, img in enumerate(kv_images):
            img_src = img.get_attribute('src')
            if img_src:
                self.logger.info(f"이미지 {index + 1} src: {img_src}")
            else:
                self.logger.info(f"이미지 {index + 1} src 속성이 없습니다.")

    def test_carousel_play_pause(self):
        carousel_play = self.driver.find_element(By.CLASS_NAME, "bo-1108-controls__play")
        carousel_play.click()
        time.sleep(2)
        
        if "is-pause" in carousel_play.get_attribute("class"):
            self.logger.info("재생버튼 클릭 후 정지버튼으로 변경됨")
        else:
            self.logger.info("정지버튼으로 변경되지 않음")

        carousel_pause = self.driver.find_element(By.CLASS_NAME, "bo-1108-controls__play.is-pause")
        carousel_pause.click()
        time.sleep(2)

    def test_slide_buttons(self):
        carousel_buttons = self.driver.find_elements(By.CSS_SELECTOR, '.swiper-pagination-custom .swiper-pagination-bullet')
        button_count = len(carousel_buttons)
        self.logger.info(f"슬라이드 버튼 갯수: {button_count}")

        for i in range(1, button_count+1):
            button = self.driver.find_element(By.CSS_SELECTOR, f'.swiper-pagination-custom .swiper-pagination-bullet[data-index="{i-1}"]')
            button.click()
            self.logger.info(f"{i}번 슬라이드 버튼 클릭")

            active_bullet = self.driver.find_element(By.CSS_SELECTOR, '.swiper-pagination-custom .swiper-pagination-bullet.swiper-pagination-bullet-active')
            active_index = int(active_bullet.get_attribute('data-index'))
            if active_index == i - 1:
                self.logger.info(f"{i}번 슬라이드 버튼이 활성화")
            else:
                self.logger.info(f"{i}번 슬라이드 버튼이 비활성화/ 현재 활성화된 슬라이드 버튼: {active_index + 1}")
            time.sleep(2)

    def test_carousel_navigation(self):
        carousel_previous = self.driver.find_element(By.CLASS_NAME, "swiper-button-prev")
        carousel_next = self.driver.find_element(By.CLASS_NAME, "swiper-button-next")
        carousel_buttons = self.driver.find_elements(By.CSS_SELECTOR, '.swiper-pagination-custom .swiper-pagination-bullet')
        button_count = len(carousel_buttons)

        for direction, limit in [("previous", 0), ("next", button_count-1)]:
            while True:
                active_bullet = self.driver.find_element(By.CSS_SELECTOR, '.swiper-pagination-custom .swiper-pagination-bullet.swiper-pagination-bullet-active')
                current_index = int(active_bullet.get_attribute('data-index'))
                aria_label = active_bullet.get_attribute('aria-label')
                
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".swiper-slide.bo-1108__slide.swiper-slide-active"))
                )
                active_slide = self.driver.find_element(By.CSS_SELECTOR, '.swiper-slide.bo-1108__slide.swiper-slide-active')
                visual_bg = active_slide.find_element(By.CSS_SELECTOR, '.visual-bg-area img').get_attribute('src')
                visual_area = active_slide.find_element(By.CSS_SELECTOR, '.visual-area .visual-content')
                button_url = visual_area.find_element(By.CSS_SELECTOR, '.c-btn-group a').get_attribute('data-gtm-click-url')
                time.sleep(2)
                self.logger.info(f"현재 {aria_label} Button URL: {button_url} | 배경: {visual_bg}")
                
                if current_index == limit:
                    break
                if direction == "previous":
                    driver.execute_script("arguments[0].click();", carousel_previous)
                elif direction == "next":
                    if current_index < limit:
                        driver.execute_script("arguments[0].click();", carousel_next)
                    else:
                        break

            time.sleep(2) 


"""
    TestCase03: 기기 추천 영역 무작위 기기 선택 후 기기명 데이터 추출, 해당 기기 상세페이지 접속 후 기기명 일치 여부 확인
"""
class TestCase03:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def execute(self):
        try:
            device_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "device-section"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", device_section)
            time.sleep(2)

            tabs = self.driver.find_elements(By.CSS_SELECTOR, '.tab-wrap ul li')
            self.random_tab = random.choice(tabs)
            self.random_tab_text = self.random_tab.text
            self.random_tab.click()

            active_tab = self.driver.find_element(By.CSS_SELECTOR, '.tab-wrap ul li.active a')
            self.logger.info(f"선택한 탭: {self.random_tab_text}")
            self.logger.info(f"활성화된 탭: {active_tab.text}")

        
            if "추천" in self.random_tab_text:
                expected_id = "recomm-tabcon-01"
            elif "삼성" in self.random_tab_text:
                expected_id = "recomm-tabcon-02"
            elif "Apple" in self.random_tab_text:
                expected_id = "recomm-tabcon-03"
            else:
                expected_id = None

            if expected_id:
                self.device_list = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, f'#{expected_id} ul.recomm-device-list li'))
                )
                self.logger.info(f"{self.random_tab_text} 탭의 기기 개수: {len(self.device_list)}")
            else:
                self.logger.info(f"탭 텍스트에 해당하는 클래스가 없습니다: {self.random_tab_text}")
            
            for index, device in enumerate(self.device_list):
                device_thumbnail = device.find_element(By.CSS_SELECTOR, '.device-thumnail img').get_attribute('src')
                device_information = device.find_element(By.CSS_SELECTOR, '.device-infomation p.device-name').text
                self.logger.info(f"기기 {index + 1}: {device_information} 썸네일: {device_thumbnail}")

        
            self.random_device = random.choice(self.device_list)
            self.device_name = self.random_device.find_element(By.CSS_SELECTOR, '.device-name').text
            self.device_url = self.random_device.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            self.random_device.click()
            self.logger.info(f"선택된 기기: {self.device_name}")
            self.logger.info(f"기기 상세 페이지 링크: {self.device_url}")

        
            if "/mobile/device" in self.device_url:
                self.logger.info(f"디바이스 상세 페이지로 이동 URL: {self.device_url}")
            else:
                self.logger.info(f"디바이스 상세 페이지로 이동 실패 URL: {self.device_url}")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.device-info-area'))
            )
            device_detail_name = self.driver.execute_script("return document.querySelector('h2.title-main').textContent.split('(')[0].trim();")
            self.logger.info(f"상세 페이지 기기명: {device_detail_name}")

            if self.device_name in device_detail_name:
                self.logger.info(f"기기명이 일치합니다.: {device_detail_name}")
            else:
                self.logger.info(f"기기명이 일치하지 않습니다. 선택된 기기: {self.device_name}, 상세 페이지 기기: {device_detail_name}")
            time.sleep(5)
        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            self.logger.error(traceback.format_exc())
            traceback.print_stack()

      
"""
     testcase_04: 테마배너 항목 텍스트 정상 노출 확인
"""
class TestCase04:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def execute(self):
        try:
            # 1. 모바일 메뉴 클릭
            mobile_button = self.driver.find_element(By.CSS_SELECTOR, "header > div.header-gnb-wrap > div.header-inner > nav > ul > li.m1")
            mobile_button.click()
            time.sleep(5)

            mobile_url = self.driver.current_url
            if "/mobile" in mobile_url:
                self.logger.info(f"모바일 페이지로 이동 URL: {mobile_url}")
            else:
                self.logger.info(f"모바일 페이지로 이동 실패 URL: {mobile_url}")

            # 2. 테마배너 섹션 포커싱
            kv_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[section-group-id="PcSubMainMobileKVSection"]'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", kv_section)
            time.sleep(2)

            kv_section = self.driver.find_element(By.CSS_SELECTOR, 'div[section-group-id="PcSubMainMobileKVSection"]')
            banners = kv_section.find_elements(By.CSS_SELECTOR, ".visual-wrap a.link_btn")
            banner_list = kv_section.find_elements(By.CSS_SELECTOR, ".slick-list div[data-index]")
            button_count = len(banner_list)
            location = kv_section.get_attribute("location")

            self.logger.info(f"배너 정보: {location}")
            self.logger.info(f"배너 슬라이드 갯수: {button_count}")
        
            # 3. 테마배너 정보 확인
            for index, banner in enumerate(banner_list):
                data_index = banner.get_attribute("data-index")
                slide_page = f"슬라이드 {int(data_index) + 1}페이지"
            
                banner_link = banners[index].get_attribute("data-gtm-click-url")  
                visual_text = banners[index].find_element(By.CSS_SELECTOR, ".visual-text img").get_attribute("alt")
                visual_bg = banners[index].find_element(By.CSS_SELECTOR, ".visual-bg img").get_attribute("src")
                self.logger.info(f"{slide_page}_링크: {banner_link}")
                self.logger.info(f"{slide_page}_문구: {visual_text}")
                self.logger.info(f"{slide_page}_배경: {visual_bg}")

            play_button = self.driver.find_element(By.CSS_SELECTOR, '.btn-play-control.btn-play')
            pause_button = self.driver.find_element(By.CSS_SELECTOR, '.btn-play-control.btn-pause')
            pause_button.click()
            time.sleep(2)
            if play_button.is_displayed():
                self.logger.info("정지버튼 > 재생버튼 변경됨")
            else:
                self.logger.info("버튼이 변경되지 않음")

            prev_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-move.btn-prev")
            next_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-move.btn-next")
            banner_list = self.driver.find_elements(By.CSS_SELECTOR, ".slick-list div[data-index]")

            # 4. 테마배너 슬라이드 버튼 확인
            for direction, limit in [("next", button_count-1), ("previous", 0)]:
                while True:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".slick-list"))
                    )
                    active_slide = self.driver.find_element(By.CSS_SELECTOR, '.slick-slide.slick-active.slick-current')
                    current_index = int(active_slide.get_attribute('data-index'))
                    visual_text = active_slide.find_element(By.CSS_SELECTOR, '.visual-text img').get_attribute('alt')
                    # visual_bg = active_slide.find_element(By.CSS_SELECTOR, '.visual-bg img').get_attribute('src')
                    time.sleep(1)
                    self.logger.info(f"슬라이드_{current_index+1} 텍스트: {visual_text}")
                    if current_index == limit:
                        break
                    if direction == "previous":
                        driver.execute_script("arguments[0].click();", prev_button)
                    elif direction == "next":
                        if current_index < limit:
                            driver.execute_script("arguments[0].click();", next_button)
                        else:
                            break
                time.sleep(2)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            self.logger.error(traceback.format_exc())
            traceback.print_stack()

        
"""
    TestCase05: 휴대폰 영역 탭(추천, 삼성, Apple, 가성비폰) 무작위 선택 후 무작위 기기 '주문하기' 클릭,
    해당 기기 장바구니에 담기 위한 조건 만족 후 장바구니 이동 및 기기명, 요금제, 금액 데이터 일치 여부 확인 후 장바구니에서 항목 삭제
"""
class TestCase05:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def execute(self):
        try:
            self.select_mobile_device()
            self.check_available_options()
            self.select_device_option()
            self.select_shipping_option()
            self.select_other_option()
            self.order_info()
            self.cart_redirection()
            self.order_delete()
        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            self.logger.error(traceback.format_exc())
            traceback.print_stack()
    

    def select_mobile_device(self):
        # 1. 모바일 메뉴 클릭
        mobile_button = self.driver.find_element(By.CSS_SELECTOR, "header > div.header-gnb-wrap > div.header-inner > nav > ul > li.m1")
        mobile_button.click()
        time.sleep(5)

        # 2. 모바일 메뉴로 리다이렉션 확인
        mobile_url = self.driver.current_url
        if "/mobile" in mobile_url:
            self.logger.info(f"모바일 페이지로 이동 URL: {mobile_url}")
        else:
            self.logger.info(f"모바일 페이지로 이동 실패 URL: {mobile_url}")

        # 3. 디바이스 섹션 포커싱
        device_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[section-group-id="PcSubMainMobileDeviceSection"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", device_section)
        time.sleep(2)

        # 4. 무작위 탭 선택
        tabs = device_section.find_elements(By.CSS_SELECTOR, '.c-tabmenu-tab.c-tab-default ul li')
        random_tab = random.choice(tabs)
        random_tab_text = random_tab.text
        driver.execute_script("arguments[0].click();", random_tab)
        self.logger.info(f"선택한 탭: {random_tab_text}")
        time.sleep(2)

        # 5. 무작위 기기 선택('style' 속성에 "display: none"이 포함X)
        active_list = device_section.find_element(By.CSS_SELECTOR, '.c-tabmenu-wrap .c-tabcontent-box:not([style*="display: none"])')
        device_list = active_list.find_elements(By.CSS_SELECTOR, '.slick-list .slick-track .slick-slide')
        visible_devices = [
            device for device in device_list
                if device.get_attribute("aria-hidden") == "false"
                and "slick-slide" in device.get_attribute("class")
        ]
        self.logger.info(f"{random_tab_text} 기기 리스트 갯수: {len(device_list)}")
        self.logger.info(f"{random_tab_text} 보여지는 기기 갯수: {len(visible_devices)}")

        # 5. 무작위 탭의 기기 리스트 확인
        for index, device in enumerate(visible_devices):
            device_name = device.find_element(By.CSS_SELECTOR, '.big-title').text
            device_price = device.find_element(By.CSS_SELECTOR, '.total-price').text
            device_colors = [
                color.text for color in device.find_elements(By.CSS_SELECTOR, 'p.color-chip span.is-blind')
            ]
            device_url = device.find_element(By.CSS_SELECTOR, 'button[data-gtm-click-url]').get_attribute('data-gtm-click-url')
            custom_logger.info(f"기기_{index + 1}: {device_name} 가격: {device_price} 색상: {device_colors} URL: {device_url}")

        # 6. 무작위 기기 선택
        random_device = random.choice(visible_devices)
        device_name = random_device.find_element(By.CSS_SELECTOR, '.big-title').text
        order_button = random_device.find_element(By.CSS_SELECTOR, 'button[data-gtm-click-url]')
        order_button_url = order_button.get_attribute('data-gtm-click-url')
        self.logger.info(f"주문하기 버튼 URL: {order_button_url}")
        order_button.click()
        self.logger.info(f"선택된 기기: {device_name}")
        time.sleep(2)

        # 7. 주문하기 버튼 클릭 후 장바구니 페이지로 리다이렉션 확인
        order_url = driver.current_url
        if "/mobile/device" in order_url:
            self.logger.info(f"주문하기 페이지로 이동 URL: {order_url}")
        else:
            self.logger.info(f"주문하기 페이지로 이동 실패 URL: {order_url}")

        # 8. 주문하기 페이지에서 기기명 확인
        device_detail_name = driver.execute_script("return document.querySelector('h2.title-main').childNodes[0].textContent.trim();")
        custom_logger.info(f"주문하는 기기명: {device_detail_name}")
        if device_name in device_detail_name:
            self.logger.info(f"선택한 기기명: {device_name} 상세페이지 기기명: {device_detail_name}로 기기명이 일치합니다.")
        else:
            self.logger.info(f"기기명이 일치하지 않습니다. 선택된 기기: {device_name}, 상세 페이지 기기: {device_detail_name}")
        driver.implicitly_wait(10)
    

    def check_available_options(self):
        # 팝업창 닫기(따로 빼기 일단 하드코딩)
        try:
            popup_close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.c-btn-close'))
            )
            popup_close_button.click()
            self.logger.info("팝업창 닫기 버튼 클릭 완료")
            driver.implicitly_wait(10)
        except TimeoutException:
            self.logger.info("팝업창이 나타나지 않았습니다.")
        
        # 1. 선택해야 할 옵션들 확인
        strong_texts = []
        option_text = driver.find_elements(By.CSS_SELECTOR, 'div.device-info-area div.color, div.device-info-area div.option-box')

        for option in option_text:
            # JavaScript로 해당 요소 내 모든 strong 태그의 텍스트를 추출
            texts = driver.execute_script("""
                var strongElements = arguments[0].querySelectorAll('strong');
                return strongElements ? Array.from(strongElements).map(function(strong) {
                    return strong.textContent.trim();
                }) : [];
            """, option)
            strong_texts.extend(texts)
        self.logger.info(f"기기 옵션: {strong_texts}")

        # 2. 탭 리스트 확인
        tab_lists = driver.find_elements(By.CSS_SELECTOR, 'div.c-tab-slidemenu ul li a')
        tab_texts = [
            tab.get_attribute('data-gtm-click-text') for tab in tab_lists
        ]
        self.logger.info(f"탭 리스트 갯수: {len(tab_lists)} {tab_texts}")

        # 3. 탭 예상 납부금액 탭에서 선택해야 할 옵션들 확인
        th_texts = []
        th_option_text = driver.find_elements(By.CSS_SELECTOR, 'div.c-table table tr[role="row"] th')
        
        for th in th_option_text:
            # JavaScript로 span 태그의 텍스트 추출
            texts = driver.execute_script("""
                var spanElements = arguments[0].querySelectorAll('span');
                return spanElements ? Array.from(spanElements).map(function(span) {
                    return span.textContent.trim();
                }) : [];
            """, th)
            th_texts.extend(texts)
        self.logger.info(f"탭 선택옵션: {th_texts}")

        # 4. 옵션 선택: 색상, 저장공간, 가입유형, 배송방법, 요금제&&할인혜택, 제휴카드, VIP멤버쉽, 추가할인, 사은품, 쿠폰
        self.color_section = driver.find_element(By.CSS_SELECTOR, 'div > div.middlearea > div > div.device-info-area > div.color')
        self.storage_section = driver.find_elements(By.CSS_SELECTOR, 'div > div.middlearea > div > div.device-info-area > div.option-box')[0]
        self.join_section = driver.find_elements(By.CSS_SELECTOR,'div > div.middlearea > div > div.device-info-area > div.option-box')[1]
        self.shipping_section = driver.find_element(By.CSS_SELECTOR,'tbody > tr:nth-child(1)')
        self.fee_section = driver.find_element(By.CSS_SELECTOR,'tbody > tr:nth-child(2) > td')
        self.installment_section = driver.find_element(By.CSS_SELECTOR,'tbody > tr:nth-child(3) > td')
        self.card_section = driver.find_element(By.CSS_SELECTOR, 'tbody > tr[name="co-card"]')
        self.vip_benefilt_section = driver.find_element(By.CSS_SELECTOR,'tbody > tr:nth-child(5)')
        if "VIP 멤버십 혜택" in th_texts:
            self.sale_plus_section = driver.find_element(By.CSS_SELECTOR, 'tbody > tr:nth-child(6)')
            self.logger.info("VIP 멤버십 혜택이 존재합니다. 추가할인 셋팅")
        else:
            self.sale_plus_section = driver.find_element(By.CSS_SELECTOR, 'tbody > tr:nth-child(5)')
        self.gift_section = driver.find_elements(By.CSS_SELECTOR,'tbody > tr.gift-list')[0]
        self.coupon_section = driver.find_elements(By.CSS_SELECTOR,'tbody > tr.gift-list')[1]
        driver.implicitly_wait(5)


    def select_device_option(self):
        # 1. 색상 선택
        # color_section에 포커싱
        driver.execute_script("arguments[0].scrollIntoView(true);", self.color_section)

        # 색상 옵션 리스트
        color_list = self.color_section.find_elements(By.CSS_SELECTOR, 'div.color div.btns button.btn-color')
        color_list_text = [
            driver.execute_script("return arguments[0].querySelector('em.is-blind').textContent.trim();", color)
            for color in color_list
        ]
        self.logger.info(f"색상옵션: {len(color_list)} {color_list_text}")

        # 색상 랜덤 선택 후 리스트 내 버튼 클릭
        selected_color_button = random.choice(color_list)
        driver.execute_script("arguments[0].click();", selected_color_button)
        selected_color = driver.execute_script("return arguments[0].querySelector('em').textContent.trim();", selected_color_button)
        self.logger.info(f"선택된 색상: {selected_color}")

        # 2. 저장공간 선택
        # storage_section에 포커싱
        driver.execute_script("arguments[0].scrollIntoView(true);", self.storage_section)
        
        # 저장 옵션 리스트
        storage_list = self.storage_section.find_elements(By.CSS_SELECTOR, 'ul.c-card-list-icon.check-type-3-1 li')
        storage_list_text = [
            driver.execute_script("return arguments[0].querySelector('span.info-tit').textContent.trim();", storage)
            for storage in storage_list
        ]
        self.logger.info(f"저장옵션: {len(storage_list)} {storage_list_text}")

        # 저장공간 리스트 랜덤 선택 후 리스트 내 버튼 클릭
        selected_storage = random.choice(storage_list)
        storage_button = selected_storage.find_element(By.CSS_SELECTOR, '.c-radio input[type="radio"]')
        driver.execute_script("arguments[0].click();", storage_button)
        selected_storage_text = driver.execute_script("return arguments[0].querySelector('.info-tit').textContent.trim();", selected_storage)
        self.logger.info(f"선택된 저장공간: {selected_storage_text}")

        # 3. 가입유형 선택
        # join_section에 포커싱
        driver.execute_script("arguments[0].scrollIntoView(true);", self.join_section)

        # 가입유형 리스트
        join_type_list = self.join_section.find_elements(By.CSS_SELECTOR, 'ul li')
        join_type_list_text = [
            driver.execute_script("return arguments[0].querySelector('span.info-tit').textContent;", join)
            for join in join_type_list
        ]
        custom_logger.info(f"가입유형: {len(join_type_list)} {join_type_list_text}")
        
        # 가입유형 리스트 랜덤 선택 후 리스트 내 버튼 클릭
        selected_join_type = random.choice(join_type_list)
        join_option_button = selected_join_type.find_element(By.CSS_SELECTOR, '.c-radio input[type="radio"]')
        driver.execute_script("arguments[0].click();", join_option_button)
        selected_join_type = driver.execute_script("return arguments[0].querySelector('span.info-tit').textContent.trim();", selected_join_type)
        self.logger.info(f"선택된 가입유형: {selected_join_type}")
        driver.implicitly_wait(5)
    

    def select_shipping_option(self):       
        # 9-4. 배송방법 선택
        # shipping_section에 포커싱
        driver.execute_script("arguments[0].scrollIntoView(true);", self.shipping_section)

        # 배송방법 리스트
        shipping_list = self.shipping_section.find_elements(By.CSS_SELECTOR, 'ul.c-card-list-icon.check-type-3-1 li')
        shipping_list_text = [
            driver.execute_script("return arguments[0].querySelector('span').textContent.trim();", shipping)
            for shipping in shipping_list
        ]
        self.logger.info(f"배송유형: {len(shipping_list)} {shipping_list_text}")

        # 배송방법 리스트 랜덤 선택 후 리스트 내 버튼 클릭   
        selected_shipping_option = random.choice(shipping_list) 
        shipping_button = selected_shipping_option.find_element(By.CSS_SELECTOR, 'div.c-card-box div.c-radio input[type="radio"]')
        driver.execute_script("arguments[0].click();", shipping_button)
        selected_shipping = driver.execute_script("return arguments[0].querySelector('.text-radio').textContent.trim();", selected_shipping_option)
        self.logger.info(f"선택된 배송방법: {selected_shipping}")

        # 오늘도착을 선택하는 경우
        try:
            # JavaScript로 adress_search가 존재하는지 확인
            address_search = driver.execute_script("""
                return document.querySelector('ul.c-bullet-type-circle ul li a');
            """)
            # adress_search가 비어 있지 않으면 실행
            if address_search:
                custom_logger.info(f"배송방법이 오늘도착으로 확인되서 주소찾기를 진행합니다.")
                # 주소찾기 클릭
                driver.execute_script("arguments[0].click();", address_search)
                address_modal = driver.find_element(By.CSS_SELECTOR, 'div.modal-content')
                header = address_modal.find_element(By.CSS_SELECTOR, 'header.modal-header h1').text.strip()
                if header == "주소찾기":
                    custom_logger.info("주소찾기 모달창 오픈 완료")
                    time.sleep(10)
                    # 하드고정 주소 입력
                    address_1 = "한강로 3가 65-228"
                    address_2 = "엘지유플러스"
                    # 하드고정 주소 넣기
                    address_input = address_modal.find_element(By.CSS_SELECTOR, 'div.c-inpform input[type="text"]')
                    address_button = address_modal.find_element(By.CSS_SELECTOR, 'div.c-inpform button.c-ibtn-find')
                    time.sleep(10)
                    ActionChains(self.driver).move_to_element(address_input).click().perform()
                    self.logger.info(f"주소찾기 입력")
                    address_input.send_keys(address_1)
                    driver.execute_script("arguments[0].click();", address_button)
                    
                    # 주소 결과 중 랜덤 선택
                    address_list = driver.find_element(By.CSS_SELECTOR, 'div.result-cont div.address-list-li')
                    selected_address = random.choice(address_list)
                    address_button = selected_address.find_element(By.CSS_SELECTOR, 'input[type="radio]')
                    driver.execute_script("arguments[0].click();", address_button)
                    
                    address_dl = address_list.execute_script("return arguments[0].querySelector('dl.address-list').textContent.trim();", selected_address)
                    selected_address_text = []
                    for address in address_dl:
                        address_1 = address.find_element(By.TAG_NAME, 'dt').text.strip()
                        address_2 = address.find_element(By.TAG_NAME, 'dd').text.strip()
                        
                        selected_address_text.append(f"{address_1}: {address_2}")
                    selected_address_text = ', '.join(selected_address_text)
                    custom_logger.info(f"선택한 주소: {selected_address_text}")  

                    # 주소찾기 나머지 주소를 입력하기
                    address_result_section = driver.find_element(By.CSS_SELECTOR, 'div.address-result > div.result-cont-select"]')
                    address_input_etc = address_result_section.find_element(By.CSS_SELECTOR, 'dl:nth-child(3) dd input[type="text"]')
                    ActionChains(self.driver).move_to_element(address_input).click().perform()
                    address_input_etc.send_keys(address_2)

                    # 확인 버튼 클릭
                    address_confirm_button = driver.find_element(By.CSS_SELECTOR, 'div.modal-footer button.c-btn-solid-1-m')
                    driver.execute_script("arguments[0].click();", address_confirm_button)

        except NoSuchElementException:
            self.logger.info("팝업창이 나타나지 않았습니다.")
        
        # 매장픽업을 선택하는 경우
        try:
            # JavaScript로 pickup가 존재하는지 확인
            pickup = driver.execute_script("""
                return document.querySelectorAll('table.b-table.c-table-rowc-table-form');
            """)
            # adress_search가 비어 있지 않으면 실행
            if pickup:
                self.logger.info(f"배송방법이 매장픽업으로 확인되서 매장찾기를 진행합니다.")
                self.logger.info(f"매장픽업 사용불가하여 다른 방법으로 선택")
                # 매장찾기 클릭
                # pickup_search = pickup.find_element(By.CSS_SELECTOR, '.c-input-inner button.c-btn-rect-1')
                # driver.execute_script("arguments[0].click();", pickup_search)
            else: 
                custom_logger.info("팝업창이 나타나지 않았습니다.")
        except NoSuchElementException:
            custom_logger.info("팝업창이 나타나지 않았습니다.")
        driver.implicitly_wait(5)


    def select_other_option(self):    
        # 1. 요금제 선택
        # fee_section에 포커싱
        driver.execute_script("arguments[0].scrollIntoView(true);", self.fee_section)

        # 요금제 리스트
        fee_list = self.fee_section.find_elements(By.CSS_SELECTOR, 'div.fee-select-box')
        fee_list_text = [
            driver.execute_script("return arguments[0].querySelector('label.text-radio div.name').textContent.trim();", fee)
            for fee in fee_list
        ]
        custom_logger.info(f"요금제유형: {len(fee_list)} {fee_list_text}")

        # 요금제 리스트 랜덤 선택 후 리스트 내 버튼 클릭
        selected_fee = random.choice(fee_list)
        fee_button = selected_fee.find_element(By.CSS_SELECTOR, 'span.c-radio input[type="radio"]')
        driver.execute_script("arguments[0].click();", fee_button)
        selected_fee = driver.execute_script("return arguments[0].querySelector('.name').textContent.trim();", selected_fee)
        custom_logger.info(f"선택된 요금제: {selected_fee}")
        
        # 2. 요금제 특별혜택 선택 
        try:
            # JavaScript로 check-line-box가 존재하는지 확인
            fee_special_list = driver.execute_script("""
                return document.querySelectorAll('div.check-line-box');
            """)

            # fee_special_list가 비어 있지 않으면 실행
            if fee_special_list:
                # 하나의 요소를 선택하고 그 안의 체크박스를 선택
                selected_fee_special = random.choice(fee_special_list)
                # 체크박스 요소 클릭
                checkbox = selected_fee_special.find_element(By.CSS_SELECTOR, 'div.check-line-box-inner span.c-checkbox input[type="checkbox"]')
                driver.execute_script("arguments[0].click();", checkbox)
                # 선택된 특별 혜택의 텍스트 가져오기
                selected_special_fee = driver.execute_script("return arguments[0].querySelector('.txt').textContent;", selected_fee_special)
                custom_logger.info(f"선택된 특별혜택: {selected_special_fee}")
            else:
                custom_logger.info("특별 혜택이 없습니다.")
        except NoSuchElementException:
            custom_logger.info("선택된 요금제에는 특별혜택이 없습니다.")
        driver.implicitly_wait(5)

        # 3. 할부금 납부 기간 포커싱
        driver.execute_script("arguments[0].scrollIntoView(true);", self.fee_section)

        # 할인방법 선택
        try:
            # JavaScript로 check-line-box가 존재하는지 확인
            discount_list = driver.execute_script("""
                return document.querySelectorAll('ul.sale-type-box.sale-type-box--type2 li');
            """)
            notice = driver.execute_script("""
                return document.querySelectorAll('ul.c-noticebox-h4');
            """)
            if discount_list:
                selected_discount = random.choice(discount_list)
                # 내부 라디오 요소 클릭
                radio = selected_discount.find_element(By.CSS_SELECTOR, 'div.c-inpfield span.c-radio input[type="radio"]')
                driver.execute_script("arguments[0].click();", radio)
                # 선택된 특별 혜택의 텍스트 가져오기
                span_texts = driver.execute_script("""
                    var spans = arguments[0].querySelectorAll('label.text-radio div.txt span');
                    return [spans[0].textContent, spans[1].textContent];
                """, selected_discount)
                first_span_text = span_texts[0]
                second_span_text = span_texts[1]
                custom_logger.info(f"선택된 할인방법: {first_span_text} {second_span_text}")
            else:
                if notice:
                    custom_logger.info(f"알림 메시지: {notice[0].text and notice[1].text}")
        except NoSuchElementException:
            custom_logger.info("선택된 요금제에는 할인방법이 없습니다.")
        driver.implicitly_wait(5)

        # 4. 할부금 납부기간 더보기 버튼 클릭
        installment_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.month-credit-box .btn-chk.is-add'))
        )
        driver.execute_script("arguments[0].click();", installment_button)

        # 할부금 납부기간 선택
        installments_list = self.installment_section.find_elements(By.CSS_SELECTOR, 'div.month-credit-box div.chk-wrap ul li')
        installments_list_text = [
            driver.execute_script("return arguments[0].querySelector('label.text-radio span.info-tit').textContent.trim();", installments)
            for installments in installments_list
        ]
        custom_logger.info(f"할부금납부 방법: {len(installments_list)} | {installments_list_text}")
        selected_installment = random.choice(installments_list)
        installment_button = selected_installment.find_element(By.CSS_SELECTOR, 'div.c-radio input[type="radio"]')
        driver.execute_script("arguments[0].click();", installment_button)

        selected_installment = driver.execute_script("return arguments[0].querySelector('label span.font-m.info-tit').textContent;", selected_installment)
        custom_logger.info(f"선택된 할부금 납부기간: {selected_installment}")
        driver.implicitly_wait(5)

        # 5. 제휴카드 선택
        # Test case failed: Message: javascript error: Cannot read properties of null (reading 'textContent')
        # Test case failed: Cannot choose from an empty sequence 에러 해결 완료
        # 제휴카드 포커싱
        driver.execute_script("arguments[0].scrollIntoView(true);", self.card_section)

        # 제휴카드 더보기 버튼 클릭
        more_card_button = self.card_section.find_element(By.CSS_SELECTOR, '.more-view.toggle a')
        driver.execute_script("arguments[0].click();", more_card_button)
        
        # 제휴카드 선택
        all_card_list = self.card_section.find_elements(By.CSS_SELECTOR, 'ul.c-card-list-icon.check-type-2 li')
        card_not_select = all_card_list[0]
        card_list = all_card_list[1:]
        card_not_select_text = driver.execute_script("return arguments[0].innerText.trim();", card_not_select)
        card_list_text = [
            driver.execute_script("return arguments[0].innerText.trim();", card) for card in card_list
        ]
        custom_logger.info(f"카드 미선택 문구: {card_not_select_text}") 
        for index, card_text in enumerate(card_list_text):
            custom_logger.info(f"카드_{index + 1}: {card_text}")

        # 제휴카드 랜덤 선택 후 리스트 내 버튼 클릭
        selected_card_list = random.choice(all_card_list)
        card_button = selected_card_list.find_element(By.CSS_SELECTOR, 'div.c-radio input[type="radio"]')
        driver.execute_script("arguments[0].click();", card_button)
        selected_card_list_text = driver.execute_script("return arguments[0].querySelector('div.info-tit').textContent;", selected_card_list)
        custom_logger.info(f"선택된 카드: {selected_card_list_text}")
        
        # 6. VIP맴버십 혜택 선택
        try:
            # JavaScript로 check-line-box가 존재하는지 확인
            vip_benefits_list = driver.execute_script("""
                return document.querySelectorAll('ul.VipBenefit li');
            """)
            if vip_benefits_list:
                # VIP 혜택 포커싱
                driver.execute_script("arguments[0].scrollIntoView(true);", self.vip_benefilt_section)
                vip_benefits_list_text = [
                    {
                        "이미지": driver.execute_script("return arguments[0].querySelector('.img img').getAttribute('src').trim();", vip),
                        "혜택": driver.execute_script("return arguments[0].querySelector('strong').textContent.trim();", vip),
                        "가격": driver.execute_script("return arguments[0].querySelector('span:last-child').textContent.trim();", vip)
                    }
                    for vip in vip_benefits_list
                ]
                custom_logger.info(f"VIP맴버십 혜택: {len(vip_benefits_list)} {vip_benefits_list_text}")
                # VIP 혜택 랜덤 선택 후 리스트 내 버튼 클릭
                selected_vip_benefit = random.choice(vip_benefits_list)
                vip_benefits_button = selected_vip_benefit.find_element(By.CSS_SELECTOR, 'div.c-radio input[type="radio"]')
                driver.execute_script("arguments[0].click();", vip_benefits_button)
                selected_vip_benefit = driver.execute_script("return arguments[0].querySelector('div.itemBenefit strong').textContent;", selected_vip_benefit)
                custom_logger.info(f"선택된 VIP 혜택: {selected_vip_benefit}")
        except NoSuchElementException:
            custom_logger.info("VIP맴버십 혜택이 없습니다.")

        # 7. 추가할인
        # 추가할인 포커싱
        driver.execute_script("arguments[0].scrollIntoView(true);", self.sale_plus_section)
        sale_plus_list = self.sale_plus_section.find_elements(By.CSS_SELECTOR, 'ul.sale-plus-list li')
        sale_plus_list_text = [
            driver.execute_script("return arguments[0].querySelector('label.text-chkbox span.txt').textContent.trim();", sale_plus)
            for sale_plus in sale_plus_list
        ]
        custom_logger.info(f"추가할인: {len(sale_plus_list)} {sale_plus_list_text}")
        # 추가할인 선택
        selected_sale_plus = random.choice(sale_plus_list)
        discount_option_button = selected_sale_plus.find_element(By.CSS_SELECTOR, 'span.c-checkbox input[type="checkbox"]')
        driver.execute_script("arguments[0].click();", discount_option_button)
        selected_sale_plus = driver.execute_script("return arguments[0].querySelector('span.txt').textContent;", selected_sale_plus)
        custom_logger.info(f"선택된 추가 할인: {selected_sale_plus}")

        # 8. 사은품
        # 사은품 포커싱
        driver.execute_script("arguments[0].scrollIntoView(true);", self.gift_section)
        gift_list = [gift for gift in self.gift_section.find_elements(By.CSS_SELECTOR, 'div.radio-image-type ul li') if not gift.find_elements(By.CSS_SELECTOR, 'span.text-sold-out')]
        gift_list_text = [
            driver.execute_script("return arguments[0].querySelector('label.text-radio span.info-tit').textContent.trim();", gift)
            for gift in gift_list
        ]
        available_gift_list = [
            gift for gift in gift_list if not gift.find_elements(By.CSS_SELECTOR, 'span.text-sold-out')
        ]
        # gift_list와 품절 정보 한 번에 가져오기
        # gift_list = driver.execute_script("""
        #     return Array.from(arguments[0].querySelectorAll('div.radio-image-type ul li')).map(gift => {
        #         return {
        #             text: gift.querySelector('label.text-radio span.info-tit') ? gift.querySelector('label.text-radio span.info-tit').textContent.trim() : '',
        #             isSoldOut: !!gift.querySelector('span.text-sold-out'),
        #             giftElement: gift
        #         };
        #     });
        # """, gift_section)

        # # 품절 제외한 리스트 추출
        # available_gift_list = [gift for gift in gift_list if not gift['isSoldOut']]
        # gift_list_text = [gift['text'] for gift in gift_list]
        custom_logger.info(f"사은품 옵션(품절 제외): {len(available_gift_list)} | {gift_list_text}")

        # 사은품 선택
        selected_gift_list = random.choice(gift_list)
        gift_button = selected_gift_list.find_element(By.CSS_SELECTOR, 'div.c-radio input[type="radio"]')
        driver.execute_script("arguments[0].click();", gift_button)
        selected_gift = driver.execute_script("return arguments[0].querySelector('.font-m.info-tit').textContent;", selected_gift_list)
        custom_logger.info(f"선택된 사은품: {selected_gift}")

        # 9. 쇼핑쿠폰백 선택
        # 쇼핑쿠폰백 포커싱
        driver.execute_script("arguments[0].scrollIntoView(true);", self.coupon_section)
        coupon_list = [
            coupon for coupon in self.coupon_section.find_elements(By.CSS_SELECTOR, 'div.coupon-gifts-list ul li') 
            if not coupon.find_elements(By.CSS_SELECTOR, 'input[type="radio"][disabled="disabled"]')
        ]
        
        gift_list_text = [
            driver.execute_script("return arguments[0].querySelector('label.text-radio span.txt2').textContent.trim();", coupon)
            for coupon in coupon_list
        ]
        custom_logger.info(f"쇼핑쿠폰팩 옵션: {len(gift_list)} | {gift_list_text}")
        selected_coupon_option = random.choice(coupon_list)
        coupon_option_button = selected_coupon_option.find_element(By.CSS_SELECTOR, 'div.c-radio input[type="radio"]:not([disabled="disabled"])')
        driver.execute_script("arguments[0].click();", coupon_option_button)
        selected_coupon = driver.execute_script("return arguments[0].querySelector('.txt2').textContent;", selected_coupon_option)
        custom_logger.info(f"선택된 쇼핑쿠폰백: {selected_coupon}")
        driver.implicitly_wait(5)

    def order_info(self):
        # 주문하기 버튼 클릭 전 선택 사항 리스트 확인
        # 계산 박스 정보 포커싱
        self.calculation_section = driver.find_element(By.CSS_SELECTOR, 'div.calculation-box')
        driver.execute_script("arguments[0].scrollIntoView(true);", self.calculation_section)

        # 계산 박스 정보 출력
        self.device_name = self.calculation_section.find_element(By.CSS_SELECTOR, '.name').text
        time.sleep(10)
        # 색상 / 기기용량 / 기기변경
        device_color = self.calculation_section.find_element(By.CSS_SELECTOR, '.c-vline-info-type-1 .info-text:nth-child(1)').text
        device_storage = self.calculation_section.find_element(By.CSS_SELECTOR, '.c-vline-info-type-1 .info-text:nth-child(2)').text
        device_change_type = self.calculation_section.find_element(By.CSS_SELECTOR, '.c-vline-info-type-1 .info-text:nth-child(3)').text

        custom_logger.info(f"선택된 기기명: {self.device_name}")
        custom_logger.info(f"선택된 색상: {device_color}")
        custom_logger.info(f"선택된 저장공간: {device_storage}")
        custom_logger.info(f"선택된 가입유형: {device_change_type}")
        driver.implicitly_wait(5)


    def cart_redirection(self):
        # 1. 장바구니 버튼 클릭
        cart_button = self.calculation_section.find_element(By.CSS_SELECTOR, '.btn-area.btn-small button:nth-of-type(2)')
        driver.execute_script("arguments[0].click();", cart_button)
        custom_logger.info("장바구니 버튼 클릭 완료")
        
        # 2. 장바구니 버튼 클릭시, 모달창 확인 버튼 클릭하기
        header = driver.find_element(By.CSS_SELECTOR, 'div.modal-content header.modal-header h1').text.strip()
        if header == "장바구니담기":
            custom_logger.info("장바구니담기 팝업창 오픈 완료")
            cart_link_button = driver.find_element(By.CSS_SELECTOR, '.modal-footer button:nth-of-type(2)')
            driver.execute_script("arguments[0].click();", cart_link_button)
            custom_logger.info("장바구니로 이동 버튼 클릭 완료")
            try:
                WebDriverWait(driver, 10).until(EC.url_contains("/cart")) 
                cart_url = driver.current_url
                custom_logger.info(f"장바구니 페이지로 이동 성공 URL: {cart_url}")
            except Exception as e:
                cart_url = driver.current_url
                custom_logger.error(f"장바구니 페이지로 이동 실패 URL: {cart_url} Error: {e}")
        else: 
            custom_logger.error("장바구니 팝업창이 나타나지 않았습니다.")
        driver.implicitly_wait(5)
 
        # 3. 장바구니에서 기기명 확인
        self.cart_list = driver.find_element(By.CSS_SELECTOR, 'div.products-tbl ul.products-tbl-list li')
        cart_device_info = self.cart_list.find_element(By.CSS_SELECTOR, 'div.p-product div')
        cart_device_name = driver.execute_script("return arguments[0].querySelector('p.tit').textContent;", cart_device_info)
        custom_logger.info(f"장바구니 기기명: {cart_device_name}")
        self.device_name = self.device_name.strip()
        cart_device_name = cart_device_name.strip().replace('\n', ' ')
        if  cart_device_name in self.device_name:
            custom_logger.info(f"선택된 기기: {self.device_name}, 장바구니 기기: {cart_device_name}와 기기명이 일치합니다")
        else:
            custom_logger.info(f"선택된 기기: {self.device_name}, 장바구니 기기: {cart_device_name}와 기기명이 일치하지 않습니다. ")
        driver.implicitly_wait(5)


    def order_delete(self):
        # 1. 장바구니에서 항목 삭제
        try: 
            selectors = ['button.btn-del', 'div.c-btn-group button.c-btn-solid-1-m','div.c-btn-group button.c-btn-solid-1-m']
            for selector in selectors:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                #driver.implicitly_wait(1)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", element)
        except TimeoutException as e :
            custom_logger.error(f"Error: {e}")
            custom_logger.error("장바구니에서 항목 삭제 실패")
        
    
        # # 두 번째 모달창의 "확인" 버튼이 나타날 때까지 대기
        # try:
        #     final_confirm_button = WebDriverWait(driver, 10).until(
        #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.c-btn-group button.c-btn-solid-1-m'))
        #     )
        #     final_confirm_button.click()  # 마지막 확인 버튼 클릭
        #     custom_logger.info("장바구니에서 항목 삭제 완료")
        # except Exception as e:
        #     custom_logger.error(f"항목 삭제 중 오류 발생: {e}")

        # # 모달창 닫기 버튼이 나타날 때까지 대기
        # try:
        #     close_button = driver.find_element(By.CSS_SELECTOR, 'button.c-btn-close')
        #     driver.execute_script("arguments[0].dispatchEvent(new Event('click', { bubbles: true }));", close_button)
        #     custom_logger.info("모달창 닫기 클릭 이벤트 트리거 완료")
        # except Exception as e:
        #     custom_logger.error(f"모달창 닫기 이벤트 트리거 중 오류 발생: {e}")


        # 2. 장바구니에서 삭제 되었는지 리스트에서 확인
        empty_cart_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cart-empty-wrap')))
        #empty_cart_list = driver.execute_script("return document.querySelector('div.cart-empty-wrap');")
        #empty_cart_list = driver.find_element(By.CSS_SELECTOR, 'div.cart-empty-wrap')
        if empty_cart_list:
            custom_logger.info("장바구니가 비어 있습니다.")
            
            # 메인 페이지로 이동
            #main_page_button = WebDriverWait(driver, 10).until(
            #    EC.presence_of_element_located((By.CSS_SELECTOR, 'button.c-btn-outline-2'))
            #)
            main_page_button = driver.execute_script("return document.querySelector('button.c-btn-outline-2');")
            #main_page_button = driver.find_element(By.CSS_SELECTOR, 'button.c-btn-outline-2')
            driver.execute_script("arguments[0].click();", main_page_button)

            #main_page_button.click()
            custom_logger.info("메인 페이지로 이동 버튼 클릭 완료")
        else:
            custom_logger.info("장바구니에 항목이 남아 있습니다.")


"""
    TestCase06: 인터넷/IPTV 결합 영역 드롭다운 항목 무작위선택 후 할인 금액 데이터 추출 및 '가입상담신청' 클릭, 상담 신청하기 페이지 내 할인 금액 데이터 비교
"""
class TestCase06:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def execute(self):
        try:
            # 1. 모바일 메뉴 클릭
            mobile_button = self.driver.find_element(By.CSS_SELECTOR, "header > div.header-gnb-wrap > div.header-inner > nav > ul > li.m1")
            mobile_button.click()
            time.sleep(5)

            # 2. 인터넷/IPTV결합 섹션 포커싱
            mobile_combined_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[section-group-id="PcSubMainMobileCombinedSection"]'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", mobile_combined_section)
            self.logger.info("인터넷/IPTV결합 섹션 포커싱 완료")

            # 3-1. 드롭다운 갯수 확인
            dropdowns = mobile_combined_section.find_elements(By.CSS_SELECTOR, '.simul-wrap .simul-dropbox-wrap')
            select_area_txt = mobile_combined_section.find_elements(By.CSS_SELECTOR, '.simul-dropbox-wrap .select-area-txt')
            for element in select_area_txt:
                select_area_txt = element.text
                self.logger.info(f"드롭다운 영역: {select_area_txt}")
            self.logger.info(f"드롭다운 갯수: {len(dropdowns)}")

            # 3-2. 핸드폰 결합 기기 수/인터넷/IPTV 드롭다운 랜덤 선택
            for dropdown in dropdowns:
                select_button = dropdown.find_element(By.CSS_SELECTOR, '.select-btn')
                select_button.click()
                time.sleep(1)
                options = dropdown.find_elements(By.CSS_SELECTOR, 'li a')
                area_txt = dropdown.find_element(By.CSS_SELECTOR, 'div.select-area-txt')
                random_option = random.choice(options)
                random_option_text = random_option.text
                random_option.click()
                self.logger.info(f"{(area_txt).text}: {random_option_text}")
                time.sleep(2)

            # 4-1. 할인 금액 데이터 추출
            results = mobile_combined_section.find_elements(By.CSS_SELECTOR, '.result-txt')
            discount_values = []
            for result in results:
                discount_text = result.text.strip()
                discount_value = int(''.join(filter(str.isdigit, discount_text)))
                discount_values.append(discount_value)
                total_discount = sum(discount_values)
                self.logger.info(f"할인금액: {discount_value}")
            self.logger.info(f"총 할인금액: {total_discount}")
           
            # 4-2. 할인 금액 데이터 추출
            discount_spans = mobile_combined_section.find_elements(By.CSS_SELECTOR, '.price-txt span')
            for discount_span in discount_spans:
                discount_text = ''.join(filter(lambda x: x.isdigit() or x == '.', discount_span.text.strip()))
                self.logger.info(f"할인금액: {discount_text}")

            # 4-3. 상담 신청하기 페이지 내 할인 금액 데이터 비교
            if total_discount == int(discount_text.replace(',', '')):
                self.logger.info(f"{total_discount}원으로 할인금액이 일치합니다.")
            else:
                self.logger.info(f"할인금액이 일치하지 않습니다. 총 할인금액: {total_discount}, 할인금액: {discount_text}")
            time.sleep(5)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            self.logger.error(traceback.format_exc())
            traceback.print_stack()


"""
     TestCase07: 청구내역 영역 청구월 무작위 월, 청구금액 데이터 추출 후 클릭, 페이지 이동 후 해당 월, 청구금액 일치 여부 확인
"""
class TestCase07:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def execute(self):
        try:
            # 1. 마이페이지 메뉴 클릭
            mypage_button = self.driver.find_element(By.CSS_SELECTOR, "header > div.header-gnb-wrap > div.header-inner > nav > ul > li.m3")
            mypage_button.click()
            time.sleep(5)

            # 2. 로그인 페이지로 리다이렉션 확인
            if "/login" in self.driver.current_url:
                self.logger.info("사용자 정보가 필요하여, 로그인 페이지로 리다이렉션되었습니다.")
                UPlusLogin(self.driver, self.logger).login()
            else:
                self.logger.info("현재 로그인 상태입니다.")
            time.sleep(2)

            # 2. 마이페이지 내의 청구 및 납부 정보 섹션 부팅까지 대기
            mypage_list = self.driver.find_element(By.CSS_SELECTOR, '#MyPageSection > div.c-content-wrap > div:nth-child(1)')

            # 3. 마이페이지 내의 청구요금 정보 확인
            billing_info = mypage_list.find_element(By.CSS_SELECTOR, "ul.my-payment-section")
            usage_period = billing_info.find_element(By.CLASS_NAME, "text-line-01").text.strip()
            usage_month = ''.join(filter(str.isdigit, billing_info.find_element(By.CLASS_NAME, "text-line-02").text.strip()))
            current_year = time.strftime("%Y")
            formatted_date = f"{current_year}-{usage_month.zfill(2)}"
         
            billing_amount = ''.join(filter(str.isdigit, billing_info.find_element(By.CLASS_NAME, "right-item-txt").text.strip()))
            self.logger.info(f"마이페이지내 사용기간: {usage_period}")
            self.logger.info(f"마이페이지내 사용년월: {formatted_date}")
            self.logger.info(f"마이페이지내 청구요금: {billing_amount}원")
            time.sleep(2)

            # 4. 사이드바 요금/납부 클릭
            cards = self.driver.find_elements(By.CSS_SELECTOR, "div.card")
            billing_header = cards[0].find_element(By.CSS_SELECTOR, 'a[data-gtm-click-text="요금/납부"]')
            billing_header.click()
            time.sleep(5)

            # 5. 요금/납부 메뉴로 리다이렉션 확인
            payinfo_url = self.driver.current_url
            if "/mypage/payinfo" in payinfo_url:
                self.logger.info(f"요금/납부 메뉴로 이동 URL: {payinfo_url}")
            else:
                self.logger.info(f"요금/납부 메뉴로 이동 실패 URL: {payinfo_url}")
           
            # 6. 가장 최근의 년도 청구내역 정보 출력
            # 테이블
            billing_table = self.driver.find_element(By.CSS_SELECTOR, "div.row.c-table.payment-table")
            billing_rows = billing_table.find_elements(By.CSS_SELECTOR, 'tbody tr[role="row"]')
            self.logger.info(f"보여지는 테이블 열 갯수: {len(billing_rows)}")

            # 가장 첫 번째 tr로 접근하여 청구내역 정보 출력
            first_row = self.driver.execute_script("return document.querySelector('div.row.c-table.payment-table tbody tr:first-child');")
            if first_row:
                billing_1 = self.driver.execute_script("return arguments[0].querySelector('td a').textContent.trim();", first_row)
                billing_2 = self.driver.execute_script("return arguments[0].querySelector('td span.font-xs').textContent.trim();", first_row)
                billing_3 = ''.join(filter(str.isdigit, self.driver.execute_script("return arguments[0].querySelector('td:nth-child(2)').textContent.trim();", first_row)))

                self.logger.info(f"요금/납부 사용년월: {billing_1}")
                self.logger.info(f"요금/납부 사용기간: {billing_2}")
                self.logger.info(f"요금/납부 청구금액: {billing_3}원")
            else:
                self.logger.info("첫번째 행을 찾을 수 없습니다.")

            # 6. 페이지 이동 후 해당 월, 청구금액 일치 여부 확인
            if formatted_date in billing_1 and billing_amount == billing_3:
                self.logger.info(f"마이페이지 내 사용년월: {formatted_date}와 요금/납부 최근 청구월: {billing_1}으로 일치합니다.")
                self.logger.info(f"마이페이지 내 청구요금: {billing_amount}원과 요금/납부 최근 청구금액: {billing_3}원으로 일치합니다.")
            else:
                self.logger.info(f"데이터 불일치")

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            self.logger.error(traceback.format_exc())
            traceback.print_stack()


"""
    TestCase08: '월별사용량조회' 탭 클릭 후 하단 '월별 사용량 상세조회' 클릭, 탭 리스트(국내통화 이용내역, 데이터 이용내역 등) 정상 노출 확인
"""
class TestCase08:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def execute(self):
        try:
            # 1. 마이페이지 메뉴 클릭
            mypage_button = self.driver.find_element(By.CSS_SELECTOR, "header > div.header-gnb-wrap > div.header-inner > nav > ul > li.m3")
            mypage_button.click()
            time.sleep(5)

            # 2. 로그인 페이지로 리다이렉션 확인
            if "/login" in self.driver.current_url:
                self.logger.info("사용자 정보가 필요하여, 로그인 페이지로 리다이렉션되었습니다.")
                UPlusLogin(self.driver, self.logger).login()
            else:
                self.logger.info("현재 로그인 상태입니다.")
            time.sleep(2)

            # 3. 마이페이지로 리다이렉션 확인
            mypage_url = self.driver.current_url 
            if "/mypage" in mypage_url:
                self.logger.info(f"마이페이지로 이동 URL: {mypage_url}")
            else:
                self.logger.info(f"마이페이지로 이동 실패 URL: {mypage_url}")
            time.sleep(2)

            # 3. 마이페이지 사이드 메뉴 정보 출력
            cards = self.driver.find_elements(By.CSS_SELECTOR, "div.card")
            # for card in cards:
            #     # 헤더 정보 출력
            #     header_link = card.find_element(By.CSS_SELECTOR, "header.card-header a")
            #     tab_name = header_link.get_attribute("data-gtm-click-text")
            #     self.logger.info(f"사이드바 메뉴: {tab_name}")
               
            #     # 사이드바 내 세부메뉴 정보 출력
            #     tabpanels = card.find_elements(By.CSS_SELECTOR, 'div[role="tabpanel"]')
            #     if tabpanels:
            #         for tabpanel in tabpanels:
            #             list_items = tabpanel.find_elements(By.CSS_SELECTOR, 'div.card-body ul li a')
            #             for item in list_items:
            #                 item_text = item.get_attribute('innerText').strip()
            #                 self.logger.info(f"{tab_name} | {item_text}")
            #     else:
            #         self.logger.info("세부메뉴 없음")

            tab_items = {}
            for card in cards:
                header_link = card.find_element(By.CSS_SELECTOR, "header.card-header a")
                tab_name = header_link.get_attribute("data-gtm-click-text")
                tab_items[tab_name] = []

                tabpanels = card.find_elements(By.CSS_SELECTOR, 'div[role="tabpanel"]')
                if tabpanels:
                    for tabpanel in tabpanels:
                        list_items = tabpanel.find_elements(By.CSS_SELECTOR, 'div.card-body ul li a')
                        for item in list_items:
                            item_text = item.get_attribute('innerText').strip()
                            tab_items[tab_name].append(item_text)

            for tab_name, items in tab_items.items():
                self.logger.info(f"{tab_name} {items}")

            # 4. 사이드바 '가입/사용 현황' 헤더 클릭 후 아코디언 세부메뉴 '사용내역 조회' 클릭
            usage_menu = cards[1].find_element(By.CSS_SELECTOR, 'aside > ul > div:nth-child(2) > header > a')
            usage_menu.click()
            time.sleep(2) 

            usage_accordion = cards[1].find_element(By.CSS_SELECTOR, 'div#accordion-1')
            if "collapse show" in usage_accordion.get_attribute("class"):
                self.logger.info("아코디언이 활성화 상태")
            else:
                self.logger.info("아코디언이 비활성화 상태")
            
            usage_details_li = cards[1].find_element(By.CSS_SELECTOR, 'div[role="tabpanel"] ul.p-main-sub-my-lnb-inner-ul li:nth-child(4) a')
            usage_details_li.click()
            time.sleep(10)

            # 5. 사용내역 조회 페이지로 리다이렉션 확인
            usage_details_url = self.driver.current_url
            if "/mypage/bilv" in usage_details_url:
                self.logger.info(f"사용내역 조회 페이지로 이동 URL: {usage_details_url}")
            else:
                self.logger.info(f"사용내역 조회 페이지로 이동 실패 URL: {usage_details_url}")

            # 6. 가입/사용 현황 탭 종류
            tab_lists = self.driver.find_elements(By.CSS_SELECTOR, 'div.swiper-container.c-tab-slidemenu ul li')
            tabs = self.driver.find_elements(By.CSS_SELECTOR, 'ul.swiper-wrapper li a')
            self.logger.info(f"탭 리스트 수: {len(tab_lists)}")
            for tab in tabs:
                self.logger.info(f"탭 텍스트: {tab.text}")
            
            # 7. 탭 리스트 중 월별사용량 조회 클릭
            usage_tab = tabs[1]
            usage_tab.click()
            custom_logger.info("월별 사용량 조회 탭 클릭 완료")
            time.sleep(2)
            detail_button = self.driver.find_element(By.CSS_SELECTOR, 'div.c-btn-group button.c-btn-solid-1')
            self.driver.execute_script("arguments[0].click();", detail_button)
            custom_logger.info("월별 사용량 상세조회 클릭 완료")
            time.sleep(2)

            # 8. 탭 리스트(국내통화 이용내역, 데이터 이용내역 등) 정상 노출 확인
            usage_details = self.driver.find_element(By.CSS_SELECTOR, '#MyPageSection > div.c-content-wrap > div')
            usage_detail_tabs = usage_details.find_elements(By.CSS_SELECTOR, 'div.c-tabmenu-tab.c-tab-slide > div > ul > li')

            for tab in usage_detail_tabs:
                tab_text = self.driver.execute_script("return arguments[0].querySelector('a').textContent;", tab)
                self.logger.info(f"탭 클릭: {tab_text}")
                self.driver.execute_script("arguments[0].click();", tab)
                time.sleep(2)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            traceback.print_stack()


"""
    testcase_09: 온라인 가입 할인 혜택 영역에서 '혜택 모두 보기' 클릭 후 온라인 구매 혜택 항목 텍스트 정상 노출 확인
"""
class TestCase09:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def execute(self):
        try:
            # 1. 혜택/맴버십 메뉴 클릭
            m4_menu_item = self.driver.find_element(By.CSS_SELECTOR, "header > div.header-gnb-wrap > div.header-inner > nav > ul > li.m4")
            m4_menu_item.click()
            time.sleep(5)

            # 2. 혜택/맴버십 페이지로 리다이렉션 확인
            benefit_url = self.driver.current_url
            if "/benefit" in benefit_url:
                self.logger.info(f"혜택/맴버십 페이지로 이동 URL: {benefit_url}")
            else:
                self.logger.info(f"혜택/맴버십 페이지로 이동 실패 URL: {benefit_url}")

            # 3. middlearea 영역 중 스크롤하여 각 div 요소에 포커싱
            contents_section = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "middlearea-contents"))
            )
            div_elements = contents_section.find_elements(By.TAG_NAME, "div")

            div_section = [
                div for div in div_elements
                if div.get_attribute("module-index")
                and div.get_attribute("class")
                and div.get_attribute("class").startswith("bo-modules")
            ]
            div_section_count = len(div_section)
            self.logger.info(f"섹션 수: {div_section_count}")

            # 섹션 정보 출력
            for div in div_section:
                location = div.get_attribute("location")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", div)
                self.logger.info(f"섹션: {location} 정보 찾기 성공")
           
            # 3. PcSubMainBenefitEventSection 섹션 안에 있는 event_link 찾기
            benefit_event_section = self.driver.find_element(By.CSS_SELECTOR, 'div[section-group-id="PcSubMainBenefitOnlineOnlySection"]')
            benefit_link = benefit_event_section.find_element(By.CSS_SELECTOR, 'a.c-link-arr-1.all-view-btn')
            # ActionChains를 사용하여 클릭
            actions = ActionChains(self.driver)
            actions.move_to_element(benefit_link).click().perform()
            time.sleep(5)
           
            # 4. 혜택 페이지 URL 확인
            current_url = self.driver.current_url
            expected_url = "https://www.lguplus.com/benefit-uplus/online-purchase-benefit/ORN0030748"
            if current_url == expected_url:
                self.logger.info("혜택 페이지 URL로 이동하였습니다.")
            else:
                self.logger.info("혜택 페이지 URL이 일치하지 않습니다.")
            time.sleep(5)

            # 5. 탭 리스트 가져오기
            tab_lists = self.driver.find_elements(By.CSS_SELECTOR, 'div.swiper-container.c-tab-slidemenu ul li')
            tab_count = len(tab_lists)
            self.logger.info(f"탭 리스트 갯수: {tab_count}")

            tab_texts = [
                    tab_list.find_element(By.TAG_NAME, 'a').text
                    for tab_list in tab_lists
            ]
            self.logger.info(f"탭 텍스트 리스트: {tab_texts}")

            # 6. 탭 리스트 클릭
            tab_selector = 'div.swiper-container.c-tab-slidemenu ul li'
            tab_count = len(self.driver.find_elements(By.CSS_SELECTOR, tab_selector))

            for i in range(tab_count):
                tab_lists = self.driver.find_elements(By.CSS_SELECTOR, tab_selector)
                tab = tab_lists[i]
                tab_link = tab.find_element(By.TAG_NAME, 'a')
                tab_text = tab_link.text
                self.logger.info(f"탭 클릭: {tab_text}")
                self.driver.execute_script("arguments[0].click();", tab_link)
                
                # 페이지 로딩 대기
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, tab_selector))
                )
                time.sleep(2)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            traceback.print_stack()      

"""
    testcase_10: 이벤트 영역에서 '이벤트 모두 보기' 클릭 후 이벤트 페이지 url 정상 이동 확인
"""
class TestCase10:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def execute(self):
        try: 
            # 1. 혜택/맴버십 메뉴 클릭
            m4_menu_item = self.driver.find_element(By.CSS_SELECTOR, "header > div.header-gnb-wrap > div.header-inner > nav > ul > li.m4")
            m4_menu_item.click()
            time.sleep(2)

            # 2. 혜택/맴버십 페이지로 리다이렉션 확인
            benefit_url = self.driver.current_url
            if "/benefit" in benefit_url:
                self.logger.info(f"혜택/맴버십 페이지로 이동 URL: {benefit_url}")
            else:
                self.logger.info(f"혜택/맴버십 페이지로 이동 실패 URL: {benefit_url}")

            # 3. middlearea 영역 중 스크롤하여 각 div 요소에 포커싱
            contents_section = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "middlearea-contents"))
            )
            div_elements = contents_section.find_elements(By.TAG_NAME, "div")

            div_section = [
                div for div in div_elements
                if div.get_attribute("module-index")
                and div.get_attribute("class")
                and div.get_attribute("class").startswith("bo-modules")
            ]
            div_section_count = len(div_section)
            self.logger.info(f"섹션 수: {div_section_count}")

            # 섹션 정보 출력
            for div in div_section:
                location = div.get_attribute("location")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", div)
                self.logger.info(f"섹션: {location} 정보찾기 성공")

            # 4. 이벤트 섹션 안에 있는 event_link 찾기
            benefit_event_section = self.driver.find_element(By.CSS_SELECTOR, 'div.bo-modules-benefit-event-list > div')
            self.driver.execute_script("arguments[0].style.display = 'block';", benefit_event_section)
            event_link = benefit_event_section.find_element(By.CSS_SELECTOR, 'a.c-link-arr-1.all-view-btn[href="/benefit-event/ongoing"]')
            driver.execute_script("arguments[0].click();", event_link)
            time.sleep(2)

            # 4. 이벤트 페이지 URL 확인
            current_url = self.driver.current_url
            expected_url = "https://www.lguplus.com/benefit-event/ongoing"
            if current_url == expected_url:
                self.logger.info("이벤트 페이지 URL로 이동하였습니다.")
            else:
                self.logger.info("이벤트 페이지 URL이 일치하지 않습니다.")
            time.sleep(5)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            traceback.print_stack()

"""
    testcase_11: 자주 찾는 검색어 항목 텍스트 비교 후 검색창에 '테스트' 검색, 검색 후 '테스트' 로 검색된 게 맞는지 확인
"""
class TestCase11:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def execute(self):
        try:
            # 1. 메뉴 고객지원 클릭
            support = self.driver.find_element(By.ID, "_uid_126")
            self.support_url = support.get_attribute("data-gtm-click-url")
            support.click()
            time.sleep(2)

            if "support" in self.support_url:
                self.logger.info(f"고객지원 페이지로 이동 URL: {self.support_url}")
            else:
                self.logger.info(f"고객지원 페이지로 이동 실패 URL: {self.support_url}")

            # 2. 자주 찾는 검색어 목록 출력
            search_keyword_div = self.driver.find_element(By.CLASS_NAME, "keyword-link")
            keywords = search_keyword_div.find_elements(By.TAG_NAME, "a")
            self.keyword_list = [
                keyword.text for keyword in keywords
            ]
            self.logger.info(self.keyword_list)
            self.keyword_random = random.choice(self.keyword_list)
            # 3. 키워드 리스트에 있는 랜덤값으로 검색어 입력
            search_section = self.driver.find_element(By.CSS_SELECTOR, "div.top-search-wrap > div > div > div.c-inpfield.column-search.search-type2") 
            search_input = search_section.find_element(By.CSS_SELECTOR, "div.c-inpform input.c-inp")
            search_input.send_keys(self.keyword_random)
            search_button = search_section.find_element(By.CSS_SELECTOR, "div.c-inpform button.c-ibtn-find")
            search_button.click()
            time.sleep(2)

            # 4. 키워드 검색 결과로 리다이렉션 성공 여부 확인
            input_value = self.driver.execute_script("return document.querySelector('input.c-inp').value;")
            faq_url = self.driver.current_url
            if input_value == self.keyword_random:
                self.logger.info(f"검색어 '{self.keyword_random}'이(가) 입력되었습니다. URL: {faq_url}")
            else:
                self.logger.warning(f"검색어 입력 실패")

            # 5. 검색 결과 확인
            search_input_value = self.driver.find_element(By.ID, "cfrmSearch-1-3").get_attribute("value")
            element = self.driver.find_element(By.XPATH, "//p[@class='faq-title']/span[@class='color-def']")
            span_text = element.get_attribute('innerHTML').strip()
            self.logger.info(f"입력값: {search_input_value} 검색결과: {span_text}")
            if self.keyword_random == search_input_value == span_text:
                self.logger.info(f"데이터가 일치합니다: {span_text}")
            else:
                self.logger.info(f"데이터가 불일치합니다")

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            traceback.print_stack()


"""
    TestCase12: 검색창에 특수문자 입력 후 결과 정상 노출 확인
"""
class TestCase12:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.special_characters = ''.join(random.choice(string.punctuation) for _ in range(10))

    def execute(self):
        try:
            # 1. 인풋창 클리어 버튼 클릭
            search_section = self.driver.find_element(By.CSS_SELECTOR, "div.c-content-wrap > div:nth-child(1) > div.c-inpfield.column-search.search-type2.flex-end.-mb-8n-2") 
            clear_button = search_section.find_element(By.CSS_SELECTOR, "button.c-btn-clear")
            search_input = search_section.find_element(By.CSS_SELECTOR, "input#cfrmSearch-1-3")
            search_button = search_section.find_element(By.CSS_SELECTOR, "button.c-ibtn-find")
            self.driver.execute_script("arguments[0].click();", clear_button)
            
            # 2. 특수문자 입력 후 검색
            ActionChains(self.driver).move_to_element(search_input).click().perform()
            search_input.send_keys(self.special_characters)
            # search_input.send_keys(Keys.ENTER)
            self.driver.execute_script("arguments[0].click();", search_button)
            time.sleep(5)

            # 3. 키워드 검색 결과로 리다이렉션 성공 여부 확인
            input_value = self.driver.execute_script("return document.querySelector('input.c-inp').value;")
            faq_url = self.driver.current_url
            if input_value == self.special_characters:
                self.logger.info(f"검색어 '{self.special_characters}'이(가) 입력되었습니다. URL: {faq_url}")
            else:
                self.logger.warning(f"검색어 입력 실패")

            self.driver.execute_script("document.getElementById('cfrmSearch-1-3').value = arguments[0];", self.special_characters)
            self.driver.execute_script("arguments[0].click();", search_button)

            # 4. 검색 결과 확인
            search_input_value = self.driver.find_element(By.ID, "cfrmSearch-1-3").get_attribute("value")
            
            element = self.driver.find_element(By.XPATH, "//p[@class='faq-title']/span[@class='color-def']")
            span_text = element.get_attribute('innerHTML').strip()
            decoded_span_text = html.unescape(span_text)
            self.logger.info(f"입력값: {search_input_value} 검색결과: {span_text}")
            if self.special_characters == search_input_value == decoded_span_text:
                self.logger.info(f"데이터가 일치합니다: {decoded_span_text}")
            else:
                self.logger.info(f"데이터가 불일치합니다")
            
            try:
                no_data_element = self.driver.find_element(By.CSS_SELECTOR, "p.h5")
                no_data_text = no_data_element.text
                if no_data_text == "검색 결과가 존재하지 않습니다.":
                    self.logger.info("'검색 결과가 존재하지 않습니다.' 메시지가 확인되었습니다.")
                else:
                    self.logger.info(f"검색 결과: {no_data_text}")
            except NoSuchElementException:
                self.logger.info("'검색 결과가 존재하지 않습니다.' 메시지를 찾을 수 없습니다.")
            time.sleep(5)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            traceback.print_stack()

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.special_characters = ''.join(random.choice(string.punctuation) for _ in range(10))

    def execute(self):
        try:
            # 1. 인풋창 클리어 버튼 클릭ㄴ
            search_section = self.driver.find_element(By.CSS_SELECTOR, "div.c-content-wrap > div:nth-child(1) > div.c-inpfield.column-search.search-type2.flex-end.-mb-8n-2") 
            clear_button = search_section.find_element(By.CSS_SELECTOR, "button.c-btn-clear")
            search_input = search_section.find_element(By.CSS_SELECTOR, "input#cfrmSearch-1-3")
            search_button = search_section.find_element(By.CSS_SELECTOR, "button.c-ibtn-find")
            self.driver.execute_script("arguments[0].click();", clear_button)
            
            # 2. 특수문자 입력 후 검색
            ActionChains(self.driver).move_to_element(search_input).click().perform()
            search_input.send_keys(self.special_characters)
            search_input.send_keys(Keys.ENTER)
            Click(self.driver, self.logger).click(search_button)
            self.driver.execute_script("arguments[0].click();", search_button)
            time.sleep(5)

            # 3. 키워드 검색 결과로 리다이렉션 성공 여부 확인
            input_value = self.driver.execute_script("return document.querySelector('input.c-inp').value;")
            faq_url = self.driver.current_url
            if input_value == self.special_characters:
                self.logger.info(f"검색어 '{self.special_characters}'이(가) 입력되었습니다. URL: {faq_url}")
            else:
                self.logger.warning(f"검색어 입력 실패")

            self.driver.execute_script("document.getElementById('cfrmSearch-1-3').value = arguments[0];", self.special_characters)
            self.driver.execute_script("arguments[0].click();", search_button)

            # 4. 검색 결과 확인
            search_input_value = self.driver.find_element(By.ID, "cfrmSearch-1-3").get_attribute("value")
            
            element = self.driver.find_element(By.XPATH, "//p[@class='faq-title']/span[@class='color-def']")
            span_text = element.get_attribute('innerHTML').strip()
            decoded_span_text = html.unescape(span_text)
            self.logger.info(f"입력값: {search_input_value} 검색결과: {span_text}")
            if self.special_characters == search_input_value == decoded_span_text:
                self.logger.info(f"데이터가 일치합니다: {decoded_span_text}")
            else:
                self.logger.info(f"데이터가 불일치합니다")
            
            try:
                no_data_text = self.driver.execute_script("return arguments[0].textContent;", self.driver.find_element(By.CSS_SELECTOR, "p.h5"))

                if no_data_text == "검색 결과가 존재하지 않습니다.":
                    self.logger.info("'검색 결과가 존재하지 않습니다.' 메시지가 확인되었습니다.")
                else:
                    self.logger.info(f"검색 결과: {no_data_text}")
            except NoSuchElementException:
                self.logger.info("'검색 결과가 존재하지 않습니다.' 메시지를 찾을 수 없습니다.")
            time.sleep(5)

        except Exception as e:
            self.logger.info(f"Test case failed: {e}")
            traceback.print_stack()

# ==================================================================================================

if __name__ == "__main__":
    TestCase01(driver, custom_logger).execute()
    TestCase02(driver, custom_logger).execute()
    TestCase03(driver, custom_logger).execute()
    TestCase04(driver, custom_logger).execute()
    TestCase05(driver, custom_logger).execute()
    TestCase06(driver, custom_logger).execute()
    TestCase07(driver, custom_logger).execute()
    TestCase08(driver, custom_logger).execute()
    TestCase09(driver, custom_logger).execute()
    TestCase10(driver, custom_logger).execute()
    TestCase11(driver, custom_logger).execute()
    TestCase12(driver, custom_logger).execute()

    driver.quit()





