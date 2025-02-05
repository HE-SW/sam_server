import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger() -> logging.Logger:
    # 로그 레벨 설정
    logger: logging.Logger = logging.getLogger("my_api_logger")
    logger.setLevel(logging.INFO)

    # 로그 저장 경로 설정
    log_file_path: str = os.path.join('logs', 'api.log')
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # 로그 파일 핸들러 설정
    file_handler: logging.handlers.BaseRotatingHandler = RotatingFileHandler(log_file_path, maxBytes=1048576, backupCount=5)
    formatter: logging.Formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


# 로거 인스턴스 생성
api_logger: logging.Logger = setup_logger()
