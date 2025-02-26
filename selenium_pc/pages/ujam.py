from base.webdriver import WebDriver
from common.function import Function
from common.debug import Debug


class UjamPage():
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)


    def ujam(self):
        self.FC.gotoHome()

        try:

            self.FC.movepage(self.FC.var['benefit_el']['benefit'],self.FC.var['ujam_el']['ujam'],address=self.FC.var['ujam_el']['url'])   # 상단 햄버거 버튼 클릭 동작
            self.FC.wait_loading()

        except  Exception :
            self.DBG.print_dbg("유잼 페이지 정상 노출 및 기능 동작 확인",False)
            return False

        else :
            self.DBG.print_dbg("유잼 페이지 정상 노출 및 기능 동작 확인")
            return True


if __name__ == "__main__":
    driver = WebDriver()
    fc = Function(driver)
    ujam = UjamPage(driver, fc)

    ujam.ujam()
