import logging
import json
import re
import os
import sys
import datetime
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from config.config import LOG_LEVEL, LOG_FILE, JSON_FILE, MAX_BYTES, BACKUP_COUNT

class JSONFormatter(logging.Formatter):
    """ 로깅 시스템을 구현한 모듈. JSON 형식, 컬러 출력, 스택트레이스 제어 등의 기능 제공 """
    def format(self, record):
        """ 로그 레코드를 JSON 문자열로 변환하는 메서드 """
        try:
            # ANSI 이스케이프 시퀀스 제거
            ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
            message = ansi_escape.sub('', str(record.msg))

            log_record = {
                "timestamp": self.formatTime(record, self.datefmt),
                "name": record.name,
                "level": record.levelname,
                "message": message,
                "pathname": record.pathname,
                "lineno": record.lineno,
                "funcName": record.funcName
            }
            return json.dumps(log_record, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                "error": f"로그 포맷팅 실패: {str(e)}"
            })

class ColoredFormatter(logging.Formatter):
    """ 로그 메시지에 색상을 추가하는 포맷터 클래스 """
    COLORS = {
        "DEBUG": "\033[92m",    # 초록색
        "INFO": "\033[94m",     # 파란색
        "WARNING": "\033[93m",  # 노란색
        "ERROR": "\033[91m",    # 빨간색
        "CRITICAL": "\033[1;91m" # 굵은 빨간색
    }
    RESET = "\033[0m"
    """ 로그 레코드에 ANSI 색상 코드를 추가하는 메서드 """
    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.msg = f"{color}{record.msg}{self.RESET}"
        return super().format(record)

class NoStacktraceFormatter(logging.Formatter):
    """ 예외 스택트레이스를 로그에서 제외하는 포맷터 클래스 """
    def formatException(self, exc_info):
        """ 예외 정보를 간단한 메시지로만 포맷팅하는 메서드 """
        return str(exc_info[1])

    def format(self, record):
        """ 스택트레이스를 제외하고 로그를 포맷팅하는 메서드 """
        record.exc_text = None
        return super().format(record)

class Logger:
    """ 커스텀 로깅 기능을 제공하는 메인 로거 클래스 """
    def __init__(self, logger_name="Logger", log_level=LOG_LEVEL, log_to_console=True, 
                 log_file=LOG_FILE, json_file=JSON_FILE,
                 max_bytes=MAX_BYTES, backup_count=BACKUP_COUNT, when='midnight',
                 fmt='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S'):
        """ 로거 초기화 및 설정값 지정 """
        
        if not isinstance(log_level, int):
            log_level = getattr(logging, log_level.upper(), logging.INFO)
            
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
        """ 파일, 콘솔, JSON 핸들러를 설정하는 메서드 """
        # 기존 핸들러 제거
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 로그 디렉토리 생성
        for file_path in [self.log_file, self.json_file]:
            log_dir = os.path.dirname(file_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

        # 로그 파일 설정
        log_file = os.path.join(os.getcwd(), self.log_file)
        if self.when:
            file_handler = TimedRotatingFileHandler(
                log_file, when=self.when, backupCount=self.backup_count, 
                encoding='utf-8', atTime=datetime.time(0, 0, 0)
            )
        else:
            file_handler = RotatingFileHandler(
                log_file, mode='a', maxBytes=self.max_bytes, 
                backupCount=self.backup_count, encoding='utf-8'
            )
        
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
        """ 구성된 로거 인스턴스를 반환하는 메서드 """
        return self.logger
    
    def log_execution_status(self, func):
        """ 함수 실행 상태를 로깅하는 데코레이터 메서드 """
        def wrapper(*args, **kwargs):
            try:
                self.logger.info(f"{func.__name__} 실행 시작")
                result = func(*args, **kwargs)
                self.logger.info(f"{func.__name__} 실행 성공")
                return result
            except Exception as e:
                self.logger.error(f"{func.__name__} 실행 중 오류 발생: {str(e)}")
                raise
        return wrapper
    
    def error(self, message):
        """에러 메시지를 로깅하는 메서드"""
        self.logger.error(message)

    def info(self, message):
        """정보 메시지를 로깅하는 메서드"""
        self.logger.info(message)

    def warning(self, message):
        """경고 메시지를 로깅하는 메서드"""
        self.logger.warning(message)

    def debug(self, message):
        """디버그 메시지를 로깅하는 메서드"""
        self.logger.debug(message)

    def critical(self, message):
        """치명적 오류 메시지를 로깅하는 메서드"""
        self.logger.critical(message)

# Logger 인스턴스 생성
custom_logger = Logger().get_logger()
