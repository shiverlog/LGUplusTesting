from base.base import Base
from pages.login import TestCase01
from pages.main import TestCase02, TestCase03
from pages.GNB_m1 import TestCase04, TestCase05, TestCase06
from pages.GNB_m3 import TestCase07, TestCase08
from pages.GNB_m4 import TestCase09, TestCase10
from pages.GNB_m5 import TestCase11, TestCase12
import time

class TestExecutor(Base):
    """ 테스트 케이스 실행을 관리하는 실행기 클래스 """
    def __init__(self):
        super().__init__()  # Base 클래스 초기화
        self.test_cases = []
        self.setup_test_cases()

    def setup_test_cases(self):
        """테스트 케이스 초기화"""
        self.test_cases = [
            # 테스트 케이스 클래스 추가
            # TestCase01(self.driver, self.logger),
            # TestCase02(self.driver, self.logger),

            TestCase03(self.driver, self.logger), 
            # TestCase04(self.driver, self.logger),
            # TestCase05(self.driver, self.logger),
            # TestCase06(self.driver, self.logger),
            # TestCase07(self.driver, self.logger),
            # TestCase08(self.driver, self.logger),
            # TestCase09(self.driver, self.logger),
            # TestCase10(self.driver, self.logger),
            # TestCase11(self.driver, self.logger),
            # TestCase12(self.driver, self.logger)
        ]

    def run_tests(self):
        """모든 테스트 케이스 실행"""
        try:
            for test_case in self.test_cases:
                try:
                    self.logger.info(f"===================================테스트 케이스 실행 시작: {test_case.__class__.__name__}===================================")
                    test_case.execute()
                    self.logger.info(f"===================================테스트 케이스 실행 완료: {test_case.__class__.__name__}===================================")
                    time.sleep(2)
                except Exception as e:
                    self.logger.error(f"===================================테스트 케이스 실행 실패: {test_case.__class__.__name__} - {str(e)}===================================")
                    self.setup_method(None)  # 실패 시 환경 재설정

        except Exception as e:
            self.logger.error(f"===================================테스트 실행 중 오류 발생: {str(e)}===================================")
        finally:
            self.teardown_method(None)

def main():
    executor = TestExecutor()
    executor.run_tests()

if __name__ == "__main__":
    main()