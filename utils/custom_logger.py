
import logging 
import json
import re
import os
import sys
import datetime
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from config import LOG_LEVEL, LOG_FILE, JSON_FILE, MAX_BYTES, BACKUP_COUNT
from contextlib import suppress

""" 
    automation.json: JSON 파일에 로그 기록
    class JSONFormatter(logging.Formatter): 로그 레코드를 JSON 형식으로 변환
    class ColoredFormatter(logging.Formatter): 로그 메시지에 색상 추가
    class Logger: 사용자 정의 로거 클래스 
    class NoStacktraceFormatter(logging.Formatter): 예외 스택 트레이스를 로그에 기록하지 않음
"""
class JSONFormatter(logging.Formatter):
    def format(self, record):
        # ANSI 이스케이프 시퀀스 제거
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        message = ansi_escape.sub('', record.msg)

        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": message,
            "pathname": record.pathname,
            "lineno": record.lineno
        }
        return json.dumps(log_record, ensure_ascii=False)

class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[92m",    # 초록색
        "INFO": "\033[94m",     # 파란색
        "WARNING": "\033[93m",  # 노란색
        "ERROR": "\033[91m",    # 빨간색
        "CRITICAL": "\033[1;91m" # 굵은 빨간색
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.msg = f"{color}{record.msg}{self.RESET}"
        return super().format(record)

class NoStacktraceFormatter(logging.Formatter):
    def formatException(self, exc_info):
        return str(exc_info[1])

    def format(self, record):
        record.exc_text = None
        return super().format(record)

class Logger:
    def __init__(self, logger_name="Logger", log_level=LOG_LEVEL, log_to_console=True, 
                 log_file=LOG_FILE, json_file=JSON_FILE,
                 max_bytes=MAX_BYTES, backup_count=BACKUP_COUNT, when='midnight',
                 fmt='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        self.log_to_console = log_to_console
        self.log_file = log_file
        self.json_file = json_file
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.when = when
        self.fmt = fmt
        self.datefmt = datefmt
        self._setup_handlers()

    def _setup_handlers(self):
        # 기존 핸들러 제거
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 로그 파일 설정
        log_file = os.path.join(os.getcwd(), self.log_file)
        if self.when:
            file_handler = TimedRotatingFileHandler(
                log_file, when=self.when, backupCount=self.backup_count, encoding='utf-8', atTime=datetime.time(0, 0, 0)
            )
        else:
            file_handler = RotatingFileHandler(log_file, mode='a', maxBytes=self.max_bytes, backupCount=self.backup_count, encoding='utf-8')
        file_handler.setLevel(self.logger.level)
        file_formatter = NoStacktraceFormatter(self.fmt, datefmt=self.datefmt)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # 콘솔 핸들러 설정
        if self.log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.logger.level)
            console_formatter = ColoredFormatter('%(name)s - %(levelname)s: %(message)s')
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

        # JSON 핸들러 추가
        json_file = os.path.join(os.getcwd(), self.json_file)
        json_handler = logging.FileHandler(json_file, mode='a', encoding='utf-8')
        json_handler.setLevel(self.logger.level)
        json_formatter = JSONFormatter()
        json_handler.setFormatter(json_formatter)
        self.logger.addHandler(json_handler)

    def get_logger(self):
        return self.logger
    
    def log_execution_status(self, func):
        def wrapper(*args, **kwargs):
            self.logger.info(f"{func.__name__} 실행 시작")
            with suppress(Exception):
                result = func(*args, **kwargs)
                self.logger.info(f"{func.__name__} 실행 성공")
                return result
            self.logger.error(f"{func.__name__} 실행 중 오류 발생")
        return wrapper

# Logger 인스턴스 생성
logger = logging.getLogger(__name__)