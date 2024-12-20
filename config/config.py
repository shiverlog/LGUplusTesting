import logging
import os

# 로그 레벨
LOG_LEVEL = logging.DEBUG
LOG_FILE = "automation.log"
JSON_FILE = "automation.json"
MAX_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# 스크린샷
SCREENSHOT_DIR = "./screenshots"

# 테스트 대상 URL
BASE_URL = "https://www.lguplus.com"

# 대기시간
IMPLICIT_WAIT = 10  # 암묵적
EXPLICIT_WAIT = 20  # 명시적

# 테스트 계정 정보 sysdm.cpl
USERNAME = os.getenv("UPLUS_ID")
PASSWORD = os.getenv("UPLUS_PW")