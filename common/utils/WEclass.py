
# 커스텀 클래스 전용 import
from typing import Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from appium.webdriver.common.touch_action import TouchAction
from typing import Callable, Dict, List, Optional, Union
import time



# 기존 WebElement(변경 후 클래스명 AppiumWebElement) 상속
class WebElement(AppiumWebElement):
    _execute: Callable #SeleniumWebElement 상속
    _id: str #SeleniumWebElement 상속

    # def re_click2(self) -> None|WebElement:
    #     self.click()

    # def re_double_click2(self) -> None|WebElement:
    #     self.click()
        
    def re_click(self) -> None|WebElement:
        """
        2023.11.06 - Iphone 12 pro max 단말 요소 잘못 클릭 개선
        """
        self._parent=self.parent
        # self._action=TouchAction(self._parent)
        if self.is_displayed() or self.is_enabled():
            pass
        else:
            raise Exception("NoSuchElementError")

        print(f"self -> {self.get_property('outerHTML')}")
        

        loc=self.location
        size=self.size
        el_x=loc.get('x') # 클릭할 요소 좌표 X
        el_y=loc.get('y') # 클릭할 요소 좌표 y
        # el_y= int(self._parent.execute_script('let offsetTop=0; el=arguments[0]; while(el){offsetTop+=el.offsetTop; el=el.offsetParent;} return offsetTop;',self))
        # print(f"el_x -> {el_x}")
        # print(f"el_y -> {el_y}")

        el_width=size.get('width') # 클릭할 요소 크기 Width
        el_height=size.get('height') # 클릭할 요소 크기 Height
        # print(f"el_width -> {el_width}")
        # print(f"el_height -> {el_height}")

        # device screen width/height
        screen=self._parent.get_screen_size()
        # screen_width=screen.get('width')
        screen_height=screen.get('height')
        # print(f"screen_width -> {screen.get('width')}")
        # print(f"screen_height -> {screen.get('height')}")

        # windows width/height
        windows=self._parent.get_window_size()
        # windows_width=windows.get('width')
        windows_height=windows.get('height')
        # print(f"screen_height*1.0/windows_height")


        # systembar2=int(round((screen_height - windows_height)/2)) # TODO 상단 systembar의 정확한 비율을 확인하는 방법이 필요함
        # print("---------------------------------")
        # print(systembar2)
        # print("---------------------------------")
        systembar=50 # TODO 상단 systembar의 정확한 비율을 확인하는 방법이 필요함
        # print(f"screen_height -> {screen.get('height')}")
        
        # X/Y = 요소 중앙 좌표 * 스크린 사이즈와 윈도우 사이즈 크기 계산값
        X=int(el_x+el_width/2.0)
        Y=int(el_y+el_height/2.0) + systembar
        # X=int(int(el_x+el_width/2.0)*(screen_width*1.0/windows_width))
        # Y=int(int(el_y+el_height/2.0)) + systembar

        print(f"X -> {X}")
        print(f"Y -> {Y}")

        # self._action.tap(None,X,Y).perform()
        self._parent.execute_script('mobile: tap',{'x':X,'y':Y})
        return self
    
    def re_double_click2(self) -> None|WebElement:
        """
        2023.11.06 - Iphone 12 pro max 단말 요소 잘못 클릭 개선
        """
        self._parent=self.parent
        # self._action=TouchAction(self._parent)
        if self.is_displayed() or self.is_enabled():
            pass
        else:
            raise Exception("NoSuchElementError")

        print(f"self -> {self.get_property('outerHTML')}")
        

        loc=self.location
        size=self.size
        el_x=loc.get('x') # 클릭할 요소 좌표 X
        el_y=loc.get('y') # 클릭할 요소 좌표 y
        # el_y= int(self._parent.execute_script('let offsetTop=0; el=arguments[0]; while(el){offsetTop+=el.offsetTop; el=el.offsetParent;} return offsetTop;',self))
        # print(f"el_x -> {el_x}")
        # print(f"el_y -> {el_y}")

        el_width=size.get('width') # 클릭할 요소 크기 Width
        el_height=size.get('height') # 클릭할 요소 크기 Height
        # print(f"el_width -> {el_width}")
        # print(f"el_height -> {el_height}")

        # device screen width/height
        screen=self._parent.get_screen_size()
        # screen_width=screen.get('width')
        screen_height=screen.get('height')
        # print(f"screen_width -> {screen.get('width')}")
        # print(f"screen_height -> {screen.get('height')}")

        # windows width/height
        windows=self._parent.get_window_size()
        # windows_width=windows.get('width')
        windows_height=windows.get('height')
        # print(f"screen_height*1.0/windows_height")


        # systembar2=int(round((screen_height - windows_height)/2)) # TODO 상단 systembar의 정확한 비율을 확인하는 방법이 필요함
        # print("---------------------------------")
        # print(systembar2)
        # print("---------------------------------")
        systembar=50 # TODO 상단 systembar의 정확한 비율을 확인하는 방법이 필요함
        # print(f"screen_height -> {screen.get('height')}")
        
        # X/Y = 요소 중앙 좌표 * 스크린 사이즈와 윈도우 사이즈 크기 계산값
        X=int(el_x+el_width/2.0)
        Y=int(el_y+el_height/2.0) + systembar
        # X=int(int(el_x+el_width/2.0)*(screen_width*1.0/windows_width))
        # Y=int(int(el_y+el_height/2.0)) + systembar

        print(f"X -> {X}")
        print(f"Y -> {Y}")

        # self._action.tap(None,X,Y).perform()
        self._parent.execute_script('mobile: doubleTap',{'x':X,'y':Y})
        return self

