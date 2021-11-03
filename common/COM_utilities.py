import os
import time
from functools import wraps
from time import perf_counter, sleep

from common.COM_path import path_resource
from common.my_log import mylog


def clock(type=None):  # 计时器
    """stop结束返回时间"""
    global start_time
    if type == "stop":
        spendtime = '%.2f' % (perf_counter() - start_time)
        print("花费时间{}秒:".format(spendtime))
        return spendtime
    else:
        start_time = perf_counter()
def timethis(func):
    """函数运行计时器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return r
    return wrapper

def time_difference(time_start):
    """计算时间差"""
    time_end = time.time()  # 结束计时
    time_c = time_end - time_start  # 运行所花时间
    return time_c

def fileCompare(filepath, size=10):
    """文件比较"""
    fileName = os.path.join(path_resource, filepath)
    filebool = os.path.exists(fileName)
    if filebool:
        mysize = os.path.getsize(fileName)
        if mysize > size:
            pass
            # print("文件大小正常")
        else:
            filebool = False
    return filebool

def report(result, type, chapter, des, roleID=None, chat=None):
    if not result:
        if type==0:
            content = "{0}-->【{1}异常】-【角色{2}】-【对白{3}】：{4}".format(chapter, type, roleID, chat, des)
            mylog.error(content)
        if chat:
            content = "{0}-->【{1}异常】-【角色{2}】-【对白{3}】：{4}".format(chapter, type, roleID, chat, des)
            mylog.error(content)
        else:
            content = "{0}-->【{1}异常】-【角色{2}】:{3}".format(chapter, type, roleID, des)
            mylog.error(content)
