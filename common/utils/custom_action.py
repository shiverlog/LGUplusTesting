from __future__ import annotations
from typing import Union

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from appium.webdriver.common.touch_action import TouchAction
from typing import Callable, Dict, List, Optional, Union



class CustomAction:
    def __init__(self, driver: WebDriver, duration: int = 250, devices: list[AnyDevice] | None = None) -> None:
        self._driver = driver

    def move_to_element(self, to_element: WebElement) -> ActionChains:

        self.w3c_actions.pointer_action.move_to(to_element)
        self.w3c_actions.key_action.pause()

        return self


class WebElement(SeleniumWebElement,TouchAction):
    _execute: Callable #SeleniumWebElement 상속
    _id: str #SeleniumWebElement 상속
    # _driver: Optional['WebDriver'] #TouchAction 상속
    # _actions: List #TouchAction 상속

    # def __init__(self) -> None:
    #     super().__init__()
    #     self.screen_width=self.driver.execute_script("return screen.availWidth")
    #     self.screen_height=self.driver.execute_script("return screen.availHeight")

    

    def re_click(self) -> None:
        """
        2023.11.06 - Iphone 12 pro max 단말 요소 잘못 클릭 개선
        """

        loc=self.location
        size=self.size
        el_x=loc.get('x') # 클릭할 요소 좌표 X
        el_y=loc.get('y') # 클릭할 요소 좌표 y
        el_width=size.get('width') # 클릭할 요소 크기 Width
        el_height=size.get('height') # 클릭할 요소 크기 Height

        # device screen width/height
        screen_width=self.driver.execute_script("return screen.availWidth")
        screen_height=self.driver.execute_script("return screen.availHeight")
        print(f"screen_width -> {screen_width}")
        print(f"screen_height -> {screen_height}")
        
        # windows width/height
        windows_width=self.driver.get_window_size().get('width')
        windows_height=self.driver.get_window_size().get('height')
        # self.switch_view('NATIVE_APP') # Native_APP 컨텍스트로 변경
        
        # # X/Y = 요소 중앙 좌표 * 스크린 사이즈와 윈도우 사이즈 크기 계산값
        X=int(int(el_x+el_width/2.0)*(screen_width*1.0/windows_width))
        Y=int(int(el_y+el_height/2.0)*(screen_height*1.0/windows_height))

        print(f"X -> {X}")
        print(f"Y -> {Y}")

        super().tap(None,X,Y).perform()
        # self.app_action.tap(None,X,Y).perform()
        



