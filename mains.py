#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import socket
import json
import pymysql.cursors

infuser={"method":"", "param":{"idT":0, "idv":0, "score":100}}
sock = socket.socket()
sock.connect(('192.168.10.32', 9090))