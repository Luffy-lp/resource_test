# coding: utf-8
# !/usr/bin/env python
import queue
import threading

# 定义同时处理任务数
from common.COM_utilities import clock
from date.Chapters_data import MyData
from check.check import Check

queue = queue.Queue(maxsize=100)


# 生成任务列表


# 把任务放入队列中
class Producer(threading.Thread):
    def __init__(self, name, queue):
        self.__name = name
        self.__queue = queue
        super(Producer, self).__init__()

    def run(self):
        print("长度：",len(MyData.check_list))
        for bookchapter in MyData.check_list:
            print("检查的章节:",bookchapter)
            self.__queue.put(bookchapter)


# 线程处理任务
class Consumer(threading.Thread):
    def __init__(self, name, queue):
        self.__name = name
        self.__queue = queue
        super(Consumer, self).__init__()

    def run(self):
        while True:
            ip = self.__queue.get()
            print('Consumer name: %s' % (self.__name))
            myCheck(ip)
            self.__queue.task_done()


# def consumer_process(ip):
#     time.sleep(1)
#     print(ip)

def myCheck(bookchapter):
    cls_instance = Check(bookchapter)
    cls_instance.getCheckList(bookchapter)


def startConsumer(thread_num):
    t_consumer = []
    for i in range(thread_num):
        c = Consumer(i, queue)
        c.setDaemon(True)
        c.start()
        t_consumer.append(c)
    return t_consumer


def main(threadAmount):
    p = Producer("Producer task0", queue)  # 把任务放入队列中
    p.setDaemon(True)  # setDaemon守护线程
    p.start()  # 启动多线程
    startConsumer(threadAmount)
    # 确保所有的任务都生成
    p.join()
    # 等待处理完所有任务
    queue.join()


if __name__ == '__main__':
    clock()
    main(MyData.checkConf["threadAmount"])
    clock("stop")
    print('------end-------')
    input('Press Enter to exit...')
