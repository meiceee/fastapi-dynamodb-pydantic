import time
import uuid


def generate_current_timestamp():
    """UNIXTIMEを生成する関数"""
    return str(int(time.time()))


def generate_uuid():
    """UUIDを生成する関数"""
    return str(uuid.uuid4())
