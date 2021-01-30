
# #####logger.py
# -*- coding:utf-8 -*-
import logging
import logging.handlers
import datetime,os

_log = None

#日志功能初始化
def init(log_format, log_format_error, log_level, log_path, env, date_format):
    global _log
    if _log is not None:
        return
    #dev环境，只打印控制台信息
    if env == "dev":
        logging.basicConfig(level=log_level, format=log_format, datefmt=date_format)
        _log = logging
        return _log
    #其他环境，写入到日志文件
    else:
        logger = logging.getLogger('mylogger')
        logger.setLevel(log_level)
        #logging.basicConfig(filename=__C.LOG_FILE, level=__C.LOG_LEVEL, format=__C.LOG_FORMAT, datefmt=__C._TIME_FORMAT)
        
        rf_handler = logging.handlers.TimedRotatingFileHandler(os.path.join(log_path, 'all.log'), when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0), encoding='utf-8')
        rf_handler.setFormatter(logging.Formatter(log_format))
        #rf_handler.encoding="utf-8"
        
        f_handler = logging.FileHandler(os.path.join(log_path, 'error.log'), encoding='utf-8')
        f_handler.setLevel(logging.ERROR)
        #f_handler.encoding="utf-8"
        f_handler.setFormatter(logging.Formatter(log_format_error))
        
        logger.addHandler(rf_handler)
        logger.addHandler(f_handler)
        _log = logger
        return _log

