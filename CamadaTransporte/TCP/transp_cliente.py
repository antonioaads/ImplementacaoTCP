# -*- coding: UTF-8 -*-

# CLIENTE

import sys
import random as rd
import time
import os
import trfunctions as tr
import textwrap as tw
import argparse as agp

#ENDEREÇOS
config_path = "config.txt"
response_path = "ifresponse.txt"

appl_req = None
appl_res = None
send_location = None
read_location = None

#VARIAVEIS DE CONTROLE
seg_size = 256
start_window_size = 5
timeout = 5
start_seq=70
lcl_port = rd.randint(1024,49151)
dst_port = 80

#ip = None

#SEQ E ACK
current_seq = start_seq
current_ack = 0

#JANELA
first_data_seq = None
status_list = None
segment_list = None
mapper = None

#Cria uma lista de segmentos que serão enviados pela janela deslizante
def create_segments(data):
    global current_seq
    global status_list
    global mapper
    l = tw.wrap(data, seg_size, replace_whitespace=False,drop_whitespace=False)
    sl = []
    for i in l:
        a = tr.Segment(tr.Header(lcl_port, dst_port, current_seq, current_ack, start_window_size), i)
        sl.append(a)
        current_seq += len(i)
    status_list = [-1 for i in range(len(l))]
    mapper = {sl[i].head.seq:i for i in range(len(l))}
    return sl

#Realiza o three-way handshake
def connect():
    global current_seq
    global current_ack
    #call_network_listener()
    start = tr.Segment(tr.Header(lcl_port, dst_port, start_seq, 0, start_window_size, syn=True))

    a = tr.send_and_confirm(send_location, read_location, start, timeout, 15)
    if a == 0:
        raise Exception('Servidor não disponível')

    current_seq += 1
    current_ack = a.head.seq+1

    final = tr.Segment(tr.Header(lcl_port, dst_port, current_seq, current_ack, start_window_size, ackn=True))
    final.head.toggle('SYN', False)
    final.head.toggle('ACK', True)
    tr.safe_send(send_location, final)

    current_seq += 1

    print("Connected")
    time.sleep(5)

#Principal método de transferência de dados
def transfer():
    global status_list
    global segment_list
    global mapper
    w_size = start_window_size
    e = 0
    d = w_size
    strike = 0
    while status_list[-1]!=-2:
        if d-e < w_size:
            d = min(len(status_list), e+w_size)
        for x in range(e, d):
            if status_list[x] == -1 or status_list[x] >= timeout:
                tr.safe_send(send_location, segment_list[x])
                status_list[x] = 0
                time.sleep(1)
                b = tr.safe_get(read_location)
                if b!=0:
                    if b.head.ack in mapper.keys():
                        index = mapper[b.head.ack]
                        if status_list[index] != -2:
                            while e < index:
                                status_list[e] = -2
                                e+=1
                            w_size = b.head.wsize
                        else:
                            strike+=1
                        if strike >= 2:
                            tr.safe_send(send_location, segment_list[index])
                            strike = 0
                    else:
                        status_list[-1] = -2
            else:
                status_list[x] += 1
    
#Realiza a finalização da conexão
def disconnect():
    global current_seq
    global current_ack
    end = tr.Segment(tr.Header(lcl_port, dst_port, current_seq, current_ack, start_window_size, fin = True))

    a = tr.send_and_confirm(send_location, read_location, end, timeout, 15)
    if a == 0:
        raise Exception('Lost Connection')

    current_seq+=1
    current_ack+=1

    final = tr.Segment(tr.Header(lcl_port, dst_port, current_seq, current_ack, start_window_size, ackn=True))
    tr.safe_send(send_location, final)


#Método principal

parser = agp.ArgumentParser()
parser.add_argument("lcl_port", help="lcl_port")
parser.add_argument("dst_port", help="dst_port")
#parser.add_argument("dst_ip", help="dst_ip")
args = parser.parse_args()
lcl_port = args.lcl_port
if args.dst_port:
    dst_port = args.dst_port
else:
    with open(response_path, "r") as f:
        dst_port = int(f.read())
#ip = args.dst_ip


with open(config_path, "r") as f:
    l = [x for x in f]
appl_req = l[0][:-1]
send_location = l[2][:-1]
read_location = l[3]
while True:
        data = 0
        if os.path.isfile(appl_req):
            time.sleep(0.02)
            with open(appl_req, 'r') as g:
                data = g.read()
            os.remove(appl_req)
            print("Começando com porta", lcl_port)
            connect()
            print("Criando Segmentos")
            segment_list = create_segments(data)
            print("Iniciando transferência: \n")
            transfer()
            print("\n Desconectando: \n")
            disconnect()
            print("\n")
            break
        else:
            print("waiting", end='\r')