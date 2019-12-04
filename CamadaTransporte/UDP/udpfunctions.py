#UDPfunctions:

import random as rd
import os
import time
import textwrap as tw
import re
from collections import OrderedDict

class Header:
    def __init__(self, src, dst, size):
        self.src_port = src
        self.dst_port = dst
        self.size = size
    def to_bytes(self):
        s='||'
        s += str(self.src_port)+'|'
        s += str(self.dst_port)+'|'
        s += str(self.size)+'||'
        return s
    @classmethod
    def unpack(cls, head):
        l = re.split("\|",head)
       # print(l)
        src = int(l[0])
        dst = int(l[1])
        size = int(l[2])
        return cls(src, dst, size)
        
# Classe pra segmento, salva tudo obtido pelo arquivo.
class Segment:
    def __init__(self, head, data=None):
        self.head = head
        self.data = data
    @classmethod
    def unpack(cls, seg):
        l = re.split(r'\|\|', seg)
        print(seg)
        pkhead = l[1]
        if l[2] != '': pkdata = l[2]
        else: pkdata = None
        h = Header.unpack(pkhead)
        return cls(h, data=pkdata)
    def pack(self):
        if self.data != None:
            return self.head.to_bytes() +self.data
        else: return self.head.to_bytes()

#Envia um segmento
def send(addr, segment):
    with open(addr, "w") as f:
        f.write(segment.pack())

def safe_send(addr, segment):
    with open(addr, 'w') as f:
        f.write(segment.pack())
    while os.path.isfile(addr): pass

# Adquire um segmento. Caso não consiga, retorna None
def get(addr):
    try:
        data = ''
        while data == '':
            with open(addr, 'r') as g:
                data = g.read()
            try:
                os.remove(addr)
            except:
                time.sleep(1)
                os.remove(addr)
            if data != '':
                a = Segment.unpack(data)
        return a
    except FileNotFoundError:
        return 0

def safe_get(addr):
    data = ''
    a = 0
    if os.path.isfile(addr):
        time.sleep(0.02)
        with open(addr, 'r') as g:
            data = g.read()
        os.remove(addr)
        if data != '':
            a = Segment.unpack(data)
    return a

