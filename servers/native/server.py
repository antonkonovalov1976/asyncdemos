#!/usr/bin/env python
#coding:utf-8

import os.path
import sys

# для того, чтобы был виден модуль settings.py
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

from json import loads
from json import dumps
from collections import defaultdict
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

from settings import SERVER_ADDRESS
from settings import SERVER_PORT
from settings import SERVER_FULL_ADDRES
from settings import NATIVE_SERVER


class CounterStorage(object):

    u"""Класс-хранилище для подсчёта запросов."""

    _req_storage = defaultdict(int)

    @classmethod
    def handle_request_info(cls, request_type):
        if isinstance(request_type, basestring):
            cls._req_storage[request_type] += 1

    @classmethod
    def get_all_request_info(cls):
        # статситика всех запросов
        return cls._req_storage

    @classmethod
    def clean(cls):
        # сброс статистики
        cls._req_storage = defaultdict(int)


class RequestHandler(BaseHTTPRequestHandler):

    u"""Обработчик HTTP-запросов для HTTPServer."""

    root_url = r'/'
    stat_url = r'/stat'
    type_url = r'/type'
    ping_url = r'/ping'

    def json_data(self):
        return loads(self.rfile.read(int(self.headers["content-length"])))

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path == self.root_url:
            self.wfile.write("Hello, I am server!")
        elif self.path == self.stat_url:
            data = CounterStorage.get_all_request_info()
            data_str = "<br>".join(
                ["%s: %d" % (key, value) for (key, value) in data.iteritems()]
            )
            self.wfile.write(data_str)
        else:
            self.wfile.write('unknown url')

    def do_POST(self):

        # отдача заголовка респонса
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        if self.path == self.ping_url:
            # пинг
            resp = self.json_data()
            action = resp.get('action')
            req_type = resp.get('req_type')
            if req_type and action == 'ping':
                CounterStorage.handle_request_info(req_type)
                self.wfile.write(
                    dumps({'reqtype': req_type, 'status': 'ok'})
                )

        elif self.path == self.type_url:
            # запрос типа сервера
            self.wfile.write(
                dumps(
                    {'server_type': NATIVE_SERVER, 'status': 'ok'}
                )
            )
        else:
            self.wfile.write(
                dumps(
                    {'message': 'unsupported url', 'status': 'error'}
                )
            )


server = HTTPServer((SERVER_ADDRESS, SERVER_PORT), RequestHandler)
print "*** NATIVE DEMOSERVER STARTED ON %s ***" % SERVER_FULL_ADDRES
server.serve_forever()


