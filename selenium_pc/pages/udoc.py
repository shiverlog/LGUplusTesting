
from base.webdriver import WebDriver
from common.function import Function
from common.debug import Debug


class UdocPage():
    def __init__(self,WebDriver:WebDriver,FC:Function):
        self.FC=FC
        self.DBG=Debug(WebDriver)


    def udoc(self):
        self.FC.gotoHome()

        try:
            self.FC.move_to_click(self.FC.loading_find_xpath_pre(self.FC.var['udoc_el']['udoc']))

        except  Exception :
            self.DBG.print_dbg("유독 페이지 정상 노출 및 기능 동작 확인",False)
            return False

        else :
            self.DBG.print_dbg("유독 페이지 정상 노출 및 기능 동작 확인")
            return True



if __name__ == "__main__":
    driver = WebDriver()
    fc = Function(driver)
    udoc = UdocPage(driver, fc)

    udoc.udoc()
