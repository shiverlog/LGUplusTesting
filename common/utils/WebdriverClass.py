    def get_screen_size(self) -> dict:
            """
            커스텀 함수
            디스플레이 사이즈 가져오기
            :Usage:
                ::
                    driver.get_screen_size()
            """
            # if windowHandle != "current":
            #     warnings.warn("Only 'current' window is supported for W3C compatible browsers.")
            command = Command.W3C_EXECUTE_SCRIPT
            converted_args = []
            script="return screen.availWidth"
            screen_width=self.execute(command, {"script": script, "args":converted_args})["value"]
            script="return screen.availHeight"
            screen_height=self.execute(command, {"script": script,"args":converted_args})["value"]
            if type(screen_width) != int:
                raise WebDriverException("screen_width를 가져오지 못했습니다.")
            if type(screen_height) != int:
                raise WebDriverException("screen_height를 가져오지 못했습니다.")
            return {"width":screen_width, "height":screen_height}  
        
    def get_current_scrollTop(self, windowHandle: str = "current") -> dict:
        """
        커스텀 함수
        :Usage:
            ::
                driver.get_current_scrollTop()
        """
        # if windowHandle != "current":
        #     warnings.warn("Only 'current' window is supported for W3C compatible browsers.")
        command = Command.W3C_EXECUTE_SCRIPT
        converted_args = []
        script="return document.documentElement.scrollTop;"
        scrollTop=self.execute(command, {"script": script, "args":converted_args})["value"]
        if scrollTop == 0:
            scrollTop = 0
        elif type(scrollTop) != int:
            raise WebDriverException("screen_height를 가져오지 못했습니다.")
        return {"scrollTop":scrollTop}  