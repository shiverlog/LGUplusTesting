import logging, os

# 로그 레벨
LOG_LEVEL = logging.INFO
LOG_FILE = os.path.join("logs", "automation.log")
JSON_FILE = os.path.join("logs", "automation.json")
MAX_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# 재시도 횟수
RETRY_COUNT = 3

# 스크린샷
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")

# 테스트 대상 URL
BASE_URL = "https://www.lguplus.com"

# 대기시간
IMPLICIT_WAIT = 10  # 암묵적
EXPLICIT_WAIT = 20  # 명시적

# 테스트 계정 정보 sysdm.cpl
USERNAME = os.getenv("UPLUS_ID")
PASSWORD = os.getenv("UPLUS_PW")