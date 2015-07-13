#!/usr/bin/env python
#coding:utf-8

import os.path
import sys

# для того, чтобы был виден модуль settings.py
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from time import time
from threading import Thread
from Queue import Queue
from json import dumps
from requests import post

from settings import SERVER_FULL_ADDRES
from settings import TORNADO_SERVER
from settings import NATIVE_SERVER

HEADERS = {'Content-type': 'application/json'}

# очередь для сбора данных
stat_queue = Queue()


def get_server_type():
    u"""Возвращает тип сервера (Tornado, Native, etc.)."""
    data = {}
    address = r"%s/type" % SERVER_FULL_ADDRES
    response = post(address, data=dumps(data), headers=HEADERS)
    result = response.json()
    response.close()
    if result.get('status') == 'ok':
        return result.get('server_type')


def work(url, req_type, count=100):
    u"""отправка POST-запросов."""
    data = {'req_type': req_type, 'action': 'ping'}
    address = r"%s/%s" % (SERVER_FULL_ADDRES, url)
    for c in xrange(count):
        t1 = time()
        response = post(address, data=dumps(data), headers=HEADERS)
        response.close()
        dt = time() - t1
        stat_queue.put(dt)


def do_threading_jobs(url, count):
    u"""Запустить запросы и подождать их."""
    # инициализация
    t1 = Thread(target=work, args=(url, 'foo', count))
    t2 = Thread(target=work, args=(url, 'bar', count))
    t3 = Thread(target=work, args=(url, 'xxx', count))
    t4 = Thread(target=work, args=(url, 'yyy', count))
    t5 = Thread(target=work, args=(url, 'zzz', count))
    # запуск
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    # ожидание
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()


def analyse():
    u"""Анализ статистики запросов."""
    data = []
    while not stat_queue.empty():
        data.append(stat_queue.get_nowait())
    if data:
        return sum(data) / len(data)


if __name__ == '__main__':

    server_type = get_server_type()
    if server_type == TORNADO_SERVER:
        do_threading_jobs('async_ping', 1000)
        print " async: mean latency: %s sec" % analyse()
        do_threading_jobs('sync_ping', 1000)
        print "  sync: mean latency: %s sec" % analyse()
    elif server_type == NATIVE_SERVER:
        do_threading_jobs('ping', 1000)
        print "  sync ping: mean latency: %s sec" % analyse()