# -*- coding: UTF-8 -*-

#SERVIDOR

import sys
import random as rd
import time
import os
import trfunctions as tr
import argparse as agp

#ENDEREÇOS
config_path = "config.txt"
response_path = "ifresponse.txt"

appl_req = None
appl_res = None
send_location = None
read_location = None

#VARIAVEIS DE CONTROLE
seg_size = 16
start_window_size = 5
timeout = 2
start_seq = 0
start_ack = 0
lcl_port = 80
dst_port = None

#SEQ E ACK
current_seq = start_seq
current_ack = 0

#JANELA
first_data_seq = None
window = {}

#Realiza o three-way handshake
def connect():
    global current_seq
    global current_ack
    global first_data_seq

    answer = tr.Segment(tr.Header(lcl_port, dst_port, current_seq, current_ack, start_window_size, syn=True, ackn=True))

    b = tr.send_and_confirm(send_location, read_location, answer, timeout, 15)
    if b == 0:
        raise Exception('Conexão Falha')
    print("Conectado")
    current_ack +=1
    current_seq +=1
    first_data_seq = current_ack

#Retorna último segmento adquirido sequencialmente
def last_seg():
    global window
    global first_data_seq
    aux = first_data_seq
    aux2 = aux
    while(aux2 in window.keys()):
        aux = aux2
        aux2 = aux2 + window[aux2][0]
    return tr.Segment(tr.Header(lcl_port,dst_port,0,aux2,start_window_size,ackn=True))

#Escuta pelos pacotes enviados pelo cliente
def listen():
    global current_ack
    global window
    exit = False
    while not exit:
        a = tr.safe_get(read_location)
        if a!=0:
            if a.head.seq != current_ack:
                b = last_seg()
            else:
                if a.head.fin == True:
                    current_ack +=1
                    b = tr.Segment(tr.Header(lcl_port, dst_port, current_seq, current_ack, start_window_size, ackn=True, fin=True))
                    exit = True
                else:
                    window[current_ack] = (len(a.data),a)
                    current_ack += len(a.data)
                    b = tr.Segment(tr.Header(lcl_port, dst_port, current_seq, current_ack, start_window_size, ackn=True))
            tr.safe_send(send_location, b)

#Após término da conexão, envia dados para a camada de aplicação
def send_to_application():
    global window
    global first_data_seq
    result = ''
    aux = first_data_seq
    aux2 = aux
    while aux2 in window.keys():
        result += window[aux2][1].data
        aux = aux2
        aux2 += window[aux2][0]
    with open(appl_req, "w") as f:
        f.write(result)
    with open(response_path, "w") as c:
        c.write(str(dst_port))

#Tenta adquirir o último ACK da conexão
def disconnect():
    for i in range(15):
        tr.safe_get(read_location)
        time.sleep(0.01)
    send_to_application()

#Método principal:

parser = agp.ArgumentParser()
parser.add_argument("lcl_port", help="lcl_port")
args = parser.parse_args()
lcl_port = args.lcl_port

#call_network_listener()
with open(config_path, "r") as f:
    l = [x for x in f]
appl_req = l[0][:-1]
appl_res = l[1][:-1]
send_location = l[2][:-1]
read_location = l[3]
while True:
    data = 0
    a = tr.safe_get(read_location)
    time.sleep(1)
    if(a != 0 and a.head.syn and not a.head.ackn):
        print("Conexão Requisitada")
        dst_port = a.head.src_port
        current_ack = a.head.seq+1
        print("Conectando")
        connect()
        print("Escutando conexão: \n")
        listen()
        disconnect()
        print("\n")
        break
    else:
        print("waiting", end='\r')