#coding:utf-8

from time import time
from gevent import joinall
from gevent import monkey
from gevent import spawn

monkey.patch_all()

from json import dumps
from requests import post

from server.server import SERVER_FULL_ADDRES


HEADERS = {'Content-type': 'application/json'}

# очередь для сбора данных
stat_queue = []


def work(url, req_type, count=100):
    u"""отправка POST-запросов."""
    data = {'req_type': req_type, 'action': 'ping'}
    address = r"%s/%s" % (SERVER_FULL_ADDRES, url)
    for c in xrange(count):
        t1 = time()
        response = post(address, data=dumps(data), headers=HEADERS)
        response.close()
        dt = time() - t1
        stat_queue.append(dt)


def do_spawn_jobs(url, count):
    t1 = spawn(work, url=url, req_type='foo', count=count)
    t2 = spawn(work, url=url, req_type='bar', count=count)
    t3 = spawn(work, url=url, req_type='xxx', count=count)
    t4 = spawn(work, url=url, req_type='yyy', count=count)
    t5 = spawn(work, url=url, req_type='zzz', count=count)
    joinall([t1, t2, t3, t4, t5], timeout=60)
    if stat_queue:
        return sum(stat_queue) / len(stat_queue)

if __name__ == '__main__':
    print do_spawn_jobs('async_ping', 1000)
    print do_spawn_jobs('sync_ping', 1000)