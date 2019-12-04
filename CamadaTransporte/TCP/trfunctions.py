# -*- coding: UTF-8 -*-


# Uma classe pra header. Lida com formatação do header, etc.
# OBS: trabalha com caracteres não-printáveis

import random as rd
import os
import time
import textwrap as tw
import re
import subprocess as sp
from collections import OrderedDict

class Header:
    def __init__(self, src, dst, seq, ack, wsize, ackn=False, syn=False, fin=False):
        self.src_port = src
        self.dst_port = dst
        self.seq = seq
        self.ack = ack
        self.wsize = wsize
        self.flag = '0'+(ackn and '1' or True and '0')+'00'+(syn and '1' or True and '0')+(fin and '1' or True and '0')
        self.ackn = ackn
        self.syn = syn
        self.fin = fin
    def toggle(self, flag, value):
        v = list(self.flag)
        if flag == 'ACK':
            v[1] = (value == True and '1' or '0') or (value == False and '1' or '0')
        elif flag == 'SYN':
            v[4] = (value == True and '1' or '0') or (value == False and '1' or '0')
        elif flag == 'FIN':
            v[5] = (value == True and '1' or '0') or (value == False and '1' or '0')
        self.flag = ''.join(v)
    def to_bytes(self):
        s='||'
        s += str(self.src_port)+'|'
        s += str(self.dst_port)+'|'
        s += str(self.seq)+'|'
        s += str(self.ack)+'|'
        s += str(self.wsize)+'|'
        s += self.flag+'||'
        return s
    @classmethod
    def unpack(cls, head):
        l = re.split("\|",head)
        src = int(l[0])
        dst = int(l[1])
        seq = int(l[2])
        ack = int(l[3])
        wsize = int(l[4])
        flgs = l[5]
        return cls(src, dst, seq, ack, wsize, ackn = flgs[1]=='1' , syn = flgs[4]=='1' ,fin = flgs[5]=='1' )
        
# Classe pra segmento, salva tudo obtido pelo arquivo.
class Segment:
    def __init__(self, head, data=None):
        self.head = head
        self.data = data
    @classmethod
    def unpack(cls, seg):
        l = re.split(r'\|\|', seg)
        pkhead = l[1]
        #print(pkhead)
        if l[2] != '': pkdata = l[2]
        else: pkdata = None
        h = Header.unpack(pkhead)
        return cls(h, data=pkdata)
    def pack(self):
        if self.data != None:
            return self.head.to_bytes() +self. data
        else: return self.head.to_bytes()

def printable_seg(a):
    if a.head.ackn or a.head.fin or a.head.syn:
        return ('[{}{}{}], seq={} ack={}'.format((a.head.syn and " SYN " or ''),(a.head.fin and " FIN " or ''),(a.head.ackn and " ACK " or ''),a.head.seq,a.head.ack))
    else:
        return ('seq={} ack={} data="{:.30s}..."'.format(a.head.seq, a.head.ack, a.data))

def call_network_sender(ip):
    command = ''
    sp.call([command, ip])

def call_network_listener():
    command = ''
    sp.call(command)

#Envia um segmento
def safe_send(addr, segment):
    print("SENDING ", printable_seg(segment))
    #call_network_sender()
    with open(addr, 'w') as f:
        f.write(segment.pack())
    while os.path.isfile(addr): pass

def unsafe_send(addr,segment):
    c = rd.randint(0,5)
    if c == 0:
        print("Opps!")
    else:
        safe_send(addr, segment)

# Adquire um segmento. Caso não consiga, retorna None
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
            print("RECEIVED ", printable_seg(a))
    return a

# Uma funçãozinha para ser usada para enviar um segmento e esperar por resposta.
# Usado para handshake e fim de transmissão apenas.
def send_and_confirm(send_location, read_location, seg, timeout, max_attempt):
    safe_send(send_location, seg)
    aux = 0
    a = safe_get(read_location)
    for i in range(max_attempt):
        if a == 0:
            time.sleep(1)
            aux += 1
            if(aux > timeout):
                print('Re-sending Package')
                safe_send(send_location, seg)
                aux = 1
            a = safe_get(read_location)
        else:
            if a.head.ack == seg.head.seq+1: return a
            else: 
                print('expected {}, found {}'.format(seg.head.seq+1, a.head.ack))
                a = 0
    return 0

