from behave import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os

@given('U+ 웹사이트에 접속한다')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.uplus.com/")

@when('"U+ID" 로그인 버튼을 클릭한다')
def step_impl(context):
    uplus_id_button = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'section.new-mem-section ul.iconLoginList li:nth-of-type(4) button'))
    )
    uplus_id_button.click()
    time.sleep(2)

@then('"/login/onid-login" 페이지로 이동한다')
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        EC.url_contains("/login/onid-login")
    )
    Uplus_login_url = context.driver.current_url
    assert "/login/onid-login" in Uplus_login_url, f"U+ 로그인 페이지로 이동 실패 URL: {Uplus_login_url}"

@when('아이디와 비밀번호를 입력한다')
def step_impl(context):
    uplus_id = os.getenv('UPLUS_ID')
    uplus_pw = os.getenv('UPLUS_PW')

    id_input = context.driver.find_element(By.ID, "username-1-6")
    id_input.send_keys(uplus_id)
    pw_input = context.driver.find_element(By.ID, "password-1")
    pw_input.send_keys(uplus_pw)
    time.sleep(5)

@when('"로그인" 버튼을 클릭한다')
def step_impl(context):
    login_button = context.driver.find_element(By.CSS_SELECTOR, 'button.c-btn-solid-1.nm-login-btn')
    login_button.click()
    time.sleep(2)

@then('로그인이 성공한다')
def step_impl(context):
    # 로그인 성공 여부를 확인하는 코드 추가 (예: 특정 element 존재 여부 확인)
    assert context.driver.find_element(By.CSS_SELECTOR, '요소'), "로그인 실패" # 성공 조건에 맞는 요소로 변경 필요