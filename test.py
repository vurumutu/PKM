# -*- coding: utf-8 -*-

from TCP_connection import Client

TCP_IP = '192.168.210.200'

client = Client()
client.connect(TCP_IP)
raw_input('Press <ENTER> to continue\n')
