# -*- coding: utf-8 -*-
"""
| type(8) | code(8) |    checksum(16)   |
|       id(16)      |      seq(16)      |

(0, 0) 回应报文，探测到了，Yeah，上报
(8, 0) 有人在 ping 你，Nooo，丢弃
(3, 3) 端口不可达，因此主机存在，探测到了（？？
# 因为用 icmp 所以不存在这个问题吧
(11, 0) TTL=1，传输终了
"""
import struct
import socket
import select
import argparse
import sys
import time
import random


"""
将校验和字段设置为0
每16个bit(即2个字节)组成一个数，相加，如果超过16个bit，把超过的高位值加到这16个bit值上，得到的新值再和下一个值相加
如果最后还剩8个bit值，不能简单的加到低位，要把这8个bit当成高位值，再用0填充一个16个bit值，相加
最后取反，填充到校验和字段
"""
def make_checksum(str_):
    str_ = bytearray(str_)
    csum = 0
    countTo = (len(str_) // 2) * 2

    for count in range(0, countTo, 2):
        thisVal = str_[count+1] * 256 + str_[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff

    if countTo < len(str_):
        csum = csum + str_[-1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return socket.htons(answer)


def build_pack():
    checksum = 0
    id = random.randint(0, 0xffff) # 16 位随便什么数字作为 id
    seq = 1

    header = struct.pack('bbHHh', 8, 0, checksum, id, seq)
    data = struct.pack('d', time.time())
    pack = header + data
    checksum = make_checksum(pack)

    header = struct.pack('bbHHh', 8, 0, checksum, id, seq)
    return header + data


def resolve_addr(addr):
    """
    @raise socket.error
    """
    host, aliases, addrs = socket.gethostbyaddr(addr)
    return host, addrs[0]


def probe(target, ttl, timeout, retry):
    result = []
    for __ in range(retry):
        icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        icmp.setsockopt(socket.SOL_IP, socket.IP_TTL, struct.pack('I', ttl))
        icmp.settimeout(timeout)

        pack = build_pack()
        # print(pack)

        icmp.sendto(pack, (target, 0))

        a = time.time()
        select.select([icmp], [], [], timeout)
        b = time.time()

        if b - a >= timeout:
            continue

        resp, info = icmp.recvfrom(1024)
        icmp.close()

        addr, port = info
        header = resp[20:28]
        type, code, check_, id_, seq_ = struct.unpack("bbHHh", header)
        
        if (type, code) == (11, 0) \
        or (type, code) == (0, 0):
            result.append((addr, b-a))
        else:
            continue
    
    return result


def main(target, ttl, timeout, retry):
    try:
        target = socket.getaddrinfo(target, 'http')[0][-1][0]
        print('target', target)
    except socket.gaierror:
        print('Resolve fail')
        exit()

    for t in range(1, ttl+1):
        print(f' === TTL {t:>2} ===')

        result = probe(target, t, timeout, retry)
        if result:
            for i in result:
                addr, elapse = i
                try:
                    host, addr = resolve_addr(addr)
                    print(f'{host} ({addr})  {elapse*1000:.3f} ms')
                except:
                    print(f'{addr}  {elapse*1000:.3f} ms')
                if addr == target:
                    print('REACH')
                    exit()

                


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='traceroute')
    parser.add_argument('target')
    parser.add_argument('-l', '--ttl', type=int, default=30, required=False,
        help='最高 ttl，以秒(s)为计 [30]')
    parser.add_argument('-t', '--timeout', type=int, default=3, required=False,
        help='超时时间，以秒(s)为计 [3]')
    parser.add_argument('-r', '--retry', type=int, default=3, required=False,
        help='每个 ttl 探测次数 [3]')
    args = parser.parse_args()

    main(args.target, args.ttl, args.timeout, args.retry)
