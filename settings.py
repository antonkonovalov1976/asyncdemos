# coding:utf-8

u"""Настройки для запуска серверов."""

# Адрес сервера
SERVER_ADDRESS = '127.0.0.1'

# Порт сервера
SERVER_PORT = 8080

# полный адрес сервера
SERVER_FULL_ADDRES = r"http://%s:%d" % (SERVER_ADDRESS, SERVER_PORT)

# типы серверов для идентификации клиентами
NATIVE_SERVER = 'native_http_server'
TORNADO_SERVER = 'tornado_server'