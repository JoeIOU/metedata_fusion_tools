#####guid.py
# Twitter's Snowflake algorithm implementation which is used to generate distributed IDs.
# https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala

import time
import socket
import logging

from common.exception import InvalidSystemClock

# 64位ID的划分
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# 最大取值计算
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 移位偏移计算
WOKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# Twitter元年时间戳
TWEPOCH = 1288834974657
worker = None

worker_id = None
datacenter_id = None


# logger = logging.getLogger('http.app')


class IdWorker(object):
    """
    用于生成IDs
    """

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 起始序号
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            logging.error('clock is moving backwards. Rejecting requests until {}'.format(self.last_timestamp))
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | \
                 (self.worker_id << WOKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


def get_guid(id_num=1):
    global worker, datacenter_id, worker_id
    if datacenter_id is None or worker_id is None:
        datacenter_id, worker_id = get_datacenter_worker_id_by_ip()
    if worker is None:
        worker = IdWorker(datacenter_id=datacenter_id, worker_id=worker_id, sequence=0)
    ids = []
    if id_num <= 0:
        id_num = 1
    for i in range(id_num):
        new_id = worker.get_id()
        ids.append(new_id)
    return ids


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    ip = "0:0:0:0"
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_datacenter_worker_id_by_ip():
    worker_id = 1
    datacenter_id = 1
    try:
        ip = get_host_ip()
        ip2int = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
        if ip is not None:
            iip = ip2int(ip)
            worker_id = iip % 31
            datacenter_id = iip % 30

        return datacenter_id, worker_id
    except Exception as e:
        return datacenter_id, worker_id


if __name__ == '__main__':
    # 测试效率
    # import datetime
    # worker = IdWorker(datacenter_id=1, worker_id=1, sequence=0)
    # ids = []
    # start = datetime.datetime.now()
    # for i in range(100):
    #     new_id = worker.get_id()
    #     ids.append(new_id)
    # end = datetime.datetime.now()
    # spend_time = end - start
    # print(spend_time, len(ids), len(set(ids)))
    # print(ids)
    ids = get_guid(100)
    print(ids)
