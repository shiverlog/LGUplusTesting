import pytest
from selenium.webdriver.common.by import By
from base.base import Base, LocatorLoader
from utils import exception_handler as eh
from utils.custom_utils import *

@pytest.fixture(scope="module")
def driver_and_logger():
    """웹드라이버 및 로거를 설정하는 Fixture"""
    base = Base()
    driver = base.driver
    logger = base.logger
    yield driver, logger
    base.quit_driver()

@pytest.fixture(scope="function")
def test_setup(driver_and_logger):
    """각 테스트 실행 전 기본 설정"""
    driver, logger = driver_and_logger
    locators = LocatorLoader.load_locators('main')
    by_type = Base().get_by_type("css")
    return driver, logger, locators, by_type

def test_case_02(test_setup):
    """메인 페이지 KV 영역 테스트 케이스"""
    driver, logger, locators, by_type = test_setup
    try:
        find_visible_sections(driver, by_type, locators, "메인페이지")
        show_elements_text(driver, by_type, locators['kv_section_img'], "src", "KV영역 이미지")
    except Exception as e:
        eh.exception_handler(driver, e, "KV 영역 테스트 실패")
        pytest.fail("KV 영역 테스트 실패")

def test_case_03(test_setup):
    """기기 추천 영역 테스트 케이스"""
    driver, logger, locators, by_type = test_setup
    try:
        move_to_element(driver, by_type, locators['device_section'], "기기추천 영역")
        select_tab, select_tab_text = select_random_item(driver, by_type, locators['device_section'] + " .tab-wrap ul li a", "기기추천")
        click(driver, select_tab, f"기기추천 {select_tab_text}")
        active_list = " div.recomm-tabcon[style*=\"display: block;\"] ul li a"
        select_device, select_device_text = select_random_item(driver, by_type, locators['device_section'] + active_list, f"기기추천 {select_tab_text}")
        click(driver, select_device, f"기기추천 {select_tab_text} {select_device_text}")
        page_redirect_confirm(driver, by_type, select_device, f"{select_device_text} 상세")
        detail_device_name = get_text(driver, by_type, " div.device-info-area > h2.title-main", "기기명")
        compare_values(select_device_text, detail_device_name, "기기명")
    except Exception as e:
        eh.exception_handler(driver, e, "기기 추천 영역 테스트 실패")
        pytest.fail("기기 추천 영역 테스트 실패")
