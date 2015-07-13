#!/usr/bin/env python
#coding:utf-8

import os.path
import sys

# для того, чтобы был виден модуль settings.py
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from collections import defaultdict

from tornado.escape import json_decode
from tornado.ioloop import IOLoop
from tornado.ioloop import PeriodicCallback
from tornado.web import asynchronous
from tornado.web import RequestHandler
from tornado.web import Application

from settings import SERVER_ADDRESS
from settings import SERVER_PORT
from settings import SERVER_FULL_ADDRES
from settings import TORNADO_SERVER


class CounterStorage(object):

    u"""Класс-хранилище для подсчёта запросов."""

    _req_storage = defaultdict(int)

    @classmethod
    def handle_request_info(cls, request_type):
        if isinstance(request_type, basestring):
            cls._req_storage[request_type] += 1

    @classmethod
    def get_all_request_info(cls):
        # статистика всех запросов
        return cls._req_storage

    @classmethod
    def clean(cls):
        # сброс статистики
        cls._req_storage = defaultdict(int)


class MainPageHandler(RequestHandler):

    u"""Класс обработчика для основной страницы."""

    @asynchronous
    def get(self):
        self.write("Hello, I am server!")
        self.finish()


class BaseHandler(RequestHandler):

    u"""Базовый класс обработчика запросов."""

    def prepare(self):
        u"""специальный метод для обработки JSON-параметров."""
        if self.request.headers.get("Content-Type") == "application/json":
            self.json_args = json_decode(self.request.body)


class AsyncPingHandler(BaseHandler):

    u"""Класс асинхронного обработчика тестовых POST-запросов.

    Для проверки можно использовать утилиту curl:
    curl -H "Content-Type: application/json" -X POST -d \
        '{"req_type":"foo", "action": "ping"}' http://127.0.0.1:8080/async_ping
    """

    @asynchronous
    def post(self):
        req_type = self.json_args.get('req_type')
        action = self.json_args.get('action')
        if action == 'ping' and req_type:
            CounterStorage.handle_request_info(req_type)
            self.write({'reqtype': req_type, 'status': 'ok'})

        self.finish()


class SyncPingHandler(BaseHandler):

    u"""Класс синхронного обработчика тестовых POST-запросов.

    Для проверки можно использовать утилиту curl:
    curl -H "Content-Type: application/json" -X POST -d \
        '{"req_type":"foo", "action": "ping"}' http://127.0.0.1:8080/sync_ping
    """

    def post(self):
        req_type = self.json_args.get('req_type')
        action = self.json_args.get('action')
        if action == 'ping' and req_type:
            CounterStorage.handle_request_info(req_type)
            self.write({'reqtype': req_type, 'status': 'ok'})


class StatHandler(RequestHandler):

    u"""Класс обработчика вывода статистики запросов."""

    @asynchronous
    def get(self):
        data = CounterStorage.get_all_request_info()
        data_str = "<br>".join(
            ["%s: %d" % (key, value) for (key, value) in data.iteritems()]
        )
        self.write(data_str)
        self.finish()


class ServerTypeHandler(BaseHandler):

    u"""Класс обработчика запроса типа сервера."""

    @asynchronous
    def post(self):
        self.write({'server_type': TORNADO_SERVER, 'status': 'ok'})
        self.finish()

if __name__ == "__main__":

    application = Application([
        (r"/", MainPageHandler),
        (r"/async_ping", AsyncPingHandler),
        (r"/sync_ping", SyncPingHandler),
        (r"/stat", StatHandler),
        (r"/type", ServerTypeHandler)
    ], debug=True)

    application.listen(address=SERVER_ADDRESS, port=SERVER_PORT)
    main_loop = IOLoop.instance()

    # периодическая задача (3 мин) сброса статистики
    PeriodicCallback(CounterStorage.clean, 3 * 60 * 1000).start()

    print "*** TORNADO DEMOSERVER STARTED ON %s ***" % SERVER_FULL_ADDRES

    main_loop.start()
